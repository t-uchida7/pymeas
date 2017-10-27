# -*- coding: utf-8 -*-
# -*- author: Taichi Uchida -*-
# -*- Last update: 2017/9/27 -*-


import numpy as np
import os
from datetime import datetime
import h5py
from collections import OrderedDict
import matplotlib.pyplot as plt

class storing(object):
	'''
	Used for data storing. Also see existing jupyter notebook for measurement for how to use.
	axis(var_name, values, unit) : Called to define axis.
	                            var_name(str) : The name of variable.
	                            values(float) : The list of specified variable.
	                            unit(str)     : The unit of values.
	loop(void) : Generates axis variables defined before.
	            The loop depth corresponds the order of defining axis.
	store(value, var_name, unit) : Stores the value as var_name.
	                            value(float)  : The value of measuring variable.
	                            var_name(str) : The name of variable.
	                            unit(str)     : the unit of value.
	comment(comments): Stores comment.
					comments(str) : The comment to memorize about the data, such as condition.'''

	def __init__(self, file_name = '', **kwargs):
		times = str(datetime.now())
		if not file_name:
			file_name = times[:4]+times[5:7]+times[8:10]+times[11:13]+times[14:16]+times[17:19] + '.h5'
		self._file      = h5py.File(file_name, 'x')
		self.axes       = OrderedDict()
		self.units      = OrderedDict()
		self._loop_call = 0
		self.dataset    = {}
		self._shape     = []
		self._loc       = []
		self._lp        = {}
		self._comment   = ''

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		dt = h5py.special_dtype(vlen=str)
		self._file.create_dataset('comment', (1,), dtype=dt)
		self._file['comment'][0] = self._comment
		self._file.flush()
		self._file.close()

	def axis(self, var_name, values, unit = None):
		self._file.create_dataset(var_name, data = values)
		self.axes[var_name] = values
		self._shape.append(len(values))
		self._loc.append(0)
		if unit == None:
			self.units[var_name] = 'None'
		else:
			self.units[var_name] = unit

	def loop(self):
		if self._loop_call+1 > len(self.axes):
			raise Exception('loop should be calld as many times as the number of axes.')
		ax_name, ax_range = list(self.axes.items())[self._loop_call]
		self._loop_call   += 1
		for idx,x in enumerate(ax_range):
			self._loc[list(self.axes.keys()).index(ax_name)] = idx
			yield x
		idx = 0
		self._loop_call -= 1
		

	def store(self,  value, var_name = 'target', unit = None):##please call '%matplotlib' on jupyter notebook for live plot.
		try:
			self.dataset[var_name]
			exec('self.dataset["' + var_name + '"]' + str(self._loc[:self._loop_call]) + '=' + 'value')
			self._lp[var_name].update(self._file, self._loc)
		except KeyError:
		# if self.dataset == None:
		# 	self.dataset = self._file.create_dataset(var_name, tuple(self._shape[:self._loop_call]))#, h5py.special_dtype(vlen=str))
			self.dataset[var_name] = self._file.create_dataset(var_name, tuple(self._shape[:self._loop_call]))
			if unit == None:
				self.units[var_name] = 'None'
			else:
				self.units[var_name] = unit
			self.axes[var_name] = 'target'
			try:
				dt = h5py.special_dtype(vlen=str)
				self._file.create_dataset('units', (len(self.units),), dtype=dt)
				self._file.create_dataset('axes', (len(self.units),), dtype=dt)
				for idx, ax in enumerate(self.units.keys()):
					unit = self.units[ax]
					self._file['axes'][idx]  = ax
					self._file['units'][idx] = 'a.u.' if unit == 'None' else unit
			except RuntimeError:
				del self._file['units'], self._file['axes']
				dt = h5py.special_dtype(vlen=str)
				self._file.create_dataset('units', (len(self.units),), dtype=dt)
				self._file.create_dataset('axes', (len(self.units),), dtype=dt)
				for idx, ax in enumerate(self.units.keys()):
					unit = self.units[ax]
					self._file['axes'][idx]  = ax
					self._file['units'][idx] = 'a.u.' if unit == 'None' else unit
			exec('self.dataset["'+ var_name + '"]' + str(self._loc[:self._loop_call]) + '=' + 'value')
			self._lp[var_name] = live_plotting(self._file, var_name)
			#print(var_name)
			
	def comment(self, comments):
		self._comment += ' , ' + comments



