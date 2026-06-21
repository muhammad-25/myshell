import os
from myshell.config import PROMPT_TEXT
from myshell.context import ShellContext


def build_prompt(context: ShellContext) -> str:
    try:
        cwd = os.getcwd()
        return f"myshell:{cwd}> "
    except Exception:
        return PROMPT_TEXT

