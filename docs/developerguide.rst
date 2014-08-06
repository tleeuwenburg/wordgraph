Developer Guide
===============


Getting Set Up
--------------

This package is currently Python 2/3 compatible and we will attempt to maintain that, in order to minimise the barrier to adoption and increase the potential reach of the library. However, Python 3 is the lingua franca, with Python 2.7 supported through backporting. Please attempt to minimise incorporating additional libraries which do not have Python 2.7 support, and all included libraries must have Python 3 support.

There are not very many external dependencies, however getting fully set up has been surprisingly challenging for some specific environments. For this reason, a functional Vagrant configuration has been supplied to support development within a virtual machine environment. 

For those wanting to develop "natively", the package can be successfully installed on recent builds of Fedora, Ubuntu and OSX, and probably older builds also. You will need to set up a Python 3 environment. We recommend using a virtual environment in order to minimise any potential conflicts with other system packages.

Detailed Architectural Overview
-------------------------------

The package is divided into the following key areas:

+The top-level 'wordgraph' method are contained within 'describer.py', which contains logic for passing data and requests off to the appropriate handlers given the source and type of the incoming data.
+The "analysers" file, which contain methods for recognising describable patterns within individual data series within a graph.
+The "grapher" file, which contains methods for creating describable-graph data structures from specific types of source input data. Individual Graph classes can be created which will make assumptions about the data being passed in.
+The "realiser" sub-module, which contains the code for generating language given the describable features of the graph identified in the grapher module. 

Choosing Work Tasks
-------------------

If you prefer, please feel free to just start working in your own direction. No guarantee is made that pull requests will be integrated. If you want to contribute back to the repository, it is best to contact the package maintainers to discuss the direction of your work before investing too much time.

A list of useful tasks are included in the github issues list. If you start working on an issue, even if you are simply looking into it and haven't yet got a solution in mind, please leave a message there. If nothing else, it will give the package maintainers some increased visibility of interest in that particular area. You may also be able to contribute background information and context that could help someone later working on that task.

The documentation pages also often contain suggestions for future work which haven't made it to the issues list, but are still potentially rewarding areas. Please feel free to add these to the issues list, and if you address them, please also update the documentation to match.

Developer Workflow
------------------

The approach of this package is fairly open and encouraging of direct contribution. Please don't commit any code which breaks test compliance, although additional input cases can be added as "xfailing" prior to the development of a solution. For those of you with the 'commit bit', please get a code review (in person or via a pull request) for anything more than about 20 lines. Feel free to get a code review on one-line changes if you would like!

The initial development team was formed during the PyCon AU 2014 sprints, and there is no specific developer induction process at this stage. For now, just flag your interest. It is likely that the process of gaining commit access will involve the submission of a few good-quality pull requests, but please don't be hesitant if you are considering getting involved.

There is also a heavy emphasis on good documentation and test practises. The goal of the project is to support those who want to get involved. There is an "all welcome" approach, not a "rocket scientists only" one.