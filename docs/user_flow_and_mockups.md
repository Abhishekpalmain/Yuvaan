# Intelli-Credit: User Flow & Mockups

The core end-user of our system is the **Credit Officer** at a mid-sized Indian corporate bank. 

## The Current User Flow (Manual)
1.  Officer receives a massive ZIP file of PDFs (Annual Reports, CIBIL) and Excel sheets (GST, Bank Statements).
2.  Spends 2 weeks manually reading, cross-referencing GST against Bank ledgers, and googling for MCA litigation history.
3.  Writes a subjective Credit Appraisal Memo (CAM) in Word.

## The Intelli-Credit User Flow (AI-Powered)

### Step 1: Bulk Ingestion
The Credit Officer accesses the Intelli-Credit Portal and drags-and-drops the client files.
*Behind the scenes:* Databricks spinning up OCR (CIBIL extraction) and Graph Analytics (Circular Trading Detection).

### Step 2: The Research Agent Dashboard
The Officer opens the dashboard. Instead of raw files, they are presented with an interactive summary.
*   **Alert:** "⚠️ GSTR-3B ITC Claim exceeds GSTR-2A supplier filings by INR 1,50,000."
*   **Alert:** "⚠️ Circular trading loop detected: Entity -> ShellCorp -> Entity."
*   **News:** "RBI tightens NBFC metrics (Found via Web Sandbox)."

### Step 3: Primary Insight Input
The Officer can augment the AI. They click "Add Field Note" and type: *"Visited the factory. Operations look slow, running at only 40% capacity."*
*Behind the scenes:* This unstructured text is passed to the LLM, which dynamically adjusts the Capacity score downward.

### Step 4: CAM Generation & Explainable Decision
The Officer clicks "Generate Final CAM".
The Engine downloads a fully formatted Word document. The document explicitly explains the exact reasoning for the ML model's rating, providing a recommended loan limit and risk premium rate, fully documented in our XAI (Explainable AI) trace logs.
