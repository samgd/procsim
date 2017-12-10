import random

from procsim.register_file import RegisterFile
from procsim.memory import Memory

LEN_ARRAY = 15
MEMORY = Memory(LEN_ARRAY)
for i in range(LEN_ARRAY):
    MEMORY[i] = LEN_ARRAY - i

REGISTER_FILE = RegisterFile(6)

def console_output():
    return 'pc: %d memory: %r' % (REGISTER_FILE['pc'], MEMORY.memory)

# r0 is zero
# r1 holds len_array - 1
# r2 holds swap flag
# r3 holds inner idx
# r4 holds arr[i]
# r5 holds arr[i + 1]
PROGRAM = ['addi r1 r1 %d' % (LEN_ARRAY - 1),
           # Reset swap flag, inner idx.
           'addi r2 r0 0',
           'addi r3 r0 0',
           # Load next pair.
           'ldr r4 r3',
           'addi r3 r3 1',
           'ldr r5 r3',
           # Swap?
           'blth r5 r4 10',
           # More iterations of inner loop?
           'blth r3 r1 3',
           # More iterations of outer loop?
           'blth r0 r2 1',
           'j 16',
           # Swap code:
           'addi r2 r2 1',
           'str r4 r3',
           'subi r3 r3 1',
           'str r5 r3',
           'addi r3 r3 1',
           'j 7',
           'halt']
