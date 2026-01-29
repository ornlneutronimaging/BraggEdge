import os
from typing import Any, Literal, TypedDict

from loguru import logger

from .braggedges_handler.braggedge_calculator import BraggEdgeCalculator
from .material_handler.retrieve_material_metadata import RetrieveMaterialMetadata
from .utilities import Utilities

CrystalStructure = Literal["BCC", "FCC"]


class NewMaterialDict(TypedDict):
    """Type definition for new material dictionary."""

    name: str
    lattice: float
    crystal_structure: CrystalStructure


class BraggEdge:
    """This is from where the user will retrieve all metadata and calculation

    Variables:

      From **python**, first you need to import the package

    >>> from neutronbraggedge.braggedge import BraggEdge

    For a particular element you can retrieve:
     - lattice parameter
     - h, k and l values
     - Crystal structure
     - bragg edges values

    For this example, we are retrieving the data for *Fe* and we are only
    interested by the first *4* crystal orientation.

    >>> _handler = BraggEdge(material = 'Fe', number_of_bragg_edges = 4)
    >>> print("Crystal Structure is: %s" %_handler.metadata['cyrstal_structure']))
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

    hkl: dict[str, list[list[int]]] | None = None
    metadata: dict[str, Any] | None = None
    bragg_edges: dict[str, list[float]] | None = None
    d_spacing: dict[str, list[float]] | None = None
    material: list[str]
    number_of_bragg_edges: int
    use_local_metadata_table: bool
    lattice: dict[str, float]
    crystal_structure: dict[str, CrystalStructure]
    _calculator: dict[str, BraggEdgeCalculator]

    def __init__(
        self,
        material: str | list[str] | None = None,
        new_material: list[NewMaterialDict] | None = None,
        number_of_bragg_edges: int = 10,
        use_local_metadata_table: bool = True,
    ) -> None:
        """
        Constructor

        Arguments:
           - material: name of the material such as 'Ni', 'Fe' ...
           - new_material: dictionary of new materials defined as
              [{'name': 'Ta',
               'lattice': 0.333,
               'crystal_structure': 'FCC'},
               {'name': 'Ur',
               'lattice': 0.5555,
               'crystal_structure': 'BCC'}]
           - number_of_bragg_edge:  Default 10. Number of row to display and calculate data for.
           - use_local_metadata_table: default True. Use local defined table to retrieve lattice parameters,
                                     crystal structure. If False, will go to wiki web page.

        """

        if material is None:
            if new_material is None:
                raise ValueError("No material or new_material defined!")
            else:
                # parse dictionary
                list_material: list[str] = []
                try:
                    for _element in new_material:
                        _name = _element["name"]
                        list_material.append(_name)
                        _lattice_constant = _element["lattice"]
                        _crystal_structure = _element["crystal_structure"]
                except:
                    raise ValueError("Check the format of the new element array!")

                material = list_material

        if type(material) is not list:
            material = [material]

        self.material = material
        self.number_of_bragg_edges = number_of_bragg_edges
        self.use_local_metadata_table = use_local_metadata_table

        self._retrieve_metadata(new_material=new_material)
        self._calculate_hkl()
        self._calculate_braggedges()

    def get_experimental_lattice_parameter(
        self,
        experimental_bragg_edge_values: list[float] | None = None,
        experimental_bragg_edge_error: list[float] | None = None,
    ) -> None:
        """Calculates the experimental lattice parameter values given an array of
        bragg edge values.

        Note: This method is not yet implemented. Use the Lattice class directly
        for experimental lattice parameter calculations.

        Args:
            experimental_bragg_edge_values: Array of experimental bragg edge values.
            experimental_bragg_edge_error: Optional array of errors corresponding to
                ``experimental_bragg_edge_values``.

        Raises:
            ValueError: If ``experimental_bragg_edge_values`` is not provided, or if
                ``experimental_bragg_edge_error`` is provided and its length does not
                match ``experimental_bragg_edge_values``.
            NotImplementedError: This method is not yet implemented. Use the Lattice
                class directly for experimental lattice parameter calculations.
        """
        if experimental_bragg_edge_values is None:
            raise ValueError("Please provide an array of bragg edge values")

        if experimental_bragg_edge_error is not None:
            if len(experimental_bragg_edge_error) != len(experimental_bragg_edge_values):
                raise ValueError("Make sure exp. bragg edge value and error have the same size!")

        raise NotImplementedError(
            "get_experimental_lattice_parameter is not yet implemented. "
            "Use the Lattice class directly for experimental lattice calculations."
        )

    def _retrieve_metadata(self, new_material: list[NewMaterialDict] | None = None) -> None:
        """This method retrieves the lattice and crystal structure of the material"""
        _lattice: dict[str, float] = {}
        _crystal_structure: dict[str, CrystalStructure] = {}

        if new_material is None:  # retrieve infos from ascii table
            for _material in self.material:
                _handler = RetrieveMaterialMetadata(material=_material, use_local_table=self.use_local_metadata_table)
                _lattice[_material] = _handler.lattice
                _crystal_structure[_material] = _handler.crystal_structure

        else:  # local infos
            for _element in new_material:
                _material = _element["name"]
                _local_lattice = _element["lattice"]
                _local_crystal_structure = _element["crystal_structure"]

                _lattice[_material] = _local_lattice
                _crystal_structure[_material] = _local_crystal_structure

        self.lattice = _lattice
        self.crystal_structure = _crystal_structure

        self.metadata = {"lattice": self.lattice, "crystal_structure": self.crystal_structure}

    def _calculate_hkl(self) -> None:
        """This method calculate the set of hkl up to the number_of_bragg_edges specified"""
        calculator: dict[str, BraggEdgeCalculator] = {}
        _hkl: dict[str, list[list[int]]] = {}

        for _material in self.material:
            _structure_name = self.metadata["crystal_structure"][_material]
            _lattice = self.metadata["lattice"][_material]

            _calculator = BraggEdgeCalculator(
                structure_name=_structure_name, lattice=_lattice, number_of_set=self.number_of_bragg_edges
            )

            _calculator.calculate_hkl()
            calculator[_material] = _calculator
            _hkl[_material] = _calculator.hkl

        self._calculator = calculator
        self.hkl = _hkl

    def _calculate_braggedges(self) -> None:
        """This method calculates the braggedges values (and the d_spacing in the same time)"""
        _d_spacing: dict[str, list[float]] = {}
        _bragg_edges: dict[str, list[float]] = {}

        for _material in self.material:
            _calculator = self._calculator[_material]

            _calculator.calculate_bragg_edges()
            _d_spacing[_material] = _calculator.d_spacing
            _bragg_edges[_material] = _calculator.bragg_edges

        self.d_spacing = _d_spacing
        self.bragg_edges = _bragg_edges

    def __repr__(self) -> str:
        """Display the metadata/hkl/d_spacing/bragg edge values"""
        nbr_ticks = 45

        for _material in self.material:
            logger.info("=" * nbr_ticks)
            logger.info("Material: %s" % _material)
            logger.info("Lattice : %.4f\u212b" % self.metadata["lattice"][_material])
            logger.info("Crystal Structure: %s" % self.metadata["crystal_structure"][_material])
            logger.info("Using local metadata Table: %s" % self.use_local_metadata_table)
            logger.info("=" * nbr_ticks)
            logger.info(" h | k | l |\t d (\u212b)  |\t BraggEdge")
            logger.info("-" * nbr_ticks)

            _hkl = self.hkl[_material]
            _bragg_edges = self.bragg_edges[_material]
            _d_spacing = self.d_spacing[_material]

            for index in range(len(_d_spacing)):
                logger.info(
                    " %d | %d | %d |\t %.5f |\t %.5f"
                    % (_hkl[index][0], _hkl[index][1], _hkl[index][2], _d_spacing[index], _bragg_edges[index])
                )

            logger.info("=" * nbr_ticks)

        return ""

    def export(self, filename: str | None = None, file_type: str = "csv") -> None:
        """Export the metadata into various file format

        Arguments:

           filename: output file name to create
           file_type: format of the file to create
              only 'csv' (simple comma separated format) is supported for now

        Exception:
           IOError: if no file name is provided

        """
        if filename is None:
            raise OSError

        for _material in self.material:
            _filename = self._format_filename(filename, _material)
            _metadata = self._format_metadata(_material)
            _data = self._format_data(_material)

            if file_type == "csv":
                Utilities.save_csv(filename=_filename, data=_data, metadata=_metadata)

            else:
                raise NotImplementedError

    def _format_filename(self, filename: str, material: str) -> str:
        _filename, _extension = os.path.splitext(filename)
        new_filename = os.path.join(_filename + "_" + material + _extension)
        return new_filename

    def _format_metadata(self, _material: str) -> list[str]:
        """Format the various metadata to put at the top of output file created"""
        _metadata: list[str] = []
        _metadata.append("Material: %s" % _material)
        _metadata.append("Lattice : %.4fAngstroms" % self.metadata["lattice"][_material])
        _metadata.append("Crystal Structure: %s" % self.metadata["crystal_structure"][_material])
        _metadata.append("Using local metadata Table: %s" % self.use_local_metadata_table)
        _metadata.append("")
        _metadata.append("h, k, l, d(Angstroms), BraggEdge")
        return _metadata

    def _format_data(self, _material: str) -> list[list[int | float]]:
        """Format the data for the output file created"""
        _data: list[list[int | float]] = []
        _hkl = self.hkl[_material]
        _bragg_edges = self.bragg_edges[_material]
        _d_spacing = self.d_spacing[_material]
        for index in range(len(_d_spacing)):
            _data.append([_hkl[index][0], _hkl[index][1], _hkl[index][2], _d_spacing[index], _bragg_edges[index]])
        return _data
