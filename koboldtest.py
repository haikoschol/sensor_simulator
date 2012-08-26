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

import kobold
import unittest

class TestChecksumFunction(unittest.TestCase):

    def setUp(self):
        self.sim = kobold.KoboldSimulator()


    def testChecksum(self):
        ''' checksum of 0x01 0x02 0x03 should be 0xfa '''
        self.assertEqual(self.sim.checksum([0x01, 0x02, 0x03]), 0xfa)


class SendBadInput(unittest.TestCase):

    def setUp(self):
        self.sim = kobold.KoboldSimulator()


    def testNoneMessage(self):
        self.assertRaises(kobold.EmptyMessageError, self.sim.send, None)


    def testMessageTooShort(self):
        msgs = [ [ 0x01 ], [ 0x01, 0x02 ] ]
        for msg in msgs:
            self.assertRaises(kobold.MessageTooShortError, self.sim.send, msg)


    def testNonTerminatedMessage(self):
        msg = [ 0x01, 0x02, 0x03, 0xfa ]
        self.assertRaises(kobold.NonTerminatedMessageError, self.sim.send, msg)


    def testIncorrectChecksum(self):
        msg = [ 0x01, 0x02, 0x03, 0x42, 0x0d ]
        self.assertRaises(kobold.IncorrectChecksumError, self.sim.send, msg)


    def testUnknownMessage(self):
        msg = [ 0x01, 0x02, 0x03, 0xfa, 0x0d ]
        self.assertRaises(kobold.UnknownMessageError, self.sim.send, msg)


class SendGoodInput(unittest.TestCase):

    def setUp(self):
        self.sim = kobold.KoboldSimulator()


    def testSwitchToPollMode(self):
        msg = [ 0x53, 0x4f, 0xff ]
        msg.append(self.sim.checksum(msg))
        msg.append(0x0d)
        expected_reply = [ 0x73, 0x6f, 0xff ]
        expected_reply.append(self.sim.checksum(expected_reply))
        expected_reply.append(0x0d)
        self.sim.send(msg)
        reply = self.sim.receive()
        self.assertEqual(reply, expected_reply)


    def testSetPollModeDelay(self):
        msg = self.sim.build_msg([ 0x41, 0x5a, 0xff ])
        expected_reply = self.sim.build_msg([ 0x61, 0x7a, 0xff ])
        self.sim.send(msg)
        reply = self.sim.receive()
        self.assertEqual(reply, expected_reply)


    def testSetCyclicModeOutputInterval(self):
        msg = self.sim.build_msg([ 0x49, 0x00, 0x10 ])
        expected_reply = self.sim.build_msg([ 0x69, 0x00, 0x10 ])
        self.sim.send(msg)
        reply = self.sim.receive()
        self.assertEqual(reply, expected_reply)


    def testReadDeviceIdentifier(self):
        msg = self.sim.build_msg([ 0x4b, 0x4e, 0x00 ])
        expected_reply = self.sim.build_msg([ 0x4b, 0x43, 0x4f, 0x44, 0x45, 0x34, 0x32 ])
        self.sim.send(msg)
        reply = self.sim.receive()
        self.assertEqual(reply, expected_reply)


if __name__=='__main__':
    unittest.main()
