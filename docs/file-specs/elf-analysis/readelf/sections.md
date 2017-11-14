## Section Headers:
There are 37 section headers, starting at offset 0x34:

| Nr | Name | Type | Address | Offset | Size | Entry Size | Flags | Link | Info | Address Align |
|---:|------|------|---------|--------|------|------------|------:|-----:|-----:|--------------:|
|  0 |                   | `NULL`     | `0x00000000` | `0x00000000` | `0x00000000` | `0x00` |       |  `0` |       `0` |   `0` |
|  1 | .syscall          | `PROGBITS` | `0x02000000` | `0x000005fc` | `0x00000008` | `0x00` |  `AX` |  `0` |       `0` |  `32` |
|  2 | .text             | `PROGBITS` | `0x02000020` | `0x00000604` | `0x021f82c8` | `0x00` |  `AX` |  `0` |       `0` |  `32` |
|  3 | .rodata           | `PROGBITS` | `0x10000000` | `0x021f88cc` | `0x00435c60` | `0x00` |  `WA` |  `0` |       `0` |  `32` |
|  4 | .data             | `PROGBITS` | `0x10435c60` | `0x0262e52c` | `0x000218cc` | `0x00` |  `WA` |  `0` |       `0` |  `32` |
|  5 | .module_id        | `PROGBITS` | `0x10457540` | `0x0264fdf8` | `0x000000e0` | `0x00` |  `WA` |  `0` |       `0` |  `32` |
|  6 | .bss              | `NOBITS`   | `0x10457700` | `0x00000000` | `0x0014bfe1` | `0x00` |  `WA` |  `0` |       `0` | `256` |
|  7 | .thrbss           | `NOBITS`   | `0x105a3700` | `0x00000000` | `0x0000000c` | `0x00` | `WAo` |  `0` |       `0` |  `32` |
|  8 | .rela.text        | `RELA`     | `0x00000000` | `0x0264fed8` | `0x009b60ac` | `0x0c` |       | `32` |       `2` |   `4` |
|  9 | .rela.rodata      | `RELA`     | `0x00000000` | `0x03005f84` | `0x002faee8` | `0x0c` |       | `32` |       `3` |   `4` |
| 10 | .rela.data        | `RELA`     | `0x00000000` | `0x03300e6c` | `0x00010fa4` | `0x0c` |       | `32` |       `4` |   `4` |
| 11 | .fimport_gx2      | `LOUSER+2` | `0xc0004580` | `0x03311e10` | `0x00000418` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 12 | .fimport_snd_core | `LOUSER+2` | `0xc00049c0` | `0x03312228` | `0x000001f0` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 13 | .fimport_snd_user | `LOUSER+2` | `0xc0004bc0` | `0x03312418` | `0x00000018` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 14 | .fimport_h264     | `LOUSER+2` | `0xc0004c00` | `0x03312430` | `0x00000070` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 15 | .fimport_nn_save  | `LOUSER+2` | `0xc0004c80` | `0x033124a0` | `0x00000050` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 16 | .fimport_vpad     | `LOUSER+2` | `0xc0004d00` | `0x033124f0` | `0x00000058` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 17 | .fimport_vpadbase | `LOUSER+2` | `0xc0004d80` | `0x03312548` | `0x00000018` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 18 | .fimport_proc_ui  | `LOUSER+2` | `0xc0004dc0` | `0x03312560` | `0x00000030` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 19 | .fimport_padscore | `LOUSER+2` | `0xc0004e00` | `0x03312590` | `0x00000068` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 20 | .fimport_coreinit | `LOUSER+2` | `0xc0004e80` | `0x033125f8` | `0x00000470` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 21 | .dimport_coreinit | `LOUSER+2` | `0xc0005300` | `0x03312a68` | `0x00000048` | `0x00` |   `A` |  `0` |       `0` |   `4` |
| 22 | .fimport_sysapp   | `LOUSER+2` | `0xc0005380` | `0x03312ab0` | `0x00000028` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 23 | .fimport_zlib125  | `LOUSER+2` | `0xc00053c0` | `0x03312ad8` | `0x00000038` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 24 | .fimport_nn_act   | `LOUSER+2` | `0xc0005400` | `0x03312b10` | `0x00000020` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 25 | .dimport_nn_act   | `LOUSER+2` | `0xc0005440` | `0x03312b30` | `0x00000010` | `0x00` |   `A` |  `0` |       `0` |   `4` |
| 26 | .fimport_nn_boss  | `LOUSER+2` | `0xc0005480` | `0x03312b40` | `0x00000090` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 27 | .dimport_nn_boss  | `LOUSER+2` | `0xc0005540` | `0x03312bd0` | `0x00000010` | `0x00` |   `A` |  `0` |       `0` |   `4` |
| 28 | .fimport_nn_aoc   | `LOUSER+2` | `0xc0005580` | `0x03312be0` | `0x00000040` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 29 | .fimport_nn_nfp   | `LOUSER+2` | `0xc00055c0` | `0x03312c20` | `0x000000a0` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 30 | .fimport_nsysnet  | `LOUSER+2` | `0xc0005680` | `0x03312cc0` | `0x00000010` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 31 | .fimport_nn_ac    | `LOUSER+2` | `0xc00056c0` | `0x03312cd0` | `0x00000010` | `0x00` |  `AX` |  `0` |       `0` |   `4` |
| 32 | .symtab           | `SYMTAB`   | `0xc0000000` | `0x03312ce0` | `0x00001e40` | `0x10` |   `A` | `33` | `1097776` |   `4` |
| 33 | .strtab           | `STRTAB`   | `0xc0001e40` | `0x03314b20` | `0x00002549` | `0x00` |   `A` |  `0` |       `0` |   `1` |
| 34 | .shstrtab         | `STRTAB`   | `0xc0004389` | `0x03317069` | `0x000001cd` | `0x00` |   `A` |  `0` |       `0` |   `1` |
| 35 |                   | `LOUSER+3` | `0x00000000` | `0x03317236` | `0x00000094` | `0x04` |       |  `0` |       `0` |   `4` |
| 36 |                   | `LOUSER+4` | `0x00000000` | `0x033172ca` | `0x000000dd` | `0x00` |       |  `0` |       `0` |   `4` |

