from __future__ import annotations

import sys
from typing import Dict, List, Optional, TypedDict


LOG_LEVELS = ("INFO", "ERROR", "DEBUG", "WARNING")


class LogRecord(TypedDict):
    date: str
    time: str
    level: str
    message: str


def parse_log_line(line: str) -> LogRecord:
    """
    Parse one log line into components: date, time, level, message.

    Expected format:
        YYYY-MM-DD HH:MM:SS LEVEL Message...

    Notes:
    - Uses split(maxsplit=3) to be robust against multiple spaces.
    """
    parts = line.strip().split(maxsplit=3)
    if len(parts) < 4:
        raise ValueError(f"Invalid log line format: {line!r}")

    date, time, level, message = parts
    if level not in LOG_LEVELS:
        raise ValueError(f"Unknown log level {level!r} in line: {line!r}")

    return {"date": date, "time": time, "level": level, "message": message}


def load_logs(file_path: str) -> List[LogRecord]:
    """
    Load logs from file and return list of parsed log records.

    - Skips empty lines.
    - For invalid lines, prints a warning to stderr and continues.
    """
    logs: List[LogRecord] = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line_no, line in enumerate(file, start=1):
                if not line.strip():
                    continue
                try:
                    logs.append(parse_log_line(line))
                except ValueError as exc:
                    print(f"Warning: line {line_no}: {exc}", file=sys.stderr)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File not found: {file_path}") from exc
    except OSError as exc:
        raise OSError(f"Error reading file {file_path!r}: {exc}") from exc

    return logs


def filter_logs_by_level(logs: List[LogRecord], level: str) -> List[LogRecord]:
    """
    Filter logs by logging level (case-insensitive input).

    Functional programming element:
    - Uses filter() with a lambda.
    """
    level_upper = level.upper()
    if level_upper not in LOG_LEVELS:
        raise ValueError(f"Unsupported level {level!r}. Use one of: {', '.join(LOG_LEVELS)}")

    return list(filter(lambda rec: rec["level"] == level_upper, logs))


def count_logs_by_level(logs: List[LogRecord]) -> Dict[str, int]:
    """
    Count number of logs for each level.
    """
    counts: Dict[str, int] = {lvl: 0 for lvl in LOG_LEVELS}
    for rec in logs:
        counts[rec["level"]] += 1
    return counts


def display_log_counts(counts: Dict[str, int]) -> None:
    """
    Print a table with log counts by level.

    Uses dynamic column width so the table is always aligned.
    """
    header_left = "Рівень логування"
    header_right = "Кількість"

    left_width = max(len(header_left), max(len(level) for level in LOG_LEVELS))
    right_width = max(len(header_right), max(len(str(counts.get(level, 0))) for level in LOG_LEVELS))

    print(f"{header_left:<{left_width}} | {header_right:>{right_width}}")
    print(f"{'-' * left_width}-+-{'-' * right_width}")

    for level in LOG_LEVELS:
        print(f"{level:<{left_width}} | {counts.get(level, 0):>{right_width}}")


def display_log_details(logs: List[LogRecord], level: str) -> None:
    """
    Print details for logs of a given level.
    """
    level_upper = level.upper()
    print(f"\nДеталі логів для рівня '{level_upper}':")

    if not logs:
        print("Немає записів для цього рівня.")
        return

    for rec in logs:
        print(f"{rec['date']} {rec['time']} - {rec['message']}")


def main(argv: List[str]) -> int:
    """
    CLI entry point.

    Usage:
        python main.py <logfile_path> [level]

    Example:
        python main.py logs.txt error
    """
    if len(argv) < 2:
        print("Usage: python main.py <logfile_path> [level]", file=sys.stderr)
        return 1

    file_path = argv[1]
    level: Optional[str] = argv[2] if len(argv) >= 3 else None

    try:
        logs = load_logs(file_path)

        counts = count_logs_by_level(logs)
        display_log_counts(counts)

        if level is not None:
            filtered = filter_logs_by_level(logs, level)
            display_log_details(filtered, level)

    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
