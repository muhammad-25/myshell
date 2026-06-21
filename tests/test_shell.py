import io
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from myshell.context import ShellContext
from myshell.shell import MiniShell


class ShellTest(unittest.TestCase):
    def make_shell(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        context = ShellContext(stdout=stdout, stderr=stderr)
        return MiniShell(context=context), stdout, stderr

    def test_empty_input_does_not_crash(self):
        shell, stdout, stderr = self.make_shell()
        status = shell.execute_line("   ")

        self.assertEqual(status, 0)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")

    def test_unknown_command_prints_tokens_for_week_one(self):
        shell, stdout, stderr = self.make_shell()
        status = shell.execute_line("ls -la")

        self.assertEqual(status, 0)
        self.assertIn("Token: ['ls', '-la']", stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")

    def test_exit_builtin_stops_shell(self):
        shell, stdout, stderr = self.make_shell()
        status = shell.execute_line("exit")

        self.assertEqual(status, 0)
        self.assertFalse(shell.context.running)
        self.assertIn("Sampai jumpa!", stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")

    def test_parse_error_is_reported(self):
        shell, stdout, stderr = self.make_shell()
        status = shell.execute_line('echo "kurang kutip')

        self.assertEqual(status, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("myshell: parse error:", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
