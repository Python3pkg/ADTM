JavaScript Object Table (JSOT) Version 1.0
==========================================

#### Glen Fletcher
[glen.fletcher@alphaomega-technology.com.au](mailto:glen.fletcher@alphaomega-technology.com.au)

## Chapter 1. Introduction

JavaScript Object Table (abbreviated JSOT) is a table based data serialization language (file format) designed to be human-friendly, and work well for scientific data storage. This document provides a Complete Speciation of JSOT language.

JSOT takes concepts form existing text base table formats such as CSV as well as data serialization languages such as JSON and YAML.

### 1.1 Goals

The Design Goals for JSOT are:

1. JSOT is easily readable by humans.
2. JSOT data is portable between programing languages.
3. JSOT provides data structures similar to Spreadsheets.
4. JSOT has a consistent model to support generic tools.
5. JSOT is expressive and extensible.
6. JSOT is easy to implement and use.
7. JSOT support advance features seen in Spreadsheet software, found in most Office Suite.
	- Multiple Sheets/Documents in One File
	- Storage of Formula and Data

### 1.2 Relation to JSON, YAML and CSV

CSV files provide tables delimited by commas and new lines. Other structure such as the type of values is not defined.

JSON and YAML provide a human readable data interchange format. YAML is more readable while white space can always be removed from JSON.

Both JSON and YAML provide List (Arrays), Dictionary’s (Hash/Maps), and Scalars (Numbers/Strings). In JSOT, a file contains data, which is considered a List of Lists.

Each Sheet is a List of Lines where Each Line is a List of Objects, Similar to Inline YAML or JSON.

### 1.3 Terminology

This specification uses key words based on RFC2119 to indicate requirement level. 

**May** This word indicate a *optional* feature of processor, these features are not required to be implemented.

**Should** This word indicates a *recommended* feature which should be implemented unless unreasonable to do so.

**Must** This word indicates a *required* feature, Software not implementing this feature doesn’t conform to this standard.

## Chapter 2. Characters

### 2.1 Character Set

For readability JSOT files use only *printable* Unicode characters. The allowed character range explicitly excludes the C0 control block ``0x0-0x1F`` (except for TAB ``0x9``, LF ``0xA``, and CR ``0xD`` which are allowed), DEL ``0x7F``, the C1 control block ``0x80-0x9F`` (except for NEL ``0x85`` which is allowed), the surrogate block ``0xD800-0xDFFF``, ``0xFFFE``, and ``0xFFFF``.

On input, a JSOT parser must accept all allowed characters it may accept non-allowed character.

On output, any non-allowed characters must be escaped. Printable character may be escaped removing the need to check Unicode characters. Non-whitespace ASCII character must not be escaped except where they have special meaning in which case the only acceptable escape sequence is a backslash followed by the character itself.

### 2.2 Character Encoding

All characters mentioned in this specification are Unicode code points. Each such code point is written as one or more bytes depending on the character encoding used. Note that in UTF-16, characters above 0xFFFF are written as four bytes, using a surrogate pair. 

The character encoding is a presentation detail and must not be used to convey content information. 

On Input the JSOT, processor must support UTF-8 character encoding. UTF-16 and UTF-32 may be supported.

The document must begin with an ASCII character or optionally a Byte Order Mark. A File not beginning with an ASCII character may be consider Invalid.

#### Byte Order Marks

Byte 1 | Byte 2 | Byte 3 | Byte 4 | Encoding
------ | ------ | ------ | ------ | --------
0x00   | 0x00   | 0x00   | ASCII  | UTF-32BE
ASCII  | 0x00   | 0x00   | 0x00   | UTF-32LE
0x00   | ASCII  |        |        | UTF-16BE
ASCII  | 0x00   |        |        | UTF-16LE
ASCII  |        |        |        | UTF-8 (default) 

On Output the JSOT, processor should output UTF-8 without a BOM

### 2.3 Special Characters

Special Characters are characters with special meaning:

A ``#`` character donates a comment that ends at the end of the line.

A ``=`` character donates a special header line and must be the first character on the line.

A ``!`` character donates a tag or data type marker similar to it usage in YAML

The characters ``@``, ``$``, ``%``, and ``&`` have no special meaning in this version but will be used in later versions, and lines beginning with these character should be treated as a comment line. Any content between a pair of these characters should be treated as a null value. If file contains these characters outside of a string, the fail may be treated as Invalid.

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

All files should have a header line as the first non-data line in the file indicating at least the File Format Version i.e. **version**.

This Line is a List of key-value pairs.

#### Special Keys

Key | Meaning/Usage | Type
--- | ------------- | ----
version | The File Format Version (should be 1.0) assumed to be 1.0 if omitted. | Float
header | Flag indicating the presents of a table header, assumed to be False or No if omitted. | Bool
typed | Flag indicating if the table is typed, assumed to be False or No if omitted. | Bool
offset | Offset of the table if extra metadata is present indicate the data row the table begins on assumed to be 0 it omitted. | Integer
name | Name of the Sheet or Table assumed to be the base file name if omitted. | String

If the first header line contains a **name** key then the file may contain multiple sheet or table each beginning with its own header line.

Header lines following the first header line must not contain a **version** key

### 3.2 Special Values
````
SpecialValue = (* Case Insenstive *) ( "true" | "yes" | "on" | "false" | "no" | "off" | "none" | "null" ) ;
````

Identifier | Value 
-----------|-------
True       | True  
Yes        | True  
On         | True
False      | False 
No         | False
Off        | False 
None       | None  
Null       | None

These values are case insensitive the value is the equivalent of the Python type.

###  3.3 Strings

Strings are a sequence of characters of arbitrary length. Strings are normally required to be quoted however, unquoted simple strings are allowed.

