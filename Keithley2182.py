# -*- coding: utf-8 -*-
# -*- author: Taichi Uchida -*-
# -*- Last update: 2017/5/30 -*-

from ut_instruments import container

def Keithley2182(container):

	def _selfinit(self):
		self.safe_write(':SENS:VOLT:NPLC 1')

	@property
	def voltage(self):
		self._voltage = self.safe_query(':MEAS:VOLT?')
		return self._voltage