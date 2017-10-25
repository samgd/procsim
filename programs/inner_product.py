from procsim.register_file import RegisterFile
from procsim.memory import Memory

LEN_ARRAY = 10
MEMORY = Memory(LEN_ARRAY * 2)
# Initialize two arrays with values [0...LEN_ARRAY - 1]
for array_idx in range(2):
    for elem_idx in range(LEN_ARRAY):
        mem_idx = array_idx * LEN_ARRAY + elem_idx
        MEMORY[mem_idx] = elem_idx

REGISTER_FILE = RegisterFile(6)

# r0 holds len_array
# r1 holds relative elem_idxs ([0...LEN_ARRAY - 1])
# r2 holds absolute elem_idxs (relative + array_idx * LEN_ARRAY)
# r3 holds value loaded from array 1 and the multiplication results
# r4 holds value loaded from array 2
# r5 holds the running sum
PROGRAM = ['addi r0 r0 %d' % LEN_ARRAY,
           'ldr r3 r1',
           'add r2 r1 r0',
           'ldr r4 r2',
           'add r2 r2 r0',
           'mul r3 r3 r4',
           'add r5 r5 r3',
           'addi r1 r1 1',
           'addi r2 r1 0',
           'blth r1 r0 1']
