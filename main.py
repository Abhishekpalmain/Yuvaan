#!/usr/bin/env python3
"""
Intelli-Credit: AI-Powered Corporate Credit Decisioning Engine

This is the main orchestrator that runs all three pillars of the system:
1. Pillar 1: Data Ingestor (GST Reconciliation + Circular Trading Detection)
2. Pillar 2: Research Agent (Secondary Research)
3. Pillar 3: Recommendation Engine (CAM Generation)

Usage:
    python main.py                        # Run complete pipeline
    python main.py --step pillar1         # Run only Pillar 1
    python main.py --step pillar2         # Run only Pillar 2
    python main.py --step pillar3         # Run only Pillar 3
    python main.py --config custom.yaml  # Use custom config
"""

import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils import load_config, setup_logging
from src.ingestor.gstr_reconciliation import flag_gst_discrepancies
from src.ingestor.circular_trading import detect_circular_trading
from src.research_agent.research_scraper import ResearchAgent
from src.recommendation_engine.generate_cam import RecommendationEngine


class IntelliCreditPipeline:
    """Main Pipeline Orchestrator"""

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize pipeline with configuration"""
        self.config = load_config(config_path)
        self.logger = setup_logging(
            log_level=self.config.get('logging', {}).get('level', 'INFO'),
            log_file=self.config.get('logging', {}).get('file')
        )
        self.results = {}

        # Ensure required directories exist
        self._ensure_directories()

    def _ensure_directories(self):
        """Create required directories if they don't exist"""
        required_dirs = [
            self.config['paths'].get('output_dir', 'data'),
            self.config['paths'].get('logs_dir', 'logs')
        ]
        for dir_path in required_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Ensured directory exists: {dir_path}")

    def run_pillar1(self) -> Dict[str, Any]:
        """
        Run Pillar 1: Data Ingestor
        - GST Reconciliation
        - Circular Trading Detection
        """
        self.logger.info("=" * 60)
        self.logger.info("STARTING PILLAR 1: DATA INGESTOR")
        self.logger.info("=" * 60)

        pillar1_results = {}

        # 1. GST Reconciliation
        self.logger.info("\n[1/2] Running GST Reconciliation...")
        try:
            gst_result = flag_gst_discrepancies(self.config['paths']['gst_data'])
            pillar1_results['gst_reconciliation'] = gst_result
            self.logger.info(f"[OK] GST Reconciliation complete: {len(gst_result['discrepancies'])} discrepancies found")
        except Exception as e:
            self.logger.error(f"[FAIL] GST Reconciliation failed: {str(e)}")
            pillar1_results['gst_reconciliation'] = {"error": str(e)}

        # 2. Circular Trading Detection
        self.logger.info("\n[2/2] Running Circular Trading Detection...")
        try:
            circular_result = detect_circular_trading(
                self.config['paths']['bank_statement'],
                self.config['company']['name']
            )
            pillar1_results['circular_trading'] = circular_result
            cycles_count = len(circular_result.get('cycles', []))
            self.logger.info(f"[OK] Circular Trading Detection complete: {cycles_count} cycle(s) detected")
        except Exception as e:
            self.logger.error(f"[FAIL] Circular Trading Detection failed: {str(e)}")
            pillar1_results['circular_trading'] = {"error": str(e)}

        self.results['pillar1'] = pillar1_results
        self.logger.info("\n" + "=" * 60)
        self.logger.info("PILLAR 1 COMPLETE")
        self.logger.info("=" * 60)

        return pillar1_results

    def run_pillar2(self) -> Dict[str, Any]:
        """
        Run Pillar 2: Research Agent
        - Web Scraping (MCA, e-Courts, News)
        - Secondary Research Synthesis
        """
        self.logger.info("=" * 60)
        self.logger.info("STARTING PILLAR 2: RESEARCH AGENT")
        self.logger.info("=" * 60)

        try:
            agent = ResearchAgent(self.config)

            self.logger.info(f"Researching: {self.config['company']['name']}")
            findings = agent.research_company(
                company_name=self.config['company']['name'],
                sector=self.config['company']['sector']
            )

            # Save report
            report_path = agent.save_report(findings, self.config['paths']['output_dir'])
            self.results['pillar2'] = findings

            self.logger.info("[OK] Research complete")
            self.logger.info(f"  - Litigation Risk: {findings['overall_assessment']['litigation_risk']}")
            self.logger.info(f"  - Sector Risk: {findings['overall_assessment']['sector_risk']}")
            self.logger.info(f"  - Report saved: {report_path}")

        except Exception as e:
            self.logger.error(f"[FAIL] Research Agent failed: {str(e)}")
            self.results['pillar2'] = {"error": str(e)}

        self.logger.info("\n" + "=" * 60)
        self.logger.info("PILLAR 2 COMPLETE")
        self.logger.info("=" * 60)

        return self.results.get('pillar2', {})

    def run_pillar3(self,
                    gst_results: Dict[str, Any] = None,
                    circular_results: Dict[str, Any] = None,
                    research_results: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run Pillar 3: Recommendation Engine
        - Synthesize all inputs
        - Generate explainable score
        - Create CAM document
        """
        self.logger.info("=" * 60)
        self.logger.info("STARTING PILLAR 3: RECOMMENDATION ENGINE")
        self.logger.info("=" * 60)

        try:
            engine = RecommendationEngine(self.config)

            # Extract CIBIL rank (mock - would come from extracted PDF in real system)
            # For demo, we'll use a default or try to get from somewhere
            cibil_rank = 4  # Default for TechForge demo

            self.logger.info("Evaluating application...")
            evaluation = engine.evaluate(
                company_name=self.config['company']['name'],
                gst_results=gst_results,
                circular_results=circular_results,
                cibil_rank=cibil_rank,
                research_findings=research_results
            )

            # Generate CAM document
            doc_path = engine.generate_cam_document(evaluation)

            self.results['pillar3'] = evaluation
            self.results['cam_path'] = doc_path

            self.logger.info("[OK] Evaluation complete")
            self.logger.info(f"  - Final Score: {evaluation['final_score']}/100")
            self.logger.info(f"  - Recommendation: {evaluation['recommendation']}")
            self.logger.info(f"  - CAM Document: {doc_path}")

        except Exception as e:
            self.logger.error(f"[FAIL] Recommendation Engine failed: {str(e)}")
            self.results['pillar3'] = {"error": str(e)}

        self.logger.info("\n" + "=" * 60)
        self.logger.info("PILLAR 3 COMPLETE")
        self.logger.info("=" * 60)

        return self.results.get('pillar3', {})

    def run_full_pipeline(self) -> Dict[str, Any]:
        """
        Run complete Intelli-Credit pipeline (all 3 pillars)
        """
        self.logger.info("=" * 60)
        self.logger.info("INTELLI-CREDIT PIPELINE - FULL EXECUTION")
        self.logger.info(f"Company: {self.config['company']['name']}")
        self.logger.info(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info("=" * 60)

        # Run Pillar 1
        pillar1_results = self.run_pillar1()

        # Run Pillar 2
        pillar2_results = self.run_pillar2()

        # Run Pillar 3 (needs results from 1 & 2)
        pillar3_results = self.run_pillar3(
            gst_results=pillar1_results.get('gst_reconciliation'),
            circular_results=pillar1_results.get('circular_trading'),
            research_results=pillar2_results
        )

        # Generate final summary
        self._print_final_summary()

        return self.results

    def _print_final_summary(self):
        """Print final summary report"""
        self.logger.info("\n" + "=" * 60)
        self.logger.info("FINAL SUMMARY")
        self.logger.info("=" * 60)

        pillar3 = self.results.get('pillar3', {})

        if pillar3:
            self.logger.info(f"\nCompany: {self.config['company']['name']}")
            self.logger.info(f"Final Credit Score: {pillar3.get('final_score', 'N/A')}/100")
            self.logger.info(f"Recommendation: {pillar3.get('recommendation', 'N/A')}")
            self.logger.info(f"Suggested Limit: {pillar3.get('credit_limit', 'N/A')}")
            self.logger.info(f"Interest Rate: {pillar3.get('interest_rate', 'N/A')}")
            self.logger.info(f"CAM Document: {self.results.get('cam_path', 'N/A')}")

            risk_factors = pillar3.get('risk_factors', [])
            if risk_factors:
                self.logger.info(f"\nRisk Factors ({len(risk_factors)}):")
                for rf in risk_factors:
                    self.logger.info(f"  - {rf}")

            adjustments = pillar3.get('adjustments', [])
            if adjustments:
                self.logger.info(f"\nScore Adjustments ({len(adjustments)}):")
                total_adjustment = sum(adj['value'] for adj in adjustments)
                self.logger.info(f"  Base Score: {pillar3.get('base_score', 80)}")
                self.logger.info(f"  Total Adjustment: {total_adjustment:+d}")
                self.logger.info(f"  Final Score: {pillar3.get('final_score', 'N/A')}")

        self.logger.info("\n" + "=" * 60)
        self.logger.info("PIPELINE EXECUTION COMPLETE")
        self.logger.info("=" * 60)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Intelli-Credit: AI-Powered Corporate Credit Decisioning Engine"
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    parser.add_argument(
        '--step',
        type=str,
        choices=['pillar1', 'pillar2', 'pillar3', 'all'],
        default='all',
        help='Which pipeline step to run (default: all)'
    )
    parser.add_argument(
        '--output-json',
        type=str,
        help='Save complete results to JSON file'
    )

    args = parser.parse_args()

    try:
        pipeline = IntelliCreditPipeline(args.config)

        if args.step == 'all':
            results = pipeline.run_full_pipeline()
        elif args.step == 'pillar1':
            results = pipeline.run_pillar1()
        elif args.step == 'pillar2':
            results = pipeline.run_pillar2()
        elif args.step == 'pillar3':
            # Need results from previous pillars
            results = pipeline.run_pillar3()
        else:
            results = {}

        # Save to JSON if requested
        if args.output_json:
            with open(args.output_json, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n[OK] Results saved to: {args.output_json}")

    except FileNotFoundError as e:
        print(f"[FAIL] Error: Configuration file not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[FAIL] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
