import random
import numpy as np
from copy import deepcopy

from procsim.memory import Memory
from procsim.register_file import RegisterFile
from procsim.unroll import unroll

LEN_ARRAY = 8634
MEMORY = Memory(LEN_ARRAY)
# Initialize array with weights and biases.
parameters = np.load('programs/mnist.npz')
weights = parameters['weights'].flatten(order='F').astype(int)
for i in range(7840):
    MEMORY[i] = int(weights[i])

biases = parameters['biases']
for i in range(10):
    MEMORY[i + 7840] = int(biases[i])

image = [0, 0, 0, 0, 0, 0, 0, 0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0,   0,   0,   0,  42, 118, 193, 105,   0,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0,   0,   0, 155, 242, 254, 254, 252, 229,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0,  46, 147, 254, 254, 254, 199, 187, 248,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0, 152, 254, 254, 235,  87,  17,   7,  60,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   5, 166, 254, 239,  68,   0,   0,   0,   0,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  4, 122, 254, 254,  62,   0,   0,   0,   0,   0,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 56, 254, 254, 187,   3,   0,   0,   0,   0,   0,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 56, 254, 241,   3,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 56, 254, 241,   0,   0,   0,  25,  91, 180, 228, 228,  97,  12,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 56, 254, 128,   0,  31, 119, 220, 254, 254, 254, 254, 254,  34,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 45, 239, 128,  26, 213, 254, 254, 245, 206, 206, 230, 254, 150, 11, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0, 173, 250, 212, 254, 245, 189,  72,   0,   0,  44, 246, 254, 55, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0, 169, 254, 254, 187,  71,   0,   0,   0,   0,   0, 242, 254, 55, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,  35, 254, 254,   6,   0,   0,   0,   0,   0,   0, 242, 254, 55, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,  21, 213, 254,   6,   0,   0,   0,   0,   0, 119, 254, 175,  3, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0, 108, 254,  51,   0,   0,   0,   0,   0, 125, 254,  52,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0,   3, 157, 231, 151,  63,  63,  78, 200, 227, 254,  34,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0,   0,  39, 233, 250, 254, 254, 254, 254, 254, 238,  28,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0,   0,   0,  52, 142, 254, 254, 254, 239,  96,  57,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0,   0,   0,   0,  42, 117, 142, 239,  50,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0, 0, 0, 0, 0, 0, 0]

for i in range(784):
    MEMORY[i + 7850] = int(image[i])

REGISTER_FILE = RegisterFile(15) # 15 GPR + 1 PC

def console_output():
    return 'pc: %2d\tComputing score for class (r1): %1d\tBest class (r3): %1d' % (REGISTER_FILE['pc'],
                                                                                   REGISTER_FILE['r3'],
                                                                                   REGISTER_FILE['r1'])

def reference_implementation():
    """Classify an MNIST image."""
    best_class = 0
    best_score = 0
    for class_idx in range(10):
        offset = class_idx * 784
        accum = 0
        for i in range(784):
            # image[i] * weights[offset + i]
            accum += MEMORY[i + 7850] * MEMORY[i + offset]
        # Add bias.
        accum += MEMORY[7840 + class_idx]
        # Keep track of the `best' class.
        if best_score < accum:
            best_class = class_idx
            best_score = accum
    print(best_class)

# r0 is zero
# r1 is best_class
# r2 is best_score
# r3 is class_idx
# r4 is offset
# r5 is accum
# r6 is i
# r7 is i + 7850, i + offset
# r8 is MEMORY[i + 7850]
# r9 is MEMORY[i + offset]
# r10 is offset

PROGRAM = ['addi r10 r0 784',
           # Compute weight offset.
           'mul r4 r3 r10',
           # Reset accum, i.
           'addi r5 r0 0',
           'addi r6 r0 0',
           # Dot product image, weights for this class.
           'addi r7 r6 7850',
           'ldr r8 r7',
           'add r7 r6 r4',
           'ldr r9 r7',
           'mul r8 r8 r9',
           'add r5 r5 r8',
           'addi r6 r6 1',
           'blth r6 r10 4',
           # Add bias.
           'addi r7 r3 7840',
           'ldr r8 r7',
           'add r5 r5 r8',
           # Keep track of the `best' class.
           'blth r5 r2 18',
           'addi r1 r3 0',
           'addi r2 r5 0',
           # Increment class_idx.
           'addi r3 r3 1',
           # Iterate again if not finished.
           'addi r8 r0 10',
           'blth r3 r8 1',
           'halt']

#PROGRAM = unroll(PROGRAM, deepcopy(REGISTER_FILE), deepcopy(MEMORY))
