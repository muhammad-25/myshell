from dataclasses import dataclass
from typing import Callable

from myshell.context import ShellContext

BuiltinHandler = Callable[[ShellContext, list[str]], int]


@dataclass(frozen=True)
class BuiltinCommand:
    name: str
    description: str
    handler: BuiltinHandler
