from myshell.context import ShellContext
from myshell.errors import ParseError
from myshell.executor import WeekOneExecutor
from myshell.parser import parse_input
from myshell.prompt import build_prompt


class MiniShell:
    def __init__(
        self,
        context: ShellContext | None = None,
        executor: WeekOneExecutor | None = None,
    ) -> None:
        self.context = context or ShellContext()
        self.executor = executor or WeekOneExecutor()

    def execute_line(self, line: str) -> int:
        if not line.strip():
            self.context.last_status = 0
            return 0

        try:
            parsed = parse_input(line)
        except ParseError as exc:
            self.context.error(f"myshell: parse error: {exc}")
            self.context.last_status = 2
            return 2

        self.context.history.add(line)
        return self.executor.execute(parsed, self.context)

    def run(self) -> int:
        while self.context.running:
            try:
                line = input(build_prompt(self.context))
            except EOFError:
                self.context.write()
                break
            except KeyboardInterrupt:
                self.context.write()
                continue

            self.execute_line(line)

        return self.context.last_status
