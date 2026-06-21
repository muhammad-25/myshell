import os
import sys
import errno
import subprocess
from myshell.builtins import load_builtins
from myshell.builtins.base import BuiltinCommand
from myshell.context import ShellContext
from myshell.parser import ParsedLine


class WeekOneExecutor:
    """Executor untuk menjalankan command built-in dan eksternal.
    """

    def __init__(self, builtins: dict[str, BuiltinCommand] | None = None) -> None:
        self.builtins = builtins or load_builtins()

    def execute(self, parsed: ParsedLine, context: ShellContext) -> int:
        if parsed.is_empty:
            context.last_status = 0
            return 0

        command = parsed.tokens[0]
        args = parsed.tokens[1:]

        # Cek command utama pada built-in
        builtin = self.builtins.get(command)
        if builtin is not None:
            status = builtin.handler(context, args)
            context.last_status = status
            return status

        # Jalankan eksternal command
        if hasattr(os, "fork"):
            try:
                pid = os.fork()
            except OSError as exc:
                context.error(f"myshell: fork failed: {exc}")
                context.last_status = 1
                return 1

            if pid == 0:
                # CHILD PROCESS
                try:
                    os.execvp(command, parsed.tokens)
                except OSError as exc:
                    if exc.errno == errno.ENOENT:
                        context.error(f"myshell: {command}: command not found")
                        os._exit(127)
                    elif exc.errno == errno.EACCES:
                        context.error(f"myshell: {command}: Permission denied")
                        os._exit(126)
                    else:
                        context.error(f"myshell: {command}: {exc.strerror}")
                        os._exit(exc.errno)
                except Exception as exc:
                    context.error(f"myshell: {command}: {exc}")
                    os._exit(1)
            else:
                # PARENT PROCESS
                try:
                    _, status = os.waitpid(pid, 0)
                    if os.WIFEXITED(status):
                        exit_status = os.WEXITSTATUS(status)
                    elif os.WIFSIGNALED(status):
                        exit_status = 128 + os.WTERMSIG(status)
                    else:
                        exit_status = 1
                except OSError as exc:
                    context.error(f"myshell: waitpid failed: {exc}")
                    exit_status = 1
                
                context.last_status = exit_status
                return exit_status
        else:
            # FALLBACK WINDOWS
            import shutil
            
            is_builtin_shell = command.lower() in {
                "dir", "cls", "copy", "del", "md", "rd", "type", "echo", "move", "ren", "mkdir", "rmdir", "clear"
            }
            
            if not is_builtin_shell and shutil.which(command) is None:
                context.error(f"myshell: {command}: command not found")
                exit_status = 127
            else:
                try:
                    capture = False
                    stdout_stream = context.stdout
                    stderr_stream = context.stderr
                    
                    if hasattr(stdout_stream, "getvalue") or hasattr(stderr_stream, "getvalue"):
                        capture = True

                    if capture:
                        res = subprocess.run(
                            parsed.tokens,
                            capture_output=True,
                            text=True,
                            shell=True
                        )
                        if res.stdout:
                            context.stdout.write(res.stdout)
                        if res.stderr:
                            context.stderr.write(res.stderr)
                        exit_status = res.returncode
                    else:
                        res = subprocess.run(
                            parsed.tokens,
                            shell=True
                        )
                        exit_status = res.returncode
                except FileNotFoundError:
                    context.error(f"myshell: {command}: command not found")
                    exit_status = 127
                except Exception as exc:
                    context.error(f"myshell: {command}: {exc}")
                    exit_status = 1

            context.last_status = exit_status
            return exit_status

