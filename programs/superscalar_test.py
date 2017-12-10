import random

from procsim.register_file import RegisterFile
from procsim.memory import Memory

MEMORY = None

REGISTER_FILE = RegisterFile(15)

def console_output():
    return 'pc: %4d\t' % REGISTER_FILE['pc']

PROGRAM = ['addi r0 r0 1',
           'addi r1 r1 1',
           'addi r2 r2 1',
           'addi r3 r3 1',
           'addi r4 r4 1',
           'addi r5 r5 1',
           'addi r6 r6 1',
           'addi r7 r7 1',
           'addi r8 r8 1',
           'addi r9 r9 1',
           'addi r10 r10 1',
           'addi r11 r11 1',
           'addi r12 r12 1',
           'addi r13 r13 1',
           'addi r14 r14 1']
PROGRAM *= 500
PROGRAM.append('halt')
