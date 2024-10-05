# AX10
A simple emulator for a virtual cpu
## About the cpu
The emulator is for a virtual cpu I called AX10 the name stands for A - Allix some old project of me, which I never ended up finishing, X - for emulator and the 10 because I wanted the cpu to have 10 registers. The emulator is probably not 100% accurat about how a real cpu works but I try my best to improve it and learn to make it better and more accourat.
## Current version
At the moment the first simple Instructions of the cpu are implemented, and I added a rust version to the original python version, and only the rust version will recive further updates the python one is more of a concept plan of this project. 
## Upcomming Versions
I plan to implement in the next versions a first bios with the options to get input, display text and save to disk.
Furthermore I plan for this bios to have the ability to display a graphics.
## Hardware
As soon as I think the emualtor is on a good point for it, I will try to write an emulator for a esp8266 to acctualy function like this cpu and build a board for vga out, keyboard in and a sd card for saving. Furthermore I plan to acctually build a functioning chip with the ability to use the same code as this emulator but this will be not in near future.
## Assembler
At the current time I havent wrote an assembler for this cpu, so if you want to code your own demo for this you will need to write it in binary.
## Binary
The commands
### Emulator Shutdown
```AX10-bin
0x0
```
### Move into register
```AX10-bin
0x1 registernum typ content
```
### add to register
```AX10-bin
0x2 registernum typ content
```
### sub from register
```AX10-bin
0x3 registernum typ content
```
### div from register
```AX10-bin
0x4 registernum typ content
```
### Mul in register
```AX10-bin
0x5 registernum typ content
```
### jmp to memory address
```AX10-bin
0x6 bit_to_jump_to
```
### wait time
```AX10-bin
0x7 time
```
### write to ram
```AX10-bin
0x8 ramaddress typ content
```
### compare bytes
```AX10-bin
0x9 register typ content
```
### Jump if equal
Looks if rh is 1 or not if 1 same as jmp
### Jump if not equal
Looks if rh is 0 or not if 0 same as jmp