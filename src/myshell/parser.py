from dataclasses import dataclass
import shlex

from myshell.errors import ParseError


@dataclass(frozen=True)
class ParsedLine:
    raw: str
    tokens: list[str]

    @property
    def is_empty(self) -> bool:
        return len(self.tokens) == 0


def tokenize(line: str) -> list[str]:
    lexer = shlex.shlex(line, posix=True, punctuation_chars="|<>")
    lexer.whitespace_split = True
    lexer.commenters = ""

    try:
        return list(lexer)
    except ValueError as exc:
        raise ParseError(str(exc)) from exc


def parse_input(line: str) -> ParsedLine:
    return ParsedLine(raw=line, tokens=tokenize(line))
