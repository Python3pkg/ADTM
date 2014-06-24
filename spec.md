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

###  3.2 Data Lines