# coding: UTF-8

import unittest


class hsl20_3:
    LOGGING_NONE = 0

    def __init__(self):
        pass

    class BaseModule:
        debug_gain = 1.0  # type: float
        debug_offset = 0.0  # type: float
        debug_set_output_value = {}
        debug_set_remanent = {}

        def __init__(self, a, b):
            pass

        def _get_framework(self):
            f = hsl20_3.Framework()
            return f

        def _get_logger(self, a, b):
            return 0

        def _get_remanent(self, key):
            if key in self.debug_set_remanent:
                return self.debug_set_remanent[key]
            else:
                return 0

        def _set_remanent(self, key, val):
            self.debug_set_remanent[key] = val

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
        self.FRAMEWORK._run_in_context_thread(self.on_init)

    ########################################################################################################
    #### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
    ###################################################################################################!!!##

    gc_sts = [0] * 3  # global counter at start of time span
    cons_prev = [0] * 3  # consumption of previous time span
    gc = 0  # global counter
    ic_curr = 0
    ic_prev = 0  # Last input counter value received, respecting gain and offset
    gain = 1
    offset = 0
    precision = 6
    init_run = True

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

        self.ic_curr = 0
        self.ic_prev = 0
        self._set_remanent(self.REM_IC_PREV, self.ic_prev)

        self.init_run = True

    def scale_ic(self, ic):
        return (ic * self.gain) - self.offset

    def calc_global_counter(self, ic):
        self.DEBUG.set_value("ic", ic)

        self.ic_prev = self.ic_curr
        self.ic_curr = self.scale_ic(ic)

        self.DEBUG.set_value("ic_curr", self.ic_curr)
        self.DEBUG.set_value("ic_prev", self.ic_prev)
        self._set_remanent(self.REM_IC_PREV, self.ic_prev)

        if self.init_run:
            self.init_run = False
            return True

        # increase global counter
        # pulse
        if ic == 1:
            self.gc += self.ic_curr
        # no update
        elif self.ic_curr == self.ic_prev:
            return False
        # overflow
        elif self.ic_prev > self.ic_curr:
            self.gc += self.ic_curr
        # usual counter
        else:
            self.gc += self.ic_curr - self.ic_prev

        self.DEBUG.set_value("gc", self.gc)

        return True

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

        self._set_output_value(self.PIN_O_TS1_CONS_PEV, self.cons_prev[0])
        self._set_output_value(self.PIN_O_TS2_CONS_PEV, self.cons_prev[1])
        self._set_output_value(self.PIN_O_TS3_CONS_PEV, self.cons_prev[2])
        self.process_counter()

    def on_input_value(self, index, value):

        if index == self.PIN_I_IC:
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


################################################
################################################


