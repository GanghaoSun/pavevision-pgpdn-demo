from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pgpdn.features import feature_array, load_feature_table
from pgpdn.model import PGPDN, PGPDNConfig
from web_demo.app import app


class PublicDocumentationTest(unittest.TestCase):
    def test_public_text_avoids_staged_release_language(self) -> None:
        files = [
            ROOT / "README.md",
            ROOT / "supplementary" / "Data_and_Model_Release_Statement.md",
            ROOT / "supplementary" / "Supplementary_Methods.md",
            ROOT / "web_demo" / "static" / "index.html",
            ROOT / "pgpdn" / "model.py",
            ROOT / "examples" / "run_inference_template.py",
        ]
        forbidden = [
            "after " + "acceptance",
            "planned " + "additions",
            "planned " + "updates",
            "will be " + "uploaded",
            "will be " + "added",
        ]
        for path in files:
            text = path.read_text(encoding="utf-8").lower()
            for phrase in forbidden:
                self.assertNotIn(phrase, text, f"{phrase!r} found in {path}")


class FeatureAndModelTest(unittest.TestCase):
    def test_synthetic_feature_table_and_model_forward(self) -> None:
        frame = load_feature_table(ROOT / "sample_data" / "synthetic_grid_features.csv")
        x = torch.from_numpy(feature_array(frame))
        model = PGPDN(PGPDNConfig())
        model.eval()
        with torch.no_grad():
            output = model(x)
        self.assertEqual(output["next_pqi_points"].shape[0], len(frame))
        self.assertTrue(torch.all(output["next_pqi_points"] >= 0))
        self.assertTrue(torch.all(output["next_pqi_points"] <= 100))
        self.assertIn("physical_rate", output)


class WebDemoDataTest(unittest.TestCase):
    def test_manifest_files_exist(self) -> None:
        sample_dir = ROOT / "web_demo" / "data" / "sample"
        manifest = json.loads((sample_dir / "manifest.json").read_text(encoding="utf-8-sig"))
        self.assertEqual(manifest["route_count"], 3)
        self.assertGreater(manifest["total_length_m"], 5000)
        for name in manifest["generated_files"]:
            self.assertTrue((sample_dir / name).is_file(), name)

    def test_api_endpoints(self) -> None:
        urls = [
            "/",
            "/api/config",
            "/api/assessment/route1/t3",
            "/api/grid/route1/t3?grid_size=0.5",
            "/api/prediction/route1",
            "/api/grid/prediction/route1?grid_size=0.5",
            "/api/traffic?route_id=route1",
            "/api/weather",
            "/api/model_params",
        ]
        with app.test_client() as client:
            for url in urls:
                response = client.get(url)
                try:
                    self.assertEqual(response.status_code, 200, url)
                    response.get_data()
                finally:
                    response.close()

    def test_route_labels_match_manuscript_terms(self) -> None:
        with app.test_client() as client:
            response = client.get("/api/config")
            try:
                payload = response.get_json()
            finally:
                response.close()
        labels = {route["id"]: route["description"] for route in payload["routes"]}
        self.assertEqual(labels["route1"], "Suburban closed-loop route")
        self.assertEqual(labels["route2"], "Urban lane-changing route")
        self.assertEqual(labels["route3"], "Industrial straight route")


if __name__ == "__main__":
    unittest.main()
