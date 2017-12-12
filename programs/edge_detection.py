import numpy as np
import matplotlib.pyplot as plt

from procsim.memory import Memory
from procsim.register_file import RegisterFile

images = np.load('programs/images.npz')
david = images['david']
(dim_y, dim_x) = david.shape
n_pixels = dim_y * dim_x
image = david.flatten()

total = 2 + n_pixels * 4
MEMORY = Memory(total)

for i in range(total):
    MEMORY.memory[i] = 0

for i in range(n_pixels):
    MEMORY.memory[1 + i] = int(image[i])

REGISTER_FILE = RegisterFile(31)

def console_output():
    return 'pc: %2d r0: %r r1: %r r2: %r r3: %r r4: %r r5: %r r6: %r r7: %r r8: %r r17: %r r18: %r r19: %r r20: %r' % (
                REGISTER_FILE['pc'],
                REGISTER_FILE['r0'],
                REGISTER_FILE['r1'],
                REGISTER_FILE['r2'],
                REGISTER_FILE['r3'],
                REGISTER_FILE['r4'],
                REGISTER_FILE['r5'],
                REGISTER_FILE['r6'],
                REGISTER_FILE['r7'],
                REGISTER_FILE['r8'],
                REGISTER_FILE['r17'],
                REGISTER_FILE['r18'],
                REGISTER_FILE['r19'],
                REGISTER_FILE['r20'])

# r0 is zero
# r1 is dim_y
# r2 is dim_x
# r3 is n_pixels
# r4 is i
# r5 is j
# r6 is idx
# r7 is in_offset + idx
# r8 is pix
# r9 is first if check tmp
# r10 is first if pix
# r11 is second if check tmp
# r12 is second if pix
# r13 is new pix summation
# r14 is col in base offset
# r15 is col out base offset
# r16 is address of kernel
# r17 is out_offset constant
# r18 is tmp_offset constant
# r19 is tmp2_offset constant
# r20-22, scratch space if needed
# r23 is the current convolution stage idx (gaussian, sobel x, sobel y)
# r24 is 3, total num of conv stages
# r25 is row in base offset
# r26 is row out base offset

