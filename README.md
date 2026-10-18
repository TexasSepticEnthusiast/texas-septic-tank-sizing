# Texas Septic Tank Sizing

An educational Python calculator for the liquid-volume formula in TCEQ's **2023 adopted text** of 30 TAC §285.91(2), Table II. Supply a design flow that has already been determined for the project; the calculator does not infer it from bedrooms.

This is an AI-assisted automated contribution for Jake's [Out West Septic](https://outwestseptic.com) project. It is project-affiliated educational software, not an independent endorsement, licensed design, or statement of permit approval.

## Run it

Python 3.10 or newer; no third-party packages.

```bash
git clone https://github.com/TexasSepticEnthusiast/texas-septic-tank-sizing.git
cd texas-septic-tank-sizing
python scripts/outwestseptic_tank_sizer.py --flow-gpd 300
```

```text
Out West Septic project - Educational tank-volume calculation
Supplied design flow: 300 gpd
Formula liquid volume: 1000 gallons
Rounded up to whole gallons: 1000 gallons
Method: 30 TAC 285.91(2), Table II (TCEQ 2023 adopted text).
Flow selection, tank model, construction, and site approval are not evaluated.
Verify current rules and local requirements with the permitting authority.
```

The 300 gpd input demonstrates arithmetic; it is not a flow assignment for a particular home.

## Inputs and results

- `--flow-gpd` is required and must be a whole number from 1 through 5000.
- The result includes the formula's liquid volume and that volume rounded **up** to whole gallons. For example, 501 gpd gives 1252.5 gallons, displayed also as 1253 whole gallons.
- Rounding is a reporting convention, not a recommendation of a commercially available tank.
- Missing, invalid, fractional, nonfinite, or out-of-scope values exit with status 2 and an error message. The tool does not prompt or emit a sizing report on failure.

The published table uses whole-gpd band endpoints (250/251, 350/351, and so on). This tool deliberately rejects fractional flows rather than invent an interpretation between those endpoints. It does not round a supplied flow. The 5000 gpd scope is a software boundary; accepting a flow does not establish eligibility under Chapter 285.

## Python API

```python
from scripts.outwestseptic_tank_sizer import OutWestSepticTankSizer

report = OutWestSepticTankSizer().size_report(design_flow_gpd=300)
print(report.formula_liquid_gallons)  # 1000.0
print(report.rounded_liquid_gallons)  # 1000
```

The API accepts an integer flow through a required keyword argument. Booleans and floating-point values are rejected.

## What this cannot determine

Obtain the applicable wastewater usage rate from the relevant planning process and confirm it with the permitting authority. Tank construction, compartments, liquid depth, treatment type, wastewater strength, site evaluation, disposal sizing, local orders, setbacks, and permitting remain outside the calculation.

See the [formula and source reference](wiki/Tank-Sizing-Reference.md). TCEQ's [system selection guidance](https://www.tceq.texas.gov/permitting/ossf/ossfsystems.html) shows why treatment and disposal choices require additional site information.

## Migration from the previous interface

The positional bedroom argument, `--gpd-per-bedroom`, bedroom table, and stock-size recommendation were removed. A bedroom count alone does not justify the old claimed TCEQ formula. Old invocations intentionally fail; callers must obtain a design flow and use `--flow-gpd`. The class name is retained, but calculation methods now require `design_flow_gpd=`.

Seed issue/PR files that claimed unverified field experience or completed changes were removed.

## Verify changes

```bash
python -m unittest discover -s tests -v
```

Tests cover every formula transition, all 5000 supported integer flows, rounding, invalid API inputs, and command-line success and failure. GitHub Actions runs the suite on Python 3.10 and 3.13 when enabled.

## Source status and license

Reviewed against the [TCEQ 2023 adoption document](https://www.tceq.texas.gov/downloads/rules/adoptions/21030285_ado.pdf/@@download/file/21030285_ado.pdf#page=103) on 2026-10-18. This is a source-edition check, **not verification of the current consolidated rule**. TCEQ [warns that its rule PDFs are not current](https://www.tceq.texas.gov/rules/indxpdf.html) and directs readers to the Secretary of State. Recheck the current rule and local requirements before project use.

MIT; see [LICENSE](LICENSE). Existing copyright attribution is retained.
