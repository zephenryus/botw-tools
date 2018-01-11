| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 2 | Unsigned Short | Height |
| `0x02` | 2 | Short | Unknown. |
| `0x04` | 2 | Short | Unknown. |
| `0x06` | 1 | Byte | Unknown. |
| `0x07` | 1 | Unsigned Byte | Water type (`0`-`7`) |

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