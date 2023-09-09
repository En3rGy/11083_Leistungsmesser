# coding: UTF-8

##!!!!##################################################################################################
#### Own written code can be placed above this commentblock . Do not change or delete commentblock! ####
########################################################################################################
##** Code created by generator - DO NOT CHANGE! **##

class Leistungsmesser_11083_11083(hsl20_4.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_4.BaseModule.__init__(self, homeserver_context, "hsl20_3_Powermeter")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_4.LOGGING_NONE,())
        self.PIN_I_IC=1
        self.PIN_I_RESET1=2
        self.PIN_I_RESET2=3
        self.PIN_I_RESET3=4
        self.PIN_I_GAIN=5
        self.PIN_I_RESET=6
        self.PIN_I_OFFSET=7
        self.PIN_O_TS1_CONS_CURR=1
        self.PIN_O_TS1_CONS_PEV=2
        self.PIN_O_TS2_CONS_CURR=3
        self.PIN_O_TS2_CONS_PEV=4
        self.PIN_O_TS3_CONS_CURR=5
        self.PIN_O_TS3_CONS_PEV=6
        self.PIN_O_GC=7
        self.REM_GC=1
        self.REM_TS1_GC_STS=2
        self.REM_TS2_GC_STS=3
        self.REM_TS3_GC_STS=4
        self.REM_IC_PREV=5
        self.REM_TS1_CONS_PREV=6
        self.REM_TS2_CONS_PREV=7
        self.REM_TS3_CONS_PREV=8

########################################################################################################
#### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
###################################################################################################!!!##

        self.data_sets = [DataSet()]
        self.g_out_sbc = {}
        self.remanent_storage_period_deltas = []
        self.remanent_storage_last_period_deltas = []
        self.input_pins_period_reset = []
        self.output_pins_period_delta = []
        self.output_pins_last_period_delta = []
        self.counter_global = 0  # global counter
        self.gain = 1
        self.offset = 0
        self.precision = 4

    def set_output_value_sbc(self, pin, val):
        """
        Round val with self.precision before output.

        :type pin: int
        :type val: Any
        :rtype: None
        """
        # print ("Entering set_output_value_sbc({}, {})".format(pin, val))
        val = round(val, self.precision)

        if pin in self.g_out_sbc:
            if self.g_out_sbc.get(pin) == val:
                # print ("# SBC: pin {} <- data not send / {}".format(pin, str(val).decode("utf-8")))
                return

        self._set_output_value(pin, val)
        self.g_out_sbc[pin] = val

    # Helper function
    def scale_value(self, value):
        """
        :param value:
        :type value: float
        :return:
        :rtype: float
        """

        # print("Entering scale_ic(self, {})".format(counter_in))
        value = (value * float(self.gain)) - self.offset
        value = round(value, self.precision)
        return value

    def on_init(self):
        print("Entering on_init")
        self.DEBUG = self.FRAMEWORK.create_debug_section()
        self.g_out_sbc = {}

        self.input_pins_period_reset = [self.PIN_I_RESET1, self.PIN_I_RESET2, self.PIN_I_RESET3]

        self.remanent_storage_period_deltas = [self.REM_TS1_GC_STS, self.REM_TS2_GC_STS, self.REM_TS3_GC_STS]
        self.remanent_storage_last_period_deltas = [self.REM_TS1_CONS_PREV, self.REM_TS2_CONS_PREV,
                                                    self.REM_TS3_CONS_PREV]
        self.output_pins_period_delta = [self.PIN_O_TS1_CONS_CURR, self.PIN_O_TS2_CONS_CURR, self.PIN_O_TS3_CONS_CURR]
        self.output_pins_last_period_delta = [self.PIN_O_TS1_CONS_PEV, self.PIN_O_TS2_CONS_PEV, self.PIN_O_TS3_CONS_PEV]

        self.data_sets = [DataSet() for _ in range(3)]

        try:
            counter_global = float(self._get_remanent(self.REM_GC))
        except:
            counter_global = 0

        for i in range(len(self.data_sets)):
            try:
                period_delta = float(self._get_remanent(self.remanent_storage_period_deltas[i]))
            except:
                period_delta = 0

            try:
                last_period_delta = float(self._get_remanent(self.remanent_storage_last_period_deltas[i]))
            except:
                last_period_delta = 0

            self.data_sets[i].restore_values(counter_global, period_delta, last_period_delta)

            self.set_output_value_sbc(self.output_pins_period_delta[i], period_delta)
            self.set_output_value_sbc(self.output_pins_last_period_delta[i], last_period_delta)

        self.set_output_value_sbc(self.PIN_O_GC, self.counter_global)

        self.gain = self._get_input_value(self.PIN_I_GAIN)
        self.offset = self._get_input_value(self.PIN_I_OFFSET)
        print("Leaving on_init")

    def on_input_value(self, index, value):
        print("Entering on_input_value({},{})".format(index, value))

        if index == self.PIN_I_IC:
            if value == 0:
                return
            else:
                value_scaled = self.scale_value(value)
                if self.counter_global == value_scaled:
                    return

                self.counter_global = value_scaled
                self.set_output_value_sbc(self.PIN_O_GC, self.counter_global)
                self._set_remanent(self.REM_GC, self.counter_global)

                for i in range(len(self.data_sets)):
                    period_delta = self.data_sets[i].set_counter_value(self.counter_global)

                    self.set_output_value_sbc(self.output_pins_period_delta[i], period_delta)
                    self._set_remanent(self.remanent_storage_period_deltas[i], period_delta)

        elif index == self.PIN_I_GAIN:
            self.gain = value

        elif index == self.PIN_I_OFFSET:
            self.offset = value

        elif index in self.input_pins_period_reset and value:
            i = self.input_pins_period_reset.index(index)
            last_period_delta = self.data_sets[i].period_reset()

            self.set_output_value_sbc(self.output_pins_last_period_delta[i], last_period_delta)
            self._set_remanent(self.remanent_storage_last_period_deltas[i], last_period_delta)

            self.set_output_value_sbc(self.output_pins_period_delta[i], 0)

        elif index == self.PIN_I_RESET and value:
            for data_set in self.data_sets:
                data_set.reset()

        print("Leaving on_input_value")


