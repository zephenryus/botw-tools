# AAMP File Specification

AAMP files are compressed xml files.

Number values are read in **Little Endian** even though the PowerPC and most Wii U files use Big Endian

## AAMP File Layout

![AAMP File Structure](images/aamp/aamp-spec.png "AAMP File Structure")

1. AAMP Header
2. Node Buffer
3. Data Buffer
4. String Buffer

## AAMP Header

```
         0001 0203 0405 0607 0809 0a0b 0c0d 0e0f
00000000 4141 4D50 0200 0000 0300 0000 2806 0000
00000010 0000 0000 0400 0000 0100 0000 1000 0000
00000020 8100 0000 2000 0000 4001 0000 0000 0000
00000030 786D 6C00
```

| Offset | Size (bytes) | Type | Description |
|---|---|---|---|
| `0x00` | 4 | String | AAMP file signature (magic) `41 41 4D 50` or "AAMP" |
| `0x04` | 4 | Unsigned Int | AAMP version. Should be version 2 |
| `0x08` | 4 | Unknown | Unknown. Usually `03 00 00 00` (Unsigned Int `3`) |
| `0x0c` | 4 | Unsigned Int | File size in bytes |
| `0x10` | 4 | Unknown | Unknown. Usually `00 00 00 00` (Unsigned Int `0`) |
| `0x14` | 4 | Unsigned Int | File extension name length |
| `0x18` | 4 | Unsigned Int | Number of root nodes |
| `0x1c` | 4 | Unsigned Int | Number of child nodes on the root node |
| `0x20` | 4 | Unsigned Int | Number of nodes excluding root nodes and root child nodes (direct descendants) |
| `0x24` | 4 | Unsigned Int | Data buffer size in bytes |
| `0x28` | 4 | Unsigned Int | String buffer size in bytes |
| `0x2c` | 4 | Unknown | Unknown. Usually `00 00 00 00` (Unsigned Int `0`) |
| `0x30` | n | String | A null-terminated string of the resulting file type. Usually `xml\0` The length is equal to value found in `0x14-0x17` (usually 4 bytes). |

The root node follows immediately after the header

## Root Node

```
         0001 0203 0405 0607 0809 0a0b
00000000 6CCB F6A4 0300 0000 0300 1000
```

| Relative Address | Type | Size | Description |
|---|---|---|---|
| `0x00-0x03` | Unsigned Int | 4 bytes | Node ID. `6C CB F6 A4` |
| `0x04-0x07` | Unknown | 4 bytes | Unknown. `03 00 00 00`, `03 00 01 00` |
| `0x08-0x09` | Unsigned Int | 2 bytes | Data offset relative to beginning node address |
| `0x0a-0x0b` | Unsigned Int | 2 bytes | Child node count |

## Node

```
         0001 0203 0405 0607
00000000 F7AD DE69 2000 1000
```

| Relative Address | Type | Size | Description |
|---|---|---|---|
| `0x00-0x03` | Unsigned Int | 4 bytes | Node ID. |
| `0x04-0x05` | Unsigned Int | 2 bytes | Data offset relative to beginning node address |
| `0x06-0x06` | Unsigned Int | 1 byte | Child node count |
| `0x07-0x07` | Unsigned Int | 1 byte | Node data type |

## Node Data Types

| Data Type | Value | Description |
|---|---|---|
| Node | 0x00 | desc |
| Boolean | 0x00 | desc |
| Float | 0x01 | desc |
| Int | 0x02 | desc |
| Vector2 | 0x03 | desc |
| Vector3 | 0x04 | desc |
| Unknown0x05 | 0x05 | desc |
| Vector4 | 0x06 | desc |
| String | 0x07 | desc |
| Actor | 0x08 | desc |
| UnknownString | 0x0f | desc |
| UnknownUnsignedInt | 0x11 | desc |
| String2 | 0x14 | desc |

## AAMP Checksum

Method for calculating a checksum to verify correct parsing:

1. Get file total size in bytes (`0x0c`)
2. Get total number of nodes (`0x18`, `0x1c` & `0x20`)
3. Get data and string buffer sizes (`0x24` & `0x28`)
4. Total the bytes
  * 52 bytes for the AAMP header
  * 12 bytes per root node
  * 8 bytes per child node
  
### Example

For example, `Lynel_Junior.bdrop`:

```
total file size:            1576 bytes
total number of nodes:      146
data buffer size:           32 bytes
string buffer size:         320 bytes

aamp header:                52 bytes
1 root node * 12 bytes:     12 bytes
145 nodes * 8 bytes:        1160 bytes
data buffer:                32 bytes
string buffer:              320 bytes

total size:                 1576 bytes
```