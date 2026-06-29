# ClauseGuard AI — Helper Utilities
import re

def calculate_reading_time(text):
    """
    Calculates estimated reading time in minutes based on 200 WPM.
    """
    words = len(re.findall(r'\w+', text))
    minutes = max(1, round(words / 200))
    return minutes

def map_risk_score_to_label(score):
    """
    Maps numerical risk score (0-100) to risk level and descriptions.
    """
    if score >= 76:
        return "CRITICAL RISK", "Extreme vulnerabilities. High possibility of legal dispute and financial loss. Do not sign."
    elif score >= 51:
        return "HIGH RISK", "Significant risks detected. Sign with caution and negotiate major terms."
    elif score >= 26:
        return "MEDIUM RISK", "Moderate risk clauses present. Standard review and tweaks recommended."
    else:
        return "LOW RISK", "Balanced and safe contract. Standard protection clauses are in place."

def get_overall_recommendation(score):
    """
    Returns a structured recommendation text based on the overall risk score.
    """
    if score >= 76:
        return "Do Not Sign. The contract contains critical one-sided clauses that expose you to extreme legal and financial risks. Demand a rewrite of the flagged sections before signing."
    elif score >= 51:
        return "Legal Review Recommended. Several high-risk clauses were found that require professional review and adjustment."
    elif score >= 26:
        return "Sign After Negotiation. The contract contains standard terms but has moderate risk areas that should be adjusted."
    else:
        return "Safe to Sign. This contract is well-balanced and contains standard protective clauses."

def generate_one_line_summary(contract_type, clause_count, issues_count, missing_count, overall_risk):
    """
    Generates a concise one-line summary statement.
    """
    if overall_risk in ["CRITICAL RISK", "HIGH RISK"]:
        return f"High-risk {contract_type} containing {clause_count} clauses with {issues_count} flagged issues and {missing_count} missing legal protections."
    elif overall_risk == "MEDIUM RISK":
        return f"Moderate-risk {contract_type} with {clause_count} clauses. Minor tweaks are suggested for the {issues_count} flagged areas."
    else:
        return f"Well-balanced, low-risk {contract_type} featuring standard terms and adequate legal protections."

