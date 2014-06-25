JavaScript Object Table (JSOT) Version 1.0
==========================================

#### Glen Fletcher
[glen.fletcher@alphaomega-technology.com.au](mailto:glen.fletcher@alphaomega-technology.com.au)

## Chapter 1. Introduction

JavaScript Object Table (abbreviated JSOT) is a table based data serialization language (file format) desgined to be human-friendly, and work well for scienftic data storage. This document provides a Complete Spefication of JSOT language.

JSOT takes concepts form existing text base table formats such as CSV as well as data serialization languages such as JSON and YAML.

### 1.1 Goals

The Design Goals for JSOT are:

1. JSOT is easily readable by humans.
2. JSOT data is portable between programing languages.
3. JSOT provides data strucutres similar to Spreedsheets.
4. JSOT has a consistent model to support generic tools.
5. JSOT is expressive and extensible.
6. JSOT is easy to impliment and use.
7. JSOT support advance features seen in Spreedsheet software, found in most Office Suite.
	- Multiple Sheets/Documents in One File
	- Storage of Forumla and Data

### 1.2 Relation to JSON, YAML and CSV

CSV files provide tables delimited by commas and new lines. Other structre such as the type of values is not defined.

JSON and YAML provide a human readable data interchange format. YAML is more reabable while white space can always be removed from JSON.

Both JSON and YAML provide List (Arrays), Dictionarys (Hash/Maps), and Scalars (Numbers/Strings). In JSOT a file contains data which is condisered to be a List of Lists.

Each Sheet is a List of Lines where Each Line is a List of Objects, Similar to Inline YAML or JSON.

### 1.3 Terminology

This specification uses key words based on RFC2119 to indicate requirement level. 

**May** This word indicate a *optional* feature of processor, these features are not required to be implimented.

**Should** This word indicates a *recommended* feature which should be implimented unless unresabonable to doso.

**Must** This word inficates a *required* feature, Software not implimenting this feature dosen't comform to this standard.

## Chapter 2. Characters

### 2.1 Character Set

For readablity JSOT files use only *printable* unicode characters. The allowed character range explicitly excludes the C0 control block ``0x0-0x1F`` (except for TAB ``0x9``, LF ``0xA``, and CR ``0xD`` which are allowed), DEL ``0x7F``, the C1 control block ``0x80-0x9F`` (except for NEL ``0x85`` which is allowed), the surrogate block ``0xD800-0xDFFF``, ``0xFFFE``, and ``0xFFFF``.

On input a JSOT parser must accept all allowed characters, it may accept non-allowed character.

On output any non-allowed characters must be escaped. Printable character may be escaped removing the need to check unicode characters. Non whitespace ASCII character must not be escaped except where they have special meaning in which case the only acceptable escape sequence is a backslash followed by the character it self.

### 2.2 Character Encoding

All characters mentioned in this specification are Unicode code points. Each such code point is written as one or more bytes depending on the character encoding used. Note that in UTF-16, characters above 0xFFFF are written as four bytes, using a surrogate pair. 

The character encoding is a presentation detail and must not be used to convey content information. 

On Input the JSOT processor must support UTF-8 character encoding. UTF-16 and UTF-32 may be supported.

The document must begin with an ASCII character or optionally a Byte Order Mark. A File not begining with an ASCII character may be consider Invalid.

#### Byte Order Marks

Byte 1 | Byte 2 | Byte 3 | Byte 4 | Encoding
------ | ------ | ------ | ------ | --------
0x00   | 0x00   | 0x00   | ASCII  | UTF-32BE
ASCII  | 0x00   | 0x00   | 0x00   | UTF-32LE
0x00   | ASCII  |        |        | UTF-16BE
ASCII  | 0x00   |        |        | UTF-16LE
ASCII  |        |        |        | UTF-8 (default) 

On Output the JSOT processor should output UTF-8 with out a BOM

### 2.3 Special Characters

Special Characters are characters with special meaning:

A ``#`` character donates a comment that ends at the end of the line.

A ``=`` character donates a special header line and must be the first character on the line.

A ``!`` character donates a tag or data type marker similar to it ussage in YAML

The characters ``@``, ``$``, ``%``, and ``&`` have no special meaning in this version but will be used in later versions, and lines begining with these character should be treated as a comment line. Any content between a pair of these characters should be treated as a null value. If file contains these character outside of a string the fail may be treated as Invalid.

A ``,`` or ``;`` character is used to seperate objects on a Data Line and withing Lists and Dictonaries.

A ``[`` character donates the start of a List.
A ``]`` character donates the end of a List.

A ``{`` character donates the start of a Dictonary.
A ``}`` character donates the end of a Dictonary.
A ``:`` character seperates the key-value pair in a Dictonary.

A ``"`` character begins and ends a String.

