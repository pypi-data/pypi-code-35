from pathlib import Path

THIS_PATH = Path(__file__)
SCRIPT_PATH = THIS_PATH.parent / "data" / "track-changed-repos.sh"
ZSHRC_PATH = Path.home() / ".zshrc"
SOURCE_LINE = f". {SCRIPT_PATH}"


def install():
    with open(ZSHRC_PATH, "a") as f:
        f.write(f"\n{SOURCE_LINE}\n")


def uninstall():
    text = ZSHRC_PATH.read_text()
    ZSHRC_PATH.write_text(
        text.replace(SOURCE_LINE, '')
    )