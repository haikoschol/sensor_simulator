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

from kobold import *
import unittest


class TestDataLogFileReplay(unittest.TestCase):

    def setUp(self):
        self.data_source = KoboldDataSource(logfile='unittest_logdata.out')


    def testReplayNoLoop(self):
        '''
        the data source should replay the following values once:
        5.6799999999999997, 5.6799999999999997, 5.7000000000000002, 5.7000000000000002
        '''
        expected_output = [5.6799999999999997, 5.6799999999999997, 5.7000000000000002, 5.7000000000000002]
        self.data_source.start_replay()
        output = []
        for value in expected_output:
            output.append(self.data_source.next())
        self.assertEqual(output, expected_output)
        

    def testReplayLoop(self):
        '''
        the data source should replay the following values twice:
        5.6799999999999997, 5.6799999999999997, 5.7000000000000002, 5.7000000000000002
        '''
        expected_output = [5.6799999999999997, 5.6799999999999997, 5.7000000000000002, 5.7000000000000002,\
                           5.6799999999999997, 5.6799999999999997, 5.7000000000000002, 5.7000000000000002]
        self.data_source.start_replay(True)
        output = []
        for value in expected_output:
            output.append(self.data_source.next())
        self.assertEqual(output, expected_output)


class TestRandomDataOutput(unittest.TestCase):

    def setUp(self):
        self.data_source = KoboldDataSource()

    
    def testRandomData(self):
        '''
        testing with default values, baseline = 1.0, variation = 1.0
        expecting values between 0.0 and 2.0
        '''
        values = []
        for i in range(5):
            values.append(self.data_source.next())
        ok = True
        for value in values:
            ok = 0.0 <= value <= 2.0
            if not ok: break
        self.assertEqual(ok, True)


if __name__=='__main__':
    unittest.main()