A `` ` `` character begins and ends a Forumla.

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
version | The File Format Version (should be 1.0) assumed to be 1.0 if ommitted. | Float
header | Flag indicating the presents of a table header, assumed to be False or No if ommitted. | Bool
typed | Flag indicating if the table is typed, assumed to be False or No if ommitted. | Bool
offset | Offset of the table if extra metadata is present indicate the data row the table begins on assumed to be 0 it ommitted. | Integer
name | Name of the Sheet or Table assumed to be the base file name if ommited. | String

If the first header line contains a **name** key then the file may contain multiple sheet or table each begining with it own header line.

Header lines following the first header line must not contain a **version** key

### 3.2 Special Values
````
SpecialValue = (* Case Insenstive *) ( "true" | "yes" | "on" | "false" | "no" | "off" | "none" | "null" ) ;
````

Idnefitier | Value 
-----------|-------
True       | True  
Yes        | True  
On         | True
False      | False 
No         | False
Off        | False 
None       | None  
Null       | None

These values are case insenstive the value is the equlivelent of the Python type.

###  3.3 Strings

Strings are a sequence of characters of arbatry length. String are normally required to be quoted however unquoted simple strings are allowed.

````
String = UnquotedString | QuotedString ;
````

#### Unquoted Strings

````
UnquotedString = ( SafeCharacter, { '.' | SafeCharacter } ) - SpecialValue ;
SafeCharacter = '\' | '/' | '-' | '_' | 'a'..'f' | 'A'..'F' | '0'..'9' ;
````
In general any value that is a valid idenfitier in a programing language is a valid unquoted string.

Unquoted string must not contain whitespace and must not be a reserved word used for Special Values.

#### Quoted String

````
QuotedString = '"', { Character }, '"" ;
Character = ? Any unicode character except \ or " ? | Escape | CodePoint ;
Escape = '\', ( '"' | '\' | '/' | 'b' | 'f' | 'n' | 'r' | 't' ) ;
CodePoint = ( '\x', 2 * HexDigit ) | ( '\u', 4 * HexDigit ) | ( '\U', 8 * HexDigit ) ; 
HexDigit = ( 'a'..'f' | 'A'..'F' | '0'..'9' ) ;
````
In effect a quoted string can contain any thing, ``\`` and ``"`` need to be escaped with a ``\`` as they respresent an escape sequence and the end of the string.

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
|  ``\t``  | Horziontal Tab
| ``\x..`` | 1 Byte Code Point
| ``\u..`` | 2 Byte Code Point
| ``\U..`` | 4 Byte Code Point   

### 3.4 Numbers

There are 3 Numerical types are supported, Intergal, Real and Complex.

````
Number = Intergal | Real | Complex
````

#### Intergal

````
Interal = [ "-" | "+" ], { "0".."9" }+ ;
````
Intergal Numbers are any length sequence of digits optionally prefixed by a ``+`` or ``-``

#### Real

````
Real = [ "-" | "+" ], ( ( { "0".."9" }+, ".", { "0".."9" } ) | ( ".", { "0".."9" }+ ) ), [ Expoent ] ;
Expoent = ( "e" | "E" ), [ "-" | "+" ], { "0".."9" }+ ;
````
Real Numbers are Integals that have been extended with a fractional compoent and optional Expoent.

#### Complex

````
Complex = [ Real ], ( Real (* Must have sign if optional real, is used *) ), ( "i" | "j" ) ;
````
Complex Numbers are just two Real numbers respresenting and Real and Imagnary Compoent, the Real Part is optional and the Imagnary Part must be followed by a ``i`` or ``j``.

### 3.5 Lists

````
List = "[", { Value / ( "," | ";" ) }, "]" ;
````
Lists are a sequence of values seperated by ``,`` or ``;``, delimited by ``[`` and ``]``.

### 3.5 Dictionary

````
Dictonary = "{", { String, ":", Value / ( "," | ";" ) }, "}" ;
````
Dictonaries are Name-Value Pair Lists, with String names and any value, delimited by ``{`` or ``}`` 

### 3.6 Tags or Special Type

The ``!`` symbol may be used to indicate the special interputation of the following value.

````
TaggedValue = "!", UnquotedString, ( [ Value - TaggedValue ] | ( "(" { Value / ( "," | ";" ) } ")" ) );
````

Note tags have both a prefix anf functional form, the prefix form acepts only 0 or 1 arguments, while the functional form takes a list of arguments. Prefix Tags can not be chained, while functional Tags can take values which include a Tag them self.

#### Buildin Tags
  Tag   | Meaning
--------|--------
!binary | Binary String, using base 64 encoding follows this tag, the value should be decode when the document is read.
!int    | Intergal String Value
!real   | Real String Value
!float  | Real String Value
!complex| Complex String Value, or 2 Reals
!vec2   | Takes Two Numerical Values, respresents a Vector.
!vec3   |  Takes Three Numerical Values, respresents a Vector.
!point2 | Alais of !vec2, Should be used spefically for positions, offset from Orgin.
!point3 | Alais of !vec3, Should be used spefically for positions, offset from Orgin.

#### Custom Tags
Custom Tags must be prefixed by a registered domain name, that you control, any other name is reserved for later usage.

i.e. ``!yourdomainname.com/customtag``

The path compounet of the URI need not exist however it is recomended it provide a spefication of the tags ussage and meaning.

### 3.7 Values

````
Value = String | Number | List | Dictonary | SpecialValue | TaggedValue ;
````

### 3.8 Data Lines

````
DataLine = { Value / ( "," | ";" ) }, ? Newline or End Of File ? ; 
````