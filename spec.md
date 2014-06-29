Adaptive Data Tabulation Markup (ADTM) Version 1.0
==================================================

#### Glen Fletcher
[glen.fletcher@alphaomega-technology.com.au](mailto:glen.fletcher@alphaomega-technology.com.au)

Copyright &copy; 2014 Glen Fletcher (AlphaOmega Technology)<br />This document may be freely copied, provided it is not modified.

## Chapter 1. Introduction

JavaScript Object Table (abbreviated ADTM) is a table based data serialization language (file format) designed to be human-friendly, and work well for scientific data storage. This document provides a Complete Speciation of ADTM language.

ADTM takes concepts form existing text base table formats such as CSV as well as data serialization languages such as JSON and YAML.

### 1.1 Goals

The Design Goals for ADTM are:

1. ADTM is easily readable by humans.
2. ADTM data is portable between programing languages.
3. ADTM provides data structures similar to Spreadsheets.
4. ADTM has a consistent model to support generic tools.
5. ADTM is expressive and extensible.
6. ADTM is easy to implement and use.
7. ADTM support advance features seen in Spreadsheet software, found in most Office Suite.
	- Multiple Sheets/Documents in One File
	- Storage of Formula and Data

### 1.2 Relation to JSON, YAML and CSV

CSV files provide tables delimited by commas and new lines. Other structure such as the type of values is not defined.

JSON and YAML provide a human readable data interchange format. YAML is more readable while white space can always be removed from JSON.

Both JSON and YAML provide List (Arrays), Dictionary’s (Hash/Maps), and Scalars (Numbers/Strings). In ADTM, a file contains data, which is considered a List of Lists.

Each Sheet is a List of Lines where Each Line is a List of Objects, Similar to Inline YAML or JSON.

