import requests
import bs4


class Entry:
    """
    Represents an entry (team/partnership) in a tournament.
    """
    def __init__(self, school: str, names: tuple):
        if len(names) != 2:
            raise Exception('Must pass at exactly two names for a partnership. Got {0}'.format(str(names)))

        self.names = names
        self.school = school

    def __repr__(self):
        return 'Entry({0}, {1})'.format(self.school, str(self.names))


def get_entries(tabroom_entries_url: str) -> list:
    """
    Get team entries from a Tabroom entries page. Return a tuple of tuples - the inner tuples contain the last names of
    the two debaters.
    :param tabroom_entries_url: URL to the Tabroom tournament entries page.
    :return List of name lists.
    """
    r = requests.get(tabroom_entries_url)
    table = get_table_from_entry_page_markup(r.text)
    return get_entries_from_table(table)


def get_table_from_entry_page_markup(markup: str) -> bs4.element:
    """
    Get a BS4 table element from the given tournament entries page markup.
    :param markup: Markup from a Tabroom tournament entries page.
    :return: A BS4 table element for the entries table.
    """
    soup = bs4.BeautifulSoup(markup, 'html.parser')
    return soup.find(id='fieldsort')


def get_entries_from_table(table: bs4.element) -> list:
    """
    Take a BS4 representation of a tournament entries table and return a list of lists, each internal list holding the
    last names of the team's members.
    :param table: Table of entries.
    :return: List of name lists.
    """
    rows = table.find_all('tr')
    for row in rows:
        if len(row.find_all('td')) > 3:
            columns = [column.text.strip() for column in row.find_all('td')]

            # Don't return TBA entries.
            if columns[2] == 'Names TBA':
                continue

            names = columns[2].replace('&', '').split()
            school = ' '.join(columns[3].split()[:-1])

            yield Entry(school, tuple(names))


if __name__ == '__main__':
    entries = get_entries('https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=13142&event_id=111039')
    for entry in entries:
        print(entry.school + ' ' + entry.names[0][0] + entry.names[1][0] + ' - ' + ' & '.join(entry.names))
