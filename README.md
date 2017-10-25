# procsim

## Usage

procsim programs are Python modules that have a `MEMORY`, `REGISTER_FILE`, and `PROGRAM` attribute. Examples can be found in the `programs/` directory. 

To run a program, pass the module name to procsim:

```sh
python -m procsim program.fib
```

and then press enter to step through each clock cycle.

## Instructions

| Operation            | Assembler       | Action                 |
|:--------------------:| --------------- | ---------------------- |
| Add register         | add  rd r1 r2   | rd := r1 + r2          |
| Add immediate        | addi rd r1 imm  | rd := r1 + imm         |
| Subtract register    | sub  rd r1 r2   | rd := r1 - r2          |
| Subtract immediate   | subi rd r1 imm  | rd := r1 - imm         |
| Multiply register    | mul  rd r1 r2   | rd := r1 * r2          |
| Multiply immediate   | muli rd r1 imm  | rd := r1 * imm         |
| Load                 | ldr  rd r1      | rd := MEM[r1]          |
| Store                | str  rs r1      | MEM[r1] := rs          |
| Jump                 | j    imm        | pc := imm              |
| Branch less than     | blth r1 r2 imm  | if (r1 < r2) pc := imm |
