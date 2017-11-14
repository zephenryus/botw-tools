There are 37 section headers, starting at offset 0x34:

## Section Headers:

| Nr | Name | Type | Addr | Offset | Size | ES | Flg | Lk | Inf | Al |
|-----:|:-----|:-----|-----:|-------:|-----:|---:|----:|---:|----:|---:|
|  0 |                   | `NULL`     | `0x00000000` | `0x00000000` | `0x00000000` | 00 |     |  0 |   0 |  0 |
|  1 | .syscall          | `PROGBITS` | `0x02000000` | `0x000005fc` | `0x00000008` | 00 |  AX |  0 |   0 | 32 |
|  2 | .text             | `PROGBITS` | `0x02000020` | `0x00000604` | `0x021f82c8` | 00 |  AX |  0 |   0 | 32 |
|  3 | .rodata           | `PROGBITS` | `0x10000000` | `0x021f88cc` | `0x00435c60` | 00 |  WA |  0 |   0 | 32 |
|  4 | .data             | `PROGBITS` | `0x10435c60` | `0x0262e52c` | `0x000218cc` | 00 |  WA |  0 |   0 | 32 |
|  5 | .module_id        | `PROGBITS` | `0x10457540` | `0x0264fdf8` | `0x000000e0` | 00 |  WA |  0 |   0 | 32 |
|  6 | .bss              | `NOBITS`   | `0x10457700` | `0x00000000` | `0x0014bfe1` | 00 |  WA |  0 |   0 | 256 |
|  7 | .thrbss           | `NOBITS`   | `0x105a3700` | `0x00000000` | `0x0000000c` | 00 | WAo |  0 |   0 | 32 |
|  8 | .rela.text        | `RELA`     | `0x00000000` | `0x0264fed8` | `0x009b60ac` | 0c |     | 32 |   2 |  4 |
|  9 | .rela.rodata      | `RELA`     | `0x00000000` | `0x03005f84` | `0x002faee8` | 0c |     | 32 |   3 |  4 |
| 10 | .rela.data        | `RELA`     | `0x00000000` | `0x03300e6c` | `0x00010fa4` | 0c |     | 32 |   4 |  4 |
| 11 | .fimport_gx2      | `LOUSER+2` | `0xc0004580` | `0x03311e10` | `0x00000418` | 00 |  AX |  0 |   0 |  4 |
| 12 | .fimport_snd_core | `LOUSER+2` | `0xc00049c0` | `0x03312228` | `0x000001f0` | 00 |  AX |  0 |   0 |  4 |
| 13 | .fimport_snd_user | `LOUSER+2` | `0xc0004bc0` | `0x03312418` | `0x00000018` | 00 |  AX |  0 |   0 |  4 |
| 14 | .fimport_h264     | `LOUSER+2` | `0xc0004c00` | `0x03312430` | `0x00000070` | 00 |  AX |  0 |   0 |  4 |
| 15 | .fimport_nn_save  | `LOUSER+2` | `0xc0004c80` | `0x033124a0` | `0x00000050` | 00 |  AX |  0 |   0 |  4 |
| 16 | .fimport_vpad     | `LOUSER+2` | `0xc0004d00` | `0x033124f0` | `0x00000058` | 00 |  AX |  0 |   0 |  4 |
| 17 | .fimport_vpadbase | `LOUSER+2` | `0xc0004d80` | `0x03312548` | `0x00000018` | 00 |  AX |  0 |   0 |  4 |
| 18 | .fimport_proc_ui  | `LOUSER+2` | `0xc0004dc0` | `0x03312560` | `0x00000030` | 00 |  AX |  0 |   0 |  4 |
| 19 | .fimport_padscore | `LOUSER+2` | `0xc0004e00` | `0x03312590` | `0x00000068` | 00 |  AX |  0 |   0 |  4 |
| 20 | .fimport_coreinit | `LOUSER+2` | `0xc0004e80` | `0x033125f8` | `0x00000470` | 00 |  AX |  0 |   0 |  4 |
| 21 | .dimport_coreinit | `LOUSER+2` | `0xc0005300` | `0x03312a68` | `0x00000048` | 00 |   A |  0 |   0 |  4 |
| 22 | .fimport_sysapp   | `LOUSER+2` | `0xc0005380` | `0x03312ab0` | `0x00000028` | 00 |  AX |  0 |   0 |  4 |
| 23 | .fimport_zlib125  | `LOUSER+2` | `0xc00053c0` | `0x03312ad8` | `0x00000038` | 00 |  AX |  0 |   0 |  4 |
| 24 | .fimport_nn_act   | `LOUSER+2` | `0xc0005400` | `0x03312b10` | `0x00000020` | 00 |  AX |  0 |   0 |  4 |
| 25 | .dimport_nn_act   | `LOUSER+2` | `0xc0005440` | `0x03312b30` | `0x00000010` | 00 |   A |  0 |   0 |  4 |
| 26 | .fimport_nn_boss  | `LOUSER+2` | `0xc0005480` | `0x03312b40` | `0x00000090` | 00 |  AX |  0 |   0 |  4 |
| 27 | .dimport_nn_boss  | `LOUSER+2` | `0xc0005540` | `0x03312bd0` | `0x00000010` | 00 |   A |  0 |   0 |  4 |
| 28 | .fimport_nn_aoc   | `LOUSER+2` | `0xc0005580` | `0x03312be0` | `0x00000040` | 00 |  AX |  0 |   0 |  4 |
| 29 | .fimport_nn_nfp   | `LOUSER+2` | `0xc00055c0` | `0x03312c20` | `0x000000a0` | 00 |  AX |  0 |   0 |  4 |
| 30 | .fimport_nsysnet  | `LOUSER+2` | `0xc0005680` | `0x03312cc0` | `0x00000010` | 00 |  AX |  0 |   0 |  4 |
| 31 | .fimport_nn_ac    | `LOUSER+2` | `0xc00056c0` | `0x03312cd0` | `0x00000010` | 00 |  AX |  0 |   0 |  4 |
| 32 | .symtab           | `SYMTAB`   | `0xc0000000` | `0x03312ce0` | `0x00001e40` | 10 |   A | 33 | 1097776  4 |
| 33 | .strtab           | `STRTAB`   | `0xc0001e40` | `0x03314b20` | `0x00002549` | 00 |   A |  0 |   0 |  1 |
| 34 | .shstrtab         | `STRTAB`   | `0xc0004389` | `0x03317069` | `0x000001cd` | 00 |   A |  0 |   0 |  1 |
| 35 |                   | `LOUSER+3` | `0x00000000` | `0x03317236` | `0x00000094` | 04 |     |  0 |   0 |  4 |
| 36 |                   | `LOUSER+4` | `0x00000000` | `0x033172ca` | `0x000000dd` | 00 |     |  0 |   0 |  4 |

Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings)
  I (info), L (link order), G (group), T (TLS), E (exclude), x (unknown)
  O (extra OS processing required) o (OS specific), p (processor specific)
