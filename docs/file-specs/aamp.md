# AAMP File Specification

AAMP files are compressed xml files.

Number values are read in **Little Endian** even though the PowerPC and most Wii U files use Big Endian

### AAMP File Layout

AAMP files are structured as follows.

![AAMP File Structure](images/aamp/aamp-spec.png "AAMP File Structure")

1. AAMP Header
  * File meta data
2. Node Table
  * Defines how XML DOM should be structured
3. Data Table
  * Table of values referenced by the Node Table
4. String Table
  * Table of null-terminated strings referenced by the Node Table

## AAMP Header

### Header Layout

![AAMP Header Structure](images/aamp/aamp-header.png "AAMP Header Layout")

| Offset | Size (bytes) | Type | Description |
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
| `0x24` | 4 | Unsigned Int | Data tabletable size in bytes |
| `0x28` | 4 | Unsigned Int | String table size in bytes |
| `0x2c` | 4 | Unknown      | Unknown. Usually `00 00 00 00` (Unsigned Int `0`) |
| `0x30` | n | String       | A null-terminated string of the resulting file type. Usually `xml\0` The length is equal to value found in `0x14-0x17` (usually 4 bytes). |

The root node follows immediately after the header

### Example

`Lynel_Junior.bdrop`

**Remember** all integers are stored in _Little Endian_ in AAMP files.

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

### Node table Layout

![AAMP Node table Structure](images/aamp/node-layout.png "AAMP Node table Structure")

### Root Node

```
         | 00 01  02 03  04 05  06 07  08 09  0a 0b  0c 0d  0e 0f |
---------+--------------------------------------------------------+-----------------
00000000 | 6C CB  F6 A4  03 00  00 00  03 00  10 00               | l...........
```

| Offset | Size | Type | Description |
|--:|:-:|---|---|
| `0x00` | 4 | Unsigned Int | Node ID. `6C CB F6 A4` |
| `0x04` | 4 | Unknown | Unknown. `03 00 00 00`, `03 00 01 00` |
| `0x08` | 2 | Unsigned Int | Data offset relative to beginning node address |
| `0x0a` | 2 | Unsigned Int | Child node count |

### Node

```
         | 00 01  02 03  04 05  06 07  08 09  0a 0b  0c 0d  0e 0f |
---------+--------------------------------------------------------+-----------------
00000000 | F7 AD  DE 69  20 00  10 00                             | ...i ...
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

## AAMP Checksum

Method for calculating a checksum to verify correct parsing:

1. Get file total size in bytes (`0x0c`)
2. Get total number of nodes (`0x18`, `0x1c` & `0x20`)
3. Get data and string table sizes (`0x24` & `0x28`)
4. Total the bytes
    * 52 bytes for the AAMP header
    * 12 bytes per root node
    * 8 bytes per child node
        * Size depends on data type
  
### Example

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

## Sources and Resources
- [Custom Mario Kart Wiki](http://mk8.tockdom.com/wiki/AAMP_(File_Format))
- [jam1garner aamp2xml](https://github.com/jam1garner/aamp2xml/blob/master/AAMP_docs.txt)
- [MrCheeze aamp.py](https://github.com/MrCheeze/botw-tools/blob/master/aamp.py)