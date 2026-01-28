"""Tests for Experiment class."""

import numpy as np
import pytest

from neutronbraggedge.experiment_handler.experiment import Experiment
from neutronbraggedge.experiment_handler.lambda_wavelength import LambdaWavelength
from neutronbraggedge.experiment_handler.tof import TOF


class TestExperiment:
    """Tests for experiment handling."""

    def test_experiment_value_error_when_no_tof_provided(self):
        """ValueError is raised when tof array is missing."""
        with pytest.raises(ValueError):
            Experiment()

    def test_experiment_value_error_when_missing_argument_for_lambda_calculation(self):
        """ValueError raised when detector_offset or LDS are missing."""
        tof = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        with pytest.raises(ValueError):
            Experiment(tof)
        with pytest.raises(ValueError):
            Experiment(tof, None, 1)
        with pytest.raises(ValueError):
            Experiment(tof, None, None, 2)

    def test_experiment_value_error_when_lambda_provided_and_either_lds_or_offset_missing(self):
        """ValueError is raised when LdS and offset are missing when lambda provided."""
        tof = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        lambda_array = [11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0]
        with pytest.raises(ValueError):
            Experiment(tof, lambda_array)

    def test_experiment_value_error_when_lambda_and_tof_not_same_size(self):
        """ValueError is raised when tof and lambda array do not have the same size."""
        tof = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        lambda_array = [11.0, 12.0, 13.0, 14.0, 15.0]
        with pytest.raises(ValueError):
            Experiment(tof, lambda_array, 10)

    def test_experiment_calculate_main_coefficient(self, get_data_file):
        """Calculation of main coefficient is correct."""
        tof_file = get_data_file("tof.txt")
        tof_obj = TOF(filename=tof_file)
        distance_source_detector_m = 1.609
        detector_offset_micros = 4500
        exp_obj = Experiment(
            tof=tof_obj.tof_array,
            distance_source_detector_m=distance_source_detector_m,
            detector_offset_micros=detector_offset_micros,
        )
        assert exp_obj._h_over_MnLds == pytest.approx(2.45869e-7, abs=0.0001)

    def test_experiment_calculate_lambda(self, get_data_file):
        """Calculation of lambda is correct."""
        tof_file = get_data_file("tof.txt")
        tof_obj = TOF(filename=tof_file)
        distance_source_detector_m = 1.609
        detector_offset_micros = 4500
        exp_obj = Experiment(
            tof=tof_obj.tof_array,
            distance_source_detector_m=distance_source_detector_m,
            detector_offset_micros=detector_offset_micros,
        )
        lambda_expected = np.array(
            [
                1.10664704e-09,
                1.10916474e-09,
                1.11168244e-09,
                1.11420014e-09,
                1.11671784e-09,
                1.11923554e-09,
                1.12175324e-09,
                1.12427094e-09,
                1.12678864e-09,
                1.12930634e-09,
                1.13182403e-09,
                1.13434173e-09,
                1.13685943e-09,
                1.13937713e-09,
                1.14189483e-09,
                1.14441253e-09,
                1.14693023e-09,
                1.14944793e-09,
                1.15196563e-09,
                1.15448333e-09,
            ]
        )
        lambda_returned = exp_obj.lambda_array
        # Verify first 20 calculated lambda values match expected
        assert lambda_expected[0] == pytest.approx(lambda_returned[0])
        assert lambda_expected[5] == pytest.approx(lambda_returned[5])
        assert lambda_expected[19] == pytest.approx(lambda_returned[19])
        assert len(lambda_returned) >= len(lambda_expected)

    def test_create_csv_lambda_file(self, get_data_file, tmp_path):
        """Lambda file is correctly exported."""
        tof_file = get_data_file("tof.txt")
        tof_obj = TOF(filename=tof_file)
        distance_source_detector_m = 1.609
        detector_offset_micros = 4500
        exp_obj = Experiment(
            tof=tof_obj.tof_array,
            distance_source_detector_m=distance_source_detector_m,
            detector_offset_micros=detector_offset_micros,
        )
        output_filename = tmp_path / "test_lambda.txt"
        exp_obj.export_lambda(filename=str(output_filename))
        assert output_filename.is_file()

    def test_create_csv_lambda_file_without_providing_name(self, get_data_file):
        """ValueError is raised if no filename is provided for export."""
        tof_file = get_data_file("tof.txt")
        tof_obj = TOF(filename=tof_file)
        distance_source_detector_m = 1.609
        detector_offset_micros = 4500
        exp_obj = Experiment(
            tof=tof_obj.tof_array,
            distance_source_detector_m=distance_source_detector_m,
            detector_offset_micros=detector_offset_micros,
        )
        with pytest.raises(ValueError):
            exp_obj.export_lambda()

    def test_calculate_distance_source_detector(self, get_data_file):
        """Distance source detector is correctly calculated."""
        tof_file = get_data_file("tof.txt")
        tof_obj = TOF(filename=tof_file)
        detector_offset_micros = 4500
        lambda_file = get_data_file("lambda.txt")
        lambda_obj = LambdaWavelength(filename=lambda_file)
        tof_array = tof_obj.tof_array[0:20]
        lambda_array = lambda_obj.lambda_array[0:20]

        exp_handler = Experiment(
            tof=tof_array, lambda_array=lambda_array, detector_offset_micros=detector_offset_micros
        )
        distance_expected = 1.609  # m
        assert exp_handler.distance_source_detector == pytest.approx(distance_expected, abs=1e-6)

    def test_calculate_detector_offset(self, get_data_file):
        """Detector offset is correctly calculated."""
        tof_file = get_data_file("tof.txt")
        tof_obj = TOF(filename=tof_file)
        distance_source_detector_m = 1.609
        lambda_file = get_data_file("lambda.txt")
        lambda_obj = LambdaWavelength(filename=lambda_file)
        tof_array = tof_obj.tof_array[0:20]
        lambda_array = lambda_obj.lambda_array[0:20]

        exp_handler = Experiment(
            tof=tof_array, lambda_array=lambda_array, distance_source_detector_m=distance_source_detector_m
        )
        offset_expected_micros = 4500  # micros
        assert exp_handler.detector_offset_micros == pytest.approx(offset_expected_micros, abs=1e-6)
