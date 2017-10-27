# -*- coding: utf-8 -*-
# -*- author: Taichi Uchida -*-
# -*- Last update: 2017/6/2 -*-

from ut_instruments import container
import re
import time

class IPS(container):

	self._term = 'CR'
	self._field_limit = 10.0

	def _selfinit(self):

		self.safe_write('$C3')
		raise Exception('Did you checked and rewrite sweep rate?')
		self.safe_write('$T')# check sweep rate and rewrite here later
		self._seep_rate = #T/min
		# I assume sweep_rate may not be changed for query problem.


	@property
	def field(self):
		return self._field

	@field.setter
	def field(self, B):
		if B > self._field_limit:
	 		raise Exception('Specidied field value is out of the limit! Maximum field of this system is ' + str(self._field_limit) + 'T.')
		B_decim = "{0:.3f}".format(B) 	
	 	self.safe_write('$J' + B_decim)
	 	self.safe_write('$A1')
	 
	 	sweep_time = abs(B-self._field)/self._sweep_rate*60
	 	time.sleep(sweep_time*3)
	 	self._field = B
	 	


	def sweep_stop(self):
		self.safe_write('A0' + self._term)



