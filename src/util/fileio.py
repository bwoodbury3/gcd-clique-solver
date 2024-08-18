"""
Problem-agnostic file IO.
"""


def read_data_lines(filename: str) -> list[str]:
    """
    Read all data lines from a file, stripping comments/whitespace.

    Args:
        filename: The filename.
    """
    lines = []
    with open(filename) as f:
        for line in f.readlines():
            # Strip comments
            if "#" in line:
                line = line[: line.find("#")]

            # Strip spaces
            line = line.strip()

            if len(line) != 0:
                lines.append(line)
    return lines
