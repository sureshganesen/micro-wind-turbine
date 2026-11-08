"""
Unit and Aerodynamic Verification Tests for Micro Wind Turbine Harvester
Author: Suresh Ganesen (Politeknik Malaysia / Atom Forge Studio)
"""

import unittest
import math
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "aerodynamics")))
from wind_power_analysis import (
    calculate_power,
    AIR_DENSITY,
    ROTOR_RADIUS,
    SWEPT_AREA,
    AERODYNAMIC_CP,
    BETZ_LIMIT,
    CUT_IN_SPEED,
    CUT_OUT_SPEED,
)


class TestWindTurbineAerodynamics(unittest.TestCase):
    def test_swept_area_geometry(self):
        """Verify rotor area complies with ⌀420 mm envelope (0.1385 m^2)."""
        expected_area = math.pi * (0.210 ** 2)
        self.assertAlmostEqual(SWEPT_AREA, expected_area, places=4)
        self.assertAlmostEqual(SWEPT_AREA, 0.1385, delta=0.001)

    def test_cut_in_speed_boundary(self):
        """Verify turbine produces 0W below 2.2 m/s and begins positive generation at >= 2.2 m/s."""
        sub_cut_in = calculate_power(2.0)
        self.assertEqual(sub_cut_in["p_mech"], 0.0)
        self.assertEqual(sub_cut_in["p_elec"], 0.0)
        self.assertEqual(sub_cut_in["status"], "SUB-CUT-IN (STATIC)")

        at_cut_in = calculate_power(2.2)
        self.assertGreater(at_cut_in["p_mech"], 0.0)
        self.assertGreater(at_cut_in["p_elec"], 0.0)
        self.assertEqual(at_cut_in["status"], "ACTIVE HARVESTING")

    def test_betz_law_compliance(self):
        """Verify power coefficient never exceeds the physical theoretical Betz limit (59.26%)."""
        for v in [3.0, 5.0, 8.0, 10.0]:
            p = calculate_power(v)
            self.assertLess(p["p_mech"], p["p_betz"])
            ratio = p["p_mech"] / p["p_wind"]
            self.assertAlmostEqual(ratio, AERODYNAMIC_CP, places=3)
            self.assertLess(ratio, BETZ_LIMIT)

    def test_cut_out_furling(self):
        """Verify aerodynamic protection halts generation above 14.0 m/s."""
        over_speed = calculate_power(15.0)
        self.assertEqual(over_speed["p_mech"], 0.0)
        self.assertEqual(over_speed["status"], "CUT-OUT (FURLING)")

    def test_rated_output_power(self):
        """Verify electrical output at rated wind speed generates suitable 5V charging current."""
        rated = calculate_power(8.5)
        self.assertGreater(rated["current_5v_ma"], 350.0)
        self.assertAlmostEqual(rated["p_elec"], 8.496, delta=0.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