### 1.3 Terminology
The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**,  **MAY**, and **OPTIONAL** in this document are to be interpreted as described in **[RFC 2119](http://tools.ietf.org/html/rfc2119)**.

## Chapter 2. Characters

### 2.1 Character Set

For readability ADTM files use only *printable* Unicode characters. The allowed character range explicitly excludes the C0 control block ``0x0-0x1F`` (except for TAB ``0x9``, LF ``0xA``, and CR ``0xD`` which are allowed), DEL ``0x7F``, the C1 control block ``0x80-0x9F`` (except for NEL ``0x85`` which is allowed), the surrogate block ``0xD800-0xDFFF``, ``0xFFFE``, and ``0xFFFF``.

On input, a ADTM parser **MUST** accept all allowed characters it **MAY** accept non-allowed character.

On output, any non-allowed characters **MUST** be escaped. Printable character **MAY** be escaped removing the need to check Unicode characters. Non-whitespace ASCII character **MUST NOT** be escaped except where they have special meaning in which case the only acceptable escape sequence is a backslash followed by the character itself.

### 2.2 Character Encoding

All characters mentioned in this specification are Unicode code points. Each such code point is written as one or more bytes depending on the character encoding used. Note that in UTF-16, characters above 0xFFFF are written as four bytes, using a surrogate pair. 

The character encoding is a presentation detail and **MUST NOT** be used to convey content information. 

On Input the ADTM, processor **MUST** support UTF-8 character encoding. UTF-16 and UTF-32 **MAY** be supported.

The document **MUST** begin with an ASCII character or a Byte Order Mark containing an ASCII character. A File not beginning with an ASCII character **MAY** be consider Invalid.

#### Byte Order Marks

Byte 1 | Byte 2 | Byte 3 | Byte 4 | Encoding
------ | ------ | ------ | ------ | --------
0x00   | 0x00   | 0x00   | ASCII  | UTF-32BE
ASCII  | 0x00   | 0x00   | 0x00   | UTF-32LE
0x00   | ASCII  |        |        | UTF-16BE
ASCII  | 0x00   |        |        | UTF-16LE
ASCII  |        |        |        | UTF-8 (default) 

On Output the ADTM, processor **SHOULD** output UTF-8 without a BOM

### 2.3 Special Characters

Special Characters are characters with special meaning:

A ``#`` character donates a comment that ends at the end of the line.

A ``=`` character donates a special header line and **MUST** be the first character on the line.

A ``!`` character donates a tag or data type marker similar to it usage in YAML

The characters ``@``, ``$``, ``%``, and ``&`` have no special meaning in this version but will be used in later versions, and lines beginning with these character **SHOULD** be treated as a comment line. Any content between a pair of these characters **SHOULD** be treated as a null value. If file contains these characters outside of a string, the fail **MAY** be treated as Invalid.

A ``,`` or ``;`` character is used to separate objects on a Data Line and witching Lists and Dictionaries.

A ``[`` character donates the start of a List.
A ``]`` character donates the end of a List.

A ``{`` character donates the start of a Dictionary.
A ``}`` character donates the end of a Dictionary.
A ``:`` character separates the key-value pair in a Dictionary.

A ``"`` character begins and ends a String.

A `` ` `` character begins and ends a Formula.

## Chapter 3. Document Structure

### 3.1 Header Line

````
HeaderLine = "=", { String, ":", Value / ( "," | ";" ) }, ? Newline or End Of File ? ; 
````

All files **SHOULD** have a header line as the first non-data line in the file indicating at least the File Format Version i.e. **version**.

This Line is a List of key-value pairs.

#### Special Keys

Key | Meaning/Usage | Type
--- | ------------- | ----
version | The File Format Version (**SHOULD** be 1.0) assumed to be 1.0 if omitted. | Float
header | Flag indicating the presents of a table header, assumed to be False or No if omitted. | Bool
typed | Flag indicating if the table is typed, assumed to be False or No if omitted. | Bool
offset | Offset of the table if extra metadata is present indicate the data row the table begins on assumed to be 0 it omitted. | Integer
name | Name of the Sheet or Table assumed to be the base file name if omitted. | String

If the first header line contains a **name** key then the file **MAY** contain multiple sheet or table each beginning with its own header line.

Header lines following the first header line **MUST NOT** contain a **version** key

#### Custom Keys

See Section 3.11 Custom Idenfiters

### 3.2 Special Values
````
SpecialValue = BoolValue | NoneValue | SpecialNumber ;
BoolValue = (* Case Insenstive *) ( "true" | "yes" | "on" | "false" | "no" | "off" ) ;
NoneValue = (* Case Insenstive *) ( "none" | "null" ) ;
SpecialNumber = (* Case Insenstive *) ( "nan" | "inf" | "infinity" | "-inf" | "-infinity" | "+inf" | "+infinity" ) ;
````
**BoolValue**: Boolean values i.e. True or False.
**NoneValue**: Respresents Nothing, i.e. a place holder for no value, or empty
**SpecialNumber**: Respresents Special Numerical Values

Identifier | Value 
-----------|-------
True       | True  
Yes        | True  
On         | True
False      | False 
No         | False
Off        | False 
None       | Nothing  
Null       | Nothing
NaN        | Not A Number
Inf        | Postive Infinity
Infinity   | Postive Infinity
+Inf       | Postive Infinity
+Infinity  | Postive Infinity
-Inf       | Negative Infinity
-Infinity  | Negative Infinity


###  3.3 Strings

Strings are a sequence of characters of arbitrary length. Strings are **SHOULD** to be quoted however, unquoted simple strings **MAY** be used.

````
String = UnquotedString | QuotedString ;
````

#### Unquoted Strings

````
UnquotedString = ( SafeCharacter, { '.' | '-' | '0'..'9' | SafeCharacter } ) - SpecialValue ;
SafeCharacter = '\' | '/' | '_' | 'a'..'f' | 'A'..'F' ;
````
In general, any value that is a valid identifier in a programing language is a valid unquoted string.

Unquoted string **MUST NOT** contain whitespace and **MUST NOT** be a reserved word used for Special Values.

#### Quoted String

````
QuotedString = '"', { Character }, '"" ;
Character = ? Any unicode character except \ or " ? | Escape | CodePoint ;
Escape = '\', ( '"' | '\' | '/' | 'b' | 'f' | 'n' | 'r' | 't' ) ;
CodePoint = ( '\x', 2 * HexDigit ) | ( '\u', 4 * HexDigit ) | ( '\U', 8 * HexDigit ) ; 
HexDigit = ( 'a'..'f' | 'A'..'F' | '0'..'9' ) ;
````
In effect a quoted string can contain any thing, ``\`` and ``"`` need to be escaped with a ``\`` as they represent an escape sequence and the end of the string.

##### Escape Sequences

| Sequence | Meaning/Value
|:--------:|--------------
|  ``\"``  | Literal ``"``
|  ``\\``  | Literal ``\``
|  ``\/``  | Literal ``/``
|  ``\b``  | Backspace
|  ``\f``  | Formfeed
|  ``\n``  | Newline
|  ``\r``  | Carriage Return
|  ``\t``  | Horizontal Tab
| ``\x..`` | 1 Byte Code Point
| ``\u..`` | 2 Byte Code Point
| ``\U..`` | 4 Byte Code Point   

### 3.4 Numbers

There are three Numerical types are supported, Integral, Real and Complex.

````
Number = Integral | Real | Complex
````

#### Integral

````
Integral = [ "-" | "+" ], { "0".."9" }+ ;
````
Integral Numbers are any length sequence of digits have an **OPTIONAL** prefixed of ``+`` or ``-``

#### Real

````
Real = [ "-" | "+" ], ( ( { "0".."9" }+, ".", { "0".."9" } ) | ( ".", { "0".."9" }+ ) ), [ Exponent ] ;
Exponent = ( "e" | "E" ), [ "-" | "+" ], { "0".."9" }+ ;
````
Real Numbers are Integrals that have been extended with a fractional component and **OPTIONAL** Exponent.

#### Complex

````
Complex = [ Real ], ( Real (* MUST have sign if **OPTIONAL** real, is used *) ), ( "i" | "j" ) ;
````
Complex Numbers are just two Real numbers representing and Real and Imaginary Component, the Real Part is **OPTIONAL** and the Imaginary Part **MUST** be followed by a ``i`` or ``j``.

### 3.5 Lists

````
List = "[", { Value / ( "," | ";" ) }, "]" ;
````
Lists are a sequence of values separated by ``,`` or ``;``, delimited by ``[`` and ``]``.

### 3.5 Dictionary

````
Dictionary = "{", { String, ":", Value / ( "," | ";" ) }, "}" ;
````
Dictionaries are Name-Value Pair Lists, with String names and any value, delimited by ``{`` or ``}`` 

### 3.6 Tags or Special Type

The ``!`` symbol **MAY** be used to indicate the special interpretation of the following value.

````
TaggedValue = "!", UnquotedString, ( [ Value - TaggedValue ] | ( "(" { Value / ( "," | ";" ) } ")" ) );
````

Note tags have both a prefix and functional form; the prefix form accepts only zero or one arguments, while the functional form takes a list of arguments. Prefix Tags cannot be chained, while functional Tags can take values which include a Tag them self.

#### Build in Tags
  Tag   | Meaning
--------|--------
!binary | Encoded Binary String.
!int    | Integral String Value
!real   | Real String Value
!float  | Real String Value
!complex| Complex String Value, or 2 Reals
!vec2   | Takes Two Numerical Values, represents a Vector.
!vec3   | Takes Three Numerical Values, represents a Vector.
!point2 | Alias of !vec2, **SHOULD** be used septically for positions, offset from Organ.
!point3 | Alias of !vec3, **SHOULD** be used septically for positions, offset from Organ.
!formula| Formula String and **OPTIONAL** recalculated value as second argument.

#### Custom Tags

See Section 3.11 Custom Idenfiters

### 3.7 Values

````
Value = String | Number | List | Dictionary | SpecialValue | TaggedValue ;
````

### 3.8 Data Lines

````
DataLine = { Value / ( "," | ";" | "|" | ":" ) }, ? Newline or End Of File ? ; 
````
Data Lines are unscaled list however, they also provide ``|`` and ``:`` as separates for improved presentation.

i.e.

The following is a valid table with two-header values/attributes/metadata, 3 Fields and an Id, by using ``|`` and ``:``, separators the text presentation of the data is more readable.

````
=version: 1.0, header: yes, offset: 2
Attribute1: value
Attribute2: valueA, valueB
 id | Field1 | Field2 | Field3
 0  |  600   |  7.89  | 1.2+3i
 1  |  500   |  8.92  | 2-1.9i
 2  |  400   |  6.45  | -1+.3i
 3  |  300   |  1.87  | 6.7-9i  
````

While the existence of four inline separators plus the implicit newline separator could be used for, multidimensional data this is not allow all inline separators **MUST** be treated the same, the usage of different separators is a presentation detail. This is due to the fact that the aim of this format is to provide human readable data tables, if you need to represent multidimensional data it is not human readable a binary standard such as HDFx formats **SHOULD** be used in these cases.

### 3.9 Typed Fields

If the key **typed** is true then a line of tags **SHOULD** immediately precede or follow the header, which ever line is first **MUST** be at the specified **offset**.

````
FieldTag = "!", UnquotedString, [ "(" { FieldValue / ( "," | ";" ) } ")" ] );
FieldValue = String | Number | List | Dictonary | SpecialValue | FieldTaggedValue | "$$" ;
FieldTaggedValue = "!", UnquotedString, ( [ FieldValue - FieldTaggedValue ] | ( "(" { FieldValue / ( "," | ";" ) } ")" ) );
````

