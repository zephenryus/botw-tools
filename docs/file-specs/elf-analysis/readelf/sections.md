There are 37 section headers, starting at offset 0x34:

## Section Headers:

| [Nr] | Name | Type | Addr | Offset | Size | ES | Flg | Lk | Inf | Al |
|-----:|:-----|:-----|-----:|-------:|-----:|---:|----:|---:|----:|---:|
| [ 0] |                   | NULL      | 00000000 | 00000000 | 00000000 | 00 |     |  0 |   0 |  0 |
| [ 1] | .syscall          | PROGBITS  | 02000000 | 000005fc | 00000008 | 00 |  AX |  0 |   0 | 32 |
| [ 2] | .text             | PROGBITS  | 02000020 | 00000604 | 021f82c8 | 00 |  AX |  0 |   0 | 32 |
| [ 3] | .rodata           | PROGBITS  | 10000000 | 021f88cc | 00435c60 | 00 |  WA |  0 |   0 | 32 |
| [ 4] | .data             | PROGBITS  | 10435c60 | 0262e52c | 000218cc | 00 |  WA |  0 |   0 | 32 |
| [ 5] | .module_id        | PROGBITS  | 10457540 | 0264fdf8 | 000000e0 | 00 |  WA |  0 |   0 | 32 |
| [ 6] | .bss              | NOBITS    | 10457700 | 00000000 | 0014bfe1 | 00 |  WA |  0 |   0 | 256 |
| [ 7] | .thrbss           | NOBITS    | 105a3700 | 00000000 | 0000000c | 00 | WAo |  0 |   0 | 32 |
| [ 8] | .rela.text        | RELA      | 00000000 | 0264fed8 | 009b60ac | 0c |     | 32 |   2 |  4 |
| [ 9] | .rela.rodata      | RELA      | 00000000 | 03005f84 | 002faee8 | 0c |     | 32 |   3 |  4 |
| [10] | .rela.data        | RELA      | 00000000 | 03300e6c | 00010fa4 | 0c |     | 32 |   4 |  4 |
| [11] | .fimport_gx2      | LOUSER+2  | c0004580 | 03311e10 | 00000418 | 00 |  AX |  0 |   0 |  4 |
| [12] | .fimport_snd_core | LOUSER+2  | c00049c0 | 03312228 | 000001f0 | 00 |  AX |  0 |   0 |  4 |
| [13] | .fimport_snd_user | LOUSER+2  | c0004bc0 | 03312418 | 00000018 | 00 |  AX |  0 |   0 |  4 |
| [14] | .fimport_h264     | LOUSER+2  | c0004c00 | 03312430 | 00000070 | 00 |  AX |  0 |   0 |  4 |
| [15] | .fimport_nn_save  | LOUSER+2  | c0004c80 | 033124a0 | 00000050 | 00 |  AX |  0 |   0 |  4 |
| [16] | .fimport_vpad     | LOUSER+2  | c0004d00 | 033124f0 | 00000058 | 00 |  AX |  0 |   0 |  4 |
| [17] | .fimport_vpadbase | LOUSER+2  | c0004d80 | 03312548 | 00000018 | 00 |  AX |  0 |   0 |  4 |
| [18] | .fimport_proc_ui  | LOUSER+2  | c0004dc0 | 03312560 | 00000030 | 00 |  AX |  0 |   0 |  4 |
| [19] | .fimport_padscore | LOUSER+2  | c0004e00 | 03312590 | 00000068 | 00 |  AX |  0 |   0 |  4 |
| [20] | .fimport_coreinit | LOUSER+2  | c0004e80 | 033125f8 | 00000470 | 00 |  AX |  0 |   0 |  4 |
| [21] | .dimport_coreinit | LOUSER+2  | c0005300 | 03312a68 | 00000048 | 00 |   A |  0 |   0 |  4 |
| [22] | .fimport_sysapp   | LOUSER+2  | c0005380 | 03312ab0 | 00000028 | 00 |  AX |  0 |   0 |  4 |
| [23] | .fimport_zlib125  | LOUSER+2  | c00053c0 | 03312ad8 | 00000038 | 00 |  AX |  0 |   0 |  4 |
| [24] | .fimport_nn_act   | LOUSER+2  | c0005400 | 03312b10 | 00000020 | 00 |  AX |  0 |   0 |  4 |
| [25] | .dimport_nn_act   | LOUSER+2  | c0005440 | 03312b30 | 00000010 | 00 |   A |  0 |   0 |  4 |
| [26] | .fimport_nn_boss  | LOUSER+2  | c0005480 | 03312b40 | 00000090 | 00 |  AX |  0 |   0 |  4 |
| [27] | .dimport_nn_boss  | LOUSER+2  | c0005540 | 03312bd0 | 00000010 | 00 |   A |  0 |   0 |  4 |
| [28] | .fimport_nn_aoc   | LOUSER+2  | c0005580 | 03312be0 | 00000040 | 00 |  AX |  0 |   0 |  4 |
| [29] | .fimport_nn_nfp   | LOUSER+2  | c00055c0 | 03312c20 | 000000a0 | 00 |  AX |  0 |   0 |  4 |
| [30] | .fimport_nsysnet  | LOUSER+2  | c0005680 | 03312cc0 | 00000010 | 00 |  AX |  0 |   0 |  4 |
| [31] | .fimport_nn_ac    | LOUSER+2  | c00056c0 | 03312cd0 | 00000010 | 00 |  AX |  0 |   0 |  4 |
| [32] | .symtab           | SYMTAB    | c0000000 | 03312ce0 | 00001e40 | 10 |   A | 33 | 1097776  4 |
| [33] | .strtab           | STRTAB    | c0001e40 | 03314b20 | 00002549 | 00 |   A |  0 |   0 |  1 |
| [34] | .shstrtab         | STRTAB    | c0004389 | 03317069 | 000001cd | 00 |   A |  0 |   0 |  1 |
| [35] |                   | LOUSER+3  | 00000000 | 03317236 | 00000094 | 04 |     |  0 |   0 |  4 |
| [36] |                   | LOUSER+4  | 00000000 | 033172ca | 000000dd | 00 |     |  0 |   0 |  4 |
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings)
  I (info), L (link order), G (group), T (TLS), E (exclude), x (unknown)
  O (extra OS processing required) o (OS specific), p (processor specific)
