# -*- coding: utf-8 -*-
# -*- author: Taichi Uchida -*-
# -*- Last update: 2017/5/31 -*-

from ut_instruments import container

class Keithley220(container):

	self._term = '　X'

	def _selfinit(self):
		self._current = 0.
		self.safe_write('REN')

	@property
	def current(self):
		return self._current

	@current.setter
	def current(self, amps):
		if amps > 101e-3:
			raise Exception('Specified value is over the limit. Limit is 101 mA.')
		self.safe_write('I'+str(amps)+'F1'+self._term)
		self._current = amps