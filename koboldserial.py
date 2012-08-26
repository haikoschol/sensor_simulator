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

import threading

class SerialPortError(Exception):
    pass


class KoboldSimulatorSerialPortAdapter(object):
    '''
    an object of this class is used for having an object of class KoboldSimulator
    communicate over a RS232 port. the class uses the pyserial module from
    http://pyserial.sourceforge.net/
    '''
    
    def __init__(self, sensor, serial_port, use_pty=False):
        self.sensor = sensor
        self.use_pty = use_pty

        if use_pty:
            import pty, os
            self._ptym, self._ptys = pty.openpty()
            self.serial = os.fdopen(self._ptym)
            self.ptsname = os.ttyname(self._ptys)
            
            # ***FIXME*** put this in GUI
            print 'KoboldSimulatorSerialPortAdapter using pty. device name: %s' % self.ptsname
        else:
            import serial
            self.serial = serial.Serial(serial_port, timeout=10)
            self.ptsname = None

        self.serial_port = serial_port
        self.keep_running = False
        self.read_thread = threading.Thread(target=self.reader)
        self.read_thread.setDaemon(1)
        self.write_thread = threading.Thread(target=self.writer)
        self.write_thread.setDaemon(1)


    def start(self):
        '''
        starts relaying data to/from the serial port from/to the sensor simulator
        '''
        self.keep_running = True
        self.read_thread.start()
        self.write_thread.start()


    def reader(self):
        '''
        read 5 byte long messages from the serial port and forward them to the
        sensor simulator
        '''
        while self.keep_running:
            try:
                msg = self.serial.read(5)
                if msg:
                    tmp = []
                    for byte in msg:
                        tmp.append(ord(byte))
                    self.sensor.send(tmp)
            except serial.SerialException, err:
                print str(err)
                #self.keep_running = False
                #self.write_thread.join()
                #raise SerialPortError(str(err))


    def writer(self):
        '''
        read messages from the sensor simulator and send them over the RS232
        connection
        '''
        while self.keep_running:
            try:
                msg = self.sensor.receive()
                if msg:
                    tmp = ''
                    for byte in msg:
                        tmp += chr(byte)
                    self.serial.write(tmp)
            except serial.SerialException, err:
                print str(err)
                #self.keep_running = False
                #self.read_thread.join()
                #raise SerialPortError(str(err))


    def stop(self):
        '''
        stop relaying data between serial port and sensor simulator
        '''
        self.keep_running = False
        self.read_thread.join()
        self.write_thread.join()


    def close(self):
        '''
        close the serial port.
        '''
        self.serial.close()


    def _get_kr(self):
        return self._keep_running


    def _set_kr(self, value):
        value = bool(value)
        self._keep_running = value


    keep_running = property(_get_kr, _set_kr)
