"""Tests for Utilities class."""

import numpy as np
import pytest

from neutronbraggedge.utilities import Utilities


class TestUtilities:
    """Tests for utility functions."""

    def test_convert_time_units_raise_value_error_when_no_data_provided(self):
        """ValueError raised when no data provided."""
        with pytest.raises(ValueError):
            Utilities.convert_time_units()

    def test_convert_time_units_raise_value_error_when_units_not_supported(self):
        """ValueError raised when units not supported."""
        with pytest.raises(ValueError):
            Utilities.convert_time_units(45, "bad_units", "s")
        with pytest.raises(ValueError):
            Utilities.convert_time_units(45, "s", "bad_units")
        with pytest.raises(ValueError):
            Utilities.convert_time_units(45, "bad_units", "bad_units")

    def test_get_time_conversion_coeff(self):
        """Correct time coefficients are returned."""
        assert Utilities.get_time_conversion_coeff(from_units="s", to_units="s") == 1
        assert Utilities.get_time_conversion_coeff(from_units="s", to_units="ms") == 1.0e3
        assert Utilities.get_time_conversion_coeff(from_units="s", to_units="micros") == 1.0e6
        assert Utilities.get_time_conversion_coeff(from_units="s", to_units="ns") == 1.0e9

        assert Utilities.get_time_conversion_coeff(from_units="ms", to_units="s") == 1.0e-3
        assert Utilities.get_time_conversion_coeff(from_units="ms", to_units="ms") == 1
        assert Utilities.get_time_conversion_coeff(from_units="ms", to_units="micros") == 1e3
        assert Utilities.get_time_conversion_coeff(from_units="ms", to_units="ns") == 1e6

        assert Utilities.get_time_conversion_coeff(from_units="micros", to_units="s") == 1.0e-6
        assert Utilities.get_time_conversion_coeff(from_units="micros", to_units="ms") == 1.0e-3
        assert Utilities.get_time_conversion_coeff(from_units="micros", to_units="micros") == 1
        assert Utilities.get_time_conversion_coeff(from_units="micros", to_units="ns") == 1e3

        assert Utilities.get_time_conversion_coeff(from_units="ns", to_units="s") == 1e-9
        assert Utilities.get_time_conversion_coeff(from_units="ns", to_units="ms") == 1e-6
        assert Utilities.get_time_conversion_coeff(from_units="ns", to_units="micros") == 1e-3
        assert Utilities.get_time_conversion_coeff(from_units="ns", to_units="ns") == 1

    def test_get_time_conversion_raise_error(self):
        """ValueError is raised when wrong units given."""
        with pytest.raises(ValueError):
            Utilities.get_time_conversion_coeff("s", "bad_units")
        with pytest.raises(ValueError):
            Utilities.get_time_conversion_coeff("bad_units", "s")
        with pytest.raises(ValueError):
            Utilities.get_time_conversion_coeff("bad_units", "bad_units")

    def test_convert_time_units_single_value(self):
        """Converting single time units value."""
        assert Utilities.convert_time_units(data=5, from_units="s", to_units="s") == 5
        result = Utilities.convert_time_units(data=4500.0, from_units="micros", to_units="s")
        assert result == pytest.approx(4.5e-3, abs=0.000000001)

    def test_convert_time_units_list_array(self):
        """Converting list time units value."""
        data = [1, 2, 3, 4, 5]
        result = Utilities.convert_time_units(data=data, from_units="s", to_units="s")
        assert all(data == result)

    def test_convert_time_units_numpy_array(self):
        """Converting numpy array time units value."""
        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        result = Utilities.convert_time_units(data=data, from_units="s", to_units="s")
        assert all(data == result)

    def test_array_multiply_coeff_with_no_array(self):
        """Multiply nothing by a coeff value raises ValueError."""
        with pytest.raises(ValueError):
            Utilities.array_multiply_coeff()

    def test_array_multiply_coeff(self):
        """Multiply array by coeff value."""
        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        coeff = 2.5
        new_data = Utilities.array_multiply_coeff(data=data, coeff=coeff)
        expected_data = np.array([2.5, 5.0, 7.5, 10, 12.5])
        assert all(expected_data == new_data)

    def test_array_add_coeff_with_no_array(self):
        """Add nothing to a coeff value raises ValueError."""
        with pytest.raises(ValueError):
            Utilities.array_add_coeff()

    def test_array_add_coeff(self):
        """Adding coeff to array."""
        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        coeff = 5.0
        new_data = Utilities.array_add_coeff(data=data, coeff=coeff)
        expected_data = np.array([6.0, 7.0, 8.0, 9.0, 10.0])
        assert all(expected_data == new_data)

    def test_array_divide_array_not_same_size(self):
        """Numerator array not same size as denominator array raises ValueError."""
        numerator = np.array([1, 2, 3])
        denominator = np.array([1, 2])
        with pytest.raises(ValueError):
            Utilities.array_divide_array(numerator, denominator)

    def test_array_divide_array_works(self):
        """Ratio of arrays works."""
        numerator = np.array([10, 20, 30, 40, 50])
        denominator = np.array([1, 2, 3, 4, 5])
        ratio_expected = np.array([10, 10, 10, 10, 10])
        ratio_returned = Utilities.array_divide_array(numerator=numerator, denominator=denominator)
        assert all(ratio_expected == ratio_returned)

    def test_array_minus_array_raise_error(self):
        """Array1 minus array2 raises error if not same size."""
        array1 = np.array([1, 2, 3])
        array2 = np.array([1, 2])
        with pytest.raises(ValueError):
            Utilities.array_minus_array(array1, array2)

    def test_array_minus_array_works(self):
        """Array1 minus array2 returns correct array."""
        array1 = np.array([2, 4, 6])
        array2 = np.array([2, 3, 4])
        array_returned = Utilities.array_minus_array(array1, array2)
        array_expected = np.array([0, 1, 2])
        assert all(array_expected == array_returned)

    def test_load_csv_raise_value_error(self, get_data_file):
        """ValueError raised when wrong file format."""
        input_file = get_data_file("bad_file.txt")
        with pytest.raises(ValueError):
            Utilities.load_csv(input_file)

    def test_load_ascii_raise_value_error(self, get_data_file):
        """ValueError is raised when file format is wrong."""
        input_file = get_data_file("bad_file.txt")
        with pytest.raises(ValueError):
            Utilities.load_ascii(input_file)

    def test_load_ascii_with_space_separator(self, get_data_file):
        """Space separated file read correctly."""
        input_file = get_data_file("good_tof.txt")
        array = Utilities.load_ascii(filename=input_file, sep=" ")[0]
        expected_start_of_array = np.array([[1.0, 20.0], [2.0, 21.0]])[0]
        returned_array = array[0:2]
        assert all(expected_start_of_array == returned_array)
