import argparse
import datetime

import Lib


def main():
    parser = argparse.ArgumentParser("Activity number 3", description="A3 for TC2008b")
    subparsers = parser.add_subparsers(dest="cmd")
    subparser = subparsers.add_parser(
        "Sim", description="This command runs this simulation"
    )
    subparser.add_argument(
        "--Tmax",
        default=10,
        type=float,
        help="Max time in seconds for the agents to run (default=10s)",
    )
    subparser.set_defaults(func=Lib.Sim)

    subparser = subparsers.add_parser("Parameters", description="Generates the dataset")
    subparser.add_argument(
        "--Method",
        type=str,
        default="zig",
        help="Movement method: \nzigsag=zig\nrandom=ran\nspiral=spi",
    )
    subparser.add_argument(
        "--Columns",
        type=int,
        default=None,
        help="Columns of the matrix",
    )
    subparser.add_argument(
        "--Rows",
        type=int,
        default=None,
        help="Rows of the matrix",
    )
    subparser.add_argument(
        "--Agents",
        type=int,
        default=1,
        help="Agents you whant to add to your simulation",
    )
    subparser.add_argument(
        "--Persentil",
        type=float,
        default=0.5,
        help="Percentage of dirty cells to clean",
    )
    subparser.set_defaults(func=Lib.Parameters)
    Options = parser.parse_args()
    print(str(Options) + "\n")
    Options.func(Options)


if __name__ == "__main__":
    print(
        "\n"
        + "\033[0;32m"
        + "[start] "
        + str(datetime.datetime.now())
        + "\033[0m"
        + "\n"
    )
    main()
    print(
        "\n" + "\033[0;32m" + "[end] " + str(datetime.datetime.now()) + "\033[0m" + "\n"
    )
