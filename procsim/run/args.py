import argparse

def get_args():
    """Return an argparse Namespace containing program arguments."""
    DESCRIPTION = 'Superscalar out-of-order processor simulator.'

    parser = argparse.ArgumentParser(prog='procsim',
                                     description=DESCRIPTION)
    parser.add_argument('PROGRAM')
    return parser.parse_args()
