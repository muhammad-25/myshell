from dataclasses import dataclass, field


@dataclass
class History:
    entries: list[str] = field(default_factory=list)

    def add(self, line: str) -> None:
        cleaned = line.strip()
        if cleaned:
            self.entries.append(cleaned)

    def list_entries(self) -> list[tuple[int, str]]:
        return list(enumerate(self.entries, start=1))
