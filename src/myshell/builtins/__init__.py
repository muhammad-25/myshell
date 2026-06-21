from myshell.builtins.base import BuiltinCommand
from myshell.builtins.core import CORE_BUILTINS


def load_builtins() -> dict[str, BuiltinCommand]:
    return dict(CORE_BUILTINS)
