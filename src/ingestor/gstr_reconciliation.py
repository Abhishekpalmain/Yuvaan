import json
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


def flag_gst_discrepancies(gst_file: str) -> Dict[str, Any]:
    """
    Pillar 1: Structured Synthesis.
    Cross-references GSTR-3B (claimed) against GSTR-2A (auto-populated).

    Returns:
        Dictionary with reconciliation results:
        {
            "company_name": str,
            "discrepancies": List[str],
            "summary": {
                "claimed_igst": float,
                "actual_igst": float,
                "discrepancy_amount": float,
                "has_discrepancy": bool
            }
        }
    """
    try:
        with open(gst_file, 'r') as f:
            data = json.load(f)

        company_name = data.get('Legal_Name', 'Unknown')
        logger.info(f"Starting GST reconciliation for {company_name}")

        claimed_itc = data['GSTR_3B_Summary']['Total_ITC_Available']
        total_claimed_igst = claimed_itc['IGST']
        total_claimed_cgst = claimed_itc['CGST']
        total_claimed_sgst = claimed_itc['SGST']

        # Calculate actual ITC from 2A invoices
        actual_igst = sum(inv['IGST'] for inv in data['GSTR_2A_B2B_Invoices'])
        actual_cgst = sum(inv['CGST'] for inv in data['GSTR_2A_B2B_Invoices'])
        actual_sgst = sum(inv['SGST'] for inv in data['GSTR_2A_B2B_Invoices'])

        discrepancies = []

        # Check IGST
        if total_claimed_igst > actual_igst:
            diff = total_claimed_igst - actual_igst
            msg = f"Overclaimed IGST by INR {diff:,}. High risk of penal action."
            discrepancies.append({
                "type": "igst_overclaim",
                "claimed": total_claimed_igst,
                "actual": actual_igst,
                "difference": diff,
                "severity": "HIGH",
                "message": msg
            })
            logger.warning(f"GST Discrepancy: {msg}")
        else:
            logger.info("IGST claims are fully backed by GSTR-2A")

        # Check CGST
        if total_claimed_cgst > actual_cgst:
            diff = total_claimed_cgst - actual_cgst
            msg = f"Overclaimed CGST by INR {diff:,}. Potential tax evasion."
            discrepancies.append({
                "type": "cgst_overclaim",
                "claimed": total_claimed_cgst,
                "actual": actual_cgst,
                "difference": diff,
                "severity": "HIGH",
                "message": msg
            })
            logger.warning(msg)

        # Check SGST
        if total_claimed_sgst > actual_sgst:
            diff = total_claimed_sgst - actual_sgst
            msg = f"Overclaimed SGST by INR {diff:,}. Potential tax evasion."
            discrepancies.append({
                "type": "sgst_overclaim",
                "claimed": total_claimed_sgst,
                "actual": actual_sgst,
                "difference": diff,
                "severity": "HIGH",
                "message": msg
            })
            logger.warning(msg)

        result = {
            "company_name": company_name,
            "discrepancies": discrepancies,
            "summary": {
                "claimed_igst": total_claimed_igst,
                "actual_igst": actual_igst,
                "claimed_cgst": total_claimed_cgst,
                "actual_cgst": actual_cgst,
                "claimed_sgst": total_claimed_sgst,
                "actual_sgst": actual_sgst,
                "has_discrepancy": len(discrepancies) > 0
            }
        }

        logger.info(f"GST reconciliation completed: {len(discrepancies)} discrepancies found")
        return result

    except Exception as e:
        logger.error(f"Error in GST reconciliation: {str(e)}")
        raise


if __name__ == "__main__":
    import yaml

    config = yaml.safe_load(open("config.yaml"))
    result = flag_gst_discrepancies(config['paths']['gst_data'])

    print("\n=== GST RECONCILIATION RESULTS ===")
    print(f"Company: {result['company_name']}")
    print(f"Discrepancies Found: {len(result['discrepancies'])}")
    for disc in result['discrepancies']:
        print(f"  - {disc['message']}")

