import unittest

import GetEntriesFromTabroom


entries_table_markup = """
<table id="fieldsort" class="tablesorter tablesorter-default tablesorter62c06f7a632ab hasStickyHeaders" role="grid">
   <tbody aria-live="polite" aria-relevant="all">
      <tr role="row" class="odd">
         <td>
            Dartmouth College
         </td>
         <td>
            NH/US
         </td>
         <td>
            Chang &amp; DeConcini
         </td>
         <td>
            Dartmouth CD
         </td>
         <td class="centeralign">
            <a href="/index/results/team_lifetime_record.mhtml?id1=842443&amp;id2=691834" class="buttonwhite bluetext hover smallish invert">
            All Results
            </a>
         </td>
         <td class="centeralign">
            <a href="/index/results/team_results.mhtml?id1=842443&amp;id2=691834" class="buttonwhite greentext hover smallish invert">
            Bid Sheet
            </a>
         </td>
      </tr>
   </tbody>
</table>
"""


class MyTestCase(unittest.TestCase):
    def test_getting_entry_from_table_markup(self):
        """
        Test pulling school and debate partner names from entry table markup.
        """
        table = GetEntriesFromTabroom.get_table_from_entry_page_markup(entries_table_markup)
        entries = GetEntriesFromTabroom.get_entries_from_table(table)
        entry = list(entries)[0]
        self.assertEqual(entry.school, 'Dartmouth College')
        self.assertEqual(entry.names[0], 'Chang')
        self.assertEqual(entry.names[1], 'DeConcini')


if __name__ == '__main__':
    unittest.main()
