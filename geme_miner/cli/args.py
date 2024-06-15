import sys
import os.path
import platform
from argparse import ArgumentParser, ArgumentTypeError, SUPPRESS
from pathvalidate import sanitize_filepath, validate_filepath, ValidationError
from geme_miner.core.normalize import FormatTypeEnum
from geme_miner.core.third_party.stores import StorefrontEnum
from geme_miner.__version__ import __version__, __copyright__, __license__

try:
    from rich_argparse import RawTextRichHelpFormatter as FormatterClass
except ImportError:
    from argparse import RawTextHelpFormatter as FormatterClass


def _arg_filepath_type(path: str) -> str:
    plat = platform.system()
    if plat not in ["Windows", "Linux"]:
        plat = "universal"

    try:
        path = sanitize_filepath(path, platform=plat)
        validate_filepath(path, platform=plat)

        path = os.path.abspath(path)
        validate_filepath(path, platform=plat)
    except ValidationError as e:
        raise ArgumentTypeError(e)

    if os.path.isdir(path):
        raise ArgumentTypeError(f"{path} is an existing directory, not a file")

    return path


def _arg_output_type(output: str) -> str:
    output = str(output).strip()

    if output == "":
        return "stdout"
    if output.lower() in ["stdout", "stderr"]:
        return output.lower()

    output = _arg_filepath_type(output)

    return output


# fmt: off
def parse(args = None):
    prog = os.path.basename(sys.argv[0])
    # check if prog contains any of these words
    if not any(t in prog.lower() for t in ["geme_miner", "gememiner", "gm"]):
        prog = "GemeMiner"
    
    parser = ArgumentParser(
        prog=prog,
        description=
            f" {__copyright__}\n"
            f" {__license__}\n",
        formatter_class=FormatterClass
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "-c", "--config_path",
        help="TODO: The path to the config file (default: %(default)s)",
        default="./config.jsonc",
        type=_arg_filepath_type,
    )

    parser.add_argument(
        "-s", "--stores",
        help="Stores to get data from (default: %(default)s)",
        default=[StorefrontEnum.RECOMMENDED.name.lower()],
        choices=[t.name.lower() for t in StorefrontEnum],
        type=str.lower,
        nargs="+",
    )
    parser.add_argument(
        "--no_stores",
        help="Don't get data from Stores",
        action="store_true",
    )
    parser.add_argument(
        "--no_reddit",
        help="Don't get data from some Subreddits",
        action="store_true",
    )

    parser.add_argument(
        "-f", "--format",
        help="Output format (default: %(default)s)",
        default=FormatTypeEnum.JSON_PRETTY.name.lower(),
        choices=[t.name.lower() for t in FormatTypeEnum],
        type=str.lower,
    )
    parser.add_argument(
        "-o", "--output",
        help="TODO: Where to output the data (default: %(default)s)",
        default="stdout",
        metavar="{stdout,stderr,{FILE_PATH}}",
        type=_arg_output_type,
    )
    parser.add_argument(
        "--force",
        help="Force overwriting an existing file. Will be applied to --output",
        action="store_true",
    )

    parser.add_argument(
        "-l", "--log_output",
        help="TODO: Where to output the data (default: %(default)s)",
        default="stdout",
        metavar="{stdout,stderr,{FILE_PATH}}",
        type=_arg_output_type,
    )
    parser.add_argument(
        "-v", "--verbose",
        help="TODO: Verbosity level",
        default=0,
        action="count",
    )

    parser.add_argument(
        "--test_links",
        help="TODO: Test links by requesting thier Headers",
        action="store_true",
    )

    parser.add_argument(
        "--__debug",
        help=SUPPRESS,
        action="store_true",
    )

    return parser.parse_args(args)
# fmt: on
