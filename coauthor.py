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

    old_commit = repository.head.commit
    if not old_commit.parents:
        sys.stderr.write('ERROR: Rewriting first commit is not supported.\n')
        return 2
    print(old_commit)
    print(old_commit.parents)
    #repository.head.reference.commit = co


if __name__ == '__main__':
    sys.exit(main())
