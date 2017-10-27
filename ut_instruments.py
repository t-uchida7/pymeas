# -*- coding: utf-8 -*-
# -*- author: Taichi Uchida -*-
# -*- Last update: 2017/5/29 -*-


import numpy
import visa
import signal


class KeyboardInterruptProtection(object):

    def __enter__(self):
        self.signal_received = False
        self.old_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self.handler)

    def handler(self, signal, frame):
        self.signal_received = (signal, frame)
        print('KeyboardInterrupt received. Delaying interrupt until a critical code finishes...')

    def __exit__(self, type, value, traceback):
        signal.signal(signal.SIGINT, self.old_handler)
        if self.signal_received:
            self.old_handler()


class container(object): # heritates this class to define each instrments.

    def __init__(self, interface = 'GPIB', bus = 0, addr = '',  **kwargs):

        bus = str(bus)
        addr = str(addr)

        if interface == 'GPIB':
            self.addr = 'GPIB' + bus + '::' + addr + '::INSTR'
        elif interface == 'Serial':
            self.addr = 'ASRL::' + addr + '::INSTR'
        #SCPI?

        rm = visa.ResourceManager()
        self.instr = rm.open_resource(self.addr)
        self._selfinit()


    def _selfinit(self): # for each instrment initialization should override this function.
        pass


    def safe_write(self, command):
        with KeyboardInterruptProtection():
            res = self.instr.write(command)
        return res

    def safe_query(self, command):
        with KeyboardInterruptProtection():
            res = self.instr.query(command)
        return res

    def safe_read(self,command):
        with KeyboardInterruptProtection():
            res = self.instr.read(commadn)
        return res

    def clear(self):
        self.instr.clear()
