from .material_handler.retrieve_material_metadata import RetrieveMaterialMetadata
from .braggedges_handler.braggedge_calculator import BraggEdgeCalculator


class BraggEdge(object):
    """This is from where the user will retrieve all metadtaa and calculation
        
    Variables:
        
      * metadata: dictionary of 'lattice' and 'crystal_structure' of material given
      * hkl: array of first 'number_of_bragg_edges' hkl available values 
      * bragg_edges: array of first 'number_of_bragg_edges' bragg edges values
    
      >>> from braggedge.braggedge import BraggEdge
      >>> _handler = BraggEdge(material = 'Fe', number_of_bragg_edges = 4)
      >>> print("Crystal Structure is: %s" %_handler.metadata['cyrstal_structure]))
      'BCC'
      >>> print("Lattice is %.2f" %_handler.metadata['lattice'])
      2.87
      >>> print("hkl are: " , _handler.hkl)
      hkl are: [][1,1,0],[2,0,0],[2,1,1],[2,2,0]]
      >>> print("bragg edges are: ", _handler.bragg_edges)
      bragg edges are: [2.0268, 1.4332, 1.1702, 1.0134]
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
    
    """
    
    hkl = None
    metadata = None
    bragg_edges = None
    d_spacing = None

    def __init__(self, material=None, 
                 number_of_bragg_edges=10, 
                 use_local_metadata_table=True):


        self.material = material
        self.number_of_bragg_edges = number_of_bragg_edges
        self.use_local_metadata_table = use_local_metadata_table
        
        self._retrieve_metadata()
        self._calculate_hkl()
        self._calculate_braggedges()
        
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
        """This method calculate the braggedges values (and the d_spacing in the same time)"""
        _calculator = self._calculator
        _calculator.calculate_bragg_edges()
        self.d_spacing = _calculator.d_spacing
        self.bragg_edges = _calculator.bragg_edges
        
    def __repr__(self):
        """This will display the metadata/hkl/d_spacing/bragg edge values"""
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
        _bragg_eges = self.bragg_edges
        _d_spacing = self.d_spacing
        
        for index in range(len(_d_spacing)):
            print(" %d | %d | %d |\t %.4f |\t %.4f" %(_hkl[index][0],
                                                      _hkl[index][1],
                                                      _hkl[index][2], 
                                                      _d_spacing[index],
                                                      _bragg_eges[index]))
        
        print('=' * nbr_ticks)
        return ""
        