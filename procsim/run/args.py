import argparse

def get_args():
    """Return an argparse Namespace containing program arguments."""
    DESCRIPTION = 'Superscalar out-of-order processor simulator.'

    parser = argparse.ArgumentParser(prog='procsim',
                                     description=DESCRIPTION)
    parser.add_argument('PROGRAM')
    parser.add_argument('--n-gpr-registers',
                        dest='n_gpr_registers',
                        type=int,
                        default=16,
                        help='Number of general purpose registers')
    parser.add_argument('--gpr-prefix',
                        dest='gpr_prefix',
                        default='r',
                        help='Prefix added to each GPR index')
    return parser.parse_args()
