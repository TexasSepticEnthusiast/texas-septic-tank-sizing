# Tank-volume formula and source reference

## Scope

This calculator evaluates one liquid-capacity formula from a stated source edition. It does not determine a home's design flow or certify a tank or septic system.

The formula comes from the septic-tank portion of **30 TAC §285.91(2), Table II**, reproduced on PDF page 103 of [TCEQ Rule Project 2021-030-285-CE, adopted in 2023](https://www.tceq.texas.gov/downloads/rules/adoptions/21030285_ado.pdf/@@download/file/21030285_ado.pdf#page=103). The section is linked to tank volume by §285.32(b)(1)(A), on PDF page 45.

## Implemented arithmetic

Q is the externally determined wastewater usage rate in gallons/day. V is liquid capacity in gallons.

| Supplied whole-number Q | Formula V |
| --- | --- |
| 1–250 | 750 |
| 251–350 | 1000 |
| 351–500 | 1250 |
| 501–1000 | 2.5 × Q |
| 1001–5000 | 1750 + 0.75 × Q |

The cited table's final band starts at 1001 without that upper endpoint; this implementation stops at 5000. The source's §285.2(44) defines an on-site sewage disposal system in part by a maximum 5000 gallons/day. Other eligibility conditions remain outside this tool.

The separate aerobic-treatment-unit table on the next source page is **not** a septic-tank liquid-volume table. This tool does not size aerobic units.

The source directs the reader to Table III for the applicable Q. It does not support the previous script's blanket 150 gpd per bedroom or its bedroom-to-tank table. Bedroom count, living area, facility type, and other applicable conditions must be considered in determining the correct design input outside this calculator.

## Numeric behavior

Only whole-gpd inputs are supported because the source lists whole-number band endpoints. Fractional flows are rejected, not silently rounded or interpolated. Formula values remain exact for supported integers: multiplying by 2.5 or 0.75 produces at most quarter-gallon increments. Displayed whole gallons use upward rounding.

Example: Q = 1001 gives V = 2500.75, and a whole-gallon display of 2501. That number is not a supplier availability claim or approval of a particular product.

## Source review

- **Source reviewed:** TCEQ 2023 adopted text, PDF pages 23, 45, 103–105.
- **Review date:** 2026-10-18.
- **Current consolidated rule:** not verified. The [Secretary of State portal](https://texas-sos.appianportalsgov.com/rules-and-meetings?interface=VIEW_TAC&part=1&title=30) did not expose readable rule text to the review tools. TCEQ's [rules page](https://www.tceq.texas.gov/rules/indxpdf.html) warns that its PDFs are not current.
- **Local orders and site approval:** not evaluated. Check the permitting authority's current requirements.

The [TCEQ system-selection page](https://www.tceq.texas.gov/permitting/ossf/ossfsystems.html) identifies septic tanks under §285.32(b)(1) and distinguishes disposal methods. A liquid-volume calculation does not select any of those methods.

## Attribution

Prepared as an AI-assisted automated contribution for Jake's [Out West Septic](https://outwestseptic.com) project. This reference makes no claim of licensed authorship, field experience, or regulatory endorsement.
