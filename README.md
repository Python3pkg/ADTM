JSOT
====

A Replacement for the nonuniform CSV, DSV, TSV type file formats for storing data tables based on JSON.

A File can be condisered as a List of Lists,
Each Line in the File shall be treated as a JSON list object i.e. ```json.decode('[' + line[:-1] + ']')``` is approximatly how a line may be read.

Extra Features
--------------

- Support for Complex Numbers
