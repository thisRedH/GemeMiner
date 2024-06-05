#!/usr/bin/env python
import sys

# This is just foolproofing
if __name__ == "__main__":
    print(
        f"{__package__} is a package and cannot be directly executed\n"
        f"Please run 'python -m {__package__}.cli' instead",
        file=sys.stderr,
    )

    sys.exit(1)
