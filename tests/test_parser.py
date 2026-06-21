import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from myshell.errors import ParseError
from myshell.parser import parse_input, tokenize


class ParserTest(unittest.TestCase):
    def test_empty_input_returns_no_tokens(self):
        self.assertEqual(tokenize("   "), [])

    def test_command_with_arguments(self):
        parsed = parse_input("cp file1.txt file2.txt")
        self.assertEqual(parsed.tokens, ["cp", "file1.txt", "file2.txt"])

    def test_quoted_argument_stays_one_token(self):
        parsed = parse_input('echo "halo dunia"')
        self.assertEqual(parsed.tokens, ["echo", "halo dunia"])

    def test_pipe_and_redirect_are_detected_as_tokens(self):
        parsed = parse_input("ls -la | grep .py > output.txt")
        self.assertEqual(
            parsed.tokens,
            ["ls", "-la", "|", "grep", ".py", ">", "output.txt"],
        )

    def test_unclosed_quote_raises_parse_error(self):
        with self.assertRaises(ParseError):
            tokenize('echo "belum selesai')


if __name__ == "__main__":
    unittest.main()
