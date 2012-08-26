#!/usr/bin/env python
#encoding: utf-8

#Copyright (c) 2007 Haiko Schol (http://www.haikoschol.com/)
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import random
import time
import Queue
from observable import *


class KoboldSimulatorError(Exception):
    pass

class EmptyMessageError(KoboldSimulatorError):
    pass

class MessageTooShortError(KoboldSimulatorError):
    pass

class NonTerminatedMessageError(KoboldSimulatorError):
    pass

class IncorrectChecksumError(KoboldSimulatorError):
    pass

class UnknownMessageError(KoboldSimulatorError):
    pass


class KoboldSimulator(Observable):
    '''
    this class represents a virtual pressure sensor of type SEN 3 manufactured by Kobold
    (http://www.kobold.com/).
    
    it implements the protocol that the real sensor speaks over a RS232 connection.
    users of this class need the following methods and attributes:
    
    send()        to send messages _to_ the sensor
    receive()     to receive messages _from_ the sensor
    flush()       to empty the queue of not yet received messages (to simulate flushing
                  RS232 buffers) 
    data_source   sets or changes the data source that is used by the object to generate
                  pressure values

    these methods may raise KoboldSimulatorError or any of its subclasses.
    '''

    POLL_MODE = 1
    CYCLIC_PRESSURE_MODE = 2
    CYCLIC_PRESSURE_TEMPERATURE_MODE = 3
    MAX_QUEUE_SIZE = 100

    def __init__(self, data_source=None):
        '''
        if no data source is given the object will create a default instance that produces
        random pressure values between 0.0 and 2.0 bar.
        '''

        Observable.__init__(self)
        self._mode = self.POLL_MODE
        self._cyclic_output_interval = 100 # in ms
        self._poll_mode_reply_delay = 0 # means reply as fast as possible, max value is 15 ms
        self._temperature = 23.5
        self.device_identifier = 'SEN3'
        self._measuring_range_begin = 0 # in bar
        self._measuring_range_end = 1000
        self._msg_counter = 0 # used for determining when to send temperature in CYCLIC_PRESSURE_TEMPERATURE_MODE

        if data_source:
            self._data_source = data_source
            data_source.sensor = self
        else:
            self._data_source = KoboldDataSource(sensor=self)

        # buffers what users of the class get when they call receive() on an object
        self._recvbuf = Queue.Queue(self.MAX_QUEUE_SIZE)

        self.poll_msgs = {
                            0x4d: self.poll_measuring_range,
                            0x50: self.poll_pressure,
                            0x54: self.poll_temperature,
                            0x4b: self.poll_device_identifier
                         }
        self.set_msgs = {
                            0x53: self.set_mode,
                            0x41: self.set_poll_mode_reply_delay,
                            0x49: self.set_cyclic_mode_output_interval
                        }


    def _set_data_source(self, data_source):
        if not data_source:
            self._data_source = KoboldDataSource(sensor=self)
        elif self._data_source != data_source:
            self._data_source = data_source
        if self._data_source.sensor is not self:
            self._data_source.sensor = self


    def _get_data_source(self):
        return self._data_source


    data_source = property(_get_data_source, _set_data_source)


    def _set_mode(self, mode):
        mode = int(mode)
        if self._mode == mode: return
        if self.POLL_MODE <= mode <= self.CYCLIC_PRESSURE_TEMPERATURE_MODE:
            if self.mode == self.POLL_MODE:
                self._recvbuf.put(self.build_msg(self.pressure2digits(self._data_source.next())))
                if mode == self.CYCLIC_PRESSURE_TEMPERATURE_MODE:
                    self._msg_counter += 1

            self._mode = mode
        else:
            self._mode = self.POLL_MODE
        self.notify(('mode', self._mode))


    def _get_mode(self):
        return self._mode


    mode = property(_get_mode, _set_mode, doc='''\
            the sensor has three different modes of operation. in POLL_MODE, it
            responds to queries for pressure or temperature. in CYCLIC_PRESSURE_MODE
            it sends the pressure value (in digits format) repeatedly in a configurable
            interval. in CYCLIC_PRESSURE_TEMPERATURE_MODE it sends the temperature
            once, after every nine pressure values.''')


    def _set_cyclic_output_interval(self, interval):
        interval = int(interval)
        if self.cyclic_output_interval == interval: return
        if interval < 1:
            self._cyclic_output_interval = 1
        elif interval > 65535:
            self._cyclic_output_interval = 65535
        else:
            self._cyclic_output_interval = interval
        self.notify(('cyclic_output_interval', self._cyclic_output_interval))


    def _get_cyclic_output_interval(self):
        return self._cyclic_output_interval


    cyclic_output_interval = property(_get_cyclic_output_interval, _set_cyclic_output_interval, doc='''\
            the time in ms, that the sensor will wait before sending the next value in cyclic output mode.
            only values between 1 and 65535 are accepted.''')


    def _set_poll_mode_reply_delay(self, delay):
        delay = int(delay)
        if self._poll_mode_reply_delay == delay: return
        if delay < 0:
            self._poll_mode_reply_delay = 0
        elif delay > 15:
            self._poll_mode_reply_delay = 15
        else:
            self._poll_mode_reply_delay = delay
        self.notify(('poll_mode_reply_delay', self._poll_mode_reply_delay))


    def _get_poll_mode_reply_delay(self):
        return self._poll_mode_reply_delay


    poll_mode_reply_delay = property(_get_poll_mode_reply_delay, _set_poll_mode_reply_delay, doc='''\
            the time in ms, that the sensor will wait before sending a reply in poll mode.
            only values between 0 and 15 are accepted.''')


    def _set_temperature(self, temp):
        temp = float(temp)
        if self._temperature == temp: return
        self._temperature = temp
        self.notify(('temperature', temp))


    def _get_temperature(self):
        return self._temperature


    temperature = property(_get_temperature, _set_temperature)


    def _set_range_begin(self, value):
        value = int(value)
        if self._measuring_range_begin == value: return
        self._measuring_range_begin = value
        self.data_source.min_value = value
        if self.measuring_range_end <= value:
            self.measuring_range_end = value + 1
        self.notify(('measuring_range_begin', value))
        

    def _get_range_begin(self):
        return self._measuring_range_begin


    measuring_range_begin = property(_get_range_begin, _set_range_begin)


    def _set_range_end(self, value):
        value = int(value)
        if self._measuring_range_end == value: return
        self._measuring_range_end = value
        self.data_source.max_value = value
        if value <= self.measuring_range_begin:
            self.measuring_range_begin = value + 1
        self.notify(('measuring_range_end', value))

    
    def _get_range_end(self):
        return self._measuring_range_end


    measuring_range_end = property(_get_range_end, _set_range_end)


    def flush(self):
        '''
        empties the queue of not yet consumed messages
        '''
        self._recvbuf = Queue.Queue(self.MAX_QUEUE_SIZE)


    def send(self, msg):
        ''' 
        send message *to* the Kobold sensor
        msg: list of bytes
        '''
        if not msg:
            raise EmptyMessageError()

        if len(msg) < 3:
            raise MessageTooShortError()

        if msg[-1] != 0x0d:
            raise NonTerminatedMessageError()

        if msg[-2] != self.checksum(msg[0:-2]):
            raise IncorrectChecksumError()

        self.dispatch(msg)


    def receive(self):
        '''
        receive messages *from* the sensor. if the sensor is in poll mode and there is nothing
        on the queue this method returns None. if the sensor is in cyclic output mode this method
        will make sure that the time between calls will be cyclic_output_interval ms. in poll mode it will
        wait poll_mode_reply_delay ms instead.
        the method will always return the next element from the queue before asking the KoboldDataSource
        object for the next value.
        '''
        self.wait()
        if self.mode == self.POLL_MODE: return self._recvbuf.get()

        if not self._recvbuf.empty(): return self._recvbuf.get()

        if self.mode == self.CYCLIC_PRESSURE_MODE:
            return self.build_msg(self.pressure2digits(self.data_source.next()))

        if self._msg_counter and self._msg_counter % 9 == 0:
            self._msg_counter = 0
            (high_byte, low_byte) = self.split(self.temperature*2.0)
            return self.build_msg([0x54, high_byte, low_byte, 0x00])
        else:
            self._msg_counter += 1
            return self.build_msg(self.pressure2digits(self.data_source.next()))


    def wait(self):
        '''
        if the sensor is in poll mode, wait poll_mode_reply_delay ms. otherwise wait cyclic_output_interval ms.

        '''
        if self.mode == self.POLL_MODE:
            time.sleep(self.poll_mode_reply_delay / 1000.0)
        else:
            time.sleep(self.cyclic_output_interval / 1000.0)



    def checksum(self, msg):
        '''
        calculate a checksum as expected and returned by the SEN 3. the checksum is obtained
        by taking the two's complement of the low byte of the byte-wise sum of the message.
        '''
        result = 0
        for byte in msg:
            result += byte

        result ^= 0xff
        result += 1
        return result % 256


    def build_msg(self, msg):
        '''
        append the checksum and \r termination to the given message
        '''
        msg.append(self.checksum(msg))
        msg.append(0x0d)
        return msg


    def split(self, value):
        '''
        split a numeric value into high byte and low byte
        '''
        high_byte = int(value) >> 8
        low_byte = int(value) - (high_byte << 8)
        return high_byte, low_byte


    def pressure2digits(self, value):
        '''
        convert a pressure value in bar into a message as returned by the sensor in digits format.
        the message is not complete! checksum and \r termination still have to be added using build_msg().
        '''
        msg = [0x6b]
        digits = (((value - self.measuring_range_begin) * 50000) / (self.measuring_range_end - self.measuring_range_begin)) + 10000
        (highbyte, lowbyte) = self.split(digits)
        msg.extend([highbyte, lowbyte, 0x00])
        return msg

        
    def dispatch(self, msg):
        handler = None
        if msg[0] in self.set_msgs:
            handler = self.set_msgs[msg[0]]
        elif msg[0] in self.poll_msgs:
            handler = self.poll_msgs[msg[0]]
        else:
            raise UnknownMessageError()
        handler(msg)


    def poll_measuring_range(self, msg):
        if msg[1] == 0x41:
            reply = [0x03]
            (high_byte, low_byte) = self.split(self.measuring_range_begin)
            mbf = 0x80 # ***FIXME*** this is faked for now...
        elif msg[1] == 0x45:
            reply = [0x04]
            (high_byte, low_byte) = self.split(self.measuring_range_end)
            mbf = 0x80
        else:
            raise UnknownMessageError()
        self._recvbuf.put(self.build_msg(reply.extend([high_bytes, low_byte, mbf])))


    def poll_pressure(self, msg):
        if msg[1] == 0x4b:
            self._recvbuf.put(self.build_msg(self.pressure2digits(self._data_source.next())))
        else:
            raise UnknownMessageError() # only understands polling pressure in digits for now...


    def poll_temperature(self, msg):
        (high_byte, low_byte) = self.split(self.temperature*2.0)
        self._recvbuf.put(self.build_msg([0x54, high_byte, low_byte, 0x00]))


    def poll_device_identifier(self, msg):
        reply = [0x4b]
        for c in self.device_identifier:
            reply.append(ord(c))
        if self._recvbuf.full(): self.recvbuf.get()
        self._recvbuf.put(self.build_msg(reply))


    def set_mode(self, msg):
        if self._recvbuf.full(): self.recvbuf.get()
        if msg[2] == 0xff:
            self.mode = self.POLL_MODE
            self._recvbuf.put(self.build_msg([0x73, 0x6f, 0xff]))
        elif msg[2] == 0xfe:
            self.mode = self.CYCLIC_PRESSURE_MODE
        elif msg[2] == 0xfd:
            self.mode = self.CYCLIC_PRESSURE_TEMPERATURE_MODE


    def set_poll_mode_reply_delay(self, msg):
        self.poll_mode_reply_delay = msg[2] / 17 # correct??
        if self._recvbuf.full(): self.recvbuf.get()
        self._recvbuf.put(self.build_msg([0x61, 0x7a, msg[2]]))


    def set_cyclic_mode_output_interval(self, msg):
        self.cyclic_output_interval = (msg[1] * 256 + msg[2]) * 10
        if self._recvbuf.full(): self.recvbuf.get()
        self._recvbuf.put(self.build_msg([0x69, msg[1], msg[2]]))



