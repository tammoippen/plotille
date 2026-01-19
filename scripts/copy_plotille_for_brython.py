#!/usr/bin/env python3
"""Copy plotille source files for Brython access."""
import shutil
from pathlib import Path


def ignore_pycache(directory, files):
    """Ignore __pycache__ directories and .pyc files."""
    return ['__pycache__'] + [f for f in files if f.endswith('.pyc')]


def main():
    project_root = Path(__file__).parent.parent
    source_dir = project_root / "plotille"
    # Use Brython's standard site-packages location
    dest_dir = project_root / "docs" / "Lib" / "site-packages" / "plotille"

    # Remove old copy
    if dest_dir.exists():
        shutil.rmtree(dest_dir)

    # Ensure parent directories exist
    dest_dir.parent.mkdir(parents=True, exist_ok=True)

    # Copy plotille source (excluding __pycache__)
    shutil.copytree(source_dir, dest_dir, ignore=ignore_pycache)
    print(f"Copied plotille to {dest_dir}")


if __name__ == "__main__":
    main()
