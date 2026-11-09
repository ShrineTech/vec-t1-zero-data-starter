"""Tests for t1_starter (SYNTHETIC data only). Needs numpy, scipy, anndata, veckit==0.1.2.

    python -m pytest -q test_t1_starter.py
"""
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import anndata as ad  # noqa: E402
import t1_starter as st  # noqa: E402


class TestStarter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.res = st.run(cls.tmp.name, n_genes=400, cells=800, quiet=True)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_copy_last_is_exactly_the_floor(self):
        self.assertAlmostEqual(self.res["copy_last"]["headline"], 50.0, places=6)

    def test_composition_shift_beats_floor_on_synthetic(self):
        self.assertGreater(self.res["composition_shift"]["headline"], 55.0)

    def test_predictions_valid_and_readable(self):
        for n in ("copy_last", "composition_shift"):
            r = self.res[n]
            self.assertTrue(r["valid"], r["errors"])
            self.assertEqual(r["warnings"], [])
            a = ad.read_h5ad(r["file"])
            self.assertEqual(a.X.dtype.name, "float32")
            self.assertEqual(a.n_vars, 400)

    def test_silent_killers_caught(self):
        k = self.res["_killers"]
        self.assertTrue(k["raw_counts"]["ok"])                    # passes format checks...
        self.assertTrue(any("library size" in w for w in k["raw_counts"]["warnings"]))   # ...but we warn
        self.assertFalse(k["shuffled_genes"]["ok"])
        self.assertIn("WRONG ORDER", k["shuffled_genes"]["errors"][0])

    def test_data_marked_synthetic(self):
        a = ad.read_h5ad(Path(self.tmp.name) / "released" / "E8.5_RNA.h5ad")
        self.assertIn("SYNTHETIC", a.uns)
        self.assertTrue(all(n.startswith("SYN_") for n in a.obs_names))

    def test_skill_map(self):
        self.assertEqual(st.skill(0.08359, 0.08359, 0.00406, True), 0.5)
        self.assertEqual(st.skill(0.00406, 0.08359, 0.00406, True), 1.0)
        self.assertEqual(st.skill(float("nan"), 0, 1, False), 0.0)



class TestNotebookInSync(unittest.TestCase):
    def test_ipynb_matches_script(self):
        import json
        import make_notebook
        self.assertEqual(json.loads((HERE / "t1_starter.ipynb").read_text()), make_notebook.build(),
                         "run `python make_notebook.py` after editing t1_starter.py")


if __name__ == "__main__":
    unittest.main()
