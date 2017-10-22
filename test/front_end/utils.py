import locale
import os
import tempfile

def make_program_file(instructions):
    """Create a temporary program file from a list of Instructions.

    Note: The caller must delete the temporary file after use!

    Args:
        instructions: List of instructions to write to file.

    Returns:
        Path to temporary file.
    """
    (program, program_file) = tempfile.mkstemp()
    encoding = locale.getpreferredencoding(False)
    test_program_str = [str(i) for i in instructions]
    data = b'\n'.join([bytearray(ins_str, encoding)
                       for ins_str in test_program_str])
    os.write(program, data)
    os.close(program)
    return program_file

def instruction_list_equal(list1, list2):
    dict1 = [ins.__dict__ for ins in list1]
    dict2 = [ins.__dict__ for ins in list2]
    return dict1 == dict2
