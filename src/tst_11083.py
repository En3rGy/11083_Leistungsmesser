# coding: UTF-8

import unittest


class hsl20_3:
    LOGGING_NONE = 0

    def __init__(self):
        pass

    class BaseModule:
        debug_gain = 1.0  # type: float
        debug_offset = 0.0  # type: float
        debug_set_output_value = {}  # type: float
        debug_set_remanent = {}  # type: float

        def __init__(self, a, b):
            pass

        def _get_framework(self):
            f = hsl20_3.Framework()
            return f

        def _get_logger(self, a, b):
            return 0

        def _get_remanent(self, key):
            return 0

        def _set_remanent(self, key, val):
            self.debug_set_remanent = val

        def _set_output_value(self, pin, value):
            self.debug_set_output_value[pin] = value

        def _get_input_value(self, pin):
            if pin == 5:
                return self.debug_gain
            elif pin == 7:
                return self.debug_offset
            else:
                return 0

    class Framework:
        def __init__(self):
            pass

        def _run_in_context_thread(self, a):
            pass

        def create_debug_section(self):
            d = hsl20_3.DebugHelper()
            return d

    class DebugHelper:
        def __init__(self):
            pass

        def set_value(self, cap, text):
            print ("DEBUG value\t'" + str(cap) + "': " + str(text))

        def add_message(self, msg):
            print ("Debug Msg\t" + str(msg))


################################################
################################################

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
        self.REM_LAST_CNT_VAL=9
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

    def process_counter(self):
        for i in range(3):
            pin = self.PIN_O_TS1_CONS_CURR
            if i == 1:
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

        try:
            self.gc = float(self._get_remanent(self.REM_GC))
            self.gc_sts[0] = float(self._get_remanent(self.REM_TS1_GC_STS))
            self.gc_sts[1] = float(self._get_remanent(self.REM_TS2_GC_STS))
            self.gc_sts[2] = float(self._get_remanent(self.REM_TS3_GC_STS))

            self.ic_prev = float(self._get_remanent(self.REM_IC_PREV))

            self.cons_prev[0] = float(self._get_remanent(self.REM_TS1_CONS_PREV))
            self.cons_prev[1] = float(self._get_remanent(self.REM_TS2_CONS_PREV))
            self.cons_prev[2] = float(self._get_remanent(self.REM_TS3_CONS_PREV))
            self.init_run = False

        except:
            self.gc = 0
            self.gc_sts[0] = 0
            self.gc_sts[1] = 0
            self.gc_sts[2] = 0
            self.ic_prev = 0
            self.cons_prev[0] = 0
            self.cons_prev[1] = 0
            self.cons_prev[2] = 0
            self.init_run = True

        self.gain = self._get_input_value(self.PIN_I_GAIN)
        self.offset = self._get_input_value(self.PIN_I_OFFSET)

        self.process_counter()
        self.process_int_reset(0)
        self.process_int_reset(1)
        self.process_int_reset(2)

    def on_input_value(self, index, value):

        if index == self.PIN_I_IC:
            ic_curr = (value * self.gain) - self.offset

            if self.init_run:
                self.ic_prev = ic_curr
                self.init_run = False
                return

            # increase global counter
            # pulse
            if value == 1:
                self.gc += ic_curr
            # overflow
            elif self.ic_prev > ic_curr:
                self.gc += ic_curr
            # usual counter
            else:
                self.gc += ic_curr - self.ic_prev

            # process counter for intervals & store data
            self.process_counter()

            # store global counter
            self.ic_prev = ic_curr
            self._set_output_value(self.PIN_O_GC, self.gc)
            self._set_remanent(self.REM_GC, self.gc)
            self._set_remanent(self.REM_IC_PREV, self.ic_prev)

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


################################################
################################################


