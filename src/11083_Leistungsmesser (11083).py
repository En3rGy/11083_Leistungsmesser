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
        self.FRAMEWORK._run_in_context_thread(self.on_init)

########################################################################################################
#### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
###################################################################################################!!!##

    gc_sts = [0] * 3  # global counter at start of time span
    cons_prev = [0] * 3  # consumption of previous time span
    gc = 0  # global counter
    ic_prev = 0  # Last input counter value received, respecting gain and offset
    gain = 1
    offset = 0
    precision = 6
    init_run = True

    # Helper function
    def scale_ic(self, ic):
        return (ic * self.gain) - self.offset

    # 1st
    def calc_global_counter(self, ic):
        self.DEBUG.set_value("1 ic", ic)

        ic_prev = self.ic_prev
        ic_scaled = self.scale_ic(ic)

        if self.init_run:
            if ic != 0:
                self.init_run = False
                return True
            else:
                return False

        # increase global counter
        # pulse
        if ic == 1:
            self.gc += ic_scaled
        # no update
        elif ic_scaled == ic_prev:
            return False
        # overflow
        elif ic_prev > ic_scaled:
            self.gc += ic_scaled
        # usual counter
        else:
            self.gc += (ic_scaled - ic_prev)

        self.ic_prev = ic_scaled

        self.DEBUG.set_value("2 ic_scaled", ic_scaled)
        self.DEBUG.set_value("3 ic_prev", self.ic_prev)
        self.DEBUG.set_value("4 gc", self.gc)
        self._set_remanent(self.REM_IC_PREV, self.ic_prev)

        return True

    # 2nd
    def process_counter(self):
        for i in range(3):
            if i == 0:
                pin = self.PIN_O_TS1_CONS_CURR
            elif i == 1:
                pin = self.PIN_O_TS2_CONS_CURR
            elif i == 2:
                pin = self.PIN_O_TS3_CONS_CURR

            ts_cons_curr = round(self.gc - self.gc_sts[i], self.precision)
            self._set_output_value(pin, ts_cons_curr)

    def process_int_reset(self, i):
        pin_prev = self.PIN_O_TS1_CONS_PEV
        pin_curr = self.PIN_O_TS1_CONS_CURR
        rem_gc_sts = self.REM_TS1_GC_STS
        rem_cons_prev = self.REM_TS1_CONS_PREV

        if i == 1:
            pin_prev = self.PIN_O_TS2_CONS_PEV
            pin_curr = self.PIN_O_TS2_CONS_CURR
            rem_gc_sts = self.REM_TS2_GC_STS
            rem_cons_prev = self.REM_TS2_CONS_PREV
        elif i == 2:
            pin_prev = self.PIN_O_TS3_CONS_PEV
            pin_curr = self.PIN_O_TS3_CONS_CURR
            rem_gc_sts = self.REM_TS3_GC_STS
            rem_cons_prev = self.REM_TS3_CONS_PREV

        self.cons_prev[i] = round(self.gc - self.gc_sts[i], self.precision)
        self.gc_sts[i] = self.gc
        self.DEBUG.set_value("gc_sts[" + str(i) + "]", self.gc_sts[i])
        self._set_output_value(pin_prev, self.cons_prev[i])
        self._set_output_value(pin_curr, 0)

        self._set_remanent(rem_gc_sts, self.gc_sts[i])
        self._set_remanent(rem_cons_prev, self.cons_prev[i])

    def reset(self):
        self.gc = 0
        self._set_remanent(self.REM_GC, self.gc)
        self._set_output_value(self.PIN_O_GC, self.gc)

        self.gc_sts[0] = 0
        self.cons_prev[0] = 0
        self._set_remanent(self.REM_TS1_GC_STS, 0)
        self._set_remanent(self.REM_TS1_CONS_PREV, 0)
        self._set_output_value(self.PIN_O_TS1_CONS_PEV, 0)
        self._set_output_value(self.PIN_O_TS1_CONS_CURR, 0)

        self.gc_sts[1] = 0
        self.cons_prev[1] = 0
        self._set_remanent(self.REM_TS2_GC_STS, 0)
        self._set_output_value(self.PIN_O_TS2_CONS_PEV, 0)
        self._set_output_value(self.PIN_O_TS2_CONS_CURR, 0)
        self._set_remanent(self.REM_TS2_CONS_PREV, 0)

        self.gc_sts[2] = 0
        self.cons_prev[2] = 0
        self._set_remanent(self.REM_TS3_GC_STS, 0)
        self._set_output_value(self.PIN_O_TS3_CONS_PEV, 0)
        self._set_output_value(self.PIN_O_TS3_CONS_CURR, 0)
        self._set_remanent(self.REM_TS3_CONS_PREV, 0)

        self.ic_prev = 0
        self._set_remanent(self.REM_IC_PREV, self.ic_prev)

        self.init_run = True

    def on_init(self):
        self.DEBUG = self.FRAMEWORK.create_debug_section()

        self.gc_sts = [0] * 3  # global counter at start of time span
        self.cons_prev = [0] * 3  # consumption of previous time span
        self.gc = 0  # global counter
        self.ic_prev = 0  # Last input counter value received, respecting gain and offset
        self.gain = 1
        self.offset = 0
        self.precision = 6
        self.init_run = True

        try:
            self.gc = float(self._get_remanent(self.REM_GC))
            self.init_run = False
        except:
            pass

        try:
            self.gc_sts[0] = float(self._get_remanent(self.REM_TS1_GC_STS))
        except:
            pass

        try:
            self.gc_sts[1] = float(self._get_remanent(self.REM_TS2_GC_STS))
        except:
            pass

        try:
            self.gc_sts[2] = float(self._get_remanent(self.REM_TS3_GC_STS))
        except:
            pass

        try:
            self.ic_prev = float(self._get_remanent(self.REM_IC_PREV))
        except:
            pass

        try:
            self.cons_prev[0] = float(self._get_remanent(self.REM_TS1_CONS_PREV))
        except:
            pass

        try:
            self.cons_prev[1] = float(self._get_remanent(self.REM_TS2_CONS_PREV))
        except:
            pass

        try:
            self.cons_prev[2] = float(self._get_remanent(self.REM_TS3_CONS_PREV))
        except:
            pass

        self.gain = self._get_input_value(self.PIN_I_GAIN)
        self.offset = self._get_input_value(self.PIN_I_OFFSET)

        self._set_output_value(self.PIN_O_TS1_CONS_PEV, self.cons_prev[0])
        self._set_output_value(self.PIN_O_TS2_CONS_PEV, self.cons_prev[1])
        self._set_output_value(self.PIN_O_TS3_CONS_PEV, self.cons_prev[2])
        self._set_output_value(self.PIN_O_TS1_CONS_CURR, self.cons_prev[0])
        self._set_output_value(self.PIN_O_TS2_CONS_CURR, self.cons_prev[1])
        self._set_output_value(self.PIN_O_TS3_CONS_CURR, self.cons_prev[2])
        self._set_output_value(self.PIN_O_GC, self.gc)

        self.process_counter()

    def on_input_value(self, index, value):

        if index == self.PIN_I_IC:
            if value == 0:
                return

            if self.init_run:
                self.ic_prev = self.scale_ic(value)
                self.init_run = False
                return

            ret = self.calc_global_counter(value)

            if ret:
                # process counter for intervals & store data
                self.process_counter()

                # store global counter
                self._set_output_value(self.PIN_O_GC, self.gc)
                self._set_remanent(self.REM_GC, self.gc)

        elif index == self.PIN_I_GAIN:
            self.gain = value

        elif index == self.PIN_I_OFFSET:
            self.offset = value

        elif index == self.PIN_I_RESET1 and value != 0:
            self.process_int_reset(0)

        elif index == self.PIN_I_RESET2 and value != 0:
            self.process_int_reset(1)

        elif index == self.PIN_I_RESET3 and value != 0:
            self.process_int_reset(2)

        elif index == self.PIN_I_RESET and value != 0:
            self.reset()
