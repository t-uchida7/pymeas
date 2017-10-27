# -*- coding: utf-8 -*-
# -*- author: Taichi Uchida -*-

from ut_instrments import container

class Yokogawa7651(container):

	def _selfinit(self, **kwargs):
		self.safe_write('O1E')


	@property
	def current(self):
		res = str(self.safe_query('OD'))
		if res[3:4] != 'A':
			raise Exception('Set value is voltage!')
		self._current = float(res[4:-3])
		return self._current

	@current.setter
	def current(self, current):
		curr = str(current)
		self.safe_write('SA%sE', %(curr,))
		self._current = current

	@property
	def voltage(self):
		res = str(self.safe_query('OD'))
		if res[3:4] != 'V':
			raise Exception('Set value is current!')
		self._voltage = float(res[4:-3])
		return self._voltage

	@voltage.setter
	def voltage(self, voltage):
		volt = str(voltage)
		self.safe_write('SV%sE', %(volt,))
		self._voltage = voltage
