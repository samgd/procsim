import argparse

def get_args():
    """Return an argparse Namespace containing program arguments."""
    DESCRIPTION = 'Superscalar out-of-order processor simulator.'

    parser = argparse.ArgumentParser(prog='procsim',
                                     description=DESCRIPTION)
    parser.add_argument('PROGRAM')

    branch_predictors = parser.add_mutually_exclusive_group()
    branch_predictors.add_argument('--branch-history-table',
                                   nargs=2,
                                   default=[2**8, 2],
                                   type=int,
                                   dest='branch_history_table',
                                   metavar=('N_ENTRIES', 'N_PREDICTION_BITS'))
    branch_predictors.add_argument('--always-taken',
                                   action='store_true',
                                   dest='always_taken')
    branch_predictors.add_argument('--never-taken',
                                   action='store_true',
                                   dest='never_taken')
    branch_predictors.add_argument('--back-taken-forward-not',
                                   action='store_true',
                                   dest='back_taken_forward_not')

    parser.add_argument('--n-integer-units',
                        action='store',
                        default=4,
                        type=int,
                        dest='n_integer_units')

    parser.add_argument('--superscalar-width',
                        action='store',
                        default=4,
                        type=int,
                        dest='superscalar_width')

    parser.add_argument('--capacity',
                        action='store',
                        default=32,
                        type=int,
                        dest='capacity')

    parser.add_argument('--step-execution',
                        action='store_true',
                        dest='step_execution')

    parser.add_argument('--plot',
                        action='store_true',
                        dest='plot')

    return parser.parse_args()
