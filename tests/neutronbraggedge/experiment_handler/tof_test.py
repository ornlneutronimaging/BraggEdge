"""Tests for TOF class."""

import numpy as np
import pytest

from neutronbraggedge.experiment_handler.tof import TOF


class TestTOF:
    """Tests for Time-of-Flight handling."""

    def test_loading_manual_tof_in_s_units(self):
        """TOF(s) array is correctly manually loaded."""
        tof_array = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        tof_handler = TOF(tof_array=tof_array)
        assert all(tof_array == tof_handler.tof_array)

    def test_loading_manual_tof_raise_error_if_no_data_provided(self):
        """ValueError is raised if no tof array provided."""
        with pytest.raises(ValueError):
            TOF()

    def test_loading_file_raise_error_if_file_does_not_exist(self, get_data_file):
        """IOError is raised when file does not exist."""
        filename = get_data_file("fake_tof.txt")
        with pytest.raises(IOError):
            TOF(filename)

    def test_loading_manual_tof_in_micros_units(self):
        """TOF(micros) array is correctly manually loaded and units are converted."""
        tof_array = np.array([1.0e6, 2.0e6, 3.0e6, 4.0e6, 5.0e6, 6.0e6, 7.0e6, 8.0e6, 9.0e6])
        tof_units = "micros"
        tof_handler = TOF(tof_array=tof_array, units=tof_units)
        assert all(tof_array * 1.0e-6 == tof_handler.tof_array)

    def test_loading_manual_tof_in_ms_units(self):
        """TOF(ms) array is correctly manually loaded and units are converted."""
        tof_array = np.array([1.0e3, 2.0e3, 3.0e3, 4.0e3, 5.0e3, 6.0e3, 7.0e3, 8.0e3, 9.0e3])
        tof_units = "ms"
        tof_handler = TOF(tof_array=tof_array, units=tof_units)
        assert all(tof_array * 1.0e-3 == tof_handler.tof_array)

    def test_loading_manual_tof_in_ns_units(self):
        """TOF(ns) array is correctly manually loaded and units are converted."""
        tof_array = np.array([1.0e9, 2.0e9, 3.0e9, 4.0e9, 5.0e9, 6.0e9, 7.0e9, 8.0e9, 9.0e9])
        tof_units = "ns"
        tof_handler = TOF(tof_array=tof_array, units=tof_units)
        assert all(tof_array * 1.0e-9 == tof_handler.tof_array)

    def test_loading_manual_tof_units_not_implemented_yet(self):
        """Error is thrown when the units is not recognized."""
        tof_array = np.array([1.0e9, 2.0e9, 3.0e9, 4.0e9, 5.0e9, 6.0e9, 7.0e9, 8.0e9, 9.0e9])
        tof_units = "crazys"
        with pytest.raises(ValueError):
            TOF(tof_array=tof_array, units=tof_units)

    def test_loading_good_tof_file(self, get_data_file):
        """Correctly formatted tof file is correctly loaded."""
        filename = get_data_file("good_tof.txt")
        tof_handler = TOF(filename=filename)
        tof_expected = np.array([1.0, 2.0, 3.0, 4.0])
        assert all(tof_expected == tof_handler.tof_array[0:4])

    def test_loading_real_tof_file(self, get_data_file):
        """Real tof file is correctly loaded."""
        filename = get_data_file("tof.txt")
        tof_handler = TOF(filename=filename)
        tof_expected = np.array([9.6e-7, 1.12e-5, 2.144e-5, 3.168e-5])
        assert all(tof_expected == tof_handler.tof_array[0:4])

    def test_loading_counts_column(self, get_data_file):
        """Second column (counts) is correctly loaded."""
        filename = get_data_file("tof.txt")
        tof_handler = TOF(filename=filename)
        counts_expected = np.array([2137, 1988, 1979, 2078])
        assert all(counts_expected == tof_handler.counts_array[0:4])

    def test_loading_second_ascii_format(self, get_data_file):
        """Tof2 can be loaded, columns are white spaced."""
        filename = get_data_file("tof2.txt")
        tof_handler = TOF(filename=filename)
        counts_expected = np.array([9120595, 10638008, 12523304, 14676656])
        assert all(counts_expected == tof_handler.counts_array[0:4])

        tof_expected = np.array([1.136e-05, 2.16e-05, 3.184e-05, 4.208e-05])
        assert all(tof_expected == tof_handler.tof_array[0:4])

    def test_loading_third_ascii_format(self, get_data_file):
        """Tof3 can be loaded, columns are white spaced."""
        filename = get_data_file("tof3.txt")
        tof_handler = TOF(filename=filename)
        counts_expected = np.array([9120595, 10638008, 12523304, 14676656])
        assert all(counts_expected == tof_handler.counts_array[0:4])

        tof_expected = np.array([1.136e-05, 2.16e-05, 3.184e-05, 4.208e-05])
        assert all(tof_expected == tof_handler.tof_array[0:4])
