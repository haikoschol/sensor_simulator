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

import ConfigParser
import serial
from koboldserial import *
from kobold import *


CONFIG_FILE_NAME = 'cfg.ini'

class KoboldController:

    CONFIG_ATTRIBUTES = {
            'serial' : ['serial_port', 'use_pty'],
            'sensor' : ['mode', 'cyclic_output_interval', 'poll_mode_reply_delay',
                        'device_identifier', 'temperature', 'measuring_range_begin',
                        'measuring_range_end'],
            'data_source' : ['baseline', 'variation']
            }

    def __init__(self):
        self.sensor = KoboldSimulator()
        self.data_source = self.sensor.data_source
        self.serial_adapter = None
        self.use_pty = False
        self.load_configuration(CONFIG_FILE_NAME)


    def load_configuration(self, filename):
        f = open(filename, 'r')
        cfg = ConfigParser.SafeConfigParser()
        cfg.readfp(f)
        f.close()
#        self.use_pty = cfg.getboolean('SERIAL', 'use pty') # ***FIXME*** feature doesn't work
        self.serial_port = cfg.get('SERIAL', 'Port')
        self.mode = cfg.getint('SENSOR', 'Mode')
        self.cyclic_output_interval = cfg.getint('SENSOR', 'Cyclic Output Interval')
        self.poll_mode_reply_delay = cfg.getint('SENSOR', 'Poll Mode Reply Delay')
        self.device_identifier = cfg.get('SENSOR', 'Device Identifier')
        self.temperature = cfg.getfloat('SENSOR', 'Temperature')
        self.measuring_range_begin = cfg.getint('SENSOR', 'Measuring Range Begin')
        self.measuring_range_end = cfg.getint('SENSOR', 'Measuring Range End')
        self.baseline = cfg.getfloat('DATASOURCE', 'Baseline')
        self.variation = cfg.getfloat('DATASOURCE', 'Variation')


    def save_configuration(self, filename=CONFIG_FILE_NAME):
        f = open(filename, 'w')
        cfg = ConfigParser.SafeConfigParser()
        cfg.add_section('SERIAL')
        cfg.add_section('SENSOR')
        cfg.add_section('DATASOURCE')
        cfg.set('SERIAL', 'Port', self.serial_port)
        cfg.set('SENSOR', 'Mode', str(self.mode))
        cfg.set('SENSOR', 'Cyclic Output Interval', str(self.cyclic_output_interval))
        cfg.set('SENSOR', 'Poll Mode Reply Delay', str(self.poll_mode_reply_delay))
        cfg.set('SENSOR', 'Device Identifier', self.device_identifier)
        cfg.set('SENSOR', 'Temperature', str(self.temperature))
        cfg.set('SENSOR', 'Measuring Range Begin', str(self.measuring_range_begin))
        cfg.set('SENSOR', 'Measuring Range End', str(self.measuring_range_end))
        cfg.set('DATASOURCE', 'Baseline', str(self.baseline))
        cfg.set('DATASOURCE', 'Variation', str(self.variation))
        try:
            cfg.write(f)
        finally:
            f.close()


    def get_serial_port_default_names(self):
        '''
        returns the default names for the first 4 serial ports on the current plattform.
        for windows this is COM1-4 and for linux it is /dev/ttyS0-3.
        '''
        if serial.plat.startswith('linux'):
            return ['/dev/ttyS0', '/dev/ttyS1', '/dev/ttyS2', '/dev/ttyS3']
        else:
            return ['COM1', 'COM2', 'COM3', 'COM4']
    
    
    def register(self, handler):
        '''
        proxy method for the register method in the model (KoboldSimulator and KoboldDataSource)
        '''
        self.sensor.register(handler)
        self.data_source.register(handler)


    def unregister(self, handler):
        '''
        proxy method for the unregister method in the model (KoboldSimulator and KoboldDataSource)
        '''
        self.sensor.unregister(handler)
        self.data_source.unregister(handler)


    def load_data_log_file(self, filename):
        self.data_source.read_logfile(filename)


    def start_replay(self):
        self.data_source.start_replay()


    def stop_replay(self):
        self.data_source.stop_replay()


    def reset_replay(self):
        self.data_source.reset_replay()


    def close(self):
        if self.serial_adapter:
            if self.sensor.mode == KoboldSimulator.POLL_MODE:
                # ugly hack to stop the writer thread in serial_adapter from blocking
                self.sensor.poll_device_identifier([])
            self.serial_adapter.stop()
            self.serial_adapter.close()


    def __getattr__(self, name):
        if name in self.CONFIG_ATTRIBUTES['serial']:
            if not self.serial_adapter: return None
            return getattr(self.serial_adapter, name)
        if name in self.CONFIG_ATTRIBUTES['sensor']:
            return getattr(self.sensor, name)
        if name in self.CONFIG_ATTRIBUTES['data_source']:
            return getattr(self.data_source, name)
        return self.__dict__[name]


    def __setattr__(self, name, value):
        if name == 'use_pty':
            self.__dict__[name] = value
            return

        if name in self.CONFIG_ATTRIBUTES['serial']:
            if name == 'serial_port':
                if self.serial_adapter: self.close()
                self.serial_adapter = KoboldSimulatorSerialPortAdapter(self.sensor,
                                                                       value,
                                                                       self.use_pty)
                self.serial_adapter.start()
            else:
                setattr(self.serial_adapter, name, value)
        elif name in self.CONFIG_ATTRIBUTES['sensor']:
            setattr(self.sensor, name, value)
        elif name in self.CONFIG_ATTRIBUTES['data_source']:
            setattr(self.data_source, name, value)
        else:
            self.__dict__[name] = value


