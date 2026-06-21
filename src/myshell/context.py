from dataclasses import dataclass, field
import sys
from typing import TextIO

from myshell.config import APP_NAME
from myshell.history import History


@dataclass
class ShellContext:
    name: str = APP_NAME
    stdin: TextIO = field(default_factory=lambda: sys.stdin)
    stdout: TextIO = field(default_factory=lambda: sys.stdout)
    stderr: TextIO = field(default_factory=lambda: sys.stderr)
    running: bool = True
    last_status: int = 0
    history: History = field(default_factory=History)

    def request_exit(self, status: int = 0) -> None:
        self.running = False
        self.last_status = status

    def write(self, message: str = "") -> None:
        print(message, file=self.stdout)

    def error(self, message: str) -> None:
        print(message, file=self.stderr)
