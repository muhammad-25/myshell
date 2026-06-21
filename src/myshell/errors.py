class ShellError(Exception):
    """Base error untuk shell."""


class ParseError(ShellError):
    """Error saat input user tidak bisa ditokenisasi."""