PROGRAM = [# Initialize constants.
           'addi r1 r0 %d' % dim_y,
           'addi r2 r0 %d' % dim_x,
           'addi r3 r0 %d' % n_pixels,
           'addi r24 r0 3',
           'add r17 r0 r3',
           'addi r17 r17 1', # out_offset
           'muli r20 r3 2',
           'add r18 r0 r20',
           'addi r18 r18 1', # tmp_offset
           'add r20 r20 r3',
           'addi r19 r20 1', # tmp2_offset                              #### 10
           # Initial offsets.
           'addi r14 r0 1',  # col_in_offset = 1
           'addi r15 r18 0', # col_out_offset = tmp_offset
           'addi r25 r18 0', # row_in_offset = tmp_offset
           'addi r26 r19 0', # row_out_offset = tmp2_offset
           # Column vec convolution.
               'addi r4 r0 0',  # i = 0
               # Outer loop start.
               'addi r5 r0 0',  # j = 0
               # Inner loop start
               'add r6 r4 r5',  # idx = i + j
               'add r7 r6 r14', # tmp_idx = in_offset + idx
               'ldr r8 r7',     # pix = memory[tmp_idx]
               # j_sub1
               'addi r10 r8 0',  # j_sub1 = pix                        #### 20
               'subi r20 r5 1',  # j - 1
               'blth r20 r0 25', # if j - 1 < 0, skip else
               'subi r21 r7 1',  # tmp_idx - 1
               'ldr r10 r21',    # memory[tmp_idx - 1]
               # j_add1
               'addi r22 r7 1',  # tmp_idx + 1
               'ldr r12 r22',    # memory[tmp_idx + 1]
               'addi r20 r5 2',  # j + 2
               'sub r21 r2 r20', # dim_x - (j + 1)
               'blth r0 r2 31',  # skip if 0 < dim_x - (j + 1)
               'addi r12 r8 0',  # j_add1 = pix                        #### 30
               # compute kernel
               'addi r20 r0 1',                                        #### 31
               'blth r23 r20 35', # < 1 so 0th iteration
               'addi r20 r0 2',
               'blth r23 r20 36', # < 2 so 1st iteration
               'j 83',
               'j 91',
               # set memory
               'add r20 r6 r15',  # tmp_offset + idx
               'str r10 r20',
               # increment counters
               'addi r5 r5 1',  # j += 1
               'blth r5 r2 17', # continue inner while loop
               'add r4 r4 r2',  # i += dim_x
               'blth r4 r3 16', # if i < n_pixels, cont                #### 42
           # Row vec convolution
               # Initial offsets
               'addi r5 r0 0',  # j = 0
               # Outer loop start.
               'addi r4 r0 0',  # i = 0                                #### 44
               # Inner loop start.
               'add r6 r4 r5',  # idx = i + j
               'add r7 r6 r25', # tmp_idx = in_offset + idx
               'ldr r8 r7',     # pix = memory[tmp_idx]
               # i_sub1
               'addi r10 r8 0',  # i_sub1 = pix
               'sub r20 r4 r2',  # i - dim_x
               'blth r20 r0 53', # continue if i - dim_x < 0
               'sub r20 r7 r2',  # tmp_idx - dim_x
               'ldr r10 r20',    # memory[tmp_idx - dim_x]
               # i_add1
               'add r20 r7 r2',  # tmp_idx + dim_x
               'ldr r12 r20',    # pix = memory[tmp_idx + dim_x]       #### 54
               'add r20 r4 r2',  # i + dim_x
               'blth r20 r3 58', # continue if i + dim_x < total
               'addi r12 r8 0',  # i_add1 = pix
               # compute kernel
               'addi r20 r0 1',                                        #### 58
               'blth r23 r20 63', # < 1 so 0th iteration
               'addi r20 r0 2',
               'blth r23 r20 63', # < 2 so 1st iteration
               'j 93',
               'j 87',
               # set memory
               'add r20 r26 r6',  # row_out_offset + idx
               'str r10 r20',
               # increment counters
               'add r4 r4 r2', # i += dim_x
               'blth r4 r3 45', # continue inner loop
               'addi r5 r5 1', # j += 1
               'blth r5 r2 44', # continue outer loop
           # incrememnt stage idx
           'addi r23 r23 1',                                           #### 70
           # change row/col offset base
           # set to stage 1 base
           'addi r14 r19 0', # col_in_offset  = tmp2_offset
           'addi r15 r17 0', # col_out_offset = out_offset
           'addi r25 r17 0', # row_in_offset  = out_offset
           'addi r26 r18 0', # row_out_offset = tmp_offset
           'addi r20 r0 2',                                            #### 75
           'blth r23 r20 81',
           # set to stage 2 base, skipped if stage 1
           'addi r14 r19 0', # col_in_offset  = tmp2_offset
           'addi r15 r17 0', # col_out_offset = out_offset
           'addi r25 r17 0', # row_in_offset  = out_offset
           'addi r26 r19 0', # row_out_offset = tmp2_offset            #### 80
           # another stage?
           'blth r23 r24 15',
           'j 95',
           # Kernels
               # Gaussian 1, Sobel Y 1
               'add r8 r8 r8',    # 2*pix                              #### 83
               'add r10 r10 r8',  # j_sub1 + 2*pix
               'add r10 r10 r12', # j_sub1 + 2*pix + j_add1
               'j 37',
                # Gaussian 2, Sobel X 2
               'add r8 r8 r8',    # 2*pix                              #### 87
               'add r10 r10 r8',  # i_sub1 + 2*pix
               'add r10 r10 r12', # i_add1 + 2*pix + i_add1
               'j 64',
               # Sobel X 1
               'sub r10 r12 r10',                                      #### 91
               'j 37',
               # Sobel Y 2
               'sub r10 r12 r10',                                      #### 93
               'j 64',
           # Sum square.
           'addi r4 r0 0',  # i = 0                                    #### 95
           # Outer loop start.
           'addi r5 r0 0',  # j = 0
           # Inner loop start
           'add r6 r4 r5',  # idx = i + j
           # Load sobel X, sobel Y
           'add r7 r6 r18', # tmp_offset + idx
           'ldr r20 r7',    # memory[tmp_offset + idx]
           'add r7 r6 r19', # tmp2_offset + idx
           'ldr r21 r7',    # memory[tmp2_offset + idx]
           'mul r20 r20 r20', # pix_x * pix_x
           'mul r21 r21 r21', # pix_y * pix_y
           'add r22 r20 r21', # pix_x^2 + pix_y^2
           'add r7 r6 r17',   # out_offset + idx
           'str r22 r7',      # memory[out_offset + idx] = pix_x^2 + pix_y^2
           # increment counters
           'addi r5 r5 1',  # j += 1
           'blth r5 r2 97', # continue inner while loop
           'add r4 r4 r2',  # i += dim_x
           'blth r4 r3 96', # if i < n_pixels, cont
           'halt'
          ]
