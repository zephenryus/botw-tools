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
| `0x14` | 4 | Unsigned Integer | Absolute offset to segment start. |
| `0x18` | 4 | Unsigned Integer | Relative offset to section. |
| `0x1c` | 4 | Unsigned Integer | Relative offset to section. |
| `0x20` | 4 | Unsigned Integer | Relative offset to section. |
| `0x24` | 4 | Unsigned Integer | Relative offset to section. |
| `0x28` | 4 | Unsigned Integer | Relative offset to section. |
| `0x2c` | 4 | Unsigned Integer | Relative offset to section. |
| `0x30` | 16 | Bytes | Padding |

## Segments

### Class Names

The `__classnames__` segment is a list of Havok classes, presumably, used by the file. HKNM2 files include the following classes:

- `hkClass`
  - `hkClassMember`
    - `hkClassEnum`
      - `hkClassEnumItem`
        - `hkRootLevelContainer`
          - `hkaiNavMesh`
          - `hkaiDirectedGraphExplicitCost`
          - `hkaiStaticTreeNavMeshQueryMediator`
            - `hkcdStaticAabbTree`
            - `hkcdStaticTreeDefaultTreeStorage6`

### Types

Unused in Breath of the Wild.

### Data

The `__data__` segment contains the data used by Havok to define [NavMeshes](https://www.youtube.com/watch?v=rlbjGiP104M). The segment header divides the data segment into four sections.

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 20 | String | `__data__` |
| `0x14` | 4 | Unsigned Integer | `data_segment_offset` Absolute offset to `Data`. Always `528` (`0x210`) Except in `0-16.hknm2`, `0-17.hknm2` and `0-18.hknm2` |
| `0x18` | 4 | Unsigned Integer | Relative offset to `DataSection[0]` from `data_segment_offset` |
| `0x1c` | 4 | Unsigned Integer | Relative offset to `DataSection[1]` from `data_segment_offset` |
| `0x20` | 4 | Unsigned Integer | Relative offset to `DataSection[2]` from `data_segment_offset` |
| `0x24` | 4 | Unsigned Integer | End of `data_segment_offset` |
| `0x28` | 4 | Unsigned Integer | Duplicate of end of `data_segment_offset` |
| `0x2c` | 4 | Unsigned Integer | Duplicate of end of `data_segment_offset` |
| `0x30` | 16 | Bytes | Padding |

- **`Data`**—The raw data (at segment's absolute offset)
- **`DataSection[0]`**—Offset table for `Data`
- **`DataSection[1]`**—An unknown table that is related to `DataSection[0]`
- **`DataSection[2]`**—An unknown table that is related to `DataSection[1]`

#### `DataSection[0]`

#### `DataSection[1]`

#### `DataSection[2]`

#### `Data`

The data table is filled with multiple data objects.

#### array[0]

Typing table?

#### array[1]

NavMesh Faces

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 4 | Int | Starting edge index |
| `0x04` | 4 | Int | User defined edge index. `-1` (`FF` or `HKAI_INVALID_PACKED_KEY`) |
| `0x08` | 2 | Short | Number of edges. |
| `0x0a` | 2 | Short | User defined number of edges. |
| `0x0c` | 2 | Short | Cluster index |
| `0x0e` | 2 | Short | Always `CD CD`. Padding. |

NavMesh Edges

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 4 | Int | Starting vertex index |
| `0x04` | 4 | Int | Ending vertex index |
| `0x08` | 4 | Int | Opposite edge index. `-1` (`FF` or `HKAI_INVALID_PACKED_KEY`) implies this edge is a boundary edge |
| `0x0c` | 4 | Int | Opposite face index. `-1` (`FF` or `HKAI_INVALID_PACKED_KEY`) implies this edge is a boundary edge |
| `0x10` | 1 | Unsigned Byte | Flags. BotW seems to always be `b00000100`. `4` = `EDGE_ORIGINAL` or the edge is on original cell boundary. |
| `0x11` | 1 | Byte | Padding |
| `0x12` | 2 | Short | Edge cost.  |

NavMesh Vertices

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 4 | Float | x |
| `0x04` | 4 | Float | y |
| `0x08` | 4 | Float | z |
| `0x0c` | 4 | Float | w |

#### array[2]

NavMesh Vertex