import unittest
from unittest import mock
from unittest.mock import Mock

from mucho.comparison.comparator import EntityComparator, DimensionComparator


class TitlesComparator(DimensionComparator):
    pass


class YearsComparator(DimensionComparator):
    pass


class WorksComparator(EntityComparator):
    titles = TitlesComparator()
    years = YearsComparator()


class EntityTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_compare_calls_compare_with_works_for_each_comparator(self):
        work_src, work_trg = Mock(), Mock()
        comparator = WorksComparator()
        with mock.patch.object(comparator.comparators['titles'], 'compare') as titles_compare,\
                mock.patch.object(comparator.comparators['years'], 'compare') as years_compare:
            comparator.compare(work_src, work_trg)
            titles_compare.assert_called_once_with(work_src, work_trg)
            years_compare.assert_called_once_with(work_src, work_trg)

    def test_compare_returns_result_with_comparator_names_as_fields(self):
        work_src, work_trg = Mock(), Mock()
        comparator = WorksComparator()
        result = comparator.compare(work_src, work_trg)
        self.assertIn('titles', result.__dict__)
        self.assertIn('years', result.__dict__)

    def test_compare_returns_result_with_comparison_results_in_fields(self):
        work_src, work_trg = Mock(), Mock()
        comparator = WorksComparator()
        titles_compare_results = True
        years_compare_results = False
        with mock.patch.object(
                comparator.comparators['titles'], 'compare',
                return_value=titles_compare_results), \
                mock.patch.object(
                    comparator.comparators['years'], 'compare',
                    return_value=years_compare_results):
            result = comparator.compare(work_src, work_trg)
            self.assertEqual(titles_compare_results, result.titles)
            self.assertEqual(years_compare_results, result.years)

if __name__ == '__main__':
    unittest.main()
