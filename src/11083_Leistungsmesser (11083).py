# coding: UTF-8
##!!!!##################################################################################################
#### Own written code can be placed above this commentblock . Do not change or delete commentblock! ####
########################################################################################################
##** Code created by generator - DO NOT CHANGE! **##

class Leistungsmesser_11083_11083(hsl20_3.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_3.BaseModule.__init__(self, homeserver_context, "hsl20_3_Powermeter")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_3.LOGGING_NONE,())
        self.PIN_I_NCOUNTER=1
        self.PIN_I_NRESET1=2
        self.PIN_I_NRESET2=3
        self.PIN_I_NRESET3=4
        self.PIN_I_NGAIN=5
        self.PIN_I_NRESET=6
        self.PIN_I_NOFFSET=7
        self.PIN_O_NTOTAL=1
        self.PIN_O_NINT1CURR=2
        self.PIN_O_NINT1PREV=3
        self.PIN_O_NINT2CURR=4
        self.PIN_O_NINT2PREV=5
        self.PIN_O_NINT3CURR=6
        self.PIN_O_NINT3PREV=7
        self.REM_INT1CURR=1
        self.REM_INT1PAST=2
        self.REM_INT2CURR=3
        self.REM_INT2PAST=4
        self.REM_INT3CURR=5
        self.REM_INT3PAST=6
        self.REM_LAST_CNT_VAL=7
        self.REM_COUNTER=8
        self.FRAMEWORK._run_in_context_thread(self.on_init)

########################################################################################################
#### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
###################################################################################################!!!##

    g_past = []         # past abs value of interval i
    g_counter = 0       # abs value
    g_last_cnt_val = 0  # last in value

    def process_counter(self, index):
        curr = self.g_counter - self.g_past[index]
        self._set_remanent(self.REM_INT1CURR + index - 1, curr)
        self._set_output_value(self.PIN_O_NINT1CURR + index - 1, curr)
        self.g_past[index] = self.g_counter

    def process_int_reset(self, index):
        new_past = self.g_counter - self.g_past[index]
        self.g_past[index] = self.g_counter

        self._set_remanent(self.REM_INT1PAST + index - 1, new_past)
        self._set_output_value(self.PIN_O_NINT1PREV + index - 1, new_past)

        self._set_remanent(self.REM_INT1CURR + index - 1, 0)
        self._set_output_value(self.PIN_O_NINT1CURR + index - 1, 0)


    def on_init(self):
        self.DEBUG = self.FRAMEWORK.create_debug_section()

        try:
            self.g_counter = float(self._get_remanent(self.REM_COUNTER))
            self.g_last_cnt_val = float(self._get_remanent(self.REM_LAST_CNT_VAL))
            self.g_past[1] = float(self._get_remanent(self.REM_INT1PAST))
            self.g_past[2] = float(self._get_remanent(self.REM_INT2PAST))
            self.g_past[3] = float(self._get_remanent(self.REM_INT3PAST))
        except:
            self.g_counter = 0
            self.g_last_cnt_val = 0
            self.g_past[1] = 0
            self.g_past[2] = 0
            self.g_past[3] = 0

    def on_input_value(self, index, value):
        if index == self.PIN_I_NCOUNTER:
            gain = self._get_input_value(self.PIN_I_NGAIN)
            offset = self._get_input_value(self.PIN_I_NOFFSET)

            value = (value * gain) - offset

            # increase global counter
            if self.g_last_cnt_val > value:
                self.g_counter += value
            else:
                self.g_counter += value - self.g_last_cnt_val

            # process counter for intervals & store data
            self.process_counter(1)
            self.process_counter(2)
            self.process_counter(3)

            # store global counter
            self._set_remanent(self.REM_COUNTER, self.g_counter)
            self.g_last_cnt_val = self.g_counter

        elif index == self.PIN_I_NRESET1:
            self.process_int_reset(1)

        elif index == self.PIN_I_NRESET2:
            self.process_int_reset(2)

        elif index == self.PIN_I_NRESET3:
            self.process_int_reset(3)

        elif index == self.PIN_I_NRESET:
            self._set_remanent(self.REM_COUNTER, 0)
            self._set_remanent(self.REM_LAST_CNT_VAL, 0)
            self._set_remanent(self.REM_INT1PAST, 0)
            self._set_remanent(self.REM_INT1CURR, 0)
            self._set_remanent(self.REM_INT2PAST, 0)
            self._set_remanent(self.REM_INT2CURR, 0)
            self._set_remanent(self.REM_INT3PAST, 0)
            self._set_remanent(self.REM_INT3CURR, 0)
            self.g_past[1] = 0
            self.g_past[2] = 0
            self.g_past[3] = 0
            self.g_counter = 0
            self.g_last_cnt_val = 0
