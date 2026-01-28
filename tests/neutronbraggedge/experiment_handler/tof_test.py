import os
import unittest

import numpy as np

from neutronbraggedge.experiment_handler.tof import TOF


class TofTest(unittest.TestCase):
    def setUp(self):
        _file_path = os.path.dirname(__file__)
        self.data_path = os.path.abspath(os.path.join(_file_path, "../../data"))

    def get_full_path(self, file_name):
        return os.path.join(self.data_path, file_name)

    def test_loading_manual_tof_in_s_units(self):
        """Assert in TOF - TOF(s) array is correctly manually loaded"""
        _tof_array = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        _tof_handler = TOF(tof_array=_tof_array)
        self.assertTrue(all(_tof_array == _tof_handler.tof_array))

    def test_loading_manual_tof_raise_error_if_no_data_provided(self):
        """Assert in TOF - that ValueError is raised if not tof array provided"""
        self.assertRaises(ValueError, TOF)

    def test_loading_file_raise_error_if_file_does_not_exist(self):
        """Assert in TOF - that IOError is raised when file does not exist"""
        _filename = self.get_full_path("fake_tof.txt")
        self.assertRaises(IOError, TOF, _filename)

    def test_loading_manual_tof_in_micros_units(self):
        """Assert in TOF - TOF(micros) array is correctly manually loaded and units are converted"""
        _tof_array = np.array([1.0e6, 2.0e6, 3.0e6, 4.0e6, 5.0e6, 6.0e6, 7.0e6, 8.0e6, 9.0e6])
        _tof_units = "micros"
        _tof_handler = TOF(tof_array=_tof_array, units=_tof_units)
        self.assertTrue(all(_tof_array * 1.0e-6 == _tof_handler.tof_array))

    def test_loading_manual_tof_in_ms_units(self):
        """Assert in TOF - TOF(ms) array is correctly manually loaded and units are converted"""
        _tof_array = np.array([1.0e3, 2.0e3, 3.0e3, 4.0e3, 5.0e3, 6.0e3, 7.0e3, 8.0e3, 9.0e3])
        _tof_units = "ms"
        _tof_handler = TOF(tof_array=_tof_array, units=_tof_units)
        self.assertTrue(all(_tof_array * 1.0e-3 == _tof_handler.tof_array))

    def test_loading_manual_tof_in_ns_units(self):
        """Assert in TOF - TOF(ms) array is correctly manually loaded and units are converted"""
        _tof_array = np.array([1.0e9, 2.0e9, 3.0e9, 4.0e9, 5.0e9, 6.0e9, 7.0e9, 8.0e9, 9.0e9])
        _tof_units = "ns"
        _tof_handler = TOF(tof_array=_tof_array, units=_tof_units)
        self.assertTrue(all(_tof_array * 1.0e-9 == _tof_handler.tof_array))

    def test_loading_manual_tof_units_not_implemented_yet(self):
        """Assert in TOF - that an error is thrown when the units is not recognized"""
        _tof_array = np.array([1.0e9, 2.0e9, 3.0e9, 4.0e9, 5.0e9, 6.0e9, 7.0e9, 8.0e9, 9.0e9])
        _tof_units = "crazys"
        self.assertRaises(ValueError, TOF, tof_array=_tof_array, units=_tof_units)

    def test_loading_good_tof_file(self):
        """Assert in TOF - that correctly formated tof file is correctly loaded"""
        _filename = self.get_full_path("good_tof.txt")
        _tof_handler = TOF(filename=_filename)
        _tof_expected = np.array([1.0, 2.0, 3.0, 4.0])
        self.assertTrue(all(_tof_expected == _tof_handler.tof_array[0:4]))

    def test_loading_real_tof_file(self):
        """Assert in TOF - that real tof file is correctly loaded"""
        _filename = self.get_full_path("tof.txt")
        _tof_handler = TOF(filename=_filename)
        _tof_expected = np.array([9.6e-7, 1.12e-5, 2.144e-5, 3.168e-5])
        self.assertTrue(all(_tof_expected == _tof_handler.tof_array[0:4]))

    def test_loading_counts_column(self):
        """Assert in TOF - second column (counts) is correctly loaded"""
        _filename = self.get_full_path("tof.txt")
        _tof_handler = TOF(filename=_filename)
        _counts_expected = np.array([2137, 1988, 1979, 2078])
        print(_counts_expected)
        print(_tof_handler.counts_array[0:4])
        self.assertTrue(all(_counts_expected == _tof_handler.counts_array[0:4]))

    def test_loading_second_ascii_format(self):
        """assert tof2 can be loaded, columns are white spaced"""
        _filename = self.get_full_path("tof2.txt")
        _tof_handler = TOF(filename=_filename)
        _counts_expected = np.array([9120595, 10638008, 12523304, 14676656])

        print(_counts_expected)
        print(_tof_handler.counts_array[0:4])

        self.assertTrue(all(_counts_expected == _tof_handler.counts_array[0:4]))

        _tof_expected = np.array([1.136e-05, 2.16e-05, 3.184e-05, 4.208e-05])
        self.assertTrue(all(_tof_expected == _tof_handler.tof_array[0:4]))

    def test_loading_third_ascii_format(self):
        """assert tof3 can be loaded, columns are white spaced"""
        _filename = self.get_full_path("tof3.txt")
        _tof_handler = TOF(filename=_filename)
        _counts_expected = np.array([9120595, 10638008, 12523304, 14676656])
        self.assertTrue(all(_counts_expected == _tof_handler.counts_array[0:4]))

        _tof_expected = np.array([1.136e-05, 2.16e-05, 3.184e-05, 4.208e-05])
        self.assertTrue(all(_tof_expected == _tof_handler.tof_array[0:4]))


if __name__ == "__main__":
    unittest.main()
