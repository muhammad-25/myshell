from dataclasses import dataclass, field
import shlex

from myshell.errors import ParseError


@dataclass(frozen=True)
class CommandSpec:
    tokens: list[str]
    input_file: str | None = None
    output_file: str | None = None

    @property
    def is_empty(self) -> bool:
        return len(self.tokens) == 0


@dataclass(frozen=True)
class ParsedLine:
    raw: str
    tokens: list[str]
    commands: list[CommandSpec] = field(default_factory=list)
    is_pipeline: bool = False

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


def parse_command_tokens(tokens: list[str]) -> CommandSpec:
    """Memisahkan token argumen command dari operator redirection '<' dan '>'."""
    cmd_tokens = []
    input_file = None
    output_file = None

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == "<":
            if i + 1 >= len(tokens):
                raise ParseError("syntax error near unexpected token 'newline'")
            next_token = tokens[i + 1]
            if next_token in ("<", ">", "|"):
                raise ParseError(f"syntax error near unexpected token '{next_token}'")
            input_file = next_token
            i += 2
        elif token == ">":
            if i + 1 >= len(tokens):
                raise ParseError("syntax error near unexpected token 'newline'")
            next_token = tokens[i + 1]
            if next_token in ("<", ">", "|"):
                raise ParseError(f"syntax error near unexpected token '{next_token}'")
            output_file = next_token
            i += 2
        else:
            cmd_tokens.append(token)
            i += 1

    return CommandSpec(tokens=cmd_tokens, input_file=input_file, output_file=output_file)


def parse_input(line: str) -> ParsedLine:
    tokens = tokenize(line)
    if not tokens:
        return ParsedLine(raw=line, tokens=[], commands=[], is_pipeline=False)

    commands = []
    current_tokens = []
    is_pipeline = False

    for token in tokens:
        if token == "|":
            is_pipeline = True
            commands.append(parse_command_tokens(current_tokens))
            current_tokens = []
        else:
            current_tokens.append(token)
    commands.append(parse_command_tokens(current_tokens))

    # Validasi jika ada segment kosong pada pipeline
    if is_pipeline:
        for cmd in commands:
            if cmd.is_empty:
                raise ParseError("syntax error near unexpected token '|'")

    return ParsedLine(
        raw=line,
        tokens=tokens,
        commands=commands,
        is_pipeline=is_pipeline
    )

