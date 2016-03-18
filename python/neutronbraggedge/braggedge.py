from .material_handler.retrieve_material_metadata import RetrieveMaterialMetadata
from .braggedges_handler.braggedge_calculator import BraggEdgeCalculator
from .utilities import Utilities


class BraggEdge(object):
    """This is from where the user will retrieve all metadata and calculation
        
    Variables:
        
      From **python**, first you need to import the package

    >>> from braggedge.braggedge import BraggEdge
    
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
    
    Then you can export the resulting metadata into a CSV file
    
    >>> _handler.export(filename = 'my_file_name.txt')
    
    """
    
    hkl = None
    metadata = None
    bragg_edges = None
    d_spacing = None

    def __init__(self, material=None, 
                 number_of_bragg_edges=10, 
                 use_local_metadata_table=True):
        """
        Constructor
        
        Arguments:
           material: name of the material such as 'Ni', 'Fe' ...
           number_of_bragg_edge:  Default 10. Number of row to display and calculate data for.
           use_local_metadata_table: default True. Use local defined table to retrieve lattice parameters,
                                     crystal structure. If False, will go to wiki web page.
        
        """

        self.material = material
        self.number_of_bragg_edges = number_of_bragg_edges
        self.use_local_metadata_table = use_local_metadata_table
        
        self._retrieve_metadata()
        self._calculate_hkl()
        self._calculate_braggedges()
        
    def get_experimental_lattice_parameter(self, experimental_bragg_edge_values = None,
                                    experimental_bragg_edge_error = None):
        """calculates the experimental lattice parameter values given an array of 
        bragg edge values"""
        
        if experimental_bragg_edge_error is None:
            raise ValueError("Please provide an array of bragg edge values")
        
        if experimental_bragg_edge_error is not None:
            if len(experimental_bragg_edge_error) != len(experimental_bragg_edge_values):
                raise ValueError("Make sure exp. bragg edge value and error have the same size!")
        
        _calculator = self._calculator
        _calculator.calculate_lattice_array(experimental_bragg_edge_values,
                                            experimental_bragg_edge_error)
        exp_lattice_parameter = _calculator.lattice_experimentatl
        return exp_lattice_parameter
        
    def _retrieve_metadata(self):
        """This method retrieves the lattice and crystal structure of the material"""
        _handler = RetrieveMaterialMetadata(material = self.material,
                                            use_local_table = self.use_local_metadata_table)
        self.lattice = _handler.lattice
        self.crystal_structure = _handler.crystal_structure
    
        self.metadata = {'lattice': self.lattice, 
                'crystal_structure': self.crystal_structure}

    def _calculate_hkl(self):
        """This method calculate the set of hkl up to the number_of_bragg_edges specified"""
        _calculator = BraggEdgeCalculator(structure_name = self.metadata['crystal_structure'],
                                          lattice = self.metadata['lattice'],
                                          number_of_set = self.number_of_bragg_edges)
        _calculator.calculate_hkl()
        self._calculator = _calculator
        self.hkl = _calculator.hkl

    def _calculate_braggedges(self):
        """This method calculates the braggedges values (and the d_spacing in the same time)"""
        _calculator = self._calculator
        _calculator.calculate_bragg_edges()
        self.d_spacing = _calculator.d_spacing
        self.bragg_edges = _calculator.bragg_edges
        
    def __repr__(self):
        """Display the metadata/hkl/d_spacing/bragg edge values"""
        nbr_ticks = 45
        print('=' * nbr_ticks)
        print("Material: %s" %self.material)
        print(u"Lattice : %.4f\u212B" %self.metadata['lattice'])
        print("Crystal Structure: %s" %self.metadata['crystal_structure'])
        print("Using local metadata Table: %s" %self.use_local_metadata_table)
        print('=' * nbr_ticks)
        print(u" h | k | l |\t d (\u212B)  |\t BraggEdge")
        print('-' * nbr_ticks)

        _hkl = self.hkl
        _bragg_edges = self.bragg_edges
        _d_spacing = self.d_spacing
        
        for index in range(len(_d_spacing)):
            print(" %d | %d | %d |\t %.5f |\t %.5f" %(_hkl[index][0],
                                                      _hkl[index][1],
                                                      _hkl[index][2], 
                                                      _d_spacing[index],
                                                      _bragg_edges[index]))
        
        print('=' * nbr_ticks)
        return ""
        
    def export(self, filename=None, file_type='csv'):
        """Export the metadata into various file format
        
        Arguments:
        
           filename: output file name to create
           file_type: format of the file to create
              only 'csv' (simple comma separated format) is supported for now
            
        Exception:
           IOError: if no file name is provided
        
        """
        if filename is None:
            raise IOError
        
        _metadata = self._format_metadata()
        _data = self._format_data()
        
        if file_type is 'csv':
            Utilities.save_csv(filename = filename,
                               data = _data,
                               metadata = _metadata)
            return
        
        raise NotImplementedError
        
        
    def _format_metadata(self):
        """Format the various metadata to put at the top of output file created"""
        _metadata = []
        _metadata.append("Material: %s" %self.material)
        _metadata.append("Lattice : %.4fAngstroms" %self.metadata['lattice'])
        _metadata.append("Crystal Structure: %s" %self.metadata['crystal_structure'])
        _metadata.append("Using local metadata Table: %s" %self.use_local_metadata_table)
        _metadata.append("")
        _metadata.append("h, k, l, d(Angstroms), BraggEdge")
        return _metadata
    
    def _format_data(self):
        """Format the data for the output file created"""
        _data = []
        _hkl = self.hkl
        _bragg_edges = self.bragg_edges
        _d_spacing = self.d_spacing
        for index in range(len(_d_spacing)):
            _data.append([_hkl[index][0],
                         _hkl[index][1],
                         _hkl[index][2],
                         _d_spacing[index],
                         _bragg_edges[index]])
        return _data

