import requests
import bs4


class Entry:
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
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    table = soup.find(id='fieldsort')
    return get_entries_from_table(table)


def get_entries_from_table(table: bs4.element) -> list:
    """
    Take a BS4 representation of a tournament entries table and return a list of lists, each internal list holding the
    last names of the team's members.
    :param table: Table of entries.
    :return: List of name lists.
    """
    rows = table.find_all('tr')
    entries_from_table = []
    for row in rows:
        if len(row.find_all('td')) > 3:
            columns = [column.text.strip() for column in row.find_all('td')]
            names = columns[2].replace('&', '').split()
            school = ' '.join(columns[3].split()[:-1])
            if names != ['Names TBA']:
                entries_from_table.append(Entry(school, tuple(names)))
    return entries_from_table


if __name__ == '__main__':
    entries = get_entries('https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=13142&event_id=111039')
    print(entries)
