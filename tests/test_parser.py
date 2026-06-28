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

    def test_parse_redirection_input_and_output(self):
        parsed = parse_input("sort < data.txt > hasil.txt")
        self.assertEqual(len(parsed.commands), 1)
        cmd = parsed.commands[0]
        self.assertEqual(cmd.tokens, ["sort"])
        self.assertEqual(cmd.input_file, "data.txt")
        self.assertEqual(cmd.output_file, "hasil.txt")

    def test_parse_pipeline_with_redirection(self):
        parsed = parse_input("cat < input.txt | grep hello > output.txt")
        self.assertTrue(parsed.is_pipeline)
        self.assertEqual(len(parsed.commands), 2)
        
        cmd1 = parsed.commands[0]
        self.assertEqual(cmd1.tokens, ["cat"])
        self.assertEqual(cmd1.input_file, "input.txt")
        self.assertIsNone(cmd1.output_file)

        cmd2 = parsed.commands[1]
        self.assertEqual(cmd2.tokens, ["grep", "hello"])
        self.assertIsNone(cmd2.input_file)
        self.assertEqual(cmd2.output_file, "output.txt")

    def test_parse_invalid_redirection_raises_error(self):
        with self.assertRaises(ParseError):
            parse_input("ls >")
        with self.assertRaises(ParseError):
            parse_input("ls < > file.txt")
        with self.assertRaises(ParseError):
            parse_input("ls | | grep txt")


if __name__ == "__main__":
    unittest.main()
