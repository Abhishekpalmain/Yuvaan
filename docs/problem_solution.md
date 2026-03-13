# Intelli-Credit: Solving the corporate Lending "Data Paradox"

## Our Mission
In the current Indian corporate lending landscape, credit managers are overwhelmed by a "Data Paradox"—there is an abundance of information across scattered sources, yet it routinely takes weeks to process a single loan application.

We built the **Intelli-Credit Decisioning Engine** to eradicate this delay by automating the end-to-end preparation of a Comprehensive Credit Appraisal Memo (CAM).

## The Manual Bottleneck
Current manual credit appraisal is:
1.  **Slow:** Manually cross-referencing hundreds of pages of Annual Reports, GSTRs, and Bank Statements.
2.  **Prone to Bias:** Lacks consistent, data-driven frameworks for setting interest limits.
3.  **Missing Early Warning Signals:** Unstructured text (like litigation notes and RBI headwinds) is frequently overlooked.

## Our AI-Powered Solution
Our engine is built on three core pillars:
1.  **The Data Ingestor (Pillar 1):** We utilize programmatic reconciliation to cross-check self-declared **GSTR-3B** against auto-generated **GSTR-2A** to catch Input Tax Credit (ITC) inflation. We deploy Graph Neural Networks targeting bank statements to detect **Circular Trading** (shell company loops). We run targeted OCR to extract the **CIBIL Commercial Rank**.
2.  **The Research Agent (Pillar 2):** A web crawler continuously scrapes the MCA portal and e-Courts for pending litigations and aggregates macroeconomic headwinds (e.g., RBI regulations on NBFCs) relevant to the borrower's specific sector.
3.  **The Recommendation Engine (Pillar 3):** All ingested and researched data feeds into a transparent, explainable AI model (using SHAP values). The result is a fully formatted Word document—the CAM—that clearly articulates the "Five Cs of Credit", recommends an exact limit and sets an appropriate risk premium.
