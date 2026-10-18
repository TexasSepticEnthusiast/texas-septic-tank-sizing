"""Regression tests for the published formula bands and safe CLI boundary."""
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from outwestseptic_tank_sizer import OutWestSepticTankSizer

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "outwestseptic_tank_sizer.py"


class TankSizerTests(unittest.TestCase):
    def setUp(self):
        self.sizer = OutWestSepticTankSizer()

    def test_each_published_band_boundary(self):
        for flow, gallons in [
            (1, 750), (250, 750), (251, 1000), (350, 1000),
            (351, 1250), (500, 1250), (501, 1252.5),
            (1000, 2500), (1001, 2500.75), (5000, 5500),
        ]:
            with self.subTest(flow=flow):
                self.assertEqual(
                    self.sizer.minimum_tank_gallons(design_flow_gpd=flow), gallons
                )

    def test_rounding_never_loses_fractional_gallons(self):
        for flow, exact, rounded in [(501, 1252.5, 1253), (1001, 2500.75, 2501)]:
            with self.subTest(flow=flow):
                report = self.sizer.size_report(design_flow_gpd=flow)
                self.assertEqual(report.formula_liquid_gallons, exact)
                self.assertEqual(report.rounded_liquid_gallons, rounded)

    def test_all_supported_flows_are_monotonic_and_round_up(self):
        previous = 0
        for flow in range(1, 5001):
            report = self.sizer.size_report(design_flow_gpd=flow)
            self.assertGreaterEqual(report.formula_liquid_gallons, previous)
            self.assertGreaterEqual(report.rounded_liquid_gallons, report.formula_liquid_gallons)
            self.assertLess(report.rounded_liquid_gallons - report.formula_liquid_gallons, 1)
            previous = report.formula_liquid_gallons

    def test_rejects_invalid_ambiguous_and_out_of_scope_flows(self):
        for value in [0, -1, 5001, True, False, 250.5, 300.0, "300", None,
                      float("nan"), float("inf"), float("-inf"), 10 ** 1000]:
            with self.subTest(value=repr(value)[:40]):
                with self.assertRaises(ValueError):
                    self.sizer.size_report(design_flow_gpd=value)

    def test_old_positional_bedroom_api_fails(self):
        with self.assertRaises(TypeError):
            self.sizer.size_report(3)
        with self.assertRaises(TypeError):
            self.sizer.minimum_tank_gallons(3)

    def test_report_identifies_source_and_limits(self):
        text = self.sizer.size_report(design_flow_gpd=300).render()
        self.assertIn("Formula liquid volume: 1000 gallons", text)
        self.assertIn("TCEQ 2023 adopted text", text)
        self.assertIn("approval are not evaluated", text)
        self.assertNotIn("recommended", text.lower())


class CommandLineTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            input="", capture_output=True, text=True, timeout=10,
        )

    def test_valid_cli(self):
        result = self.run_cli("--flow-gpd", "300")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Formula liquid volume: 1000 gallons", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_invalid_cli_returns_usage_without_report_or_traceback(self):
        for args in [
            (), ("3",), ("3", "--gpd-per-bedroom", "-1"),
            ("--flow-gpd", "0"), ("--flow-gpd", "-1"),
            ("--flow-gpd", "5001"), ("--flow-gpd", "250.5"),
            ("--flow-gpd", "nan"), ("--flow-gpd", "inf"),
            ("--flow-gpd", "abc"),
        ]:
            with self.subTest(args=args):
                result = self.run_cli(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_help_is_noninteractive(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("--flow-gpd", result.stdout)


if __name__ == "__main__":
    unittest.main()
