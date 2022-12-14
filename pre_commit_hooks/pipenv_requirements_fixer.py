from __future__ import annotations

import argparse
import os
import subprocess
from typing import IO
from typing import Sequence


def fix_file() -> int:
    try:
        with open('requirements.txt', 'rb') as f:
            content = f.read()
    except FileNotFoundError:
        content = b''

    subprocess.run(['pipenv', 'install'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = subprocess.run(['pipenv', 'requirements'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if content != result.stdout:
        with open('requirements.txt', 'wb') as f:
            f.write(result.stdout)

        return 1

    return 0



def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retv = 0

    if args.filenames:
        ret_for_file = fix_file()
        if ret_for_file:
            print('Fixing requirements.txt')

        retv |= ret_for_file

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