class KoboldDataSourceError(Exception):
    pass

class NoDataLogFileLoadedError(KoboldDataSourceError):
    pass

class DataLogFileFormatError(KoboldDataSourceError):
    pass


class KoboldDataSource(Observable):
    '''
    objects of this class provide a data source that can be used by objects of
    class KoboldSimulator.
    
    it can read recorded data from logfiles and generate values randomly scattered
    around a "baseline" value. baseline is the pressure value (in bar), that this
    data source generates when simulating values returned by an "idle" sensor. the
    variation determines how much the baseline value scatters.
    example: a baseline of 23 bar with a variation of 5.0 will generate random values
    between 18 and 28 bar.
    '''
    
    def __init__(self, baseline=1.0, variation=1.0, logfile=None, sensor=None):

        Observable.__init__(self)
        self._baseline = baseline
        self._variation = variation
        self._sensor = sensor
        self._replaying = False
        self._replay_index = 0
        self._replay_loop = False
        self._random_value = self.baseline
        self._min_value = sensor and sensor.measuring_range_begin or 0.0
        self._max_value = sensor and sensor.measuring_range_end or 1000.0
        random.seed()
        
        if logfile:
            self.read_logfile(logfile)
        else:
            self._replay_data = None


    def _set_baseline(self, value):
        value = float(value)
        if (self.min_value <= (value - self.variation)) and ((value + self.variation) <= self.max_value):
            self._baseline = value
        else:
            raise ValueError('The baseline value must be within the measuring range of the sensor.')
        if not self._replaying:
            self._random_value = value
        self.notify(('baseline', value))

    
    def _get_baseline(self):
        return self._baseline


    baseline = property(_get_baseline, _set_baseline)


    def _set_variation(self, value):
        value = float(value)
        if self._baseline - value < self._min_value \
            or self._baseline + value > self._max_value:
            raise ValueError('This variation will generate values outside the sensors measuring range.')
        self._variation = value
        self.notify(('variation', value))


    def _get_variation(self):
        return self._variation


    variation = property(_get_variation, _set_variation)


    def _set_sensor(self, sensor):
        self._sensor = sensor
        if not sensor:
            self._min_value = 0.0
            self._max_value = 1000.0
            return
        self._min_value = sensor.measuring_range_begin
        self._max_value = sensor.measuring_range_end
        if sensor.data_source is not self:
            sensor.data_source = self


    def _get_sensor(self):
        return self._sensor


    def _del_sensor(self):
        self._set_sensor(None)


    sensor = property(_get_sensor, _set_sensor, _del_sensor)


    def _get_min_value(self):
        return self._min_value


    def _set_min_value(self, value):
        value = int(value)
        self._min_value = value
        if self.sensor: self.sensor.measuring_range_begin = value
        if value > self.baseline - self.variation:
            self.baseline = value + self.variation


    min_value = property(_get_min_value, _set_min_value)


    def _get_max_value(self):
        return self._max_value


    def _set_max_value(self, value):
        value = int(value)
        self._max_value = value
        if self.sensor: self.sensor.measuring_range_end = value
        if value <= self.baseline + self.variation:
            self.baseline = value - self.variation


    max_value = property(_get_max_value, _set_max_value)


    def digits2pressure(self, msg):
        return ((float(ord(msg[1])) * 256.0 + float(ord(msg[2])) - 10000.0) * (self._max_value - self._min_value)) / 50000.0


    def read_logfile(self, filename):
        '''
        read data from a logfile that was recorded by connecting to a real sensor.
        it is assumed, that this logfile only contains 6 byte long messages with
        pressure data in digits format.
        '''
        data = []
        f = open(filename, 'rb')
        while 1:
            msg = f.read(6)
            if not msg: break
            if len(msg) < 6 or ord(msg[0]) != 0x6b or ord(msg[5]) != 0x0d:
                raise DataLogFileFormatError('Malformed logfile')

            if self.sensor:
                tmp = []
                for ch in msg[:4]: tmp.append(ord(ch))
                if ord(msg[4]) != self.sensor.checksum(tmp):
                    raise DataLogFileFormatError('Incorrect Checksum in logfile')

            data.append(self.digits2pressure(msg))
        f.close()
        self._replay_data = data


    def next(self):
        '''
        this is the only method that is called by the instance of class KoboldSimulator.
        the method either returns random values within the bounds of
        self.baseline and self.variation or those read from a logfile.
        '''
        if self._replaying:
            return self._next_replay_value()
        else:
            return self._next_random_value()


    def start_replay(self, loop=False):
        '''
        when recorded values from a logfile have been loaded, calling this method will cause
        next() to return those values. if loop is True, the generator will start returning
        the first value after it reached the end until stop_replay() is called.
        otherwise next() will return the last value from the recorded data +/- self.variation.
        '''
        if not self._replay_data:
            raise NoDataLogFileLoadedError()
        self._replaying = True
        self._replay_loop = loop


    def stop_replay(self):
        '''
        if the data source has been put into a loop of replaying recorded data (using start_replay()),
        calling this method will return to the "idle" state. this means next() will generate
        random values between self.baseline-self.variation and self.baseline+self.variation.
        '''
        self._replaying = False


    def reset_replay(self):
        '''
        set replay_index to 0 to start the replay from the beginning
        (that is, if a file was loaded and start_replay() called)
        '''
        self._replay_index = 0


    def has_logfile(self):
        '''
        return true if the data from a logfile has been loaded
        '''
        return self._replay_data is not None


    def reset(self):
        '''
        calling this method will cause the object to return to the default state and initial settings.
        '''
        self._replaying = False
        self._replay_index = 0
        self._replay_loop = False
        self._random_value = self.baseline


    def _next_replay_value(self):
        value = self._replay_data[self._replay_index]
        if self._replay_loop:
            self._replay_index = (self._replay_index + 1) % len(self._replay_data)
        else:
            if self._replay_index+1 == len(self._replay_data):
                self.stop_replay()
            else:
                self._replay_index += 1
        self._random_value = value
        return value


    def _next_random_value(self):
        if self.variation == 0: return self._random_value
        range_start = int((self._random_value - self.variation) * 100)
        range_end = int((self._random_value + self.variation) * 100)
        return random.randrange(range_start, range_end) / 100.0

