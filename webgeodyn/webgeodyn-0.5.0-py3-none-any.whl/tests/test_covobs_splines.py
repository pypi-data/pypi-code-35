import unittest
import os.path
import numpy as np

from webgeodyn.inout.covobs_splines import read_spline_coeffs_file, get_date_indexes_for_spl_eval, eval_spline, build_gnm_from_spline_coeffs, build_gnm_from_spline_coeffs_all_splines


class TestBuildingFromSplines(unittest.TestCase):
    def setUp(self):
        file_folder = os.path.join(os.path.dirname(__file__), 'Spline_benchmark')
        self.spl_dates, self.spl_coeffs, self.spl_order, self.knot_sp = read_spline_coeffs_file(os.path.join(file_folder,'real_001'))

        raw_benchmark = np.genfromtxt(os.path.join(file_folder, 'real001_mf_int_coefs.dat'))
        self.dates_benchmark = raw_benchmark[:, 0]
        self.gnm_benchmark = raw_benchmark[:, 1:]

    def test_get_required_splines(self):
        """ Test that the date indexes required for the evaluation include ALL the non-zero splines """
        eval_date = np.random.choice(self.dates_benchmark)
        required_date_indexes = get_date_indexes_for_spl_eval(eval_date, self.spl_dates, self.spl_order)
        for j, center_date in enumerate(self.spl_dates):
            with self.subTest(date=center_date):
                if j not in required_date_indexes:
                    self.assertEqual(eval_spline(eval_date, center_date, self.spl_order, self.knot_sp), 0.)

    def test_building_gnm_few_splines(self):
        """ Test the method building from the splines around the date asked """
        dates_gnm, gnm = build_gnm_from_spline_coeffs(self.dates_benchmark, self.spl_dates, self.spl_coeffs, self.spl_order)
        self.assertTrue(np.alltrue(np.abs(gnm - self.gnm_benchmark) < 1))

    def test_building_gnm_all_splines(self):
        """ Test the method building from all the splines """
        dates_gnm, gnm = build_gnm_from_spline_coeffs_all_splines(self.dates_benchmark, self.spl_dates, self.spl_coeffs, self.spl_order)
        self.assertTrue(np.alltrue(np.abs(gnm - self.gnm_benchmark) < 1))

    def test_two_building_methods(self):
        """ Test that the two methods give the same result """
        dates_gnm, gnm = build_gnm_from_spline_coeffs(self.dates_benchmark, self.spl_dates, self.spl_coeffs, self.spl_order)
        dates_gnm_2, gnm_2 = build_gnm_from_spline_coeffs_all_splines(self.dates_benchmark, self.spl_dates, self.spl_coeffs, self.spl_order)
        np.testing.assert_equal(gnm, gnm_2)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestBuildingFromSplines)
    RES = unittest.TextTestRunner(verbosity=2).run(SUITE)
    import sys
    sys.exit(max(len(RES.failures), len(RES.errors)))

