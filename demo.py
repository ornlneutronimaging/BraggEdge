from braggedge.braggedge import BraggEdge

# Looking for the first 4 bragg edges of Fe
_handler = BraggEdge(material = 'Fe', 
                     number_of_bragg_edges = 4)
print(_handler)


