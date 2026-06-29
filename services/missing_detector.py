# ClauseGuard AI — Missing Protection Detection Service
from detectors.missing_rules import MISSING_RULES, DEFAULT_MISSING

class MissingDetector:
    @staticmethod
    def detect_missing_clauses(clauses, contract_type):
        """
        Detects missing clauses based on the contract type and the categories present.
        Returns: list of dicts [{'name': str, 'why_missing': str, 'remedy': str}]
        """
        # Collect all classified categories present in the contract
        present_categories = set(clause["category"] for clause in clauses)
        
        # Look up missing rules for this contract type
        normalized_type = contract_type
        if contract_type == "Employment Agreement":
            normalized_type = "Employment Contract"
            
        rules = MISSING_RULES.get(normalized_type, DEFAULT_MISSING)
        
        missing_protections = []
        
        for required_cat, details in rules.items():
            # If the required category is not represented in the contract clauses
            if required_cat not in present_categories:
                # Also do a quick check if related categories exist
                # e.g., if Dispute Resolution is present but Arbitration is missing, it might be acceptable,
                # but if both are missing, flag them. We can do simple matching.
                if required_cat == "Dispute Resolution" and "Arbitration" in present_categories:
                    continue
                if required_cat == "Arbitration" and "Dispute Resolution" in present_categories:
                    continue
                if required_cat == "Termination" and "Notice Period" in present_categories:
                    # If notice period is present, it might define termination
                    pass
                    
                missing_protections.append({
                    "name": details["name"],
                    "why_missing": details["why_missing"],
                    "remedy": details["remedy"]
                })
                
        return missing_protections
