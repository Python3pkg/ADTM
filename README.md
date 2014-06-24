JSOT
====

A Replacement for the nonuniform CSV, DSV, TSV type file formats for storing data tables based on JSON.

A File can be condisered as a Array of Arrays,
Each Line in the File shall be treated as a JSON Array i.e. `json.decode('[' + line[:-1] + ']')` is approximatly how a line may be read.

Extra Features
--------------

- Support for Complex Numbers

Specification
=============

Version 1.0
-----------

File MUST uset UTF-8 encoding.

Line begining with a `#` shall be ingored as comments excluding the first line which may be a unix shebang

i.e.

````
#!/usrbin/env myreader
````
- - -

````
#!/usrbin/env myreader
#Headers
"Id", "Filename"
#Data
0, "x893.jsot"
1, "y741.jsot"
````
is the same as the file
````
"Id", "Filename"
0, "x893.jsot"
1, "y741.jsot"
````
and will automaticly be opened by myreader on unix systems

Optional File Header if the first non-comment line begins with `=` the reiminder of the line shall be treated as a json object i.e.

````
=Version: 1.0, Headers: True
"Id", "Filename"
0, "x893.jsot"
1, "y741.jsot"
````
explicitly defines the file to be version 1.0.

Special tags don't need to be quoted on this line, for improved readability.

Programs may expect their own tags these tags SHOULD be of the form `"programid/tagname"` and MUST be quoted.

### Special Tags

| Tag  | Meaning |
|------|---------|
| Version | Explicitly mark the File Version,should be 1.0 for this version, if ommited file is always version 1.0. |
| Headers | Flag indicating the file has a header line, defaults to False, unless reader requires headers than defaults to True. |
| Name | Name of the table |


### Reserved Symbols

The Following symbols have been reserved and will be used for special meaning in future version of this specification: `!`, `@`, `$`, `%`, `&`. Also Note that `=` and `#` are reserved and have been given meaning in this version of the specification.

Note: Non defined reserved symbols SHOULD be treated as comments and ingored.

### Multiple Tables/Sheets

A file may contain several table seperated by header lines, if first no comment line is a header line with `Name` defined, each following line must define `Name` also.

Note: `Version` is only valid on the first header and applies to the entire files

i.e.

```` 
=Version: 1.0, Headers: True, Name: Index
"Id", "Name", "Desc"
0, "x893", "..."
1, "y741", "..."
=Headers: False, Name: x893
0.34, 0.4+2.1i
0.5, -0.5+1.0i
=Headers: False, Name: y741
0.34, 1.4+3.1i
0.5, 0.5+0.8i
````

### Data Lines

The File shall be treted as an Array of Data Lines, which are them selves Arrays as defined in the [JSON specification](http://json.org/)

i.e.

````
"Id", "Filename"
0, "x893.jsot"
1, "y741.jsot"
````

is equlivelent to 

````
[["Id", "Filename"], [0, "x893.jsot"], [1, "y741.jsot"]]
````

### Values

All indivdual value match the [JSON specification](http://json.org/)

#### Numbers

One critical numerical type missing fron the JSON specification is Complex Numbers as such Number are redefined to be a super set of JSON number type:

````
Number := ('-'|'+')? (('0'...'9')* ( '.' ('0'...'9')+)?|('0'...'9')+ '.') ( ('e'|'E') ('-'|'+')? ('0'...'9')+ )?
Complex := (Number)? ((Number /* Sign Required if has Real Part */) ("i"|"j"))
````

