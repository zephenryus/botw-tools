# Contents

# FSHA File Specification

FSHA files ?

## FSHA File Layout

## FSHA Header

### Header Layout

### Header Structure

```c
struct FSHAHeader {
    char            signature[4];
    unsigned byte   version[0];
    unsigned byte   version[1];
    unsigned byte   version[2];
    unsigned byte   version[3];
    unsigned short  byte_order_mark;
    unsigned short  unknown0x0a;
    unsigned int    file_size;
};
```

| Offset | Length | Type | Description |
|-------:|:------------:|------|-------------|
| `0x00` | 4 | String | FSHA file signature (magic) `46 53 48 41` or "FSHA" |
| `0x04` | 1 | Unsigned Byte | Version digit 1 (Major release), BotW is `4.5.0.4` |
| `0x05` | 1 | Unsigned Byte | Version digit 2 (Minor release) |
| `0x06` | 1 | Unsigned Byte | Version digit 3 (Minor release) |
| `0x07` | 1 | Unsigned Byte | Version digit 4 (Minor release) |
| `0x08` | 2 | Unsigned Short | Byte Order Mark (`FE FF` is Big-Endian, `FF FE` is Little-Endian |
| `0x0a` | 2 | Unsigned Short | Unknown |
| `0x0c` | 4 | Unsigned Int | File size in bytes |

## References

Special thanks to Mystixor!
