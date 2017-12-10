from procsim.register_file import RegisterFile

MEMORY = None

REGISTER_FILE = RegisterFile(6, init_values={'r5': 1836311903})

def console_output():
    return 'pc: %2d r0: %10d' % (REGISTER_FILE['pc'], REGISTER_FILE['r0'])

PROGRAM = ['addi r0 r0 1',
           'addi r1 r1 1',
           'add r2 r0 r1',
           'addi r0 r1 0',
           'addi r1 r2 0',
           'blth r0 r5 2',
           'halt']
