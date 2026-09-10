## Hydraulic Model in development

The model is built from bottom up using:

- A class for Nodes (see node.py) which have AODs as properties.
  
- Classes for Pipes and Channels (see pipe.py and channel.py) which are constructed with design parameters (dimensions, roughness, fittings etc) and hydraulic methods where relevant e.g. head losses in filled pipes, gradually varied profiles in channels.

- A Network class (see network.py) which assigns Pipes and Channels to Nodes as 'Links'. This Network object orchestrates the calculation by calling the appropriate method for each Pipe, Channel and Node object

The intent is for the model to work by:

- User defined inputs for each Pipe, Channel and Node object. Currently this edited in-line in system.py but the intent is to replace with an API e.g. JSON format

- Fixed parameters and look-up data exist in constants.py and fittings.py

- The Network object is constructed using the above objects. The appropriate method is called to estimate head loss from node to node. How this is determined requires development, but is currently manually edited in-line and presumably should be passed as an argument.


Actions to develop this model:

- Determine algorithm for calling the appropriate method, can be user controlled as input using the method name as an argument, with default values to assess gradually varied flows (GVF) and pipe head loss (check for filled pipe and re-assess for partial fill)

- User input API e.g. GUI with JSON
