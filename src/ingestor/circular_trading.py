import json
import networkx as nx
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


def detect_circular_trading(bank_file: str, company_name: str = None) -> Dict[str, Any]:
    """
    Pillar 1: Graph Analytics for Circular Trading Detection.
    Builds a directed graph of financial transactions and looks for cycles.

    Args:
        bank_file: Path to bank statement JSON file
        company_name: Name of the core company (extracted from data if None)

    Returns:
        Dictionary with detection results:
        {
            "company_name": str,
            "total_entities": int,
            "total_transactions": int,
            "cycles_detected": bool,
            "cycles": List[Dict]  # List of cycles with paths and transaction details
        }
    """
    try:
        with open(bank_file, 'r') as f:
            transactions = json.load(f)

        if company_name is None:
            company_name = "TechForge Solutions Pvt Ltd"

        logger.info(f"Starting circular trading detection for {company_name}")

        G = nx.DiGraph()

        for tx in transactions:
            desc = tx['Description'].upper()
            txn_id = tx['Transaction_ID']

            # Parse simple TO/FROM heuristic from mock data
            if "TO" in desc:
                target = desc.split("TO")[1].strip()
                G.add_edge(company_name, target, weight=tx['Withdrawal'], txn_id=txn_id)
            elif "FROM" in desc:
                source = desc.split("FROM")[1].strip()
                G.add_edge(source, company_name, weight=tx['Deposit'], txn_id=txn_id)

        logger.info(f"Graph constructed: {G.number_of_nodes()} entities, {G.number_of_edges()} transactions")

        # Find cycles (circular loops)
        cycles_info = []
        cycles_detected = False

        try:
            cycles = list(nx.simple_cycles(G))
            if cycles:
                cycles_detected = True
                logger.warning(f"Circular trading loops detected: {len(cycles)} cycle(s)")

                for cycle in cycles:
                    # Extract transaction details for this cycle
                    cycle_details = []
                    for i in range(len(cycle)):
                        src = cycle[i]
                        dst = cycle[(i + 1) % len(cycle)]
                        # Get edge data
                        if G.has_edge(src, dst):
                            edge_data = G[src][dst]
                            cycle_details.append({
                                "from": src,
                                "to": dst,
                                "amount": edge_data.get('weight', 0),
                                "transaction_id": edge_data.get('txn_id', 'N/A')
                            })

                    cycles_info.append({
                        "path": cycle,
                        "loop_length": len(cycle),
                        "transactions": cycle_details
                    })

                    cycle_path = " -> ".join(cycle) + " -> " + cycle[0]
                    logger.warning(f"Circular loop: {cycle_path}")
            else:
                logger.info("No circular trading loops detected")
        except nx.NetworkXNoCycle:
            logger.info("No circular trading loops detected")

        result = {
            "company_name": company_name,
            "total_entities": G.number_of_nodes(),
            "total_transactions": G.number_of_edges(),
            "cycles_detected": cycles_detected,
            "cycles": cycles_info
        }

        return result

    except Exception as e:
        logger.error(f"Error in circular trading detection: {str(e)}")
        raise


if __name__ == "__main__":
    import yaml
    config = yaml.safe_load(open("config.yaml"))
    result = detect_circular_trading(config['paths']['bank_statement'])

    print("\n=== CIRCULAR TRADING DETECTION RESULTS ===")
    print(f"Company: {result['company_name']}")
    print(f"Entities analyzed: {result['total_entities']}")
    print(f"Transactions processed: {result['total_transactions']}")
    print(f"Cycles detected: {result['cycles_detected']}")
    if result['cycles_detected']:
        for cycle in result['cycles']:
            print(f"  - Loop: {' -> '.join(cycle['path'])} -> {cycle['path'][0]}")
            print(f"    Transactions: {len(cycle['transactions'])}")

