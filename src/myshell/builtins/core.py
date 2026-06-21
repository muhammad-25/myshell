from myshell.config import EXIT_MESSAGE
from myshell.context import ShellContext
from myshell.builtins.base import BuiltinCommand


def exit_command(context: ShellContext, args: list[str]) -> int:
    status = 0

    if args:
        try:
            status = int(args[0])
        except ValueError:
            context.error("myshell: exit: numeric argument required")
            status = 2

    context.write(EXIT_MESSAGE)
    context.request_exit(status)
    return status


def help_command(context: ShellContext, args: list[str]) -> int:
    context.write("Built-in minggu pertama:")
    context.write("  exit [status]  keluar dari shell")
    context.write("  help           tampilkan bantuan singkat")
    context.write("  history        tampilkan riwayat input")
    context.write("  tokens ...     tampilkan token dari argumen")
    context.write("")
    context.write("Perintah lain pada minggu pertama ditampilkan sebagai token.")
    return 0


def history_command(context: ShellContext, args: list[str]) -> int:
    for number, entry in context.history.list_entries():
        context.write(f"{number:>4}  {entry}")
    return 0


def tokens_command(context: ShellContext, args: list[str]) -> int:
    context.write(f"Token: {args!r}")
    return 0


CORE_BUILTINS = {
    "exit": BuiltinCommand(
        name="exit",
        description="Keluar dari shell.",
        handler=exit_command,
    ),
    "help": BuiltinCommand(
        name="help",
        description="Tampilkan bantuan singkat.",
        handler=help_command,
    ),
    "history": BuiltinCommand(
        name="history",
        description="Tampilkan riwayat input.",
        handler=history_command,
    ),
    "tokens": BuiltinCommand(
        name="tokens",
        description="Tampilkan token dari argumen yang diberikan.",
        handler=tokens_command,
    ),
}
