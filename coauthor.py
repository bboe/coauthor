#!/usr/bin/env python
from __future__ import print_function
import os
import sys

from git import Repo
from git.exc import InvalidGitRepositoryError

COAUTHORS = {'bboe': 'bbzbryce@gmail.com'}

def main():
    from git import Repo
    try:
        repository = Repo(os.getcwd())
    except InvalidGitRepositoryError:
        sys.stderr.write(
            'ERROR: The current directory is not a git respository.\n')
        return 1

    print(repository)


if __name__ == '__main__':
    sys.exit(main())
