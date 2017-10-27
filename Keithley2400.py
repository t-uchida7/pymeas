# -*- coding: utf-8 -*-
# -*- author: Taichi Uchida -*-
# -*- Last update: 2017/5/30 -*-

from ut_instruments import container

class Keithley2400_Meter(container):

	def _selfinit(self):

		self._term = 'LF'
		self.safe_write(':CURR:NPLC 1')
		self.safe_write(':VOLT:NPLC 1')
		self.safe_write(':RES:NPLC 1')


	@property
	def current(self):
		self._current = self.safe_query(':MEAS:CURR?')
		return self._current

	@property
	def voltage(self):
		self._voltage = self.safe_query(':MEAS:VOLT?')
		return self._voltage

	@property
	def resistance(self):
		self._resistance = self.safe_query(':MEAS:RES?')
		return self._resistance


class Keithley2400_Source(container):
	
	def _selfinit(self):
		self._term = 'LF'
		self.safe_write(':CURR:NPLC 1')
		self.safe_write(':VOLT:NPLC 1')
		self.safe_write(':RES:NPLC 1')
		self.safe_write(':OUTP 1')
		self.safe_write(':SOUR:CLE:AUTO 1')
		self.safe_write(':SOUR:CURR:RANG:AUTO 1')
		self.safe_write(':SOUR:VOLT:RANG:AUTO 1')

	@property
	def current(self):
		self._current = self.safe_query(':CURR?')
		return self._current

	@current.setter
	def current(self, amp):
		if abs(amp) > 1.05:
			raise Exception('Specified value is out of the limit. Limit is 1.05A.')
		self.safe_write(':SOUR:CURR ' + str(amp))
		self._current = amp

	@property
	def voltage(self):
		self._voltage = self.safe_query(':VOLT?')
		return self._voltage

	@voltage.setter
	def voltage(self, volt):
		if abs(volt) > 210:
			raise Exception('Specified value is out of the limit. Limit is 210 V.')
		self.safe_write(':SOUR:VOLT ' + str(volt))
		self._voltage = volt



