# How Intelli-Credit Meets the Evaluation Criteria

Our solution was built *specifically* to address the nuanced challenges of the Indian corporate lending landscape outlined in the hackathon prompt.

### 1. Extraction Accuracy (Messy Indian PDFs)
Rather than relying on basic OCR, our pipeline is tuned for specific commercial templates.
-   **Targeted CIBIL Extraction:** We utilize structured keyword bounding boxes to cleanly pull the "CIBIL Rank" (1-10) directly out of scanned commercial credit reports, ensuring the Recommendation engine operates on near-perfect base data.

### 2. Research Depth (Beyond Provided Files)
Our "Digital Credit Manager" operates autonomously on the web.
-   **MCA and e-Courts Integration:** Our agent actively searches external portals to cross-reference the entity name against pending litigation, moving beyond the provided PDF sanctions.
-   **Macro-Headwinds:** We query real-time sector news (e.g., "RBI regulations on NBFCs") to dynamically adjust the systemic risk associated with the borrower's industry.

### 3. Explainability ("Walking the Judge Through the Logic")
Our Recommendation Engine is entirely transparent; it is not a black box.
-   Every single score deduction or addition is accompanied by a plain English explanation in the final CAM.
-   **Example:** If a loan is rejected, the generated CAM will explicitly print: `"REJECT: Despite strong GST flows, high litigation risk found in e-Courts secondary research, combined with a Circular Trading loop detected in Bank Statement TXN9902."`

### 4. Indian Context Sensitivity
This is our primary differentiator. We do not just pass text to an LLM; we built programmatic checks for Indian financial mechanisms:
-   **GSTR-2A vs 3B Reconciliation:** We wrote specific Python scripts that automatically compare the theoretically available Input Tax Credit (auto-populated by suppliers in 2A) against the actively claimed ITC (self-declared by the borrower in 3B). Any over-claim is immediately flagged to prevent tax evasion lending.
-   **Circular Trading Loops:** Using graph analytics in Python, we map RTGS/NEFT transfers to detect instances where money is sent to "ShellCorp Consultants" only to immediately return through "ShellCorp Holdings"—a common Indian tactic to artificially inflate bank balances.
