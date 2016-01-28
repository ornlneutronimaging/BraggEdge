How to use This library
=======================

>>> import braggedge

From **python**, first you need to import the package


>>> from braggedge.braggedge import BraggEdge

Metadata of Elements
--------------------

For a particular element you can retrieve:
 - lattice parameter
 - h, k and l values
 - Crystal structure
 - bragg edges values
 
For this example, we are retrieving the data for *Fe* and we are only
interested by the first *4* crystal orientation.

>>> _handler = BraggEdge(material = 'Fe', number_of_bragg_edges = 4)
>>> print("Crystal Structure is: %s" %_handler.metadata['cyrstal_structure]))
'BCC'
>>> print("Lattice is %.2f" %_handler.metadata['lattice'])
2.87
>>> print("hkl are: " , _handler.hkl)
hkl are: [][1,1,0],[2,0,0],[2,1,1],[2,2,0]]
>>> print("bragg edges are: ", _handler.bragg_edges)
bragg edges are: [2.0268, 1.4332, 1.1702, 1.0134]


It is also possible to display all metadata at once

>>> print(_handler)
===================================
Material: Fe
Lattice: 2.8664A
Crystal Structure: BCC
Using local metadata Table: True
===================================
 h | k | l |   d(A)  |    BraggEdge
===================================
 1 | 1 | 0 |  2.0269 |    4.0537
 2 | 0 | 0 |  1.4332 |    2.8664
 2 | 1 | 1 |  1.1702 |    2.3404
 2 | 2 | 0 |  1.0134 |    2.0269
===================================


Lambda Calculation
------------------

>>> import braggedge.experiment_handler

In order to convert a TOF range into lambda, you will need to provide:
 - distance sample-detector (in meters)
 - detector offset (micros)
 - tof array 
 
First, you need to load your TOF range. You can either provide this array
 
>>> _tof_handler = TOF(tof = [9.6000E-07, 1.1200E-05, 2.1440E-05, 3.1680E-05], units = 'micros')
 
or by providing the name of an ascii file name where each tof is on its own row

>>> _tof_handler = TOF(filename = my_tof.txt, units = 'micros')
 
Then it is possible to calculate the Lambda array

>>> distance_sample_detector_m = 1.609
>>> detector_offset_micros = 4500
>>> _exp = Experiment(tof = _tof_handler.tof, distance_sample_detector_m = distance_sample_detector_m, detector_offset_micros = detector_offset_micros)
>>> print(_exp.lambda_array)
[1.10664e-9, 1.109165e-9, 1.111682e-9, 1.114200e-9]

To export lambda into a csv file

>>> _exp.export_lambda(filename = 'my_lambda_file.txt')


Distance Sample-Detector Calculation
------------------------------------

>>> import braggedge.experiment_handler

In order to calculate the *Sample-detector* length, you must provide:
 - detector offset (micros)
 - tof array
 - lambda array (Angstroms)
 
First, you need to load your TOF range. You can either provide this array
 
>>> _tof_handler = TOF(tof = [9.6000E-07, 1.1200E-05, 2.1440E-05, 3.1680E-05], units = 'micros')
 
or by providing the name of an ascii file name where each tof is on its own row

>>> _tof_handler = TOF(filename = my_tof.txt, units = 'micros')
 
Same thing with lambda array

>>> _lambda_handler = LambdaWavelength(data = [1.10664e-9, 1.109165e-9, 1.111682e-9, 1.114200e-9])

or by providing the name of an ascii file where each lambda is on its own row

>>> _lambda_handler = LambdaWavelength(filename = 'my_lambda.txt')

Then

>>> detector_offset_micros = 4500
>>> _exp = Experiment(tof = _tof_handler.tof, lambda_array = _lambda_handler.lambda, detector_offset_micros = detector_offset_micros)
>>> print(_exp.distance_sample_detector_m)
1.609


Detector Offset Calculation
---------------------------

>>> import braggedge.experiment_handler

In order to calculate the *detector offsetr*, you must provide:
 - distance sample-detector (m)
 - tof array
 - lambda array (Angstroms)
 
First, you need to load your TOF range. You can either provide this array
 
>>> _tof_handler = TOF(tof = [9.6000E-07, 1.1200E-05, 2.1440E-05, 3.1680E-05], units = 'micros')
 
or by providing the name of an ascii file name where each tof is on its own row

>>> _tof_handler = TOF(filename = my_tof.txt, units = 'micros')
 
Same thing with lambda array

>>> _lambda_handler = LambdaWavelength(data = [1.10664e-9, 1.109165e-9, 1.111682e-9, 1.114200e-9])

or by providing the name of an ascii file where each lambda is on its own row

>>> _lambda_handler = LambdaWavelength(filename = 'my_lambda.txt')

Then

>>> distance_sample_detector_m = 1.409
>>> _exp = Experiment(tof = _tof_handler.tof, lambda_array = _lambda_handler.lambda, distance_sample_detector_m = distance_sample_detector_m)
>>> print(_exp.detector_offset_micros)
4500
