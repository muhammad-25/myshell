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

    def test_cd_command_changes_directory(self):
        import os
        shell, stdout, stderr = self.make_shell()
        original_dir = os.getcwd()
        
        try:
            # Pindah ke subdirektori tests
            status = shell.execute_line("cd tests")
            self.assertEqual(status, 0)
            self.assertTrue(os.getcwd().endswith("tests"))
            
            # Cek pwd menampilkan direktori baru
            status = shell.execute_line("pwd")
            self.assertEqual(status, 0)
            self.assertIn("tests", stdout.getvalue())
        finally:
            os.chdir(original_dir)

    def test_cd_command_missing_arg_reports_error(self):
        shell, stdout, stderr = self.make_shell()
        status = shell.execute_line("cd")
        self.assertEqual(status, 1)
        self.assertIn("myshell: cd: missing argument", stderr.getvalue())

    def test_cd_command_invalid_dir_reports_error(self):
        shell, stdout, stderr = self.make_shell()
        status = shell.execute_line("cd non_existent_directory_xyz")
        self.assertEqual(status, 1)
        self.assertIn("myshell: cd: non_existent_directory_xyz: No such file or directory", stderr.getvalue())

    def test_pwd_command_prints_current_directory(self):
        import os
        shell, stdout, stderr = self.make_shell()
        status = shell.execute_line("pwd")
        self.assertEqual(status, 0)
        self.assertIn(os.getcwd(), stdout.getvalue())

    def test_external_command_execution(self):
        shell, stdout, stderr = self.make_shell()
        # Di Windows atau Unix, echo hello biasanya disupport
        status = shell.execute_line("echo hello_external")
        self.assertEqual(status, 0)
        # Pada fallback Windows (subprocess) kita capture stdout ke context.stdout
        # Pada Unix (fork) kita tidak menjamin StringIO bisa mengcapture output eksternal secara langsung
        # tapi minimal command berjalan sukses.
        self.assertEqual(status, 0)

    def test_external_command_not_found(self):
        shell, stdout, stderr = self.make_shell()
        status = shell.execute_line("invalidcommandabc123")
        self.assertEqual(status, 127)
        self.assertIn("command not found", stderr.getvalue())

    def test_fork_exec_error_handling_mocked(self):
        from unittest.mock import patch
        import os
        shell, stdout, stderr = self.make_shell()

        # Mock os.fork untuk mensimulasikan kegagalan fork
        if hasattr(os, "fork"):
            with patch("os.fork", side_effect=OSError("Fork failed")):
                status = shell.execute_line("ls")
                self.assertEqual(status, 1)
                self.assertIn("myshell: fork failed:", stderr.getvalue())


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

    def test_output_redirection(self):
        import os
        shell, stdout, stderr = self.make_shell()
        output_file = "test_output.txt"
        if os.path.exists(output_file):
            os.remove(output_file)
            
        try:
            status = shell.execute_line(f"echo test_redirection > {output_file}")
            self.assertEqual(status, 0)
            self.assertTrue(os.path.exists(output_file))
            with open(output_file, "r") as f:
                content = f.read().strip()
            self.assertEqual(content, "test_redirection")
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

    def test_input_redirection(self):
        import os
        shell, stdout, stderr = self.make_shell()
        input_file = "test_input.txt"
        with open(input_file, "w") as f:
            f.write("line3\nline1\nline2\n")
            
        try:
            output_file = "test_sorted.txt"
            if os.path.exists(output_file):
                os.remove(output_file)
            status = shell.execute_line(f"sort < {input_file} > {output_file}")
            self.assertEqual(status, 0)
            with open(output_file, "r") as f:
                content = f.read()
            self.assertEqual(content, "line1\nline2\nline3\n")
            if os.path.exists(output_file):
                os.remove(output_file)
        finally:
            if os.path.exists(input_file):
                os.remove(input_file)

    def test_pipe_execution(self):
        import os
        shell, stdout, stderr = self.make_shell()
        output_file = "test_pipe_out.txt"
        if os.path.exists(output_file):
            os.remove(output_file)
            
        try:
            cmd = "python3 -c \"print('hello\\nworld')\" | grep hello > " + output_file
            status = shell.execute_line(cmd)
            self.assertEqual(status, 0)
            with open(output_file, "r") as f:
                content = f.read().strip()
            self.assertEqual(content, "hello")
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

    def test_input_redirection_file_not_found(self):
        shell, stdout, stderr = self.make_shell()
        status = shell.execute_line("sort < non_existent_xyz_123.txt")
        self.assertEqual(status, 1)


if __name__ == "__main__":
    unittest.main()