````
String = UnquotedString | QuotedString ;
````

#### Unquoted Strings

````
UnquotedString = ( SafeCharacter, { '.' | '-' | SafeCharacter } ) - SpecialValue ;
SafeCharacter = '\' | '/' | '_' | 'a'..'f' | 'A'..'F' | '0'..'9' ;
````
In general, any value that is a valid identifier in a programing language is a valid unquoted string.

Unquoted string must not contain whitespace and must not be a reserved word used for Special Values.

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
Integral Numbers are any length sequence of digits optionally prefixed by a ``+`` or ``-``

#### Real

````
Real = [ "-" | "+" ], ( ( { "0".."9" }+, ".", { "0".."9" } ) | ( ".", { "0".."9" }+ ) ), [ Exponent ] ;
Exponent = ( "e" | "E" ), [ "-" | "+" ], { "0".."9" }+ ;
````
Real Numbers are Integrals that have been extended with a fractional component and optional Exponent.

#### Complex

````
Complex = [ Real ], ( Real (* Must have sign if optional real, is used *) ), ( "i" | "j" ) ;
````
Complex Numbers are just two Real numbers representing and Real and Imaginary Component, the Real Part is optional and the Imaginary Part must be followed by a ``i`` or ``j``.

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

The ``!`` symbol may be used to indicate the special interpretation of the following value.

````
TaggedValue = "!", UnquotedString, ( [ Value - TaggedValue ] | ( "(" { Value / ( "," | ";" ) } ")" ) );
````

Note tags have both a prefix and functional form; the prefix form accepts only zero or one arguments, while the functional form takes a list of arguments. Prefix Tags cannot be chained, while functional Tags can take values which include a Tag them self.

#### Build in Tags
  Tag   | Meaning
--------|--------
!binary | Binary String, using base 64 encoding follows this tag; the value should be decode when the document is read.
!int    | Integral String Value
!real   | Real String Value
!float  | Real String Value
!complex| Complex String Value, or 2 Reals
!vec2   | Takes Two Numerical Values, represents a Vector.
!vec3   | Takes Three Numerical Values, represents a Vector.
!point2 | Alias of !vec2, Should be used septically for positions, offset from Organ.
!point3 | Alias of !vec3, Should be used septically for positions, offset from Organ.
!formula| Formula String and optional recalculated value as second argument.

#### Custom Tags
Custom Tags must be prefixed by a registered domain name, that you control, any other name is reserved for later usage.

i.e. ``!yourdomainname.com/customtag``

The path component of the URI need not exist however; it is recommended it provide a speciation of the tags usage and meaning.

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

While the existence of four inline separators plus the implicit newline separator could be used for, multidimensional data this is not allow all inline separators must be treated the same, the usage of different separators is a presentation detail. This is due to the fact that the aim of this format is to provide human readable data tables, if you need to represent multidimensional data it is not human readable a binary standard such as HDFx formats should be used in these cases.

### 3.9 Typed Fields

If the key **typed** is true then a line of tags should immediately precede or follow the header, which ever line is first must be at the specified **offset**.

````
FieldTag = "!", UnquotedString, [ "(" { FieldValue / ( "," | ";" ) } ")" ] );
FieldValue = String | Number | List | Dictonary | SpecialValue | FieldTaggedValue | "$$" ;
FieldTaggedValue = "!", UnquotedString, ( [ FieldValue - FieldTaggedValue ] | ( "(" { FieldValue / ( "," | ";" ) } ")" ) );
````

Note the difference in the Tags for this line, prefix tags have no value as they implicitly prefix every value in the table, while function tags use ``$$`` to indicate a placeholder for the value. Field Tags must contain either the ``!formula`` tag or the ``$$`` placeholder. The Deepest level formula must be a relative formula so it can be applied to generate the values in the table. i.e. ``!formula("T[Field1]*T[Field2]-B1",$$)`` provides a table relative that uses an attribute value and indicate that the field contains precalculated values. This format is recommended whenever the value can be calculated from other data in the table, as it is more describe.

### 3.10 Formula

In this version, there is no shorthand notation for Formula; later versions may introduce such notation. Hence formulas are introduce by the notation ``!formula("FORUMLA"[,result])`` or ``!formula "FORUMLA"``.

Most Spreadsheet program use a Cell notation of ``[ "$" ], { "A".."Z" }+, [ "$" ], { "0".."9" }+ ;`` with the ``$`` indicating the value is fixed when the formula is copied. This concept doesn’t make sense in JSOT format, as formula would be hard to read; hence, we define relative and absolute formula here.

````
Cell = NCell | ACell ;
NCell = "C", ( [ "$", ( "+" | "-" ) ], { "0".."9" }+ | "=" ), "R", ( [ "$", [ "+" | "-" ] ], { "0".."9" }+ | "=" ) ;
ACell = { "A".."Z" }+ { "0".."9" }+ ;
``` 

ACell or Alphanumeric cells are always absolute positions, NCell of Numeric Cells May be both Absolute and Relative with the ``$`` indicating the value is relative to the current cell. ``=`` is an alias for ``$+0`` i.e. the same column or row. ``C$-1`` in column 3 or C refers to column 2 or B, while ``C$+1`` refers to column 4 or D. Note the sign is not optional the idea here is we can think of ``$`` as being the number for the current column or row.

There is a third method of reference for tables with a header, only valid in the fields of the table i.e. below the header.

````
TCell = "T", "[", String, "]", [ "[", ( [ "+" | "-" ], { "0".."9" } | TFunc ), "]" ] ;
TFunc = (* Case insensitive *) "Max" | "Min" | "Avg" | "Std" | "Sum" | "Count" ;
````