class live_plotting(object):
	'''
	For the moment, this class can deal with 1D plot. 
	'''
	def __init__(self, file_obj, var_name):
		self.fig, self.ax = plt.subplots(1,1)
		live_axes = [ax for ax in file_obj['axes'] if ax != 'units']
		self.x_key = live_axes[0]
		self.y_key = var_name
		init_x = file_obj[self.x_key].value[0]
		init_y = file_obj[self.y_key].value[0]
		self.live_lines, = self.ax.plot(init_x, init_y)

	def update(self, file_obj, loc):
		x = file_obj[self.x_key].value[:loc[0]+1]
		y = file_obj[self.y_key].value[:loc[0]+1]
		self.live_lines.set_data(x,y)
		self.ax.set_xlim((x.min(), x.max()))
		self.ax.set_ylim((y.min(), y.max()))
		plt.pause(0.05)
##################################3
	# def init2D(self, file_obj, var_name)
	# 	self.fig, self.ax = plt.subplots(1,1)
	# 	live_axes = [ax for ax in file_obj['axes'] if ax != 'units']
	# 	im  = plt.gca().pcolormesh(x_arr, y_arr, z_arr, cmap = cmap, vmax = vmax)
	# 	fig.colorbar(im)
##################################33


def loading(file_name=None):

	class var_dict(object):
		def __init__(self):
			pass

	list_types = [list, np.ndarray]

	if file_name == None:
		file_list = [name for name in os.listdir() if name.endswith('.h5')]
		file_name = file_list[-1]
	else:
		if not file_name.endswith('.h5'):
			file_name += '.h5'
	file  = h5py.File(file_name, 'r')
	axes  = [ax for ax in file['axes'] if ax != 'units']
	#print(file['axes'])
	var   = {}

	for idx, ax in enumerate(axes):
		vd = var_dict()
		vd.values = file[ax].value
		depth = '0'
		try:
			vd.unit   = file['units'].value[idx]
		except KeyError:
			pass
		var[ax] = vd
	var['file_name'] = file_name
	var['comment']   = file['comment']
	return var


def plotting(loaded_object = None, title = None, facet =False, reverse = False):

	x_arr  = {}; y_arr = {}; z_arr = {}
	plot_axes = []
	if title == None:
		title = loaded_object['file_name'].split('.')[0]
		print(title)
	
	not_axis = ['comment', 'file_name']

	for ax in loaded_object.keys():
		if not ax in not_axis:
			values = loaded_object[ax].values
			unit   = loaded_object[ax].unit
			if len(np.shape(values)) == 2 :
				if z_arr:
					raise Exception('There seem to be more  than 2 data likely to be z_array.')
				z_axis      = ax
				z_array[ax] = (unit, values)
			else:
				plot_axes.append({'axis':ax, 'arr':(unit, values)})

				# if not x_arr:
				# 	x_axis    = ax
				# 	x_arr[ax] = (unit, values)
				# elif not y_arr:
				# 	y_axis    = ax
				# 	y_arr[ax] = (unit, values)
				# else:
				# 	print(x_axis, y_axis, ax)
				# 	raise Exception('There seem to be mo re than 3 data likely to be x/y array.')

	if not reverse:
		x_axis, x_arr = plot_axes[0]['axis'], plot_axes[0]['arr']
		y_axis, y_arr = plot_axes[1]['axis'], plot_axes[1]['arr']

	if reverse:
		x_axis, x_arr = plot_axes[1]['axis'], plot_axes[1]['arr']
		y_axis, y_arr = plot_axes[0]['axis'], plot_axes[0]['arr']

	if x_arr and y_arr and z_arr:
		print (x_arr, y_arr, z_arr)
		plot_2D(x_arr[x_axis][1], y_arr[y_axis][1], z_arr[z_axis][1], \
			x_label = x_axis + ' ' + x_arr[x_axis][0], \
			y_label = y_axis + ' ' + y_arr[y_axis][0], \
			z_label = z_axis + ' ' + z_arr[z_axis][0], \
			title = title)

	elif x_arr and y_arr:
		plot_1D(x_arr[1], y_arr[1], \
			x_label = x_axis + ' (' + x_arr[0] + ')', \
			y_label = y_axis + ' (' + y_arr[0] + ')', \
			title = title)



