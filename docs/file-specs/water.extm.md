| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 2 | Unsigned Short | Height |
| `0x02` | 1 | Unsigned Byte | Unknown (`0`-`255`) |
| `0x03` | 1 | Unsigned Byte | Unknown (`15`-`255` in 5000000000.water.extm) |
| `0x04` | 1 | Unsigned Byte | Unknown (`0`-`255`) |
| `0x05` | 1 | Unsigned Byte | Unknown (`15`-`140` in 5000000000.water.extm) |
| `0x06` | 1 | Unsigned Byte | Unknown<sup>*</sup> (`3`-`10`) |
| `0x07` | 1 | Unsigned Byte | Water type (`0`-`7`) |

<sup>*</sup> This value is usually the water type `+` `3`. It most likely references a table entry.

```
[
	Water,
	HotWater,
	Poison,
	Lava,
	IceWater,
	Mud,
	Clear01,
	Sea
]

[
	Water,
	Water,
	Water,
	Lava,
	Water,
	Bog,
	Water,
	Water
]

[
	Water,
	Water_Hot,
	Water_Poison,
	Lava,
	Water_Ice,
	Bog,
	Water,
	Water
]
```