class RequirementsVerification(unittest.TestCase):

    def setUp(self):
        pass

    def test_req01_cons_curr_timespan(self):
        tst = Leistungsmesser_11083_11083(0)
        tst.on_init()
        tst.init_run = False
        tst.on_input_value(tst.PIN_I_IC, 10)      # gc 10
        tst.on_input_value(tst.PIN_I_RESET1, 1)   # gc_sts1 = 10
        self.assertEqual(0, tst.debug_set_output_value[tst.PIN_O_TS1_CONS_CURR], "msg=1")

        tst.on_input_value(tst.PIN_I_IC, 20)      # gc 20
        tst.on_input_value(tst.PIN_I_RESET2, 1)   # gc_sts2 = 20

        self.assertEqual(10, tst.debug_set_output_value[tst.PIN_O_TS1_CONS_CURR], "msg=2")
        self.assertEqual(0, tst.debug_set_output_value[tst.PIN_O_TS2_CONS_CURR], "msg=3")

        tst.on_input_value(tst.PIN_I_IC, 30.1)    # gc 30.1
        tst.on_input_value(tst.PIN_I_RESET3, 1)   # gc_sts3 = 30.1
        self.assertEqual(0, tst.debug_set_output_value[tst.PIN_O_TS3_CONS_CURR], "msg=4")

        tst.on_input_value(tst.PIN_I_IC, 40.2)    # gc 40.2

        self.assertEqual(30.2, tst.debug_set_output_value[tst.PIN_O_TS1_CONS_CURR], "msg=5")
        self.assertEqual(20.2, tst.debug_set_output_value[tst.PIN_O_TS2_CONS_CURR], "msg=6")
        self.assertEqual(10.1, tst.debug_set_output_value[tst.PIN_O_TS3_CONS_CURR], "msg=7")

    def test_req02_cons_prev_timespan(self):
        tst = Leistungsmesser_11083_11083(0)
        tst.on_init()
        tst.init_run = False
        tst.on_input_value(tst.PIN_I_IC, 10)      # gc 10
        tst.on_input_value(tst.PIN_I_RESET1, 1)   # gc_sts1 = 10
        self.assertEqual(10, tst.debug_set_output_value[tst.PIN_O_TS1_CONS_PEV])

        tst.on_input_value(tst.PIN_I_IC, 20)      # gc 20
        tst.on_input_value(tst.PIN_I_RESET2, 1)   # gc_sts2 = 20
        self.assertEqual(20, tst.debug_set_output_value[tst.PIN_O_TS2_CONS_PEV])

        tst.on_input_value(tst.PIN_I_IC, 30.1)    # gc 30.1
        tst.on_input_value(tst.PIN_I_RESET3, 1)   # gc_sts3 = 30.1
        tst.on_input_value(tst.PIN_I_IC, 40.2)    # gc 40.2
        self.assertEqual(30.1, tst.debug_set_output_value[tst.PIN_O_TS3_CONS_PEV])

    def test_req03_counter_input(self):
        tst = Leistungsmesser_11083_11083(0)
        tst.on_init()
        tst.init_run = False
        tst.on_input_value(tst.PIN_I_IC, 10)      # gc 10
        tst.on_input_value(tst.PIN_I_IC, 20)      # gc 20
        tst.on_input_value(tst.PIN_I_IC, 30.1)    # gc 30.1
        tst.on_input_value(tst.PIN_I_IC, 40.2)    # gc 40.2

        self.assertEqual(40.2, tst.debug_set_output_value[tst.PIN_O_GC])

    def test_req04_pulse_input(self):
        tst = Leistungsmesser_11083_11083(0)
        tst.on_init()
        tst.init_run = False
        tst.on_input_value(tst.PIN_I_GAIN, 10)
        tst.on_input_value(tst.PIN_I_IC, 1)
        tst.on_input_value(tst.PIN_I_IC, 1)
        tst.on_input_value(tst.PIN_I_IC, 1)
        tst.on_input_value(tst.PIN_I_IC, 1)

        self.assertEqual(40, tst.debug_set_output_value[tst.PIN_O_GC])

    def test_req05_start_timespan(self):
        tst = Leistungsmesser_11083_11083(0)
        tst.on_init()
        tst.init_run = False
        tst.on_input_value(tst.PIN_I_IC, 10)
        self.assertEqual(10, tst.gc)
        self.assertEqual(0, tst.gc_sts[0])

        tst.on_input_value(tst.PIN_I_RESET1, 1)
        self.assertEqual(10, tst.gc)
        self.assertEqual(10, tst.gc_sts[0])

        tst.on_input_value(tst.PIN_I_IC, 20)
        self.assertEqual(20, tst.gc)
        self.assertEqual(0, tst.gc_sts[1])

        tst.on_input_value(tst.PIN_I_RESET2, 1)
        tst.on_input_value(tst.PIN_I_IC, 30.1)
        tst.on_input_value(tst.PIN_I_RESET3, 1)
        tst.on_input_value(tst.PIN_I_IC, 40.2)

        self.assertEqual(10, tst.gc_sts[0])
        self.assertEqual(20, tst.gc_sts[1])
        self.assertEqual(30.1, tst.gc_sts[2])
        self.assertEqual(40.2, tst.gc)

    def test_req06_gain_input(self):
        tst = Leistungsmesser_11083_11083(0)
        tst.on_init()
        tst.init_run = False
        gain = 4
        tst.on_input_value(tst.PIN_I_GAIN, gain)
        self.assertEqual(gain, tst.gain)

    def test_req07_global_reset(self):
        tst = Leistungsmesser_11083_11083(0)
        tst.on_init()
        tst.init_run = False
        tst.gc = 100
        tst.gc_sts[0] = 10
        tst.gc_sts[1] = 20
        tst.gc_sts[2] = 30
        self.assertEqual(tst.gc_sts[2], 30)
        tst.on_input_value(tst.PIN_I_RESET, 1)
        self.assertEqual(tst.gc_sts[0], 0)
        self.assertEqual(tst.gc_sts[1], 0)
        self.assertEqual(tst.gc_sts[2], 0)
        self.assertEqual(tst.gc, 0)
        self.assertEqual(tst.ic_prev, 0)

    def test_req09_gain_offset(self):
        tst = Leistungsmesser_11083_11083(0)
        tst.debug_gain = 5
        tst.debug_offset = 2
        tst.on_init()
        tst.init_run = False
        tst.on_input_value(tst.PIN_I_IC, 10)
        self.assertEqual(tst.gc, 48)

    def test_req10_overflow(self):
        tst = Leistungsmesser_11083_11083(0)
        tst.on_init()
        tst.init_run = False
        self.assertEqual(tst.gc, 0)
        self.assertEqual(tst.ic_prev, 0)

        tst.on_input_value(tst.PIN_I_IC, 10)
        self.assertEqual(tst.gc, 10)
        self.assertEqual(tst.ic_prev, 10)

        tst.on_input_value(tst.PIN_I_IC, 5)
        self.assertEqual(tst.gc, 15)
        self.assertEqual(tst.ic_prev, 5)

    def test_req11_1st_run(self):
        tst = Leistungsmesser_11083_11083(0)
        tst.on_init()
        tst.init_run = True
        self.assertEqual(tst.gc, 0, "a")
        self.assertEqual(tst.ic_prev, 0, "b")

        tst.on_input_value(tst.PIN_I_IC, 5000)
        self.assertEqual(5000, tst.ic_prev, "c")
        self.assertEqual(0, tst.gc, "d")

        tst.on_input_value(tst.PIN_I_IC, 5005)
        self.assertEqual(5, tst.gc, "e")
        self.assertEqual(5005, tst.ic_prev, "f")


if __name__ == '__main__':
    unittest.main()