Note the difference in the Tags for this line, prefix tags have no value as they implicitly prefix every value in the table, while function tags use ``$$`` to indicate a placeholder for the value. Field Tags **MUST** contain either the ``!formula`` tag or the ``$$`` placeholder. The Deepest level formula **MUST** be a relative formula so it can be applied to generate the values in the table. i.e. ``!formula("T[Field1]*T[Field2]-B1",$$)`` provides a table relative that uses an attribute value and indicate that the field contains precalculated values. This format is **RECOMMENDED** whenever the value can be calculated from other data in the table, as it is more describe.

### 3.10 Custom Idenfiters

Custom idenfitiers (tags and header keys) **MUST** be prefixed by a registered domain name, that you control, or path on a public domain you control, idenfitiers that don't contain a ``/`` **MUST** be defined in this specification. This forms a basic url with out the schema, port and other non meaning full features, in this context (as this is just a unique name).  

URN's **MAY** also be used by replacing ``:`` with ``/``, the value ``urn`` is reserved in all cases for this ussage and will never be overriden.

i.e. ``yourdomainname.com/tagname``, ``github.com/yourname/projectname/tagname``, ``code.google.com/p/projectname/tagname``, ``urn/isbn/isbnnumber``

For the most part all these names **SHOULD** be valid Unquoted Strings, however there **MAY** exist case in which this is not possible, in such cases the idenfitier is invalid as a tag name as tag **MUST** be Unquoted Strings, however it can be used as a header key in Quoted form.

