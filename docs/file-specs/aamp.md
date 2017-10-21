# AAMP File Specification

Number values are read in **Little Endian** even though the PowerPC and most Wii U files use Big Endian

## AAMP Header

```
         0001 0203 0405 0607 0809 0a0b 0c0d 0e0f
00000000 4141 4D50 0200 0000 0300 0000 2806 0000
00000010 0000 0000 0400 0000 0100 0000 1000 0000
00000020 8100 0000 2000 0000 4001 0000 0000 0000
00000030 786D 6C00
```

| Address | Type | Size | Description |
|---|---|---|---|
| `0x00-0x03` | String | 4 bytes | AAMP file signature (magic) `41 41 4D 50` or "AAMP" |
| `0x04-0x07` | Unsigned Int | 4 bytes | AAMP version. Should be version 2 |
| `0x08-0x0b` | Unknown | 4 bytes | Unknown. Usually `03 00 00 00` (Unsigned Int `3`) |
| `0x0c-0x0f` | Unsigned Int | 4 bytes | File size in bytes |
| `0x10-0x13` | Unknown | 4 bytes | Unknown. Usually `00 00 00 00` (Unsigned Int `0`) |
| `0x14-0x17` | Unsigned Int | 4 bytes | File extension name length |
| `0x18-0x1b` | Unsigned Int | 4 bytes | Number of root nodes |
| `0x1c-0x1f` | Unsigned Int | 4 bytes | Number of child nodes on the root node |
| `0x20-0x23` | Unsigned Int | 4 bytes | Number of nodes excluding root nodes and root child nodes (direct descendants) |
| `0x24-0x27` | Unsigned Int | 4 bytes | Data buffer size in bytes |
| `0x28-0x2b` | Unsigned Int | 4 bytes | String buffer size in bytes |
| `0x2c-0x2f` | Unknown | 4 bytes | Unknown. Usually `00 00 00 00` (Unsigned Int `0`) |
| `0x30-0x33` | String | n bytes | A null-terminated string of the resulting file type. Usually `xml\0` The length is equal to value found in `0x14-0x17` (usually 4 bytes). |

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
00000000 XXXX XXXX XXXX XXXX
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