# coding: UTF-8

import unittest


class hsl20_3:
    LOGGING_NONE = 0

    def __init__(self):
        pass

    class BaseModule:

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
            pass

        def _set_output_value(self, pin, value):
            print("### Out \tPin " + str(pin) + ", Value: " + str(value))
            return ("### Out \tPin " + str(pin) + ", Value: " + str(value))

        def _get_input_value(self, pin):
            if pin == 5:
                return 1
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

        def get_homeserver_private_ip(self):
            return "192.168.143.30"

    class DebugHelper():
        def __init__(self):
            pass

        def set_value(self, p_sCap, p_sText):
            print ("DEBUG value\t" + str(p_sCap) + ": " + str(p_sText))

        def add_message(self, p_sMsg):
            print ("Debug Msg\t" + str(p_sMsg))

################################################
################################################

class Leistungsmesser_11083_11083(hsl20_3.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_3.BaseModule.__init__(self, homeserver_context, "hsl20_3_Powermeter")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_3.LOGGING_NONE, ())
        self.PIN_I_IC=1
        self.PIN_I_RESET1=2
        self.PIN_I_RESET2=3
        self.PIN_I_RESET3=4
        self.PIN_I_GAIN=5
        self.PIN_I_RESET=6
        self.PIN_I_OFFSET=7
        self.PIN_O_GC=1
        self.PIN_O_TS1_CONS_CURR=2
        self.PIN_O_TS1_CONS_PEV=3
        self.PIN_O_TS2_CONS_CURR=4
        self.PIN_O_TS2_CONS_PEV=5
        self.PIN_O_TS3_CONS_CURR=6
        self.PIN_O_TS3_CONS_PEV=7
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

    gc_sts = [0] * 3     # global counter at start of time span
    cons_prev = [0] * 3  # consumption of previous time span
    gc = 0          # global counter
    ic_prev = 0     # Last input counter value received, respecting gain and offset

    def process_counter(self):
        for i in range(3):
            ts_cons_curr = self.gc - self.gc_sts[i]
            self._set_output_value(self.PIN_O_TS1_CONS_CURR + i, ts_cons_curr)

    def process_int_reset(self, i):
        self.cons_prev[i] = self.gc - self.gc_sts[i]
        self.gc_sts[i] = self.gc
        self._set_output_value(self.PIN_O_TS1_CONS_PEV + i, self.cons_prev[i])
        self._set_output_value(self.PIN_O_TS1_CONS_CURR + i, 0)

        self._set_remanent(self.REM_TS1_GC_STS + i, self.gc_sts[i])
        self._set_remanent(self.REM_TS1_CONS_PREV + i, self.cons_prev[i])

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

        except:
            self.gc = 0
            self.gc_sts[0] = 0
            self.gc_sts[1] = 0
            self.gc_sts[2] = 0

            self.ic_prev = 0

            self.cons_prev[0] = 0
            self.cons_prev[1] = 0
            self.cons_prev[2] = 0

        self.process_counter()
        self.process_int_reset(0)
        self.process_int_reset(1)
        self.process_int_reset(2)

    def on_input_value(self, index, value):

        self.DEBUG.set_value("index", index)

        if index == self.PIN_I_IC:
            self.DEBUG.add_message("found self.PIN_I_IC")
            gain = self._get_input_value(self.PIN_I_GAIN)
            offset = self._get_input_value(self.PIN_I_OFFSET)

            ic_curr = (value * gain) - offset

            self.DEBUG.set_value("gain", gain)
            self.DEBUG.set_value("offset", offset)
            self.DEBUG.set_value("ic_curr", ic_curr)

            # increase global counter
            if self.ic_prev > ic_curr:
                self.gc += ic_curr
            else:
                self.gc += ic_curr - self.ic_prev

            # process counter for intervals & store data
            self.process_counter()

            # store global counter
            self.ic_prev = ic_curr
            self._set_remanent(self.REM_GC, self.gc)
            self._set_remanent(self.REM_IC_PREV, self.ic_prev)

        elif index == self.PIN_I_RESET1:
            self.process_int_reset(0)

        elif index == self.PIN_I_RESET2:
            self.process_int_reset(1)

        elif index == self.PIN_I_RESET3:
            self.process_int_reset(2)

        elif index == self.PIN_I_RESET:
            self.gc = 0
            self._set_remanent(self.REM_GC, 0)

            self.gc_sts[1] = 0
            self._set_remanent(self.REM_TS1_GC_STS, 0)
            self.gc_sts[2] = 0
            self._set_remanent(self.REM_TS2_GC_STS, 0)
            self.gc_sts[3] = 0
            self._set_remanent(self.REM_TS3_GC_STS, 0)

            self.ic_prev = 0
            self._set_remanent(self.REM_IC_PREV, self.ic_prev)

            self._set_remanent(self.REM_TS1_CONS_PREV, 0)
            self._set_remanent(self.REM_TS2_CONS_PREV, 0)
            self._set_remanent(self.REM_TS3_CONS_PREV, 0)

################################################
################################################


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_process_counter(self):
        tst = Leistungsmesser_11083_11083(0)
        tst.on_init()
        self.assertEqual(tst.gc, 0)
        self.assertEqual(tst.ic_prev, 0)

        tst.on_input_value(tst.PIN_I_IC, 10)
        self.assertEqual(tst.gc, 10)
        self.assertEqual(tst.ic_prev, 10)

        tst.on_input_value(tst.PIN_I_IC, 5)
        self.assertEqual(tst.gc, 15)
        self.assertEqual(tst.ic_prev, 5)

    def test_process_int_reset(self):
        tst = Leistungsmesser_11083_11083(0)
        tst.on_init()
        tst.gc = 100
        tst.gc_sts[0] = 10
        tst.gc_sts[1] = 20
        tst.gc_sts[2] = 30
        self.assertEqual(tst.gc_sts[2], 30)
        tst.process_int_reset(0)
        self.assertEqual(tst.gc_sts[0], 100)
        self.assertEqual(tst.gc_sts[1], 20)
        self.assertEqual(tst.gc_sts[2], 30)


if __name__ == '__main__':
    unittest.main()
