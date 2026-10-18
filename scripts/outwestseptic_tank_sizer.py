"""Educational septic-tank liquid-volume arithmetic from a supplied design flow.

Source: TCEQ 2023 adopted rule, 30 TAC 285.91(2), Table II, septic-tank
portion. See the repository documentation for source and scope limitations.
This automated contribution is for Jake's Out West Septic project.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass


def _validate_flow(design_flow_gpd: int) -> int:
    """Accept only whole-gpd inputs inside this calculator's stated scope."""
    if isinstance(design_flow_gpd, bool) or not isinstance(design_flow_gpd, int):
        raise ValueError("Design flow must be a whole number of gallons per day.")
    if not 1 <= design_flow_gpd <= 5000:
        raise ValueError("Design flow must be between 1 and 5000 gpd.")
    return design_flow_gpd


class OutWestSepticTankSizer:
    """Apply the cited tank-volume formula; do not determine design flow."""

    def minimum_tank_gallons(self, *, design_flow_gpd: int) -> float:
        """Return formula liquid volume, before rounding, in gallons.

        A named flow argument prevents old bedroom-based calls from silently
        being treated as gallons/day. Fractional flows are deliberately rejected:
        the published table labels its bands with whole-gpd endpoints.
        """
        flow = _validate_flow(design_flow_gpd)
        if flow <= 250:
            return 750.0
        if flow <= 350:
            return 1000.0
        if flow <= 500:
            return 1250.0
        if flow <= 1000:
            return 2.5 * flow
        return 1750.0 + 0.75 * flow

    def size_report(self, *, design_flow_gpd: int) -> "OutWestSepticTankSizeReport":
        minimum = self.minimum_tank_gallons(design_flow_gpd=design_flow_gpd)
        return OutWestSepticTankSizeReport(
            design_flow_gpd=design_flow_gpd,
            formula_liquid_gallons=minimum,
            rounded_liquid_gallons=math.ceil(minimum),
        )


@dataclass(frozen=True)
class OutWestSepticTankSizeReport:
    design_flow_gpd: int
    formula_liquid_gallons: float
    rounded_liquid_gallons: int

    def render(self) -> str:
        return "\n".join([
            "Out West Septic project - Educational tank-volume calculation",
            f"Supplied design flow: {self.design_flow_gpd} gpd",
            f"Formula liquid volume: {self.formula_liquid_gallons:g} gallons",
            f"Rounded up to whole gallons: {self.rounded_liquid_gallons} gallons",
            "Method: 30 TAC 285.91(2), Table II (TCEQ 2023 adopted text).",
            "Flow selection, tank model, construction, and site approval are not evaluated.",
            "Verify current rules and local requirements with the permitting authority.",
        ])


# Preserve the previous report type import for existing callers.
TankSizeReport = OutWestSepticTankSizeReport


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="outwestseptic_tank_sizer",
        description="Educational tank-volume arithmetic from an externally determined flow.",
        epilog="This does not select design flow or establish site approval or compliance.",
        allow_abbrev=False,
    )
    parser.add_argument(
        "--flow-gpd", type=int, required=True,
        help="Externally determined design flow, a whole number from 1 to 5000 gpd.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    try:
        report = OutWestSepticTankSizer().size_report(design_flow_gpd=args.flow_gpd)
    except ValueError as error:
        parser.error(str(error))
    print(report.render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
