import json
import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


class ResearchAgent:
    """
    Pillar 2: Autonomous Research Agent
    Performs web-scale secondary research on companies
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.company_name = None
        self.sector = None

    def research_company(self, company_name: str, sector: str, user_notes: str = None) -> Dict[str, Any]:
        """
        Conduct comprehensive secondary research on a company

        Args:
            company_name: Name of company to research
            sector: Business sector
            user_notes: Optional qualitative notes from credit officer

        Returns:
            Dictionary with research findings
        """
        self.company_name = company_name
        self.sector = sector

        logger.info(f"Starting secondary research for {company_name} ({sector} Sector)")

        findings = {
            "company": company_name,
            "sector": sector,
            "research_timestamp": datetime.now().isoformat(),
            "sources_checked": [],
            "mca_data": {},
            "litigation_data": {},
            "sector_risks": [],
            "user_notes": user_notes,
            "overall_assessment": {}
        }

        # Check MCA portal (simulated)
        if self.config.get('research', {}).get('enable_mca_check', True):
            mca_data = self._check_mca_portal(company_name)
            findings['mca_data'] = mca_data
            findings['sources_checked'].append("MCA Portal")

        # Check e-Courts (simulated)
        if self.config.get('research', {}).get('enable_ecourts_check', True):
            litigation_data = self._check_ecourts(company_name)
            findings['litigation_data'] = litigation_data
            findings['sources_checked'].append("e-Courts")

        # Get sector headwinds
        if self.config.get('research', {}).get('enable_news_scraping', True):
            sector_risks = self._scrape_sector_news(sector)
            findings['sector_risks'] = sector_risks
            findings['sources_checked'].append("Sector News/RBI Circulars")

        # Assess risks
        findings['overall_assessment'] = self._assess_risks(findings)

        logger.info(f"Research completed: Litigation Risk={findings['overall_assessment'].get('litigation_risk')}, "
                    f"Sector Risk={findings['overall_assessment'].get('sector_risk')}")

        return findings

    def _check_mca_portal(self, company_name: str) -> Dict[str, Any]:
        """Check MCA portal for company compliance status (simulated)"""
        logger.info(f"Querying MCA portal for {company_name}")

        # Simulated MCA response
        return {
            "status": "Active, but compliance delayed",
            "delayed_filings": True,
            "annual_filing_status": "Delayed FY 2023-24",
            "director_status": "Active",
            "charges_created": "2 active charges"
        }

    def _check_ecourts(self, company_name: str) -> Dict[str, Any]:
        """Check e-Courts for litigation history (simulated)"""
        logger.info(f"Searching e-Courts for {company_name}")

        # Simulated e-Courts response
        return {
            "total_cases": 2,
            "active_cases": 2,
            "case_types": [
                {"type": "Commercial Dispute", "status": "Pending", "severity": "High"},
                {"type": "Tax Matter", "status": "Pending", "severity": "Medium"}
            ],
            "latest_case_date": "2024-02-15",
            "promoter_involved": True
        }

    def _scrape_sector_news(self, sector: str) -> List[Dict[str, Any]]:
        """Scrape news for sector-specific risks (simulated)"""
        logger.info(f"Scraping sector news for {sector}")

        # Simulated news based on sector
        sector_news_map = {
            "IT Services / Cloud": [
                {"source": "RBI Circular", "headline": "RBI tightens lending norms for NBFCs", "date": "2024-03-01", "impact": "High"},
                {"source": "Economic Times", "headline": "Cloud computing sector faces new data localization requirements", "date": "2024-02-20", "impact": "Medium"}
            ],
            "Manufacturing": [
                {"source": "RBI Circular", "headline": "New environmental compliance norms for manufacturing sector", "date": "2024-03-05", "impact": "Medium"}
            ]
        }

        return sector_news_map.get(sector, [
            {"source": "General", "headline": "RBI maintains repo rate at 6.5%", "date": "2024-02-08", "impact": "Low"}
        ])

    def _assess_risks(self, findings: Dict[str, Any]) -> Dict[str, str]:
        """Assess overall risk based on research findings"""
        # Litigation risk assessment
        litigation_cases = findings['litigation_data'].get('total_cases', 0)
        high_severity_cases = sum(1 for case in findings['litigation_data'].get('case_types', [])
                                  if case.get('severity') == 'High')
        promoter_involved = findings['litigation_data'].get('promoter_involved', False)

        if litigation_cases > 0 or promoter_involved:
            litigation_risk = "High" if high_severity_cases > 0 else "Medium-High"
        else:
            litigation_risk = "Low"

        # Sector risk assessment
        sector_risks = findings['sector_risks']
        high_impact_count = sum(1 for risk in sector_risks if risk.get('impact') == 'High')
        sector_risk = "High" if high_impact_count > 0 else "Medium"

        return {
            "litigation_risk": litigation_risk,
            "sector_risk": sector_risk,
            "has_mca_delays": findings['mca_data'].get('delayed_filings', False),
            "assessment_summary": f"Research flags {litigation_risk} litigation risk and {sector_risk} sector risk."
        }

    def save_report(self, findings: Dict[str, Any], output_path: str) -> str:
        """Save research findings to JSON file"""
        filename = f"{output_path}/{self.company_name.replace(' ', '_')}_Research_Report.json"
        with open(filename, 'w') as f:
            json.dump(findings, f, indent=2)
        logger.info(f"Research report saved to {filename}")
        return filename


def synthesize_secondary_research(company_name: str, sector: str, config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Main entry point for research agent (backward compatibility)

    Args:
        company_name: Name of company
        sector: Business sector
        config_path: Path to config file

    Returns:
        Research findings dictionary
    """
    import yaml
    config = yaml.safe_load(open(config_path))

    agent = ResearchAgent(config)
    findings = agent.research_company(company_name, sector)
    agent.save_report(findings, config['paths']['output_dir'])

    return findings


if __name__ == "__main__":
    import yaml
    config = yaml.safe_load(open("config.yaml"))
    agent = ResearchAgent(config)
    findings = agent.research_company(
        config['company']['name'],
        config['company']['sector']
    )
    agent.save_report(findings, config['paths']['output_dir'])

    print(json.dumps(findings, indent=2))

