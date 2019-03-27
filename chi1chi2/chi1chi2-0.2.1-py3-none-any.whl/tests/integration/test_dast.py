from tests.integration.test_runner import ITTests, _get_options, _get_from_fra_options, _get_from_crystal_options, \
    _get_input_preparator_options, _get_main_options, _get_analysis_options


class DASTITTests(ITTests):
    def test_from_fra_DAST(self):
        params = {}
        params["case"] = "dast_input"
        params["options"] = _get_options(_get_from_fra_options("asym.fra"))
        params["module-method"] = ["chi1chi2.from_fra", "run"]
        self._run_it(params)

    def test_from_crystal_DAST(self):
        params = {}
        params["case"] = "dast_crystal"
        params["options"] = _get_options(_get_from_crystal_options("dast.inp", "opt.out", "opt.SCFLOG"))
        params["module-method"] = ["chi1chi2.from_crystal", "run"]
        self._run_it(params)

    def test_input_preparator_DAST(self):
        params = {}
        params["case"] = "dast_input_preparator"
        params["options"] = _get_options(_get_input_preparator_options("dast.inp", "100."))
        params["module-method"] = ["chi1chi2.input_preparator", "run"]
        self._run_it(params)

    def test_lft_DAST(self):
        params = {}
        params["case"] = "dast_lft"
        params["options"] = _get_options(_get_main_options("dast.inp", "L.dat", "bchf", None))
        params["module-method"] = ["chi1chi2.main", "run"]
        self._run_it(params)

    def test_lft_qlft_DAST(self):
        params = {}
        params["case"] = "dast_lft_qlft"
        params["options"] = _get_options(_get_main_options("dast.inp", "L.dat", "bchf", None, "bp"))
        params["module-method"] = ["chi1chi2.main", "run"]
        self._run_it(params)

    def test_lft_analysis_DAST(self):
        params = {}
        params["case"] = "dast_analysis_lft"
        params["options"] = _get_options(_get_analysis_options("dast_lft.out"))
        params["module-method"] = ["chi1chi2.analyze", "run"]
        self._run_it(params)

    def test_qlft_analysis_DAST(self):
        params = {}
        params["case"] = "dast_analysis_qlft"
        params["options"] = _get_options(_get_analysis_options("dast_qlft.out"))
        params["module-method"] = ["chi1chi2.analyze", "run"]
        self._run_it(params)
