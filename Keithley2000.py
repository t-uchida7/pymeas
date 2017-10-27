from ut_instrments import container
import numpy as np

class Keithley2000(container):

    '''
    Below descriptiuons are about current measuremetn.
    All functions are the same between current and voltage. So change 'current'->'voltage' about voltage. Also 'resistance' or 'fresistance' (four wire) can be measured.
    functions for AC also exist. You can call them like 'current_AC', 'current_AC_range', ...
    current                            : Read only. You can measure current value with this.
    current_range (float)              : Measurement range. Default is 3A. You can change this with float value [0,3.1]. In machine, this is discrete value, so it uses the best value refering the value you input.
    current_range_auto (bool)          : Automatically decide measurement range. Default is True.
    current_reference (bool, float)    : You can decide reference current (may be used to remove offset?). Default is False. 
                                         Input 'False' trun off reference. Input 'True' turn on reference and decide its value automatically refering input of front panel.
                                         Input float turn on reference and decide its value manually.
    current_filter (bool)              : Current averaging filter. Default is False. When read this value, you can see its on/off , type and count.
    current_filter_type ('MOV', 'REP') : Current averaging filter type. 'MOV' is moving average, 'REP' is repeating average.
    current_filter_count (int)         : Current averanging count [1,100].
    current_AC_bandwidth (float)       : Only for AC. For accuracy, this machine has 3 bandwidth type, [3Hz-300kHz], [30Hz-300kHz] and [300Hz-300kHz]. Default is [300Hz-300kHz].
                                         Input measurement frequency and automatically best bandwidth is selected.
                                         Note that for [3Hz-300kHz] and [3Hz-300kHz] bandwidth NPLC is off.
    '''

    def _selfinit(self):
        self.safe_write(':CURR:DC:NPLC 1') #NPLC = 1
        self.safe_write(':CURR:DC:RANG 3')
        self.safe_write(':CURR:DC:RANG:AUTO 1')
        self.safe_write(':CURR:DC:REF 0')
        self.safe_write(':CURR:DC:REF:STAT 0')
        self.safe_write(':CURR:DC:AVER:COUN 10')
        self.safe_write(':CURR:DC:AVER:STAT 0')

        self.safe_write(':CURR:AC:NPLC 1')
        self.safe_write(':CURR:AC:RANG 3')
        self.safe_write(':CURR:AC:RANG:AUTO 1')
        self.safe_write(':CURR:AC:REF 0')
        self.safe_write(':CURR:AC:REF:STAT 0')
        self.safe_write(':CURR:AC:AVER:COUN 10')
        self.safe_write(':CURR:AC:AVER:STAT 0')
        self.safe_write(':CURR:AC:DET:BAND 300')
        
        self.safe_write(':VOLT:DC:NPLC 1') 
        self.safe_write(':VOLT:DC:RANG 1000')
        self.safe_write(':VOLT:DC:RANG:AUTO 1')
        self.safe_write(':VOLT:DC:REF 0')
        self.safe_write(':VOLT:DC:REF:STAT 0')
        self.safe_write(':VOLT:DC:AVER:STAT 0')

        self.safe_write(':VOLT:AC:NPLC 1')
        self.safe_write(':VOLT:AC:RANG 757.5')
        self.safe_write(':VOLT:AC:RANG:AUTO 1')
        self.safe_write(':VOLT:AC:REF 0')
        self.safe_write(':VOLT:AC:REF:STAT 0')
        self.safe_write(':VOLT:AC:AVER:COUN 10')
        self.safe_write(':VOLT:AC:AVER:STAT 0')
        self.safe_write(':VOLT:AC:DET:BAND 300')

        self.safe_write(':RES:NPLC 1')
        self.safe_write(':RES:RANG 100e6')
        self.safe_write(':RES:RANG:AUTO 1')
        self.safe_write(':RES:REF 0')
        self.safe_write(':RES:REF:STAT 0')
        self.safe_write(':RES:AVER:COUN 10')
        self.safe_write(':RES:AVER:STAT 0')

        self.safe_write(':FRES:NPLC 1')
        self.safe_write(':FRES:RANG 100e6')
        self.safe_write(':FRES:RANG:AUTO 1')
        self.safe_write(':FRES:REF 0')
        self.safe_write(':FRES:REF:STAT 0')
        self.safe_write(':FRES:AVER:COUN 10')
        self.safe_write(':FRES:AVER:STAT 0')




    @property
    def current(self):
        self._current = float(self.safe_query(':MEAS:CURR?')[:-1])
        return self._current

    @property
    def current_range(self):
        self._current_range = float(self.safe_query(':CURR:RANG?')[:-1])
        return self._current_range

    @current_range.setter
    def current_range(self, upper):
        if upper > 3.1:
            raise Exception('Current range limit is 3.1A.')
        self.safe_write(':CURR:DC:RANG ' + str(upper))
        self._current_range = upper

    @property
    def current_range_auto(self):
        self._current_range_auto = bool(int(self.safe_query(':CURR:DC:RANG:AUTO?')[:-1]))
        return self._current_range_auto

    @current_range_auto.setter
    def current_range_auto(self, on_off):
        on_off_int = int(on_off)
        self.safe_write(':CURR:DC:RANG:AUTO %d'%(on_off_int))
        self._current_range_auto = on_off

    @property
    def current_reference(self):
        on_off = bool(int(self.safe_query(':CURR:DC:REF:STAT?')[:-1]))
        self._current_reference = float(self.safe_query(':CURR:DC:REF?')[:-1])
        print('DC current reference:' + str(on_off), '  AC reference current value:' + str(self._current_reference))
        return self._current_reference

    @current_reference.setter
    def current_reference(self, ref_val): #if False, off the reference. if True, automatically get reference. if given value, set it.
        if ref_val == False and isinstance(ref_val, bool):
            self.safe_write(':CURR:DC:REF:STAT 0')
        elif ref_val == True and isinstance(ref_val, bool):
            self.safe_write(':CURR:DC:REF:STAT 1')
            self.safe_write(':CURR:DC:REF:ACQ')
            self._current_reference = self.safe_query(':CURR:DC:REF?')[:-1]
        else:
            if abs(ref_val) > 3.1:
                raise Exception('Reference current limit is 3.1A.')
            self.safe_write(':CURR:DC:REF:STAT 1')
            self.safe_write(':CURR:DC:REF ' + str(ref_val))
            self._current_reference = ref_val

    @property
    def current_filter(self):
        self._current_filter_on    = bool(int(self.safe_query(':CURR:DC:AVER:STAT?')[:-1]))
        self._current_filter_type  = self.safe_query(':CURR:DC:AVER:TCON?')[:-1]
        self._current_filter_count = self.safe_query(':CURR:DC:AVER:COUN?')[:-1]
        print('filter:' + str(self._current_filter_on), '  type:' + self._current_filter_type, '  count:' + self._current_filter_count)
        return self._current_filter_on

    @current_filter.setter
    def current_filter(self, on_off):
        on_off_int = int(on_off)
        self.safe_write(':CURR:DC:AVER:STAT ' + str(on_off_int))
        self._current_filter_on = on_off

    @property
    def current_filter_type(self):
        self._current_filter_type = self.safe_query(':CURR:DC:AVER:TCON?')[:-1]
        return self._current_filter_type

    @current_filter_type.setter
    def current_filter_type(self, f_type):
        if not f_type in ['REP', 'MOV']:
            raise Exception("Filter type is 'REP' or 'MOV'.")
        self.safe_write(':CURR:DC:AVER:TCON ' + f_type)
        self._current_filter_type = f_type

    @property
    def current_filter_count(self):
        self._current_filter_count = float(self.safe_query(':CURR:DC:AVER:COUN?')[:-1])
        return self._current_filter_count

    @current_filter_count.setter
    def current_filter_count(self, f_count):
        if not 1 <= f_count <= 100:
            raise Exception('filter count limit is [1,100].')
        else:
            self.safe_write('CURR:DC:AVER:STAT %f'%(f_count))






    @property
    def current_AC(self):
        self._current_AC = float(self.safe_query(':MEAS:CURR:AC?')[:-1])
        return self._current_AC

    @property
    def current_AC_range(self):
        self._current_AC_range = float(self.safe_query(':CURR:AC:RANG?')[:-1])
        return self._current_AC_range

    @current_AC_range.setter
    def current_AC_range(self, upper):
        if upper > 3.1:
            raise Exception('Current range limit is 3.1A.')
        self.safe_write(':CURR:AC:RANG ' + str(upper))
        self._current_AC_range = upper

    @property
    def current_AC_range_auto(self):
        self._current_AC_range_auto = bool(int(self.safe_query(':CURR:AC:RANG:AUTO?')[:-1]))
        return self._current_AC_range_auto

    @current_AC_range_auto.setter
    def current_AC_range_auto(self, on_off):
        on_off_int = int(on_off)
        self.safe_write(':CURR:AC:RANG:AUTO %d'%(on_off_int))
        self._current_AC_range_auto = on_off

    @property
    def current_AC_reference(self):
        on_off = bool(int(self.safe_query(':CURR:AC:REF:STAT?')[:-1]))
        self._current_AC_reference = float(self.safe_query(':CURR:AC:REF?')[:-1])
        print('AC current reference:' + str(on_off), '  AC reference current value:' + str(self._current_AC_reference))
        return self._current_AC_reference

    @current_AC_reference.setter
    def current_AC_reference(self, ref_val): #if False, off the reference. if True, automatically get reference. if given value, set it.
        if ref_val == False and isinstance(ref_val, bool):
            self.safe_write(':CURR:AC:REF:STAT 0')
        elif ref_val == True and isinstance(ref_val, bool):
            self.safe_write(':CURR:AC:REF:STAT 1')
            self.safe_write(':CURR:AC:REF:ACQ')
            self._current_AC_reference = self.safe_query(':CURR:AC:REF?')[:-1]
        else:
            if abs(ref_val) > 3.1:
                raise Exception('AC Reference current limit is 3.1A.')
            self.safe_write(':CURR:AC:REF:STAT 1')
            self.safe_write(':CURR:AC:REF ' + str(ref_val))
            self._current_AC_reference = ref_val

    @property
    def current_AC_filter(self):
        self._current_AC_filter_on    = bool(int(self.safe_query(':CURR:AC:AVER:STAT?')[:-1]))
        self._current_AC_filter_type  = self.safe_query(':CURR:AC:AVER:TCON?')[:-1]
        self._current_AC_filter_count = self.safe_query(':CURR:AC:AVER:COUN?')[:-1]
        print('filter:' + str(self._current_AC_filter_on), '  type:' + self._current_AC_filter_type, '  count:' + self._current_AC_filter_count)
        return self._current_AC_filter_on

    @current_AC_filter.setter
    def current_AC_filter(self, on_off):
        on_off_int = int(on_off)
        self.safe_write(':CURR:AC:AVER:STAT ' + str(on_off_int))
        self._current_filter_AC_on = on_off

    @property
    def current_AC_filter_type(self):
        self._current_AC_filter_type = self.safe_query(':CURR:AC:AVER:TCON?')[:-1]
        return self._current_AC_filter_type

    @current_AC_filter_type.setter
    def current_AC_filter_type(self, f_type):
        if not f_type in ['REP', 'MOV']:
            raise Exception("Filter type is 'REP' or 'MOV'.")
        self.safe_write(':CURR:AC:AVER:TCON ' + f_type)
        self._current_AC_filter_type = f_type

    @property
    def current_AC_filter_count(self):
        self._current_AC_filter_count = float(self.safe_query(':CURR:AC:AVER:COUN?')[:-1])
        return self._current_AC_filter_count

    @current_AC_filter_count.setter
    def current_AC_filter_count(self, f_count):
        if not 1 <= f_count <= 100:
            raise Exception('filter count limit is [1,100].')
        else:
            self.safe_write('CURR:AC:AVER:STAT %f'%(f_count))

    @property
    def current_AC_bandwidth(self):
        self._current_AC_bandwidth = float(self.safe_query(':CURR:AC:DET:BAND?')[-1])
        if self._current_AC_bandwidth == 3:
            ret = '3Hz-300kHz'
        elif self._current_AC_bandwidth == 30:
            ret = '30Hz-300kHz'
        else:
            ret = '300Hz-300kHz'
        return ret

    @current_AC_bandwidth.setter
    def current_AC_bandwidth(self, freq):
        if not 3 <= freq <= 300e3:
            raise Exception('Bandwidth limit is [3,300e3].')
        self.safe_write(':CURR:AC:DET:BAND %f'%(freq))
        self._current_AC_bandwidth = freq








    @property
    def voltage(self):
        self._voltage = float(self.safe_query(':MEAS:VOLT?')[:-1])
        return self._voltage

    @property
    def voltage_range(self):
        self._voltage_range = float(self.safe_query(':VOLT:RANG?')[:-1])
        return self._voltage_range

    @voltage_range.setter
    def voltage_range(self, upper):
        if upper > 1010:
            raise Exception('voltage range limit is 1010 V.')
        self.safe_write(':VOLT:DC:RANG ' + str(upper))
        self._voltage_range = upper

    @property
    def voltage_range_auto(self):
        self._voltage_range_auto = bool(int(self.safe_query(':VOLT:DC:RANG:AUTO?')[:-1]))
        return self._voltage_range_auto

    @voltage_range_auto.setter
    def voltage_range_auto(self, on_off):
        on_off_int = int(on_off)
        self.safe_write(':VOLT:DC:RANG:AUTO %d'%(on_off_int))
        self._voltage_range_auto = on_off

    @property
    def voltage_reference(self):
        on_off = bool(int(self.safe_query(':VOLT:DC:REF:STAT?')[:-1]))
        self._voltage_reference = float(self.safe_query(':VOLT:DC:REF?')[:-1])
        print('voltage reference:' + str(on_off), 'reference voltage value:' + str(self._voltage_reference))
        return self._voltage_reference

    @voltage_reference.setter
    def voltage_reference(self, ref_val): #if False, off the reference. if True, automatically get reference. if given value, set it.
        if ref_val == False and isinstance(ref_val, bool):
            self.safe_write(':VOLT:DC:REF:STAT 0')
        elif ref_val == True and isinstance(ref_val, bool):
            self.safe_write(':VOLT:DC:REF:STAT 1')
            self.safe_write(':VOLT:DC:REF:ACQ')
            self._voltage_reference = self.safe_query(':VOLT:DC:REF?')[:-1]
        else:
            if abs(ref_val) > 1010:
                raise Exception('Reference voltage limit is 1010V.')
            self.safe_write(':VOLT:DC:REF:STAT 1')
            self.safe_write(':VOLT:DC:REF ' + str(ref_val))
            self._voltage_reference = ref_val

    @property
    def voltage_filter(self):
        self._voltage_filter_on    = bool(int(self.safe_query(':VOLT:DC:AVER:STAT?')[:-1]))
        self._voltage_filter_type  = self.safe_query(':VOLT:DC:AVER:TCON?')[:-1]
        self._voltage_filter_count = self.safe_query(':VOLT:DC:AVER:COUN?')[:-1]
        print('filter:' + str(self._voltage_filter_on), 'type:' + self._voltage_filter_type, 'count:' + self._voltage_filter_count)
        return self._voltage_filter_on

    @voltage_filter.setter
    def voltage_filter(self, on_off):
        on_off_int = int(on_off)
        self.safe_write(':VOLT:DC:AVER:STAT ' + str(on_off_int))
        self._voltage_filter_on = on_off

    @property
    def voltage_filter_type(self):
        self._voltage_filter_type = self.safe_query(':VOLT:DC:AVER:TCON?')[:-1]
        return self._voltage_filter_type

    @voltage_filter_type.setter
    def voltage_filter_type(self, f_type):
        if not f_type in ['REP', 'MOV']:
            raise Exception("Filter type is 'REP' or 'MOV'.")
        self.safe_write(':VOLT:DC:AVER:TCON ' + f_type)
        self._voltage_filter_type = f_type

    @property
    def voltage_filter_count(self):
        self._voltage_filter_count = self.safe_query(':VOLT:DC:AVER:COUN?')[:-1]
        return self._voltage_filter_count

    @voltage_filter_count.setter
    def voltage_filter_count(self, f_count):
        if not 1 <= f_count <= 100:
            raise Exception('filter count limit is [1,100].')
        else:
            self.safe_write(':VOLT:DC:AVER:STAT %f'%(f_count))






    @property
    def voltage_AC(self):
        self._voltage_AC = float(self.safe_query(':MEAS:VOLT:AC?')[:-1])
        return self._voltage_AC

    @property
    def voltage_AC_range(self):
        self._voltage_AC_range = float(self.safe_query(':VOLT:AC:RANG?')[:-1])
        return self._voltage_AC_range

    @voltage_AC_range.setter
    def voltage_AC_range(self, upper):
        if upper > 757.5:
            raise Exception('voltage range limit is 757.5 V.')
        self.safe_write(':VOLT:AC:RANG ' + str(upper))
        self._voltage_AC_range = upper

    @property
    def voltage_AC_range_auto(self):
        self._voltage_AC_range_auto = bool(int(self.safe_query(':VOLT:AC:RANG:AUTO?')[:-1]))
        return self._voltage_AC_range_auto

    @voltage_AC_range_auto.setter
    def voltage_AC_range_auto(self, on_off):
        on_off_int = int(on_off)
        self.safe_write(':VOLT:AC:RANG:AUTO %d'%(on_off_int))
        self._voltage_AC_range_auto = on_off

    @property
    def voltage_AC_reference(self):
        on_off = bool(int(self.safe_query(':VOLT:AC:REF:STAT?')[:-1]))
        self._voltage_AC_reference = float(self.safe_query(':VOLT:AC:REF?')[:-1])
        print('AC voltage reference:' + str(on_off), '  AC reference voltage value:' + str(self._voltage_AC_reference))
        return self._voltage_AC_reference

    @voltage_AC_reference.setter
    def voltage_AC_reference(self, ref_val): #if False, off the reference. if True, automatically get reference. if given value, set it.
        if ref_val == False and isinstance(ref_val, bool):
            self.safe_write(':VOLT:AC:REF:STAT 0')
        elif ref_val == True and isinstance(ref_val, bool):
            self.safe_write(':VOLT:AC:REF:STAT 1')
            self.safe_write(':VOLT:AC:REF:ACQ')
            self._voltage_AC_reference = self.safe_query(':VOLT:AC:REF?')[:-1]
        else:
            if abs(ref_val) > 1010:
                raise Exception('Reference voltage limit is 1010V.')
            self.safe_write(':VOLT:AC:REF:STAT 1')
            self.safe_write(':VOLT:AC:REF ' + str(ref_val))
            self._voltage_AC_reference = ref_val

    @property
    def voltage_AC_filter(self):
        self._voltage_AC_filter_on    = bool(int(self.safe_query(':VOLT:AC:AVER:STAT?')[:-1]))
        self._voltage_AC_filter_type  = self.safe_query(':VOLT:AC:AVER:TCON?')[:-1]
        self._voltage_AC_filter_count = self.safe_query(':VOLT:AC:AVER:COUN?')[:-1]
        print('filter:' + str(self._voltage_AC_filter_on), '  type:' + self._voltage_AC_filter_type, '  count:' + self._voltage_AC_filter_count)
        return self._voltage_AC_filter_on

    @voltage_AC_filter.setter
    def voltage_AC_filter(self, on_off):
        on_off_int = int(on_off)
        self.safe_write(':VOLT:AC:AVER:STAT ' + str(on_off_int))
        self._voltage_AC_filter_on = on_off

    @property
    def voltage_AC_filter_type(self):
        self._voltage_AC_filter_type = self.safe_query(':VOLT:AC:AVER:TCON?')[:-1]
        return self._voltage_AC_filter_type

    @voltage_AC_filter_type.setter
    def voltage_filter_type(self, f_type):
        if not f_type in ['REP', 'MOV']:
            raise Exception("Filter type is 'REP' or 'MOV'.")
        self.safe_write(':VOLT:AC:AVER:TCON ' + f_type)
        self._voltage_AC_filter_type = f_type

    @property
    def voltage_AC_filter_count(self):
        self._voltage_AC_filter_count = self.safe_query(':VOLT:ACC:AVER:COUN?')[:-1]
        return self._voltage_AC_filter_count

    @voltage_AC_filter_count.setter
    def voltage_AC_filter_count(self, f_count):
        if not 1 <= f_count <= 100:
            raise Exception('filter count limit is [1,100].')
        else:
            self.safe_write(':VOLT:AC:AVER:STAT %f'%(f_count))

    @property
    def voltage_AC_bandwidth(self):
        self._voltage_AC_bandwidth = float(self.safe_query(':VOLT:AC:DET:BAND?')[-1])
        if self._voltage_AC_bandwidth == 3:
            ret = '3Hz-300kHz'
        elif self._voltage_AC_bandwidth == 30:
            ret = '30Hz-300kHz'
        else:
            ret = '300Hz-300kHz'
        return ret

    @voltage_AC_bandwidth.setter
    def voltage_AC_bandwidth(self, freq):
        if not 3 <= freq <= 300e3:
            raise Exception('Bandwidth limit is [3,300e3].')
        self.safe_write(':VOLT:AC:DET:BAND %f'%(freq))
        self._voltage_AC_bandwidth = freq






    @property
    def resistance(self):
        self._resistance = float(self.safe_query(':MEAS:RES?')[:-1])
        return self._resistance

    @property
    def resistance_range(self):
        self._resitance_range = float(self.safe_query(':RES:RANG?')[:-1])
        return self._resistance_range

    @resistance_range.setter
    def resistance_range(self, upper):
        if upper > 120e6:
            raise Exception('voltage range limit is 120e6 Ohm.')
        self.safe_write(':RES:RANG ' + str(upper))
        self._resistance_range = upper

    @property
    def resistance_range_auto(self):
        self._resistance_range_auto = bool(int(self.safe_query(':RES:RANG:AUTO?')[:-1]))
        return self._resistance_range_auto

    @resistance_range_auto.setter
    def resistance_range_auto(self, on_off):
        on_off_int = int(on_off)
        self.safe_write(':RES:RANG:AUTO %d'%(on_off_int))
        self._resistance_range_auto = on_off

    @property
    def resistance_reference(self):
        on_off = bool(int(self.safe_query(':RES:REF:STAT?')[:-1]))
        self._resistance_reference = float(self.safe_query(':RES:REF?')[:-1])
        print('resistance reference:' + str(on_off), 'reference resistance value:' + str(self._resistance_reference))
        return self._resistance_reference

    @resistance_reference.setter
    def resistance_reference(self, ref_val): #if False, off the reference. if True, automatically get reference. if given value, set it.
        if ref_val == False and isinstance(ref_val, bool):
            self.safe_write(':RES:REF:STAT 0')
        elif ref_val == True and isinstance(ref_val, bool):
            self.safe_write(':RES:REF:STAT 1')
            self.safe_write(':RES:REF:ACQ')
            self._resistance_reference = self.safe_query(':RES:REF?')[:-1]
        else:
            if abs(ref_val) > 120e6:
                raise Exception('Reference resistance limit is 120e6 Ohm.')
            self.safe_write(':RES:REF:STAT 1')
            self.safe_write(':RES:REF ' + str(ref_val))
            self._resistance_reference = ref_val

    @property
    def resistance_filter(self):
        self._resistance_filter_on    = bool(int(self.safe_query(':RES:AVER:STAT?')[:-1]))
        self._resistance_filter_type  = self.safe_query(':RES:AVER:TCON?')[:-1]
        self._resistance_filter_count = self.safe_query(':RES:AVER:COUN?')[:-1]
        print('filter:' + str(self._resistance_filter_on), 'type:' + self._resistance_filter_type, 'count:' + self._resisntance_filter_count)
        return self._resistance_filter_on

    @resistance_filter.setter
    def resistance_filter(self, on_off):
        on_off_int = int(on_off)
        self.safe_write(':RES:AVER:STAT ' + str(on_off_int))
        self._resistance_filter_on = on_off

    @property
    def resistance_filter_type(self):
        self._resistance_filter_type = self.safe_query(':RES:AVER:TCON?')[:-1]
        return self._resistance_filter_type

    @resistance_filter_type.setter
    def resistance_filter_type(self, f_type):
        if not f_type in ['REP', 'MOV']:
            raise Exception("Filter type is 'REP' or 'MOV'.")
        self.safe_write(':RES:AVER:TCON ' + f_type)
        self._resistance_filter_type = f_type

    @property
    def resistance_filter_count(self):
        self._resistance_filter_count = self.safe_query(':RES:AVER:COUN?')[:-1]
        return self._resistance_filter_count

    @resistance_filter_count.setter
    def resistance_filter_count(self, f_count):
        if not 1 <= f_count <= 100:
            raise Exception('filter count limit is [1,100].')
        else:
            self.safe_write(':RES:AVER:STAT %f'%(f_count))





    @property
    def fresistance(self):
        self._fresistance = float(self.safe_query(':MEAS:FRES?')[:-1])
        return self._fresistance

    @property
    def fresistance_range(self):
        self._fresitance_range = float(self.safe_query(':FRES:RANG?')[:-1])
        return self._fresistance_range

    @fresistance_range.setter
    def fresistance_range(self, upper):
        if upper > 101e6:
            raise Exception('fresistance range limit is 101e6 Ohm.')
        self.safe_write(':FRES:RANG ' + str(upper))
        self._fresistance_range = upper

    @property
    def fresistance_range_auto(self):
        self._fresistance_range_auto = bool(int(self.safe_query(':FRES:RANG:AUTO?')[:-1]))
        return self._fresistance_range_auto

    @fresistance_range_auto.setter
    def fresistance_range_auto(self, on_off):
        on_off_int = int(on_off)
        self.safe_write(':FRES:RANG:AUTO %d'%(on_off_int))
        self._fresistance_range_auto = on_off

    @property
    def fresistance_reference(self):
        on_off = bool(int(self.safe_query(':FRES:REF:STAT?')[:-1]))
        self._fresistance_reference = float(self.safe_query(':FRES:REF?')[:-1])
        print('resistance reference:' + str(on_off), 'reference resistance value:' + str(self._fresistance_reference))
        return self._fresistance_reference

    @fresistance_reference.setter
    def fresistance_reference(self, ref_val): #if False, off the reference. if True, automatically get reference. if given value, set it.
        if ref_val == False and isinstance(ref_val, bool):
            self.safe_write(':FRES:REF:STAT 0')
        elif ref_val == True and isinstance(ref_val, bool):
            self.safe_write(':FRES:REF:STAT 1')
            self.safe_write(':FRES:REF:ACQ')
            self._fresistance_reference = self.safe_query(':FRES:REF?')[:-1]
        else:
            if abs(ref_val) > 120e6:
                raise Exception('fReference resistance limit is 101e6 Ohm.')
            self.safe_write(':FRES:REF:STAT 1')
            self.safe_write(':FRES:REF ' + str(ref_val))
            self._fresistance_reference = ref_val

    @property
    def fresistance_filter(self):
        self._fresistance_filter_on    = bool(int(self.safe_query(':FRES:AVER:STAT?')[:-1]))
        self._fresistance_filter_type  = self.safe_query(':FRES:AVER:TCON?')[:-1]
        self._fresistance_filter_count = self.safe_query(':FRES:AVER:COUN?')[:-1]
        print('filter:' + str(self._fresistance_filter_on), 'type:' + self._fresistance_filter_type, 'count:' + self._fresisntance_filter_count)
        return self._fresistance_filter_on

    @fresistance_filter.setter
    def fresistance_filter(self, on_off):
        on_off_int = int(on_off)
        self.safe_write(':FRES:AVER:STAT ' + str(on_off_int))
        self._fresistance_filter_on = on_off

    @property
    def fresistance_filter_type(self):
        self._fresistance_filter_type = self.safe_query(':FRES:AVER:TCON?')[:-1]
        return self._fresistance_filter_type

    @fresistance_filter_type.setter
    def fresistance_filter_type(self, f_type):
        if not f_type in ['REP', 'MOV']:
            raise Exception("Filter type is 'REP' or 'MOV'.")
        self.safe_write(':FRES:AVER:TCON ' + f_type)
        self._fresistance_filter_type = f_type

    @property
    def fresistance_filter_count(self):
        self._fresistance_filter_count = self.safe_query(':FRES:AVER:COUN?')[:-1]
        return self._fresistance_filter_count

    @fresistance_filter_count.setter
    def fresistance_filter_count(self, f_count):
        if not 1 <= f_count <= 100:
            raise Exception('filter count limit is [1,100].')
        else:
            self.safe_write(':FRES:AVER:STAT %f'%(f_count))