class RequirementsVerification(unittest.TestCase):

    def setUp(self):
        pass

    def test_req01_cons_curr_timespan(self):
        print("### test_req01_cons_curr_timespan")
        tst = Leistungsmesser_11083_11083(0)
        tst.reset()
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
        print("### test_req02_cons_prev_timespan")
        tst = Leistungsmesser_11083_11083(0)
        tst.reset()
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
        print("### test_req03_counter_input")
        tst = Leistungsmesser_11083_11083(0)
        tst.reset()
        tst.on_init()
        tst.init_run = False
        tst.on_input_value(tst.PIN_I_IC, 10)      # gc 10
        tst.on_input_value(tst.PIN_I_IC, 20)      # gc 20
        tst.on_input_value(tst.PIN_I_IC, 30.1)    # gc 30.1
        tst.on_input_value(tst.PIN_I_IC, 40.2)    # gc 40.2

        self.assertEqual(40.2, tst.debug_set_output_value[tst.PIN_O_GC])

    def test_req04_pulse_input(self):
        print("### test_req04_pulse_input")
        tst = Leistungsmesser_11083_11083(0)
        tst.reset()
        tst.on_init()
        tst.init_run = False
        tst.on_input_value(tst.PIN_I_GAIN, 10)
        tst.on_input_value(tst.PIN_I_IC, 1)
        tst.on_input_value(tst.PIN_I_IC, 1)
        tst.on_input_value(tst.PIN_I_IC, 1)
        tst.on_input_value(tst.PIN_I_IC, 1)

        self.assertEqual(40, tst.debug_set_output_value[tst.PIN_O_GC])

    def test_req05_start_timespan(self):
        print("### test_req05_start_timespan")
        tst = Leistungsmesser_11083_11083(0)
        tst.reset()
        tst.on_init()
        tst.init_run = False
        tst.on_input_value(tst.PIN_I_IC, 10)
        tst.gc_sts[0] = 0

        tst.on_input_value(tst.PIN_I_RESET1, 1)
        self.assertEqual(10, tst.gc, 'a')
        self.assertEqual(10, tst.gc_sts[0], 'b')
        self.assertEqual(0, tst.debug_set_output_value[tst.PIN_O_TS1_CONS_CURR], 'c')
        self.assertEqual(10, tst.debug_set_output_value[tst.PIN_O_TS1_CONS_PEV], 'd')

        tst.on_input_value(tst.PIN_I_IC, 20)
        self.assertEqual(20, tst.gc, 'e')
        self.assertEqual(0, tst.gc_sts[1], 'f')
        self.assertEqual(10, tst.debug_set_output_value[tst.PIN_O_TS1_CONS_CURR], 'g')
        self.assertEqual(10, tst.debug_set_output_value[tst.PIN_O_TS1_CONS_PEV], 'h')

        tst.on_input_value(tst.PIN_I_RESET2, 1)
        tst.on_input_value(tst.PIN_I_IC, 30.1)
        tst.on_input_value(tst.PIN_I_RESET3, 1)
        tst.on_input_value(tst.PIN_I_IC, 40.2)

        tst.on_input_value(tst.PIN_I_RESET1, 0)

        self.assertEqual(10, tst.gc_sts[0])
        self.assertEqual(20, tst.gc_sts[1])
        self.assertEqual(30.1, tst.gc_sts[2])
        self.assertEqual(40.2, tst.gc)
        self.assertEqual(30.2, tst.debug_set_output_value[tst.PIN_O_TS1_CONS_CURR], 'i')
        self.assertEqual(10, tst.debug_set_output_value[tst.PIN_O_TS1_CONS_PEV], 'j')
        self.assertEqual(20.2, tst.debug_set_output_value[tst.PIN_O_TS2_CONS_CURR], 'k')
        self.assertEqual(20, tst.debug_set_output_value[tst.PIN_O_TS2_CONS_PEV], 'l')
        self.assertEqual(10.1, tst.debug_set_output_value[tst.PIN_O_TS3_CONS_CURR], 'm')
        self.assertEqual(30.1, tst.debug_set_output_value[tst.PIN_O_TS3_CONS_PEV], 'n')

    def test_req06_gain_input(self):
        print("### test_req06_gain_input")
        tst = Leistungsmesser_11083_11083(0)
        tst.reset()
        tst.on_init()
        tst.init_run = False
        gain = 4
        tst.on_input_value(tst.PIN_I_GAIN, gain)
        self.assertEqual(gain, tst.gain)

    def test_req07_global_reset(self):
        print("### test_req07_global_reset")
        tst = Leistungsmesser_11083_11083(0)
        tst.reset()
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
        print("### test_req09_gain_offset")
        tst = Leistungsmesser_11083_11083(0)
        tst.reset()
        tst.debug_gain = 5
        tst.debug_offset = 2
        tst.on_init()
        tst.init_run = False
        tst.on_input_value(tst.PIN_I_IC, 10)
        self.assertEqual(tst.gc, 48)

    def test_req10_overflow(self):
        print("### test_req10_overflow")
        tst = Leistungsmesser_11083_11083(0)
        tst.reset()
        tst.on_init()
        tst.init_run = False
        self.assertEqual(0, tst.gc, "a")
        self.assertEqual(0, tst.ic_prev, "b")

        tst.on_input_value(tst.PIN_I_IC, 10)
        self.assertEqual(10, tst.gc, "d")
        self.assertEqual(10, tst.ic_curr, "e")

        tst.on_input_value(tst.PIN_I_IC, 5)
        self.assertEqual(15, tst.gc, "g")
        self.assertEqual(5, tst.ic_curr, "h")

    def test_req11_1st_run(self):
        print("### test_req11_1st_run")
        tst = Leistungsmesser_11083_11083(0)
        tst.reset()
        tst.on_init()
        tst.init_run = True
        self.assertEqual(tst.gc, 0, "a")
        self.assertEqual(tst.ic_prev, 0, "b")

        tst.on_input_value(tst.PIN_I_IC, 5000)
        self.assertEqual(0, tst.ic_prev, "c")
        self.assertEqual(5000, tst.ic_curr, "c1")
        self.assertEqual(0, tst.gc, "d")

        tst.on_input_value(tst.PIN_I_IC, 5005)
        self.assertEqual(5, tst.gc, "e")
        self.assertEqual(5000, tst.ic_prev, "f")
        self.assertEqual(5005, tst.ic_curr, "f")

class FunctionalTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_scale(self):
        print("### test_scale")
        tst = Leistungsmesser_11083_11083(0)
        tst.gain = 1000.0
        tst.offset = 10
        res = tst.scale_ic(1)
        self.assertEqual(990, res)

    def test_reboot(self):
        print("### test_reboot")
        tst = Leistungsmesser_11083_11083(0)
        tst.reset()
        tst.gc = 10000.0
        tst.ic_prev = 5000.0
        tst.gc_sts[0] = 2500.0
        tst.debug_set_remanent[tst.REM_TS1_GC_STS] = tst.gc_sts[0]
        tst.debug_set_remanent[tst.REM_GC] = tst.gc
        tst.debug_set_remanent[tst.REM_IC_PREV] = tst.ic_prev
        tst.debug_set_remanent[tst.REM_TS1_CONS_PREV] = 1000.0

        tst.on_init()

        self.assertEqual(5000, tst.ic_prev, "tst.ic_prev")
        self.assertEqual(1000, tst.debug_set_output_value[tst.PIN_O_TS1_CONS_PEV])
        self.assertEqual(7500.0, tst.debug_set_output_value[tst.PIN_O_TS1_CONS_CURR])

    def test_ic_no_change(self):
        tst = Leistungsmesser_11083_11083(0)
        tst.on_init()
        tst.gc = 5000.0
        tst.gc_sts[0] = 2000.0
        tst.ic_curr = 4000.0

        tst.on_input_value(tst.PIN_I_IC, 5000.0)  # --> gc = 6000 because of ic increase by 1000

        self.assertEqual(4000.0, tst.ic_prev, "a")
        self.assertEqual(4000.0, tst.debug_set_output_value[tst.PIN_O_TS1_CONS_CURR], "b")

        tst.on_input_value(tst.PIN_I_IC, 5000.0)

        self.assertEqual(5000, tst.ic_prev, "c")
        self.assertEqual(4000.0, tst.debug_set_output_value[tst.PIN_O_TS1_CONS_CURR], "d")

if __name__ == '__main__':
    unittest.main()
