"""Tests for LambdaWavelength class."""

import numpy as np
import pytest

from neutronbraggedge.experiment_handler.lambda_wavelength import LambdaWavelength


class TestLambdaWavelength:
    """Tests for lambda wavelength handling."""

    def test_loading_manual_lambda_array(self):
        """Manual loading of array."""
        lambda_array = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        lambda_handler = LambdaWavelength(data=lambda_array)
        assert all(lambda_array == lambda_handler.lambda_array)

    def test_loading_normal_array_data(self):
        """Loading of np.array array."""
        lambda_array = np.array([1, 2.0, 3.0, 4.0])
        lambda_handler = LambdaWavelength(data=lambda_array)
        assert all(lambda_array == lambda_handler.lambda_array)

    def test_not_lambda_array_provided(self):
        """No lambda array provided raises ValueError."""
        with pytest.raises(ValueError):
            LambdaWavelength()

    def test_loading_auto_lambda_array(self, get_data_file):
        """Auto loading of array from file."""
        lambda_filename = get_data_file("lambda.txt")
        lambda_handler = LambdaWavelength(filename=lambda_filename)
        lambda_expected = np.array(
            [
                1.10664703784e-09,
                1.10916473754e-09,
                1.11168243725e-09,
                1.11420013696e-09,
                1.11671783666e-09,
            ]
        )
        assert all(lambda_expected == lambda_handler.lambda_array[0:5])

    def test_load_bad_file_name(self, get_data_file):
        """File name is provided but does not exist raises IOError."""
        lambda_filename = get_data_file("i_do_not_exist.txt")
        with pytest.raises(IOError):
            LambdaWavelength(lambda_filename)