Also valid for header keys are URN prefixes i.e. ``urn/isbn`` is a valid header key given the expected value is an isbn

### 3.11 Binary Strings

Binary String are prefixed with the tag ``!binary``.

Binary Strings **MUST** be encoded using url safe base 64 without padding (see **[RFC 3548](http://tools.ietf.org/html/rfc3548.html)**).

Padding **MUST** be striped from the encode string on output.

#### Other Encodings

Base 16 and 32 encodings are also supported (see **[RFC 3548](http://tools.ietf.org/html/rfc3548.html)**), to use these encodings the string **MUST** be prefixed with ``/xx/``, where ``xx`` is the base.

i.e. 
``!binary QmluYXJ5IERhdGE`` is the string "Binary Data"
``!binary /16/d41d8cd98f00b204e9800998ecf8427e`` for an md5 checksum

Note Base 16 and 32 are always valid Unquoted Strings, Base 64 is only valid if it starts with a letter or a ``_``.

## Chapter 4. Document Presentation

This chapter describes the **RECOMENDED** presentation style of ADTM documents, all requirements in this section are modified by this requirement level. This section is provide to describe how to produce easy to read documents.

### 4.1 Tables with Fields (header: yes)

For tables with a table header defining field names, the ``|`` seperator **MUST** be used, and all coloums **MUST** be fixed width.

i.e.

````
 Field1 | Field2 | Field3
  600   |  True  | "The First Row"
  955   |  False | "The Second Row"
   45   |  True  | "The Third Row"
 1000   |  True  | "The Fourth Row"
````
As Showen here when such a table is displayed using monospace fonts the coloums are aligned with the Field names in the header row, and the seperator acts to draw visual lines between the coloums this makes for a more readable document.

To futher improve readablity every 2-6 lines a blank line or comment containing only the seperators **SHOULD** be added, the interval **SHOULD** be constant. Every 4-6 Intervals **SHOULD** use a comment line that repeats the fields names. (4 x 5 is **RECOMENDED**)

i.e.

````
 Field1 | Field2 | Field3
  600   |  True  | "The First Row"
  955   |  False | "The Second Row"
   45   |  True  | "The Third Row"
 1000   |  True  | "The Fourth Row"
#       |        |               
  600   |  True  | "The 2nd First Row"
  955   |  False | "The 2nd Second Row"
   45   |  True  | "The 2rdThird Row"
 1000   |  True  | "The 2nd Fourth Row"
# ..... |        | ..... (jump a few intervals)
#Field1 | Field2 | Field3
  600   |  True  | "The 6th First Row"
  955   |  False | "The 6th Second Row"
   45   |  True  | "The 6th Third Row"
 1000   |  True  | "The 6th Fourth Row"
#       |        |               
  600   |  True  | "The 7th First Row"
  955   |  False | "The 7th Second Row"
   45   |  True  | "The 7th Third Row"
 1000   |  True  | "The 7th Fourth Row"               
````  
This allow for a long document to be easily read the blank lines help to isolate indivdual lines, and the repeated field name, allow for the field names to be always visible when reading the document in text format.

### 4.2 Document Meta Data

Often a table is respresenting some data set, it is useful to attach Meta Data to these tables. Here the Meta Data **MUST** be a the top of the document, using the **offset** value to shift the fields header down.

Meta Data values should have a name associated with them, this **MUST** appear in the cell before the value and use the ``:`` seperator, if multiple values are associate they **MUST** be seperated by the ``,`` seperator. Where revlent the ``;`` seperator **MAY** be used to add another value to the line however this value **SHOULD** be related to the first value.
i.e.

````
Range: 0, 100; Count: 5
Name: "Name of dataset"
Resolution: 500
````
By structuring the data in such a way it is easy to follow what the Meta Data is describing, the Names here tell a human what the value are. On the first line A Range of value, with a speficied count, i.e. 0,   25,   50,   75,  100 is describe, hence it uses the ``;`` seperator, the next two line are seperate as they aren't related to any of the other lines hence a Name followed by a value.

Note: the Names here are not part of the ADTM spec, and stylist only, unless a more specific spec says otherwise the position of the values i.e. B1, C1, E1, B2, B3 are whats important.

### 4.3 Field Names

Field Names as describe in the previous two sections **SHOULD** always be an Unquoted String, think of them as an identifier for a variable.

## Chapter 5. Forumla

This chapter fullign describes the forumla type, incluing syntax and functions.

### 5.1 Basic Syntax

In this version, there is no shorthand notation for Formula; later versions **MAY** introduce such notation. Hence formulas are introduce by the notation ``!formula("FORUMLA"[,result])`` or ``!formula "FORUMLA"``.

Most Spreadsheet program use a Cell notation of ``[ "$" ], { "A".."Z" }+, [ "$" ], { "0".."9" }+ ;`` with the ``$`` indicating the value is fixed when the formula is copied. This concept doesn’t make sense in ADTM format, as formula would be hard to read; hence, we define relative and absolute formula here.

````
Cell = NCell | ACell ;
NCell = "C", ( [ "$", ( "+" | "-" ) ], { "0".."9" }+ | "=" ), "R", ( [ "$", [ "+" | "-" ] ], { "0".."9" }+ | "=" ) ;
ACell = { "A".."Z" }+ { "0".."9" }+ ;
``` 

ACell or Alphanumeric cells are always absolute positions, NCell of Numeric Cells **MAY** be both Absolute and Relative with the ``$`` indicating the value is relative to the current cell. ``=`` is an alias for ``$+0`` i.e. the same column or row. ``C$-1`` in column 3 or C refers to column 2 or B, while ``C$+1`` refers to column 4 or D. Note the sign is **REQUIRED** the idea here is that ``$`` is the number for the current column or row.

There is a third method of reference for tables with a header, only valid in the fields of the table i.e. below the header.

````
TCell = "T", "[", String, "]", [ "[", ( [ "+" | "-" ], { "0".."9" } | TFunc ), "]" ] ;
TFunc = (* Case insensitive *) "Max" | "Min" | "Avg" | "Std" | "Sum" | "Count" ;
````

### 5.2 Operators

Operator |    Order   | Operation
--------:|:----------:|:----------
minus sign ( - ) |     5      | Subtraction 
plus sign ( + ) |     4      | Addition  
asterisk ( * ) |     3      | Multiplication
forward slash ( / ) |     2      | Division
caret ( ^ ) |     1      | Exponentiation

The Operators are applied base on the Listed Order

### 5.3 Brackets

Brackets ``(`` and ``)`` may be used to alter the order of operators the content inside will be evaluated first.

### 5.4 Functions

All Function names are case insenstive

 Function | Description
---------:|:-------------
 **FLOOR**( number) | Round number down to the previous Integer
 **CEIL**( number ) | Round number up to the next Integer
 **ROUND**( number [, digits=0] ) | Round number to digits numer of decimal places.
 **ROUNDDOWN**( number [, digits=0] ) | Round number down to digits numer of decimal places. 
 **ROUNDUP**( number [, digits=0] ) | Round number up to digits numer of decimal places.
 **ABS**( number ) | Absolute value of number
  
