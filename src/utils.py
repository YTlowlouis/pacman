import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_resource_path(relative_path: str) -> Path:
    """Build the absolute path of a file shipped with the game.

    The path does not depend on the directory the game is launched
    from: it is based on the project root, or on the PyInstaller
    bundle directory when the game is packaged.

    Args:
        relative_path: Path relative to the project root, such as
            ``src/assets/pacgum.png``.

    Returns:
        The absolute path of the file.
    """
    base = Path(getattr(sys, "_MEIPASS", PROJECT_ROOT))
    return base / relative_path