class DataSet:
    def __init__(self):
        self.counter_global_value = 0
        self.counter_global_period_start = 0
        self.period_delta = 0
        self.last_period_delta = 0

    def restore_values(self, counter_global_value, period_delta, last_period_delta):
        """
        :param counter_global_value:
        :type counter_global_value: float
        :param period_delta:
        :type period_delta: float
        :param last_period_delta:
        :type last_period_delta: float
        :return: None
        :rtype: None
        """
        self.counter_global_value = counter_global_value
        self.last_period_delta = last_period_delta
        self.counter_global_period_start = counter_global_value - period_delta
        self.period_delta = period_delta

    def set_counter_value(self, counter_global_value_new):
        """
        :param counter_global_value_new: Corrected new global counter value
        :type counter_global_value_new: float
        :return: New period value, based on the new global counter value
        """
        if counter_global_value_new == self.counter_global_value:
            return counter_global_value_new

        elif counter_global_value_new < self.counter_global_value:
            print("Warning: Counter overrun detected. Values from last trigger to the overflow point are lost.")
            # Definitely correct!
            # --> new start = - the delta between the last start and the last counter before the overrun.
            self.counter_global_period_start = self.counter_global_period_start - self.counter_global_value

        self.counter_global_value = counter_global_value_new
        self.period_delta = self.counter_global_value - self.counter_global_period_start
        return self.period_delta

    def period_reset(self):
        """
        :rtype: float
        :return: Relative counter of last period.
        """
        self.counter_global_period_start = self.counter_global_value
        last_period_delta = self.period_delta
        self.period_delta = 0
        return last_period_delta

    def get_period_delta(self):
        """
        :return:
        :rtype: float
        """
        return self.period_delta

    def get_last_period_delta(self):
        """
        :return:
        :rtype: float
        """
        return self.last_period_delta

    def reset(self):
        self.counter_global_value = 0
        self.counter_global_period_start = 0
        self.period_delta = 0
        self.last_period_delta = 0

