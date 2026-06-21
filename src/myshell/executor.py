from myshell.builtins import load_builtins
from myshell.builtins.base import BuiltinCommand
from myshell.context import ShellContext
from myshell.parser import ParsedLine


class WeekOneExecutor:
    """Executor sementara untuk progress minggu pertama.

    Minggu pertama belum menjalankan external command. Perintah selain
    built-in akan ditampilkan sebagai token agar hasil parser mudah diuji.
    """

    def __init__(self, builtins: dict[str, BuiltinCommand] | None = None) -> None:
        self.builtins = builtins or load_builtins()

    def execute(self, parsed: ParsedLine, context: ShellContext) -> int:
        if parsed.is_empty:
            context.last_status = 0
            return 0

        command = parsed.tokens[0]
        args = parsed.tokens[1:]

        builtin = self.builtins.get(command)
        if builtin is not None:
            status = builtin.handler(context, args)
        else:
            context.write(f"Token: {parsed.tokens!r}")
            status = 0

        context.last_status = status
        return status
