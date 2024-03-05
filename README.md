## Simplified Instructional Computer Two Pass Assembler
### Two Version
* SIC
* SIC/XE

### Memory
A word = 3 bytes = 24 bits, byte addresses.

### Register
* **A** : Accumulator
* **X** : Index Register
* **L** : Linkage Register
* **PC** : Program Counter
* **SW** : Status Word

### Addressing modes
* Direct : TA = address
* Indexed : TA = address + (X)

### Instruction set
　Load and store registers : 
> LDA, LDX, STA, STX

　Integer arithmetic operations : 
> ADD, SUB, MUL, DIV  
> ADD M  (A <- A+ (M))

　Comparison :
> COMP

　Conditional jump instructions :
> JLT, JEQ, JGT

　Subroutine linkage :
> JSUB, RSUB
