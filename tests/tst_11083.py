# coding: UTF-8

import unittest

################################
# get the code
with open('framework_helper.py', 'r') as f1, open('../src/11083_Leistungsmesser (11083).py', 'r') as f2:
    framework_code = f1.read()
    debug_code = f2.read()

exec (framework_code + debug_code)

################################################################################


class FunctionalTests(unittest.TestCase):

    def setUp(self):
        print("Entering setUp()")
        self.tst = Leistungsmesser_11083_11083(0)
        self.tst.debug_input_value[self.tst.PIN_I_GAIN] = 1
        print("Leaving setUp()")

    def test_scale(self):
        print("Entering test_scale()")
        self.tst.gain = 1000.0
        self.tst.offset = 10
        res = self.tst.scale_value(1)
        self.assertEqual(990, res)
        print("Leaving test_scale()")

    def test_data_set(self):
        print("Entering test_data_set()")
        data_set = DataSet()  # type DataSet
        print("- Testing increasing counter")
        period_delta = data_set.set_counter_value(10)
        self.assertEqual(10, period_delta)
        period_delta = data_set.set_counter_value(20)
        self.assertEqual(20, period_delta)
        print("- Testing counter overrun")
        period_delta = data_set.set_counter_value(10)
        self.assertEqual(30, period_delta)
        period_delta = data_set.set_counter_value(20)
        self.assertEqual(40, period_delta)
        print("- Testing period reset")
        last_period = data_set.period_reset()
        self.assertEqual(40, last_period)
        period_delta = data_set.set_counter_value(30)
        self.assertEqual(10, period_delta)
        print("- Testing reset")
        data_set.reset()
        period_delta = data_set.get_period_delta()
        self.assertEqual(0, period_delta)
        print("- Re-Testing increasing counter")
        period_delta = data_set.set_counter_value(10)
        self.assertEqual(10, period_delta)
        period_delta = data_set.set_counter_value(20)
        self.assertEqual(20, period_delta)
        print("- Testing restore_values")
        data_set.restore_values(counter_global_value=100, period_delta=50, last_period_delta=20)
        period_delta = data_set.set_counter_value(110)
        self.assertEqual(60, period_delta)
        last_period_delta = data_set.get_last_period_delta()
        self.assertEqual(20, last_period_delta)
        print("- Re-testing period reset")
        last_period = data_set.period_reset()
        self.assertEqual(60, last_period)
        period_delta = data_set.set_counter_value(120)
        self.assertEqual(10, period_delta)
        print("Leaving test_data_set()")

    def test_round_values(self):
        print("Entering test_round_values()")
        self.tst.set_output_value_sbc(0, 1.111111111111)
        self.assertEqual(1.1111, self.tst.debug_output_value[0])
        self.tst.set_output_value_sbc(0, 99999.99989)
        self.assertEqual(99999.9999, self.tst.debug_output_value[0])
        print("Leaving test_round_values()")

    def test_on_init(self):
        print("Entering test_on_init()")
        self.tst.on_init()
        self.assertEqual(3, len(self.tst.data_sets))
        print("Leaving test_on_init()")

    def test_full(self):
        print("Entering test_full()")
        self.tst.on_init()
        print("- Testing 0 counter")
        self.tst.on_input_value(self.tst.PIN_I_IC, 0)
        self.assertEqual(0, self.tst.debug_output_value[4])
        print("- Testing normal counter")
        self.tst.on_input_value(self.tst.PIN_I_IC, 10)
        self.assertEqual(10, self.tst.debug_output_value[self.tst.PIN_O_GC])
        self.assertEqual(10, self.tst.debug_set_remanent[self.tst.REM_GC])
        self.tst.on_input_value(self.tst.PIN_I_IC, 20)
        self.assertEqual(20, self.tst.debug_output_value[self.tst.PIN_O_GC])
        self.assertEqual(20, self.tst.debug_set_remanent[self.tst.REM_GC])
        print("- Testing non-change counter")
        self.tst.on_input_value(self.tst.PIN_I_IC, 20)
        self.assertEqual(20, self.tst.debug_output_value[self.tst.PIN_O_GC])
        self.assertEqual(20, self.tst.debug_set_remanent[self.tst.REM_GC])
        print("Leaving test_full()")

    # todo HS reboot
    def test_hs_reboot(self):
        print("Entering test_hs_reboot()")
        self.tst.on_init()
        self.tst.on_input_value(self.tst.PIN_I_IC, 0)
        self.tst.on_input_value(self.tst.PIN_I_IC, 10)
        self.tst.on_input_value(self.tst.PIN_I_IC, 20)
        self.tst.on_input_value(self.tst.PIN_I_RESET1, True)
        self.tst.on_input_value(self.tst.PIN_I_IC, 30)
        self.assertEqual(30, self.tst.debug_output_value[self.tst.PIN_O_GC])
        self.assertEqual(20, self.tst.debug_output_value[self.tst.PIN_O_TS1_CONS_PEV])
        self.assertEqual(10, self.tst.debug_output_value[self.tst.PIN_O_TS1_CONS_CURR])
        print("- Testing Reboot")
        self.tst.on_init()
        self.assertEqual(30, self.tst.debug_output_value[self.tst.PIN_O_GC])
        self.assertEqual(20, self.tst.debug_output_value[self.tst.PIN_O_TS1_CONS_PEV])
        self.assertEqual(10, self.tst.debug_output_value[self.tst.PIN_O_TS1_CONS_CURR])
        self.tst.on_input_value(self.tst.PIN_I_IC, 40)
        self.assertEqual(40, self.tst.debug_output_value[self.tst.PIN_O_GC])
        self.assertEqual(20, self.tst.debug_output_value[self.tst.PIN_O_TS1_CONS_PEV])
        self.assertEqual(20, self.tst.debug_output_value[self.tst.PIN_O_TS1_CONS_CURR])

        print("Leaving test_hs_reboot()")

    def test_overflow(self):
        print("Entering test_overflow()")
        self.tst.on_init()
        print("- Testing increasing counter")
        self.tst.on_input_value(self.tst.PIN_I_IC, 0)
        self.tst.on_input_value(self.tst.PIN_I_IC, 20)
        print("- Testing counter overrun")
        self.tst.on_input_value(self.tst.PIN_I_IC, 10)
        self.assertEqual(30, self.tst.debug_output_value[self.tst.PIN_O_TS1_CONS_CURR])
        self.tst.on_input_value(self.tst.PIN_I_IC, 20)
        self.assertEqual(40, self.tst.debug_output_value[self.tst.PIN_O_TS1_CONS_CURR])
        print("Leaving test_overflow()")
    # todo overflow


if __name__ == '__main__':
    unittest.main()
