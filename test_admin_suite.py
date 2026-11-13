"""
End-to-End Automated Verification Suite for HanzCraft 7-Part Admin Overhaul
"""

import os
import pathlib
import sys
import unittest

from app import ADMIN_PASSWORD, BASE_DIR, app
from cv_architect import (
    CV_HUB_OUTPUT_DIR,
    CV_HUB_ROOT,
    build_initial_cv_state,
    build_inverted_index,
    query_inverted_index,
    rank_projects_for_job,
    refine_cv_state_with_prompt,
    validate_cv_truth,
)
from internship_hunter import get_boot_sync_payload, load_hunter_state


class TestAdminOverhaulSuite(unittest.TestCase):
    def test_01_truth_linter_rejects_and_rewrites_hallucinations(self):
        dirty_payload = {
            "summary": "Student concurrently completing my 4th-year BSc in Computer Engineering at KNUST (Ghana).",
            "education": "KNUST 2023 – June 2027 (In progress) | JUNIA ISEN Lille 2025 – Present",
            "experience": "ACES President Août 2025 – En cours",
            "project": "Physical E.Leclerc PCB fabricated",
        }
        report = validate_cv_truth(dirty_payload)
        self.assertTrue(report["auto_fixed"])
        self.assertGreaterEqual(len(report["violations_found"]), 4)
        self.assertTrue(report["truth_verified"], f"Remaining violations: {report['remaining_violations']}")
        cleaned = report["rewritten_payload"]
        self.assertNotIn("2027", cleaned["education"])
        self.assertNotIn("In progress", cleaned["education"])
        self.assertIn("2022 – 2026", cleaned["education"])
        self.assertNotIn("En cours", cleaned["experience"])

    def test_02_all_workspace_and_hub_templates_clean(self):
        workspace_templates = [
            "templates/cv_en_ats.html",
            "templates/cv_fr_ats.html",
            "templates/cv_en.html",
            "templates/cv_fr.html",
            "cv_general_fr.html",
            "cv_ing_teal_fr.html",
        ]
        for rel in workspace_templates:
            p = pathlib.Path(BASE_DIR) / rel
            self.assertTrue(p.exists(), f"Missing template {rel}")
            text = p.read_text(encoding="utf-8", errors="replace")
            rep = validate_cv_truth(text)
            self.assertTrue(rep["valid"], f"Template {rel} has truth violations: {rep['violations_found']}")

        admin_html = (pathlib.Path(BASE_DIR) / "templates" / "admin_dashboard.html").read_text(encoding="utf-8")
        self.assertNotIn("africa is strictly excluded", admin_html.lower())

        hub = pathlib.Path(CV_HUB_ROOT)
        if hub.exists():
            for hp in hub.rglob("*.html"):
                if "Tailored_Applications" in str(hp) or "output" in str(hp):
                    continue
                rep = validate_cv_truth(hp.read_text(encoding="utf-8", errors="replace"))
                self.assertTrue(rep["valid"], f"CV Hub file {hp} has truth violations: {rep['violations_found']}")

    def test_03_dynamic_tier_project_ranking(self):
        pcb_job = {
            "id": "test_pcb",
            "company": "ST Micro",
            "title": "Microelectronics Hardware PCB Design Engineer (KiCad)",
            "skills": ["KiCad", "PCB Layout", "Schematic Capture", "Soldering", "Analog"],
            "description": "Design custom power PCB schematics in KiCad, copper etching and hardware testing.",
        }
        ranked_pcb = rank_projects_for_job(pcb_job, lang="en")
        self.assertEqual(ranked_pcb[0]["id"], "charger_pcb", f"Expected charger_pcb #1, got {ranked_pcb[0]['id']}")
        self.assertEqual(ranked_pcb[0]["verification_tier"], 1)

        sql_job = {
            "id": "test_sql",
            "company": "OVHcloud",
            "title": "Systems Backend & PostgreSQL Database Engineer",
            "skills": ["PostgreSQL", "SQL", "3NF", "Python", "REST API"],
            "description": "Relational database schema normalization 3NF and Python backend architecture.",
        }
        ranked_sql = rank_projects_for_job(sql_job, lang="en")
        self.assertEqual(ranked_sql[0]["id"], "logistics_sql")
        self.assertEqual(ranked_sql[1]["id"], "portfolio_python")

        robot = next(p for p in ranked_pcb if p["id"] == "robot_stm32")
        self.assertIn("Active R&D", robot["title"])

    def test_04_o1_inverted_index_speed_and_regions(self):
        state = load_hunter_state()
        jobs = state["jobs"]
        idx = state["inverted_index"]
        self.assertGreater(len(jobs), 0)

        # Verify no Africa leakage
        for j in jobs:
            self.assertNotIn("ghana", (j.get("location") or "").lower())
            self.assertNotIn("nigeria", (j.get("location") or "").lower())

        res_union = query_inverted_index(jobs, filters={"regions": ["lille", "north_america"]}, inverted_index=idx)
        self.assertLess(res_union["elapsed_ms"], 5.0)
        for j in res_union["jobs"]:
            self.assertIn(j["region"], ("lille", "north_america"))

        res_fr_union = query_inverted_index(jobs, filters={"regions": ["lille", "france"], "contract": "alternance"}, inverted_index=idx)
        self.assertLess(res_fr_union["elapsed_ms"], 5.0)
        for j in res_fr_union["jobs"]:
            self.assertIn(j["region"], ("lille", "france"))

        for tok in ("portal:junia_jobteaser", "portal:wttj", "portal:linkedin_live", "portal:direct_ats"):
            self.assertIn(tok, idx, f"Missing portal token {tok} in inverted index")
        res_jt = query_inverted_index(jobs, filters={"portals": ["junia_jobteaser"]}, inverted_index=idx)
        self.assertLess(res_jt["elapsed_ms"], 5.0)
        self.assertGreater(res_jt["total"], 0)

    def test_05_flask_endpoints_refine_and_export(self):
        client = app.test_client()
        login_res = client.post("/admin/login", data={"password": ADMIN_PASSWORD}, follow_redirects=False)
        self.assertIn(login_res.status_code, (200, 302))

        boot_res = client.get("/admin/api/boot-sync")
        self.assertEqual(boot_res.status_code, 200)
        boot_json = boot_res.get_json()
        self.assertTrue(boot_json["ok"])
        self.assertIn("inverted_index", boot_json)
        self.assertIn("cv_hub_templates", boot_json)

        q_res = client.post("/admin/api/jobs/query", json={"regions": ["lille", "france"]})
        self.assertEqual(q_res.status_code, 200)
        self.assertLess(q_res.get_json()["elapsed_ms"], 5.0)

        base_state = build_initial_cv_state(lang="fr")
        ref_res = client.post(
            "/admin/api/cv/refine",
            json={"cv_state": base_state, "prompt": "Translate to English, put KiCad Charger PCB first, and condense to 1 page"},
        )
        self.assertEqual(ref_res.status_code, 200)
        ref_json = ref_res.get_json()
        self.assertTrue(ref_json["truth_report"]["truth_verified"])
        self.assertEqual(ref_json["cv_state"]["meta"]["lang"], "en")
        self.assertEqual(ref_json["cv_state"]["projects"][0]["id"], "charger_pcb")
        self.assertLess(ref_json["cv_state"]["layout"]["font_scale"], 1.0)

        exp_res = client.post(
            "/admin/api/cv/export",
            json={"cv_state": ref_json["cv_state"], "job": {"company": "Exotec Test", "title": "Embedded Engineer"}},
        )
        self.assertEqual(exp_res.status_code, 200)
        exp_json = exp_res.get_json()
        self.assertTrue(exp_json["ok"])
        self.assertTrue(exp_json["truth_verified"])
        self.assertTrue(os.path.exists(exp_json["html_path"]))
        self.assertTrue(exp_json["html_path"].startswith(CV_HUB_OUTPUT_DIR))

        # Verify public routes remain 200 OK
        self.assertEqual(client.get("/").status_code, 200)
        self.assertEqual(client.get("/api/v1/profile").status_code, 200)
        self.assertEqual(client.get("/api/v1/projects").status_code, 200)

    def test_06_live_multi_source_search_and_lille_depth(self):
        client = app.test_client()
        client.post("/admin/login", data={"password": ADMIN_PASSWORD})
        res = client.post(
            "/admin/api/jobs/live-search",
            json={"regions": ["lille"], "freshness": "7d", "contract": "all"},
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["ok"])
        lille_jobs = data["jobs"]
        self.assertGreaterEqual(len(lille_jobs), 15, f"Expected >= 15 Lille jobs, got {len(lille_jobs)}")
        for j in lille_jobs:
            self.assertTrue(str(j.get("direct_apply_url", "")).startswith("http"))
            self.assertTrue(str(j.get("junia_jobteaser_url", "")).startswith("https://junia.jobteaser.com"))
            self.assertTrue(str(j.get("wttj_url", "")).startswith("https://www.welcometothejungle.com"))
            self.assertIn("f_TPR=", str(j.get("linkedin_fresh_url", "")))
            self.assertNotEqual(j.get("direct_apply_url"), j.get("linkedin_fresh_url"))
            self.assertNotEqual(j.get("junia_jobteaser_url"), j.get("wttj_url"))

        dash_html = (pathlib.Path(BASE_DIR) / "templates" / "admin_dashboard.html").read_text(encoding="utf-8")
        self.assertIn("let HAS_SEARCHED = false", dash_html)
        self.assertIn("toggleAutonomousMode()", dash_html)
        self.assertIn("executeLiveSearch(", dash_html)
        self.assertIn('id="portalChecklist"', dash_html)
        self.assertIn('id="customRoleModal"', dash_html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
