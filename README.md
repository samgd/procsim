# procsim

## Usage

procsim programs are Python modules that have a `MEMORY`, `REGISTER_FILE`, and `PROGRAM` attribute. Examples can be found in the `programs/` directory.

To run a program, pass the module name to procsim:

```sh
python -m procsim programs.fib
```

and then press enter to step through each clock cycle.

## Instructions

| Operation            | Assembler       | Action                       | Execution Cycles |
|:--------------------:| --------------- | ---------------------------- |:----------------:|
| Add register         | add  rd r1 r2   | rd := r1 + r2                | 2                |
| Add immediate        | addi rd r1 imm  | rd := r1 + imm               | 2                |
| Subtract register    | sub  rd r1 r2   | rd := r1 - r2                | 2                |
| Subtract immediate   | subi rd r1 imm  | rd := r1 - imm               | 2                |
| Multiply register    | mul  rd r1 r2   | rd := r1 * r2                | 2                |
| Multiply immediate   | muli rd r1 imm  | rd := r1 * imm               | 2                |
| Load                 | ldr  rd r1      | rd := MEM[r1]                | 4                |
| Store                | str  rs r1      | MEM[r1] := rs                | 4                |
| Jump                 | j    imm        | pc := imm                    | 1                |
| Branch less than     | blth r1 r2 imm  | if (r1 < r2) pc := imm       | 2                |
| Halt                 | halt            | raise EndOfProgram exception | N/A              |
