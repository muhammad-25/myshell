import os
from myshell.config import EXIT_MESSAGE
from myshell.context import ShellContext
from myshell.builtins.base import BuiltinCommand


def cd_command(context: ShellContext, args: list[str]) -> int:
    if not args:
        context.error("myshell: cd: missing argument")
        return 1

    path = args[0]
    try:
        os.chdir(path)
        return 0
    except FileNotFoundError:
        context.error(f"myshell: cd: {path}: No such file or directory")
        return 1
    except PermissionError:
        context.error(f"myshell: cd: {path}: Permission denied")
        return 1
    except Exception as exc:
        context.error(f"myshell: cd: {path}: {exc}")
        return 1


def pwd_command(context: ShellContext, args: list[str]) -> int:
    try:
        cwd = os.getcwd()
        context.write(cwd)
        return 0
    except Exception as exc:
        context.error(f"myshell: pwd: {exc}")
        return 1


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
    context.write("Built-in:")
    context.write("  cd <dir>       ubah direktori aktif")
    context.write("  exit [status]  keluar dari shell")
    context.write("  help           tampilkan bantuan singkat")
    context.write("  history        tampilkan riwayat input")
    context.write("  pwd            tampilkan direktori aktif saat ini")
    context.write("  tokens ...     tampilkan token dari argumen")
    context.write("")
    context.write("Perintah eksternal dijalankan secara langsung.")
    return 0


def history_command(context: ShellContext, args: list[str]) -> int:
    for number, entry in context.history.list_entries():
        context.write(f"{number:>4}  {entry}")
    return 0


def tokens_command(context: ShellContext, args: list[str]) -> int:
    context.write(f"Token: {args!r}")
    return 0


CORE_BUILTINS = {
    "cd": BuiltinCommand(
        name="cd",
        description="Ubah direktori aktif.",
        handler=cd_command,
    ),
    "pwd": BuiltinCommand(
        name="pwd",
        description="Tampilkan direktori aktif saat ini.",
        handler=pwd_command,
    ),
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

