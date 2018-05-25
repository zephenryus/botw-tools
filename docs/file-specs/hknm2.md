# Contents

# HKNM2 File Specification

HKNM2 files are Havok NavMesh files.

## HKNM2 File Layout

## HKNM2 Header

### Header Layout

### Header Structure

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 8 | Bytes | HKNM2 file signature (magic) `57 E0 E0 57 10 C0 C0 10` |
| `0x08` | 4 | Integer | Unknown. Always `0`. Possibly User settable tags (http://forum.xentax.com/viewtopic.php?f=16&t=8667) |
| `0x0c` | 4 | Integer | Unknown. Always `11`. |
| `0x10` | 4 | Integer | Unknown. Always `67108865`. |
| `0x14` | 4 | Integer | Unknown. Always `3`. |
| `0x18` | 4 | Integer | Unknown. Always `2`. |
| `0x1c` | 4 | Integer | Unknown. Always `0`. Possibly padding. |
| `0x20` | 4 | Integer | Unknown. Always `0`. Possibly padding. |
| `0x24` | 4 | Integer | Unknown. Always `75`. |
| `0x28` | 16 | String | Havok SDK Version. `hk_2014.2.0-r1` for Breath of the Wild. |
| `0x38` | 4 | Integer | Unknown. Always `0`. |
| `0x3c` | 4 | Integer | Unknown. (`00 15 00 10` or `1376272`) |
| `0x40` | 4 | Integer | Unknown. (`00 14 00 00`) or `1310720` |
| `0x44` | 4 | Integer | Unknown. Possibly padding. |
| `0x48` | 4 | Integer | Unknown. Possibly padding. |
| `0x4c` | 4 | Integer | Unknown. Possibly padding. |

`-1` or signed integer `0xff` is often used as padding or end of section. 

### Segment Headers

The file header is followed by three segment headers that reference Havok classnames, types and data.

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 20 | String | Segment name (`__classnames__`, `__types__` or `__data__`) |
| `0x14`1 | 4 | Unsigned Integer | Absolute offset to segment start. |
| `0x18` | 4 | Unsigned Integer | Relative offset to section. |
| `0x1c` | 4 | Unsigned Integer | Relative offset to section. |
| `0x20` | 4 | Unsigned Integer | Relative offset to section. |
| `0x24` | 4 | Unsigned Integer | Relative offset to section. |
| `0x28` | 4 | Unsigned Integer | Relative offset to section. |
| `0x2c` | 4 | Unsigned Integer | Relative offset to section. |
| `0x30` | 16 | Bytes | Padding |

## Segments

### Class Names

The `__classnames__` segment is a list of Havok classes, presumably, used by the file.

### Types

Unused in Breath of the Wild.

### Data

The `__data__` segment contains the data used by Havok.