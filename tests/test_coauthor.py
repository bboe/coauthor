from coauthor import (add_co_authors_by_alias, add_co_authors_to_message,
                      extract_co_authors_from_message,
                      strip_co_authors_from_message)


class TestAddCoAuthorsByAlias(object):
    def test_add_author_does_not_mutate_original(self):
        authors = {}
        add_co_authors_by_alias(authors, ['bboe'])
        assert {} == authors

    def test_add_single_author(self):
        expected = {'bbzbryce@gmail.com': 'Bryce Boe'}
        assert expected == add_co_authors_by_alias({}, ['bboe'])

    def test_add_multiple_authors(self):
        expected = {'bbzbryce@gmail.com': 'Bryce Boe', 'z@a.com': 'A B C'}
        assert expected == add_co_authors_by_alias({}, ['bboe', 'temp'])

    def test_add_zero_authors(self):
        assert {} == add_co_authors_by_alias({}, [])


class TestExtractCoAuthorsFromMessage(object):
    def test_full_commit_with_no_co_authors(self):
        assert {} == extract_co_authors_from_message(
            'Commit\n\nThis is a test commit.\n')

    def test_commit_with_single_duplicate_email_as_coauthor(self):
        message = """Test commit

Co-authored-by: a <a@a>
Co-authored-by: A <a@a>
"""
        assert {'a@a': 'A'} == extract_co_authors_from_message(message)

    def test_commit_with_single_multiple_coauthors(self):
        message = """Test commit

Co-authored-by: a <a@a>
Co-authored-by: b <b@b>
"""
        expected = {'a@a': 'a', 'b@b': 'b'}
        assert expected == extract_co_authors_from_message(message)

    def test_commit_with_single_co_author(self):
        message = """Test commit

Co-authored-by: a <a@a>
"""
        assert {'a@a': 'a'} == extract_co_authors_from_message(message)

    def test_single_line_commits_have_no_co_authors(self):
        for message in ['', '\n', '\n\n', 'Test', 'Test\n', 'Test\n\n']:
            assert {} == extract_co_authors_from_message(message)


class TestStripCoAuthorsFromMessage(object):
    def test_multiple_line_messages_without_coauthors(self):
        expected = 'Test\n\nTest commit.\n'
        for message in ['Test\n\nTest commit.', 'Test\n\nTest commit.\n']:
            assert expected == strip_co_authors_from_message(message)

    def test_single_line_messages_without_coauthors(self):
        for message in ['Test', 'Test\n', 'Test\n\n']:
            assert 'Test\n' == strip_co_authors_from_message(message)
