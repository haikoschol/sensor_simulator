#/usr/bin/env python
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


class Observable(object):
    '''
    implements half of the observer pattern. it is not neccessary to use objects as
    observers. any kind of callable can be registered to be called, when the observable
    notifies the observers. the only constraint is, that the callable must take two
    arguments. first the observable that emitted the notification and second some kind
    of optional user supplied data that defaults to None.
    '''

    def __init__(self):
        self.__observers = set()


    def register(self, handler):
        '''
        register a callable that gets invoked when the observable notifies its observers.
        the callable must accept two arguments. the first will be the observable object,
        the second can be used by users of the Observable class to pass arbitrary data.
        '''
        self.__observers.add(handler)


    def unregister(self, handler):
        '''
        removes a notification handler
        '''
        try:
            self.__observers.remove(handler)
        except:
            pass


    def notify(self, userdata=None):
        '''
        notifies all registered observers of an update
        '''
        for handler in self.__observers:
            handler(self, userdata)

