# Contents

# TSCB File Specification

TSCB files are **t**errain **sc**ene **b**inary files

## TSCB File Layout

## TSCB Header

### Header Layout

### Header Structure

```c
struct TSCBHeader {
	char           signature[4];
	unsigned short version;
	unsigned short unknown0x06;
	unsigned int   unknown0x08;
	unsigned int   file_base_offset;
	float          unknown0x10;
	float          unknown0x14;
	unsigned int   material_info_array_length;
	unsigned int   area_array_length;
	unsigned int   unknown0x20;
	unsigned int   unknown0x24;
	float          world_scale;
	unsigned int   unknown0x2c;
};
```

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 4 | String       | TSCB file signature (magic) `54 53 43 42` or "TSCB" |
| `0x04` | 2 | Unsigned Short | TSCB version?. `0A 00` or "10.0"<sup>[1](#reference-1)</sup> |
| `0x06` | 2 | Unsigned Short | Unknown. `00 00` (Unsigned Short `0`) |
| `0x08` | 4 | Unsigned Int | Unknown. `00 00 00 01` (Unsigned Int `1`) |
| `0x0c` | 4 | Unsigned Int | `file_base` table relative offset (0x0c + offset) |
| `0x10` | 4 | Float | Unknown `500.0`. See following notes. |
| `0x14` | 4 | Float | Unknown `800.0`. See following notes. |
| `0x18` | 4 | Unsigned Int | `material_info_array` length. Number of elements in array. |
| `0x1c` | 4 | Unsigned Int | `area_array` length. Number of elements in array. |
| `0x20` | 4 | Unknown | Unknown. `00 00 00 00` (Unsigned Int`0`) |
| `0x24` | 4 | Unknown | Unknown. `00 00 00 00` (Unsigned Int`0`) |
| `0x28` | 4 | Float | `world_scale`. Value used by `area_array` for tile size |
| `0x2c` | 4 | Unsigned Int | Unknown. `00 00 00 08` (Unsigned Int `8`) |

The float values in `0x10` and `0x14` seem to be related to the size of the playable map area. The in game playable map is `-5000.0` to `5000.0` along the z-axis and `-8000.0` to `8000.0` along the x-axis. While `500.0` and `800.0` do not exactly map to those values, they do seem to be related.

## Material Information Array

### Header

The material information header is one value, the section size. This includes the index table and the value table.

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 4 | Unsigned Int | Material info section size in bytes (0x30 + offset) |

### Material Information Array Lookup Table

Following the header is a table of relative offsets to each entry in `material_info_array`

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 4 | Unsigned Int | Relative offset to array entry |

### Material Information Value Table

Each entry in the array contains an index and four attributes

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 4 | Unsigned Int | Array index (`mat_index`) of `material_info_array` |
| `0x04` | 4 | Float | Unknown |
| `0x08` | 4 | Float | Unknown |
| `0x0c` | 4 | Float | Unknown |
| `0x10` | 4 | Float | Unknown |

* Unknown 0x04 values range between (0.03-0.59)
* Unknown 0x08 values range between (0.03-0.59)
* Unknown 0x0c values range between (0-1)
* Unknown 0x10 values range between (0.2-1.63)

## Area Array

### Area Array Lookup Table

Following the material information section is a table of relative offsets to each entry in `area_array`

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 4 | Unsigned Int | Relative offset to array entry |

### Area Array Value Table

Each entry contains meta data for one tile in the terrain scene. There are multiple levels of detail (LOD) for the terrain.

Entries range from 0x30 to 0x54 depending on the size of `extra_info_array`

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 4 | Float | X Position |
| `0x04` | 4 | Float | Z Position |
| `0x08` | 4 | Float | Scale? |
| `0x0c` | 4 | Float | `area_min_height_ground` |
| `0x10` | 4 | Float | `area_max_height_ground` |
| `0x14` | 4 | Float | `area_min_height_water` |
| `0x18` | 4 | Float | `area_max_height_water` |
| `0x1c` | 4 | Unsigned Int | Unknown. Usually `0`, `1` or `2` |
| `0x20` | 4 | Unsigned Int | `file_base`. Relative offset to file base name string |
| `0x24` | 4 | Unsigned Int | Unknown. Usually `0` |
| `0x28` | 4 | Unsigned Int | Unknown. Usually `0` |
| `0x2c` | 4 | Unsigned Int | `ref_extra`. It seems to be a flag to indicate if there is an attached `extra_info_array` |

### Extra Information Array

if `ref_extra` does not equal `0` there is an `extra_info_array` attached to this area. The array is 4 or 8 values long.

Every area includes a .hght and .mate file. The `extra_info_array` indicates if there is an additional .water.extm and / or .grass.extm file

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x30` | 4 | Unsigned Int | `extra_info_array` length Number of elements in array. |
| `0x34` | 4 | Unsigned Int | Unknown. Usually `20` or `3` |
| `0x38` | 4 | Unsigned Int | Unknown. Usually `0`, `1` or `3` |
| `0x3c` | 4 | Unsigned Int | Unknown. Usually `0` or `1` |
| `0x40` | 4 | Unsigned Int | Unknown. Usually `0` or `1` |
| `0x44` | 4 | Unsigned Int | Unknown. Always `0` |
| `0x48` | 4 | Unsigned Int | Unknown. Always `3` |
| `0x4c` | 4 | Unsigned Int | Unknown. Usually `0` or `1` |
| `0x50` | 4 | Unsigned Int | Unknown. Always `1` |

```
[20, 3, 0, 1, 0, 3, 1, 1] = water, grass
[20, 3, 1, 1, 0, 3, 0, 1] = water, grass
[ 3, 1, 1, 0]             = water
[ 3, 0, 1, 0]             = grass
```

## References
<a name="reference-1">1. U-King.elf:0x024D2F8C-0x024D300A holds two error messages: "【データロード】メジャーバージョンの不一致" ("[Data load] Major version mismatch") and "【データロード】マイナーバージョンの不一致" ("[Data Load] Minor version mismatch")
