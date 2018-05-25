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
	unsigned int   version;
	unsigned int   unknown0x08;
	unsigned int   file_base_offset;
	float          world_scale;
	float          unknown0x14;
	unsigned int   material_info_array_length;
	unsigned int   area_array_length;
	unsigned int   unknown0x20;
	unsigned int   unknown0x24;
	float          tile_size;
	unsigned int   unknown0x2c;
};
```

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 4 | String       | TSCB file signature (magic) `54 53 43 42` or "TSCB" |
<<<<<<< HEAD
| `0x04` | 4 | Unsigned Short | TSCB version?. `0A 00 00 00` or "10.0.0.0"<sup>[1](#reference-1)</sup> |
| `0x08` | 4 | Unsigned Int | Unknown. `00 00 00 01` (Unsigned Int `1`) |
| `0x0c` | 4 | Unsigned Int | `file_base` table relative offset (0x0c + offset) |
| `0x10` | 4 | Float | `world_scale` `500.0` |
| `0x14` | 4 | Float | Terrain Mesh Altitude `800.0` |
=======
| `0x04` | 4 | Unsigned Short | TSCB version?. `0A 00 00 00` or "10.0.0.0"<sup>[1](#reference-1)</sup>. game crashes on load screen if not equal to `0A 00 00 00`. |
| `0x08` | 4 | Unsigned Int | Unknown. `00 00 00 01` (Unsigned Int `1`). game crashes on load screen if not equal to `00 00 00 01`. |
| `0x0c` | 4 | Unsigned Int | `file_base` table relative offset (0x0c + offset) |
| `0x10` | 4 | Float | `world_scale` `500.0`. Scales the world along the x- and z-axis. |
| `0x14` | 4 | Float | Terrain Mesh Altitude `800.0`. Moves the terrain along the y-axis (up-and-down). |
>>>>>>> 4f9546b6bb48e673a404399d9c2fe9fca2e6f4aa
| `0x18` | 4 | Unsigned Int | `material_info_array` length. Number of elements in array. |
| `0x1c` | 4 | Unsigned Int | `area_array` length. Number of elements in array. |
| `0x20` | 4 | Unknown | Unknown. `00 00 00 00` (Unsigned Int`0`). Most likely padding. |
| `0x24` | 4 | Unknown | Unknown. `00 00 00 00` (Unsigned Int`0`). Most likely padding. |
| `0x28` | 4 | Float | Tile size `32`. |
<<<<<<< HEAD
| `0x2c` | 4 | Unsigned Int | Unknown. `00 00 00 08` (Unsigned Int `8`) |

#### Parameters

##### TSCB Version

game crashes on load screen if not equal to `0A 00 00 00`.

##### Unknown `0x08`

game crashes on load screen if not equal to `00 00 00 01`.

##### Unknown `0x10`

Scales the world along the x- and z-axis

##### Terrain Mesh Altitude

Moves the terrain along the y-axis (up-and-down).

##### Unknown `0x2c`

`1`, `2`, `4`, `5`, `6`, `8` Affects textures. `0`, `3`, `7`, `15`, `16` will crash the game
=======
| `0x2c` | 4 | Unsigned Int | Unknown. `00 00 00 08` (Unsigned Int `8`). `1`, `2`, `4`, `5`, `6`, `8` Affects textures. `0`, `3`, `7`, `15`, `16` will crash the game |
>>>>>>> 4f9546b6bb48e673a404399d9c2fe9fca2e6f4aa

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
| `0x04` | 4 | Float | Texture u-axis (x-axis) |
| `0x08` | 4 | Float | Texture v-axis (y-axis) |
| `0x0c` | 4 | Float | Unknown |
| `0x10` | 4 | Float | Unknown |

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
| `0x08` | 4 | Float | unknown - Inverse height scale? (lower numbers give greater height). Also seems that this is affected by `world_scale` in the header |
| `0x0c` | 4 | Float | unknown - Affects grass density (0 is normal? higher numbers are more dense) |
| `0x10` | 4 | Float | unknown |
| `0x14` | 4 | Float | unknown |
| `0x18` | 4 | Float | unknown |
| `0x1c` | 4 | Unsigned Int | Unknown. Usually `0`, `1` or `2`, crashes on `4`, `16`. May be a flag for grass and water? `0` seems to indicate no water or grass.  |
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

It seems that water is [3, 1, 1] and grass is [3, 0, 1]

```
[20, `3, 0, 1`, 0, `3, 1, 1`] = grass, water
[20, `3, 1, 1`, 0, `3, 0, 1`] = water, grass
[`3, 1, 1`, 0]                = water
[`3, 0, 1`, 0]                = grass
```

## References
<a name="reference-1">1. U-King.elf:0x024D2F8C-0x024D300A holds two error messages: "【データロード】メジャーバージョンの不一致" ("[Data load] Major version mismatch") and "【データロード】マイナーバージョンの不一致" ("[Data Load] Minor version mismatch")
