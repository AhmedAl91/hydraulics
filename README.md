## Hydraulic Model in development

This is a back-end model for 1D hydraulic assessments. It is built from bottom up using:

- Dataclasses for hydraulic states/results (see data_classes.py) which allows the user to define the downstream boundary (e.g. an outfall), and enables the model to propagate the hydraulic state through a calculation loop.

- Fixed parameters and default look-up data exist in constants.py and fittings.py
  
- Classes for Conduits (see conduit.py, pipe.py, channel.py) and Components (see weir.py) which are constructed with design parameters (dimensions, roughness, fittings etc) and hydraulic methods where relevant for their geometry e.g. head losses in filled pipes, gradually varied profiles in channels. Methods have the same name across child classes to ensure abstraction. 

- A class for Nodes (see node.py) which have AODs as properties. This is not implemented yet but will be needed for constructing junctions.

- A Network class (see network.py) which orchestrates the calculation by looping through each object assigned to the network and calling the appropriate solver method for each object. Currently, only serial networks are constructed using a 'position' property to assign the order for each object in the series, where '1' is the object directly upstream of the downstream boundary. Subcritical regimes are assumed by default and therefore solving from downstream -> upstream is the default configuration. Supercritical regimes are identified using a heuristic, where some components are considered a form of hydraulic control (e.g. flumes) and the solver checks for a change in regime. If a supercritical regime is identified, the loop is segmented where the calculated is dictated by the upstream state and the previous downstream states are updated.

- Objects are constructed and methods orchestrated via main.py, fetching data in system.py; this will need replacing with an API for user input.


Further work to develop this model:

- A Network method for connecting serial networks to each other to create junctions, creating a parent network. The Network object will assess flow continuity, where the flow at each node must resolve as:

  **∑Qin - ∑Qout = 0**

- If the residual flow > tolerance then the head losses are re-calculated using an iterative method (presumably bi-section of flows)

- User input API with JSON
