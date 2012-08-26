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

import time
import sys
import Gnuplot


def checksum(msg):
    result = 0
    for byte in msg:
        result += byte

    result ^= 0xff
    result += 1
    return result % 256


def build_msg(msg):
    msg.append(checksum(msg))
    msg.append(0x0d)
    return msg


def split(value):
    high_byte = int(value) >> 8
    low_byte = int(value) - (high_byte << 8)
    return high_byte, low_byte


def pressure2digits(value):
    msg = [0x6b]
    digits = (((value - 0.0) * 50000) / (1000.0 - 0.0)) + 10000
    (highbyte, lowbyte) = split(digits)
    msg.extend([highbyte, lowbyte, 0x00])
    return msg


def msg2value(msg):
    return ((float(ord(msg[1])) * 256.0 + float(ord(msg[2])) - 10000.0) * 1000.0) / 50000.0


def value2msg(value):
    bytelist = build_msg(pressure2digits(value))
    msg = ''
    for byte in bytelist:
        msg += chr(byte)
    return msg


def read_data(filename):
    data = []
    f = open(filename, 'rb')
    while 1:
        try:
            msg = f.read(6)
        except: break
        if not msg: break
        data.append(msg)
    f.close()
    return data


def get_range(data):
    min = 0.0
    max = 0.0
    for msg in data:
        tmp = msg2value(msg)
        if min > tmp: min = tmp
        if max < tmp: max = tmp
    return min, max


def get_plot_data(data):
    result = []
    count = 1
    for msg in data:
        result.append([0.1*count, msg2value(msg)])
        count += 1
    return result


def main():
    if len(sys.argv) < 2:
        print 'usage: ' + sys.argv[0] + ' <filename> [interval start] [interval end]'
        sys.exit(1)

    try:
        data = read_data(sys.argv[1])
    except Exception, ex:
        print str(ex)
        sys.exit(1)

    if len(sys.argv) > 2:
        start = int(sys.argv[2])
    else:
        start = 0

    if len(sys.argv) > 3:
        end = int(sys.argv[3])
    else:
        end = len(data)
    
    #outfile = file('druckdaten_mit_4800kg_ausschnitt1.out', 'ab')
    #[outfile.write(msg) for msg in data[450:800]]
    #outfile.close()

    gp = Gnuplot.Gnuplot(persist = 1)
    gp('set data style lines')
    plot_data = get_plot_data(data[start:end])
    plot1 = Gnuplot.PlotItems.Data(plot_data, with='lines', title=sys.argv[1])
    gp.plot(plot1)


if __name__ == "__main__": main()
