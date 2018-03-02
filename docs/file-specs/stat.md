### Header

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 4 | String       | STAT file signature (magic) `53 54 41 54` or "STAT" |
| `0x04` | 4 | Unsigned Int | Unknown. Usually `00 01 00 00`. Probably Version |
| `0x08` | 4 | Unsigned Int | Unknown (1) |
| `0x0c` | 4 | Unsigned Int | Unknown (40) |
| `0x10` | 4 | Float | X position on map of top-left of area |
| `0x14` | 4 | Float | Z position on map of top-left of area |
| `0x18` | 4 | Float | Height of of area `500.0` (could be width) |
| `0x1c` | 4 | Float | Width of of area `500.0` (could be height) |
| `0x20` | 4 | Unsigned Int | Unknown (100) |
| `0x24` | 4 | Unsigned Int | Unknown (100) |
| `0x28` | 4 | Unsigned Int | Unknown (0, 4, 6, 8, 10) |
| `0x2c` | 4 | Unsigned Int | Unknown (1, 2) |
| `0x30` | 4 | Unsigned Int | Unknown (8) |
| `0x34` | 4 | Unsigned Int | Relative offset to file type name |

```
1, 40, x, z, 500.0, 500.0, 100, 100,  0, 1, 8  10000   forest_density
1, 40, x, z, 500.0, 500.0, 100, 100,  0, 1, 8  10000   water_flow
1, 40, x, z, 500.0, 500.0, 100, 100,  0, 1, 8  10000   water_gradient
1, 40, x, z, 500.0, 500.0, 100, 100,  8, 1, 8  10000   forest_type
1, 40, x, z, 500.0, 500.0, 100, 100,  8, 1, 8  10000   rock_distribution
1, 40, x, z, 500.0, 500.0, 100, 100,  4, 1, 8  20000   water_depth
1, 40, x, z, 500.0, 500.0, 100, 100,  6, 1, 8  20000   route_distance
1, 40, x, z, 500.0, 500.0, 100, 100,  0, 2, 8  20000   water_distance
1, 40, x, z, 500.0, 500.0, 100, 100, 10, 1, 8  40000   terrain_embedded_edge
1, 40, x, z, 500.0, 500.0, 100, 100, 10, 1, 8  40000   autoplacement_forbid
1, 40, x, z, 500.0, 500.0, 100, 100, 10, 1, 8  40000   player_safety_restart
1, 40, x, z, 500.0, 500.0, 100, 100, 10, 1, 8  40000   terrain_hidden
1, 40, x, z, 500.0, 500.0, 100, 100, 10, 1, 8  40000   terrain_is_in_door
1, 40, x, z, 500.0, 500.0, 100, 100, 10, 2, 8  80000   material_map
```
