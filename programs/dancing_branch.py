import random

from procsim.register_file import RegisterFile
from procsim.memory import Memory

MEMORY = None

REGISTER_FILE = RegisterFile(4, init_values={'r0': 500,
                                             'r1': 0,
                                             'r2': 2,
                                             'r3': 3})

def console_output():
    return 'pc: %2d r1: %3d' % (REGISTER_FILE['pc'], REGISTER_FILE['r1'])

# r0 holds number of iterations
# r1 holds current iteration index
# r2 = 2
# r3 = 3
PROGRAM = ['blth r3 r2 0',  # 0  Not Taken
           'blth r2 r3 8',  # 1      Taken
           'blth r3 r2 0',  # 2  Not Taken
           'blth r2 r3 6',  # 3      Taken
           'blth r3 r2 0',  # 4  Not Taken
           'blth r2 r3 10', # 5      Taken
           'blth r3 r2 0',  # 6  Not Taken
           'blth r2 r3 4',  # 7      Taken
           'blth r3 r2 0',  # 8  Not Taken
           'blth r2 r3 2',  # 9      Taken
           'addi r1 r1 1',
           'blth r1 r0 0',
           'halt']
