import argparse

from myshell.context import ShellContext
from myshell.shell import MiniShell


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="myshell",
        description="Custom shell Python progress minggu pertama.",
    )
    parser.add_argument(
        "-c",
        "--command",
        help="jalankan satu baris perintah lalu keluar",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    shell = MiniShell(context=ShellContext())

    if args.command is not None:
        return shell.execute_line(args.command)

    return shell.run()