### Key to Section Names

`.syscall`
~~[IOSU Syscalls](http://wiiubrew.org/wiki/IOSU_Syscalls)~~
~~[Cafe OS Syscalls](http://wiiubrew.org/wiki/Cafe_OS_Syscalls)~~
Need to figure out which library is actually being linked to.

`.text`
This section holds the "text," or executable instructions, of a program.

`.rodata`
These sections hold read-only data that typically contribute to a non-writable segment in the process image.

`.data`
These sections hold initialized data that contribute to the program's memory image.

`.module_id`

`.bss`
This section holds uninitialized data that contribute to the program's memory image. By definition, the system initializes the data with zeros when the program begins to run. The section occupies no file space, as indicated by the section type, SHT_NOBITS.

`.thrbss`

`.rela.text`
These sections hold relocation information, as described in "Relocation." If the file has a loadable segment that includes relocation, the sections' attributes will include the `SHF_ALLOC` bit; otherwise, that bit will be off. Conventionally, _name_ is supplied by the section to which the relocations apply. Thus a relocation section for `.text` normally would have the name `.rel.text` or `.rela.text`.

`.rela.rodata`
These sections hold relocation information, as described in ["Relocation."](https://refspecs.linuxfoundation.org/elf/gabi4+/ch4.reloc.html) If the file has a loadable segment that includes relocation, the sections' attributes will include the `SHF_ALLOC` bit; otherwise, that bit will be off. Conventionally, _name_ is supplied by the section to which the relocations apply. Thus a relocation section for `.text` normally would have the name `.rel.text` or `.rela.text`.

`.rela.data`
These sections hold relocation information, as described in "Relocation." If the file has a loadable segment that includes relocation, the sections' attributes will include the `SHF_ALLOC` bit; otherwise, that bit will be off. Conventionally, _name_ is supplied by the section to which the relocations apply. Thus a relocation section for `.text` normally would have the name `.rel.text` or `.rela.text`.

`.fimport_gx2`
Link to the Graphics library [`gx2.rpl`](http://wiiubrew.org/wiki/Gx2.rpl).

`.fimport_snd_core`
Link to the Sound-1 Core library `snd_core.rpl`.

`.fimport_snd_user`
Link to the Sound-1 User library `snd_user.rpl`.

`.fimport_h264`
Link to the H.264 library `h264.rpl`.

`.fimport_nn_save`
Link to the Nintendo Network Save File library `nn_save.rpl`.

`.fimport_vpad`
Link to the Gamepad Input library [`vpad.rpl`](http://wiiubrew.org/wiki/Vpad.rpl).

`.fimport_vpadbase`
Link to the Gamepad Base library [`vpadbase.rpl`](http://wiiubrew.org/wiki/Vpadbase.rpl).

`.fimport_proc_ui`
Link to library `proc_ui.rpl`.

`.fimport_padscore`
Link to the Wii Remote and Balance Board library [`padscore.rpl`](http://wiiubrew.org/wiki/Padscore.rpl).

`.fimport_coreinit`
Link to the Kernel, Memory and File System libraries [`coreinit.rpl`](http://wiiubrew.org/wiki/Coreinit.rpl).

`.dimport_coreinit`
Link to the Kernel, Memory and File System libraries [`coreinit.rpl`](http://wiiubrew.org/wiki/Coreinit.rpl).

`.fimport_sysapp`
Link to library `sysapp.rpl`.

`.fimport_zlib125`
Link to the zlib 1.2.5 Compression library [`zlib125.rpl`](https://github.com/madler/zlib/tree/9712272c78b9d9c93746d9c8e156a3728c65ca72).

`.fimport_nn_act`
Link to the Nintendo Network Accounts library [`nn_act.rpl`](http://wiiubrew.org/wiki/Nn_act.rpl).

`.dimport_nn_act`
Link to the Nintendo Network Accounts library [`nn_act.rpl`](http://wiiubrew.org/wiki/Nn_act.rpl).

`.fimport_nn_boss`
Link to the Nintendo Network BOSS (Streetpass) library `nn_boss.rpl`.

`.dimport_nn_boss`
Link to the Nintendo Network BOSS (Streetpass) library `nn_boss.rpl`.

`.fimport_nn_aoc`
Link to the Nintendo Network Add-On Content library `nn_aoc.rpl`.

`.fimport_nn_nfp`
Link to the Nintendo Network Nintendo Figurine Platform (Amiibo) library [`nn_nfp.rpl`](http://wiiubrew.org/wiki/Nn_nfp.rpl).

`.fimport_nsysnet`
Link to the BSD Sockets, Network Configuration and SSL library [`nsysnet.rpl`](http://wiiubrew.org/wiki/Nsysnet.rpl).

`.fimport_nn_ac`
Link to the Nintendo Network Auto Connection library [`nn_ac.rpl`](http://wiiubrew.org/wiki/Nn_ac.rpl).

`.symtab`
This section holds a symbol table, as ["Symbol Table"](https://refspecs.linuxfoundation.org/elf/gabi4+/ch4.symtab.html) in this chapter describes. If the file has a loadable segment that includes the symbol table, the section's attributes will include the `SHF_ALLOC` bit; otherwise, that bit will be off.

`.strtab`
This section holds strings, most commonly the strings that represent the names associated with symbol table entries. If the file has a loadable segment that includes the symbol string table, the section's attributes will include the `SHF_ALLOC` bit; otherwise, that bit will be off.

`.shstrtab`
This section holds section names.

### Key to Flags
  W (write), A (alloc), X (execute), M (merge), S (strings)
  I (info), L (link order), G (group), T (TLS), E (exclude), x (unknown)
  O (extra OS processing required) o (OS specific), p (processor specific)

### Resources
1. [ELF File Specification](https://refspecs.linuxfoundation.org/elf/gabi4+/ch4.eheader.html)
2. [Cafe OS](http://wiiubrew.org/wiki/Cafe_OS)