# Intelli-Credit: Technical Architecture

Our prototype is defined by a deep understanding of Indian-context financial nuance, backed by robust data engineering pipelines.

## The End-to-End Pipeline

```mermaid
graph TD
    %% Define Data Sources
    A1[Unstructured Docs: Annual Reports, CIBIL] --> B
    A2[Structured Data: GSTR-2A, GSTR-3B] --> B
    A3[Bank Transaction Ledgers] --> B
    
    %% Pillar 1: Ingestor
    subgraph Pillar 1: Data Ingestor
        B[Databricks Ingestion Layer]
        B --> C1[OCR Pipeline & PDF Parsing]
        B --> C2[GSTR-2A/3B Reconciliation Engine]
        B --> C3[Graph Analytics: Circular Trading Detection]
    end
    
    %% Pillar 2: Research
    subgraph Pillar 2: Web Research Agent
        R1[Scraping: MCA Portal / e-Courts] --> D[LLM Insight Synthesizer]
        R2[RBI News & Sector Headwinds] --> D
        R3[Credit Officer UI Portal] --> D
    end
    
    %% Aggregation
    C1 --> E[Unified Financial Knowledge Graph]
    C2 --> E
    C3 --> E
    D --> E
    
    %% Pillar 3: Recommendation
    subgraph Pillar 3: Recommendation Engine
        E --> F[XGBoost Risk Scoring Model]
        F --> G[Explainable AI Layer using SHAP]
        G --> H{Final Decision Logic: Limit & Rate}
    end
    
    %% Output
    H --> I[Automated Word/PDF CAM Generator]
    
    classDef highlight fill:#f9f,stroke:#333,stroke-width:2px;
    class I highlight;
```

## System Components

-   **Data Processing:** We rely on Databricks to handle high-latency pipelines and massive unstructured document stores.
-   **Graph Analytics:** Circular trading and shell company relations are identified using `networkx` to build directed graphs of bank transfers.
-   **Explainable ML:** We bypass "Black Box AI" by implementing explicit deduction rules (simulating SHAP values) that attach English sentences (e.g., "Deduction: GST 3B claims exceed 2A") to every point subtracted from the base credit score.
-   **Documentation Assembly:** The `python-docx` library programmatic compiles the finalized "Five Cs of Credit" into the industry-standard Credit Appraisal Memo.
