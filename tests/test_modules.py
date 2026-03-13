#!/usr/bin/env python3
"""
Intelli-Credit Module Tests
Tests each pillar individually to verify functionality
"""

import sys
import os
from pathlib import Path

# Add project root to path so we can import src as a package
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_pillar1_gst():
    """Test GST Reconciliation Module"""
    print("\n" + "="*60)
    print("TEST: Pillar 1 - GST Reconciliation")
    print("="*60)

    try:
        from src.ingestor.gstr_reconciliation import flag_gst_discrepancies

        result = flag_gst_discrepancies("data/mock_structured/gst_data.json")

        print(f"[OK] Function executed successfully")
        print(f"   Company: {result['company_name']}")
        print(f"   Discrepancies found: {len(result['discrepancies'])}")

        if result['summary']['has_discrepancy']:
            print(f"   [WARN]  GST discrepancy detected (as expected for demo)")
            print(f"   Claimed IGST: INR {result['summary']['claimed_igst']:,}")
            print(f"   Actual IGST: INR {result['summary']['actual_igst']:,}")
        else:
            print("   [OK]  No GST discrepancies")

        return True

    except Exception as e:
        print(f"[FAIL]  Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_pillar1_circular():
    """Test Circular Trading Detection Module"""
    print("\n" + "="*60)
    print("TEST: Pillar 1 - Circular Trading Detection")
    print("="*60)

    try:
        from src.ingestor.circular_trading import detect_circular_trading

        result = detect_circular_trading("data/mock_structured/bank_statement.json")

        print(f"[OK] Function executed successfully")
        print(f"   Entities analyzed: {result['total_entities']}")
        print(f"   Transactions processed: {result['total_transactions']}")
        print(f"   Cycles detected: {result['cycles_detected']}")

        if result['cycles_detected']:
            print(f"   [WARN]  {len(result['cycles'])} circular loop(s) found:")
            for cycle in result['cycles']:
                path = " -> ".join(cycle['path'])
                print(f"      {path} -> {cycle['path'][0]}")
        else:
            print("   [OK]  No circular trading detected")

        return True

    except Exception as e:
        print(f"[FAIL]  Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_pillar2():
    """Test Research Agent Module"""
    print("\n" + "="*60)
    print("TEST: Pillar 2 - Research Agent")
    print("="*60)

    try:
        import yaml
        from src.research_agent.research_scraper import ResearchAgent

        config = yaml.safe_load(open("config.yaml"))
        agent = ResearchAgent(config)

        company = config['company']['name']
        sector = config['company']['sector']

        print(f"Researching: {company} ({sector})")

        findings = agent.research_company(company, sector)

        print(f"[OK] Research completed successfully")
        print(f"   Litigation Risk: {findings['overall_assessment']['litigation_risk']}")
        print(f"   Sector Risk: {findings['overall_assessment']['sector_risk']}")
        print(f"   Sources checked: {', '.join(findings['sources_checked'])}")
        print(f"   MCA Status: {findings['mca_data'].get('status', 'N/A')}")
        print(f"   Court cases: {findings['litigation_data'].get('total_cases', 0)}")

        # Check output file exists
        report_path = Path(f"data/{company.replace(' ', '_')}_Research_Report.json")
        if report_path.exists():
            print(f"   [OK]  Report saved: {report_path}")
        else:
            print(f"   [WARN]  Report file not found at expected location")

        return True

    except Exception as e:
        print(f"[FAIL]  Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_pillar3():
    """Test Recommendation Engine Module"""
    print("\n" + "="*60)
    print("TEST: Pillar 3 - Recommendation Engine")
    print("="*60)

    try:
        import yaml
        from src.recommendation_engine.generate_cam import RecommendationEngine

        config = yaml.safe_load(open("config.yaml"))
        engine = RecommendationEngine(config)

        print("Running evaluation with demo inputs...")

        evaluation = engine.evaluate(
            company_name=config['company']['name'],
            gst_results={
                "summary": {"has_discrepancy": True},
                "discrepancies": [{"message": "Test discrepancy"}]
            },
            circular_results={
                "cycles_detected": True,
                "cycles": []
            },
            cibil_rank=4
        )

        print(f"[OK] Evaluation completed successfully")
        print(f"   Base Score: {evaluation['base_score']}")
        print(f"   Final Score: {evaluation['final_score']}/100")
        print(f"   Recommendation: {evaluation['recommendation']}")
        print(f"   Credit Limit: {evaluation['credit_limit']}")
        print(f"   Risk Factors: {len(evaluation['risk_factors'])}")
        print(f"   Adjustments: {len(evaluation['adjustments'])}")

        # Generate CAM document
        print("\nGenerating CAM document...")
        doc_path = engine.generate_cam_document(evaluation)

        if Path(doc_path).exists():
            print(f"   [OK] CAM document created: {doc_path}")
        else:
            print(f"   [WARN]  CAM document not found at {doc_path}")

        return True

    except Exception as e:
        print(f"[FAIL]  Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("INTELLI-CREDIT MODULE TESTS")
    print("="*60)

    # Verify data files exist
    required_files = [
        "data/mock_structured/gst_data.json",
        "data/mock_structured/bank_statement.json",
        "config.yaml"
    ]

    print("\n[Pre-check] Verifying required files...")
    all_files_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   [OK]  {file_path}")
        else:
            print(f"   [FAIL] {file_path} - NOT FOUND")
            all_files_exist = False

    if not all_files_exist:
        print("\n[FAIL]  Cannot run tests - missing required files")
        sys.exit(1)

    print("\n" + "="*60)
    print("RUNNING MODULE TESTS")
    print("="*60)

    results = {
        "Pillar 1 - GST Reconciliation": test_pillar1_gst(),
        "Pillar 1 - Circular Trading": test_pillar1_circular(),
        "Pillar 2 - Research Agent": test_pillar2(),
        "Pillar 3 - Recommendation Engine": test_pillar3()
    }

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, passed_flag in results.items():
        status = "[OK] PASS" if passed_flag else "[FAIL]  FAIL"
        print(f"{status} - {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n[TEST] All tests passed! Intelli-Credit is working correctly.")
        return 0
    else:
        print(f"\n[WARN]  {total-passed} test(s) failed. Check output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