def plot_1D(x_arr, y_arr, x_label = None, y_label = None, title = None, show = True): # facet mo toritaine
	
	if x_label != None and y_label != None:
		if show:
			fig = plt.figure()
		plt.plot(x_arr, y_arr)
		plt.xlabel(x_label)
		plt.ylabel(y_label)
		if title:
			plt.title(title)
		fig.patch.set_alpha(1.0);fig.patch.set_facecolor('w');plt.tight_layout()
		if show:
			plt.show()
		return fig

	with cframe() as stack:

		var_names = stack_search(stack, 'plot_1D')
		if show:
			fig = plt.figure()
		plt.plot(x_arr, y_arr)
		if x_label:
			plt.xlabel(x_label)
		else:
			plt.xlabel(var_names[0])
		if y_label:
			plt.ylabel(y_label)
		else:
			plt.ylabel(var_names[1])
		if title:
			plt.title(title)
		fig.patch.set_alpha(1.0);fig.patch.set_facecolor('w');plt.tight_layout()
		if show:
			plt.show()
		return fig


def plot_2D(x_arr, y_arr, z_arr, x_label = None, y_label = None, z_label = None, title = None, cmap = 'plasma', vmax = None, show = True):
	
	with cframe() as stack:
		fig, ax = plt.subplots(figsize = (5.5, 4))
		im  = plt.gca().pcolormesh(x_arr, y_arr, z_arr, cmap = cmap, vmax = vmax)
		fig.colorbar(im)
		var_names = stack[1].code_context[0].split('(')[1].split(')')[0].split(',')
		if x_label:
			plt.xlabel(x_label)
		else:
			plt.xlabel(var_names[0])
		if y_label:
			plt.ylabel(y_label)
		else:
			plt.ylabel(var_names[1])

		plt.title(title)
		fig.patch.set_alpha(1.0);fig.patch.set_facecolor('w');plt.tight_layout() #with this line, we can copy graph with axis.
		if show:
			fig.canvas.draw()



def loading_and_plotting(file_name = None):
	if file_name == None:
		file_list = [name for name in os.listdir() if name.endswith('.h5')]
		file_name = file_list[-1]
	else:
		if not file_name.endswith('.h5'):
			file_name += '.h5'

	file_obj= loading(file_name)
	plotting(loaded_object = file_obj)



##--ancillas--

class cframe(object):

	def __init__(self):
		globals()['inspect'] = __import__('inspect')

	def __enter__(self):
		self.frame = inspect.currentframe()
		self.stack = inspect.getouterframes(self.frame)
		return self.stack

	def __exit__(self, exception_type, exception_value, Traceback):
		del self.stack


def stack_search(stack, context): #this function might have to be rewritten when official python changed the specification of frame object.
	frame_dicts = []
	infomations = ['frame', 'filename', 'lineno', 'function', 'code_context', 'index']
	for frame in stack:
		div_frame = str(frame)[10:-1].split(', ') # I'd like to rewrite here more elegantly.. (more good process for FrameInfo )
		for n, info in enumerate(infomations):
			if n == 0:
				frame_dicts.append({info:div_frame[n][len(info)+1:]})
			else:
				frame_dicts[-1][info] = div_frame[n][len(info)+1:]

	for frame in frame_dicts:
		if frame['code_context'].find(context) != -1:
			args = frame['code_context'].split('(')[1].split(')')[0].split(',')

	return args