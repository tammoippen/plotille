#!/usr/bin/env python3
"""Copy plotille source files for Brython access."""
import shutil
from pathlib import Path

def main():
    project_root = Path(__file__).parent.parent
    source_dir = project_root / "plotille"
    dest_dir = project_root / "docs" / "src" / "lib" / "plotille"

    # Remove old copy
    if dest_dir.exists():
        shutil.rmtree(dest_dir)

    # Copy plotille source
    shutil.copytree(source_dir, dest_dir)
    print(f"Copied plotille to {dest_dir}")

if __name__ == "__main__":
    main()
