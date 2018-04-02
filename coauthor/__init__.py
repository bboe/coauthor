from __future__ import print_function
import os
import re
import sys

from git import Repo
from git.exc import InvalidGitRepositoryError

from .const import __version__  # NOQA


COAUTHORS = {'bboe': {'email': 'bbzbryce@gmail.com', 'name': 'Bryce Boe'},
             'temp': {'email': 'z@a.com', 'name': 'A B C'}}
RE_CO_AUTHOR_LINE = re.compile('Co-authored-by: ([^<]+)<([^>]+)>',
                               re.MULTILINE)


def add_co_authors_by_alias(authors, aliases):
    authors = authors.copy()
    for alias in aliases:
        info = COAUTHORS[alias]
        authors[info['email']] = info['name']
    return authors


def add_co_authors_to_message(message, authors):
    if not authors:
        return message
    co_author_lines = (['Co-authored-by: {} <{}>\n'.format(name, email)
                        for email, name in sorted(authors.items(),
                                                  key=lambda x: x[1].lower())])
    return '{}\n{}'.format(message, ''.join(co_author_lines))


def amend_head(repository, message):
    repository.head.reference.commit = repository.head.commit.parents[0]
    repository.index.commit(message)


def extract_co_authors_from_message(message):
    authors = {}
    for name, email in RE_CO_AUTHOR_LINE.findall(message):
        authors[email.strip()] = name.strip()
    return authors


def strip_co_authors_from_message(message):
    lines = []
    for line in message.strip().split('\n'):
        if RE_CO_AUTHOR_LINE.match(line):
            continue
        lines.append(line + '\n')
    return ''.join(lines).rstrip() + '\n'


def main():
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
    if len(old_commit.parents) > 1:
        sys.stderr.write('ERROR: Rewriting merge commit is not supported.\n')
        return 3

    existing_authors = extract_co_authors_from_message(old_commit.message)
    authors = add_co_authors_by_alias(existing_authors, ['bboe'])
    base_message = strip_co_authors_from_message(old_commit.message)
    new_message = add_co_authors_to_message(base_message, authors)
    print(new_message)

    # amend_head(repository, new_message))
