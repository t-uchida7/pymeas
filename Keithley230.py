# -*- coding: utf-8 -*-
# -*- author: Taichi Uchida -*-
# -*- Last update: 2017/5/30 -*-

from ut_instruments import container

class Keithley230(container):

	self._term = '　X'

	def _selfinit(self):
		self._voltage = 0.
		self.safe_write('REN')

	@property
	def voltage(self):
		return self._voltage

	@voltage.setter
	def voltage(self, volt):
		if volt > 101:
			raise Exception('Specified value is over the limit. Limit is 101 V.')
		self.safe_write('V'+str(volt)+'F1'+self._term)
		self._voltage = volt