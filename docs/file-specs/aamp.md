# Contents

* [AAMP File Specification](#aamp-file-specification)
  * [AAMP File Layout](#aamp-file-layout)
  * [AAMP Header](#aamp-header)
    * [Header Layout](#header-layout)
    * [Header Structure](#header-structure)
    * [Example](#example)
  * [Nodes](#nodes)
    * [Node Table Layout](#node-table-layout)
    * [Root Node](#root-node)
      * [Root Node Structure](#root-node-structure)
    * [Node](#node)
      * [Node Structure](#node-structure)
    * [Node Data Types](#node-data-types)
* [AAMP to XML Parsing Algorithm](#aamp-to-xml-parsing-algorithm)
  * [Example](#example-1)
    * [First Node](#first-node)
    * [Second Node](#second-node)
* [AAMP Checksum](#aamp-checksum)
  * [Example](#example-2)
* [Sources and Resources](#sources-and-resources)

# AAMP File Specification

AAMP files are compressed xml files.

## AAMP File Layout

AAMP files are structured as follows.

![AAMP File Structure](images/aamp/aamp-spec.png "AAMP File Structure")

1. **AAMP Header** - File metadata
2. **Node Table** - Defines how XML DOM should be structured
3. **Data Table** - Table of values referenced by the Node Table
4. **String Table** - Table of null-terminated strings referenced by the Node Table

## AAMP Header

The AAMP header contains metadata relating to the total size, number of nodes, expected file extension and sizes of tables to help proper parsing.

### Header Layout

![AAMP Header Structure](images/aamp/aamp-header.png "AAMP Header Layout")

### Header Structure

```c#
struct AAMPHeader {
    char[4]     magic;
    uint        version;
    uint        unknown0x08;
    uint        fileSize;
    uint        unknown0x10;
    uint        fileExtensionLength;
    uint        rootNodeCount;
    uint        childCount;
    uint        listNodes;
    uint        dataTableSize;
    uint        stringTableSize;
    uint        unknown0x2c;
    string      fileExtension;
}
```

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 4 | String       | AAMP file signature (magic) `41 41 4D 50` or "AAMP" |
| `0x04` | 4 | Unsigned Int | AAMP version. Should be version 2 |
| `0x08` | 4 | Unknown      | Unknown. Usually `03 00 00 00` (Unsigned Int `3`) |
| `0x0c` | 4 | Unsigned Int | File size in bytes |
| `0x10` | 4 | Unknown      | Unknown. Usually `00 00 00 00` (Unsigned Int `0`) |
| `0x14` | 4 | Unsigned Int | File extension name length |
| `0x18` | 4 | Unsigned Int | Number of root nodes |
| `0x1c` | 4 | Unsigned Int | Number of child nodes on the root node |
| `0x20` | 4 | Unsigned Int | Number of nodes excluding root nodes and root child nodes (direct descendants) |
| `0x24` | 4 | Unsigned Int | Data table size in bytes |
| `0x28` | 4 | Unsigned Int | String table size in bytes |
| `0x2c` | 4 | Unknown      | Unknown. Usually `00 00 00 00` (Unsigned Int `0`). Maybe Node table offset? |
| `0x30` | n | String       | A null-terminated string of the resulting file type. Usually `xml\0` The length is equal to value found in `0x14-0x17` (usually 4 bytes). |

### Example

`Lynel_Junior.bdrop`

**Remember** all integers are stored as _Little Endian_ in AAMP files.

| Name | Hex Value | Type | Value |
|------|----------:|:----:|-------|
| Signature | `41 41 4D 50` | string | `AAMP` |
| Version | `02 00 00 00` | unsigned int 32 | `2` |
| Unknown 0x08 | `03 00 00 00` | unsigned int 32 | `3` |
| File Size | `28 06 00 00` | unsigned int 32 | `1576` |
| Unknown 0x10 | `00 00 00 00` | Unknown |  |
| File Extension Length | `04 00 00 00` | unsigned int 32 | `4` |
| Root Nodes Count | `01 00 00 00` | unsigned int 32 | `1` |
| Root Node Children Count | `10 00 00 00` | unsigned int 32 | `16` |
| Remaining Nodes | `81 00 00 00` | unsigned int 32 | `129` |
| Data table Size | `20 00 00 00` | unsigned int 32 | `32` |
| String table Size | `40 01 00 00` | unsigned int 32 | `320` |
| Unknown 0x2c | `00 00 00 00` | Unknown | |
| File Extension | `78 6D 6C 00` | string | `xml` |

## Nodes

There are two types of node structures found in AAMP files, the root node and child nodes. The root node follows immediately after the header (`0x34`). The root node is followed by section nodes. Each section node contains a list of value nodes (see [Node Data Types](#node-data-types)).

### Node Table Layout

![AAMP Node table Structure](images/aamp/node-layout.png "AAMP Node table Structure")

### Root Node

The root node differs from other nodes because it is 12 bytes long and can contain up to 255 (`0xFF`) child nodes.

#### Root Node Structure

```
Offset(h) | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F |
----------+-------------------------------------------------+--------------
 00000000 | 6C CB F6 A4 03 00 00 00 03 00 10 00             | l.......    
```

```c#
struct RootNode {
    char[4]     id;
    uint        unknown0x04;
    ushort      offset;
    ushort      childCount;
}
```

| Offset | Size | Type | Description |
|--:|:-:|---|---|
| `0x00` | 4 | Unsigned Int | Node ID. `6C CB F6 A4` |
| `0x04` | 4 | Unknown | Unknown. `03 00 00 00`, `03 00 01 00` |
| `0x08` | 2 | Unsigned Int | Data offset relative to beginning node address |
| `0x0a` | 2 | Unsigned Int | Child node count |

### Node

Nodes are 8 bytes long and contain a [data type](#node-data-types) and an offset to the node's value or first child node. 

#### Node Structure

```
Offset(h) | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F |
----------+-------------------------------------------------+----------
 00000000 | F7 AD DE 69 20 00 10 00                         | ...i ...
```

```c#
struct Node {
    char[4]     id;
    ushort      offset;
    byte        childCount;
    byte        dataType;
}
```

| Offset | Size | Type | Description |
|--:|:-:|---|---|
| `0x00` | 4 | Unsigned Int | Node ID. |
| `0x04` | 2 | Unsigned Int | Offset to first child node or node value in bytes |
| `0x06` | 1 | Unsigned Int | Child node count |
| `0x07` | 1 | Unsigned Int | Node data type |

The offset is calculated by multiplying the number of bytes by 4 and adding it to the node address

### Node Data Types

Each node has a data type to determine how to correctly parse the node value. If a node's child count is greater than 0
it is _always_ a node regardless of the data type indicated.

| Value | Data Type | Node Size (bytes) | Description |
|:---:|---|:---:|---|
| `0x00` | Node | 4 | The current node has child nodes |
| `0x00` | Boolean | 4? | `0` or `1` |
| `0x01` | Float | 4 | Floating-point number |
| `0x02` | Int | 4 | Integer |
| `0x03` | Vector2 | | Vector array with two floating-point numbers `x`, `y` |
| `0x04` | Vector3 | | Vector array with three floating-point numbers `x`, `y`, `z` |
| `0x06` | Vector4 | | Vector array with four floating-point numbers `x`, `y`, `z`, `w` |
| `0x07` | String | n | Null-terminated string |
| `0x08` | Actor | n | Null-terminated string linking to a BotW Actor object |
| `0x0f` | UnknownString | n | Null-terminated string |
| `0x11` | UnknownUnsignedInt | | |
| `0x14` | String2 | n | Null-terminated string |

# AAMP to XML Parsing Algorithm

An AAMP is parsed to XML by reading through each node and fetching the value from the data table and string table.

1. Parse AAMP Header
2. Read Root Node
3. Recursively read each child node

```
AAMPHeader
└── Root Node
    ├── Child Node
    |   ├── List Node
    |   |   └── Value
    |   ├── List Node
    |       └── Value
    
   ...
   
    └── Child Node
        ├── List Node
        |   └── Value
        ├── List Node
        |   └── Value
        
       ...
       
        └── List Node
            └── Value
```

4. Parse Node Tree to XML DOM

```xml
<?xml version="1.0" encoding="utf-8"?>
<root id="6CCBF6A4" type="complex" length="9">
    <node id="F7ADDE69" type="complex" length="9">
        <node id="B466C697" type="unsignedInt" length="4">8</node>
        <node id="B19DD8D8" type="Actor" length="6">Normal</node>
        
        ...
        
        <node id="152504A2" type="Actor" length="11">Electronic2</node>
    </node>
    
    ...
    
    <node id="19228410" type="complex" length="7">
        <node id="B78496C5" type="unsignedInt" length="4">1</node>
        <node id="EEBB9BF9" type="unsignedInt" length="4">1</node>

        ...

        <node id="6EC61A7E" type="float" length="4">30.0f</node>
    </node>
</root>
```

## Example

For example, `Chuchu_Normal.bdrop`:

```
Offset(h) | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F |
----------+-------------------------------------------------+------------------
 00000000 | 41 41 4D 50 02 00 00 00 03 00 00 00 30 03 00 00 | AAMP........0...
 00000010 | 00 00 00 00 04 00 00 00 01 00 00 00 09 00 00 00 | ................
 00000020 | 41 00 00 00 14 00 00 00 8C 00 00 00 00 00 00 00 | A.......Œ.......
 00000030 | 78 6D 6C 00                                     | xml.
```

Parsing the header would give us the metadata

```c#
AAMPHeader {
    magic =                 'AAMP';
    version =               2;
    unknown0x08 =           3;
    fileSize =              816;        // in bytes
    unknown0x10 =           0;
    fileExtensionLength =   4;
    rootNodeCount =         1;
    childCount =            9;
    listNodes =             65;
    dataTableSize =         20;         // in bytes
    stringTableSize =       140;        // in bytes
    unknown0x2c =           0;
    fileExtension =         'xml';      // null-terminated string
}
```

The root node is immediately following the header

```
Offset(h) | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F |
----------+-------------------------------------------------+------------------
 00000030 |             6C CB F6 A4 03 00 00 00 03 00 09 00 |     lËö¤........
```

Parsing to XML would yield

```c#
RootNode {
    id =            0x6CCBF6A4;
    unknown0x04 =   3;
    offset =        0x40;     // 0x34 + 3 * 0x04
    childCount =    9;
}
```

The next node to read is located at `0x40`. The offset is calculated by multiplying the offset value at `0x0c` with 4 bytes and adding it to the address of the current node (`0x34`). Hence, `0x34 + 0x03 * 0x04 = 0x40`.

In the XML document we would add the root node and add the number of children nodes. I chose to give it a type of "complex" because that is the type found in the `cos.xml` and `app.xml` of the root node.

```xml
<?xml version="1.0" encoding="utf-8"?>
<root id="6CCBF6A4" type="complex" length="9">
    <node></node>
    <node></node>
    <node></node>
    <node></node>
    <node></node>
    <node></node>
    <node></node>
    <node></node>
    <node></node>
</root>
```

>**Note:** The IDs are *probably* hashed references to strings in U-King.rpx and other files. I am  currently working on generating a hash table that matches but have not yet been successful. Once I have a hash table I will no longer use the id attribute, but just call the tag what the hash table indicates. 

Next are 9 child nodes, each 4 bytes in length, that follow one after another

```
Offset(h) | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F |
----------+-------------------------------------------------+------------------
 00000040 | F7 AD DE 69 12 00 09 00 D2 6D 29 26 22 00 07 00 | ÷.Þi....Òm)&"...
 00000050 | 98 24 2E 72 2E 00 07 00 48 A0 57 0B 3A 00 07 00 | ˜$.r....H W.:...
 00000060 | 0F 20 D9 62 46 00 07 00 71 87 9C DF 52 00 07 00 | . ÙbF...q‡œßR...
 00000070 | 20 63 08 3D 5E 00 07 00 8E 33 32 51 6A 00 07 00 |  c.=^...Ž32Qj...
 00000080 | 19 22 84 10 76 00 07 00                         | ."„.v...        
```

For each node

```c#
Node {
    id =            0xF7ADDE69;
    offset =        0x88;           // 0x40 + 18 * 0x04
    childCount =    9;
    dataType =      0;              // Node
}
```

Because this node has a data type of Node, the first child node is located at `0x88`. The offset is calculated by multiplying the offset value at `0x44` with 4 bytes and adding it to the address of the current node (`0x40`). Hence, `0x40 + 0x12 * 0x04 = 0x88`.

Parsing to XML would yield

```xml
<?xml version="1.0" encoding="utf-8"?>
<root id="6CCBF6A4" type="complex" length="9">
    <node id="F7ADDE69" type="complex" length="9">
        <node></node>
        <node></node>
        <node></node>
        <node></node>
        <node></node>
        <node></node>
        <node></node>
        <node></node>
        <node></node>
    </node>
    <node id="D26D2926" type="complex" length="7">
        <node></node>
        <node></node>
        <node></node>
        <node></node>
        <node></node>
        <node></node>
        <node></node>
    </node>
    
    ...
    
    <node id="19228410" type="complex" length="7">
        <node></node>
        <node></node>
        <node></node>
        <node></node>
        <node></node>
        <node></node>
        <node></node>
    </node>
</root>
```

Next are the child node lists. Each is a list of nodes, 4 bytes in length. The starting point is the offset of the parent node and continues `4 bytes * the child count`.

```
Offset(h) | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F |
----------+-------------------------------------------------+------------------
 00000080 |                         B4 66 C6 97 82 00 00 02 |         ´fÆ—‚...
 00000090 | B1 9D D8 DB 85 00 00 08 0B CC D1 42 85 00 00 08 | ±.ØÛ…....ÌÑB…...
 000000A0 | 9D FC D6 35 85 00 00 08 3E 69 B2 AB 85 00 00 08 | .üÖ5…...>i²«…...
 000000B0 | A8 59 B5 DC 86 00 00 08 12 08 BC 45 86 00 00 08 | ¨YµÜ†.....¼E†...
 000000C0 | 84 38 BB 32 86 00 00 08 15 25 04 A2 87 00 00 08 | „8»2†....%.¢‡...
```

Parse each node as a Node

### First Node

```
Offset(h) | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F |
----------+-------------------------------------------------+------------------
 00000080 |                         B4 66 C6 97 82 00 00 02 |         ´fÆ—‚...
```

```c#
Node {
    id =            0xB466C697;
    offset =        0x0290;         // 0x88 + 130 * 0x04
    childCount =    0;
    dataType =      2;              // unsignedInt
}
```

Check offset `0x0290` for the node value

```
Offset(h) | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F |
----------+-------------------------------------------------+------------------
 00000290 | 08 00 00 00                                     | ....            
```

`80 00 00 00` parsed as `unsignedInt` (little Endian-ness) is `8`

Parsing to XML would yield

```xml
<?xml version="1.0" encoding="utf-8"?>
<root id="6CCBF6A4" type="complex" length="9">
    <node id="F7ADDE69" type="complex" length="9">
        <node id="B466C697" type="unsignedInt" length="4">8</node>
        <node></node>
        
        ...
        
    </node>
    
    ...
    
</root>
```

### Second Node

```
Offset(h) | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F |
----------+-------------------------------------------------+------------------
 00000090 | B1 9D D8 DB 85 00 00 08                         | ±.ØÛ…...        
```

```c#
Node {
    id =            0xB19DD8DB;
    offset =        0x02A4;         // 0x90 + 133 * 0x04
    childCount =    0;
    dataType =      8;              // Actor
}
```

Check offset `0x02A4` for the node value

```
Offset(h) | 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F |
----------+-------------------------------------------------+------------------
 00000290 | 00 00 F0 41 4E 6F 72 6D 61 6C 00 00 4E 6F 72 6D | ..ðANormal..Norm
```

Actor data types are parsed as a null-terminated string. `Normal` would be the value for this actor.

Parsing to XML would yield

```xml
<?xml version="1.0" encoding="utf-8"?>
<root id="6CCBF6A4" type="complex" length="9">
    <node id="F7ADDE69" type="complex" length="9">
        <node id="B466C697" type="unsignedInt" length="4">8</node>
        <node id="B19DD8D8" type="Actor" length="6">Normal</node>
        
        ...
        
    </node>
    
    ...
    
</root>
```

# AAMP Checksum

Method for calculating a checksum to verify correct parsing:

1. Get file total size in bytes (`0x0c`)
2. Get total number of nodes (`0x18`, `0x1c` & `0x20`)
3. Get data and string table sizes (`0x24` & `0x28`)
4. Total the bytes
    * 52 bytes for the AAMP header
    * 12 bytes per root node
    * 8 bytes per child node
        * Size depends on data type
  
## Example

For example, `Lynel_Junior.bdrop`:

```
total file size:            1576  bytes
total number of nodes:      146
data table size:            32    bytes
string table size:          320   bytes

aamp header:                52    bytes
1 root node * 12 bytes:     12    bytes
145 nodes * 8 bytes:        1160  bytes
data table:                 32    bytes
string table:             + 320   bytes
                         ---------------
total size:                 1576  bytes
```

# Sources and Resources
- [Custom Mario Kart Wiki](http://mk8.tockdom.com/wiki/AAMP_(File_Format))
- [jam1garner aamp2xml](https://github.com/jam1garner/aamp2xml/blob/master/AAMP_docs.txt)
- [MrCheeze aamp.py](https://github.com/MrCheeze/botw-tools/blob/master/aamp.py)