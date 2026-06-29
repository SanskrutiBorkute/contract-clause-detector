# ClauseGuard AI — Risk Assessment Engine
import re
from utils.legal_db import LEGAL_DATABASE
from utils.helpers import map_risk_score_to_label, get_overall_recommendation
from detectors.predatory_rules import run_predatory_rules

def extract_party_names(text):
    """
    Extracts the names of the two main contracting parties (e.g. Landlord & Tenant)
    from the first 1500 characters of the contract.
    """
    sample = text[:1500]
    parties = {"party_1": "First Party", "party_2": "Second Party"}
    
    # 1. Look for "between [Name] ... and [Name]"
    between_match = re.search(
        r'(?:between|betwixt)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)[\s,]+(?:and|&)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', 
        sample
    )
    if between_match:
        parties["party_1"] = between_match.group(1).strip()
        parties["party_2"] = between_match.group(2).strip()
    else:
        # 2. Search for names near roles (Landlord / Lessor / Employer / Disclosing Party)
        landlord_match = re.search(
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s*(?:\(.*?\))?\s*(?:hereinafter|called|referred to as)?\s*(?:the\s+)?["\'(]?(?:landlord|lessor|employer|disclosing party|owner)["\')]?', 
            sample, re.IGNORECASE
        )
        tenant_match = re.search(
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s*(?:\(.*?\))?\s*(?:hereinafter|called|referred to as)?\s*(?:the\s+)?["\'(]?(?:tenant|lessee|employee|receiving party|renter)["\')]?', 
            sample, re.IGNORECASE
        )
        if landlord_match:
            parties["party_1"] = landlord_match.group(1).strip()
        if tenant_match:
            parties["party_2"] = tenant_match.group(1).strip()
            
    return parties

def generate_dynamic_rewrite(category, text, parties, rent_amount, is_flagged=True):
    """
    Performs live regex mutations on the original clause text to scrub predatory terms,
    maintaining the original grammar while injecting the extracted party names and values.
    """
    if not is_flagged:
        return text

    p1 = parties["party_1"]
    p2 = parties["party_2"]
    
    # Retrieve base template from legal database as fallback
    db_entry = LEGAL_DATABASE.get(category, LEGAL_DATABASE["Other"])
    base_rewrite = db_entry["default_rewrite"]
    base_rewrite = base_rewrite.replace("[Landlord]", p1).replace("[Tenant]", p2)
    base_rewrite = base_rewrite.replace("[Amount]", f"₹{rent_amount:,}")
    base_rewrite = base_rewrite.replace("[Months]", "3")
    
    # Clone original text for mutation
    custom_rewrite = text
    
    if category == "Security Deposit":
        custom_rewrite = re.sub(r'\b(10|8|6|12)\s*months\b', '2 months', custom_rewrite, flags=re.IGNORECASE)
        custom_rewrite = re.sub(r'\b(180|90|60|120)\s*days\b', '30 days', custom_rewrite, flags=re.IGNORECASE)
        custom_rewrite = re.sub(r'including\s+(normal\s+)?wear\s+and\s+tear', 'excluding normal wear and tear', custom_rewrite, flags=re.IGNORECASE)
        custom_rewrite = re.sub(r'at\s+his\s+sole\s+discretion\s+for\s+any\s+damage', 'only for actual documented damage exceeding normal wear and tear', custom_rewrite, flags=re.IGNORECASE)
        custom_rewrite = re.sub(r'forfeit\s+the\s+entire\s+deposit', 'deduct only actual repair costs', custom_rewrite, flags=re.IGNORECASE)
        custom_rewrite = re.sub(r'wear\s+and\s+tear\s+to\s+be\s+deducted', 'wear and tear excepted', custom_rewrite, flags=re.IGNORECASE)
        custom_rewrite = re.sub(r'sole\s+discretion\s+of\s+the\s+(landlord|owner|lessor)', 'mutual agreement of the parties', custom_rewrite, flags=re.IGNORECASE)

        
    elif category in ["Termination", "Notice Period"]:
        custom_rewrite = re.sub(r'\b(24\s*hours|immediate|oral|without\s*notice)\b', '30 days\' written notice', custom_rewrite, flags=re.IGNORECASE)
        custom_rewrite = re.sub(r'the\s+(landlord|owner|lessor)\s+reserves\s+the\s+right\s+to\s+terminate', 'either party may terminate', custom_rewrite, flags=re.IGNORECASE)
        custom_rewrite = re.sub(r'the\s+(landlord|owner|lessor)\s+may\s+terminate', 'either party may terminate', custom_rewrite, flags=re.IGNORECASE)
        
    elif category == "Maintenance":
        custom_rewrite = re.sub(r'tenant\s+shall\s+be\s+responsible\s+for\s+all\s+repairs,\s+including\s+structural', f'Landlord ({p1}) shall be responsible for structural repairs, and Tenant ({p2}) shall be responsible for minor routine upkeep', custom_rewrite, flags=re.IGNORECASE)
        custom_rewrite = re.sub(r'lessee\s+shall\s+be\s+responsible\s+for\s+all\s+structural\s+repairs', f'Lessor ({p1}) shall be responsible for structural repairs, and Lessee ({p2}) shall be responsible for minor routine upkeep', custom_rewrite, flags=re.IGNORECASE)
        
    elif category == "Lock-in":
        custom_rewrite = re.sub(r'forfeiture\s+of\s+the\s+full\s+deposit', 'with no forfeiture of the security deposit', custom_rewrite, flags=re.IGNORECASE)
        custom_rewrite = re.sub(r'penalty\s+of\s+\d+\s*months\s*rent', 'penalty capped at 1 month\'s rent', custom_rewrite, flags=re.IGNORECASE)
        custom_rewrite = re.sub(r'remaining\s+months\s+of\s+the\s+lock-in\s+period', 'a maximum of 1 month\'s rent', custom_rewrite, flags=re.IGNORECASE)
        
    elif category in ["Inspection Rights", "Entry Rights"]:
        custom_rewrite = re.sub(r'at\s+any\s+time\s+without\s+prior\s+notice', 'upon providing at least 24 hours\' prior written notice, during reasonable business hours and in the presence of the Tenant', custom_rewrite, flags=re.IGNORECASE)
        custom_rewrite = re.sub(r'without\s+any\s+prior\s+notice', 'upon providing at least 24 hours\' prior written notice', custom_rewrite, flags=re.IGNORECASE)
        
    elif category in ["Liability", "Unlimited Liability"]:
        custom_rewrite = re.sub(r'unlimited\s+liability', 'liability capped at the total contract value', custom_rewrite, flags=re.IGNORECASE)
        custom_rewrite = re.sub(r'shall\s+not\s+be\s+liable\s+for\s+any\s+damage', 'shall remain liable for damages arising from gross negligence', custom_rewrite, flags=re.IGNORECASE)
        
    elif category == "Late Fees":
        custom_rewrite = re.sub(r'(\d+)%\s+interest\s+per\s+day', '1% interest per month', custom_rewrite, flags=re.IGNORECASE)
        custom_rewrite = re.sub(r'penalty\s+of\s+₹?\d+\s*per\s+day', 'interest not exceeding 12% per annum', custom_rewrite, flags=re.IGNORECASE)
        
    elif category == "Refund":
        custom_rewrite = re.sub(r'non-refundable\s+under\s+any\s+circumstances', 'refundable pro-rata in the event of provider default or early termination for convenience by the provider', custom_rewrite, flags=re.IGNORECASE)
        custom_rewrite = re.sub(r'no\s+refunds\s+shall\s+be\s+issued', 'pro-rata refunds shall be issued for uncompleted services', custom_rewrite, flags=re.IGNORECASE)

    # General fallback substitutions for flagged clauses
    if custom_rewrite == text:
        if "sole discretion" in custom_rewrite.lower():
            custom_rewrite = re.sub(r'sole\s+discretion', 'mutual agreement', custom_rewrite, flags=re.IGNORECASE)
        else:
            return base_rewrite
        
    return custom_rewrite

class RiskDetector:
    def __init__(self, classifier):
        self.classifier = classifier

    def analyze_clauses(self, clauses, contract_type):
        """
        Analyzes a list of segmented clauses: categorizes them, checks for predatory terms,
        and builds a detailed risk profile for each.
        Returns: (analyzed_clauses, overall_score, issues)
        """
        analyzed_clauses = []
        issues = []
        
        critical_count = 0
        high_count = 0
        warning_count = 0
        safe_count = 0
        
        # Combine all clause texts to extract party names and rent values
        full_contract_text = "\n\n".join(c["text"] for c in clauses)
        parties = extract_party_names(full_contract_text)
        
        rent_amount = 0
        for clause in clauses:
            if "rent" in clause["text"].lower():
                rent_match = re.search(r'(?:₹|rs\.?|rupees)?\s*(\d{1,3}(?:,\d{3})+|\d{4,6})', clause["text"].lower())
                if rent_match:
                    rent_str = rent_match.group(1).replace(",", "")
                    try:
                        rent_amount = int(rent_str)
                        break
                    except ValueError:
                        pass
        
        if rent_amount == 0:
            rent_amount = 12000 # default fallback
            
        for i, clause in enumerate(clauses):
            text = clause["text"]
            num = clause["number"]
            clause_id = clause["id"]
            
            # 1. Categorize using the NLP classifier
            category, confidence = self.classifier.classify(text)
            title = f"{category}"
            
            # 2. Check for predatory terms
            predatory_details = run_predatory_rules(category, text)
            
            # 3. Dynamic Rewrite Generation (customized per clause)
            rewrite = generate_dynamic_rewrite(category, text, parties, rent_amount, is_flagged=(predatory_details is not None))
            
            if predatory_details:
                risk_level = predatory_details["risk_level"]
                risk_weight = predatory_details["risk_weight"]
                matched_evidence = predatory_details["matched_evidence"]
                detected_sentence = predatory_details["detected_sentence"]
                
                reason = predatory_details["reason"]
                explanation = predatory_details["explanation"]
                consequences = predatory_details["consequences"]
                negotiation_advice = predatory_details["negotiation_advice"]
                financial_impact = predatory_details["financial_impact"]
                legal_impact = predatory_details["legal_impact"]
                
                # Replace placeholders
                deposit_value = rent_amount * 10
                explanation = explanation.replace("[Amount]", f"₹{rent_amount:,}")
                consequences = consequences.replace("[Amount]", f"₹{deposit_value:,}")
                financial_impact = financial_impact.replace("[Amount]", f"₹{deposit_value:,}")
                
                if risk_level == "CRITICAL":
                    critical_count += 1
                elif risk_level == "HIGH":
                    high_count += 1
                elif risk_level == "WARNING":
                    warning_count += 1
                else:
                    risk_level = "WARNING" # default to WARNING if predatory details matched
                    warning_count += 1
                    
                issues.append({
                    "clause_id": clause_id,
                    "title": f"{title} — {num}",
                    "why": reason,
                    "risk_level": risk_level,
                    "financial_impact": financial_impact
                })
            else:
                # Standard non-predatory clause
                db_entry = LEGAL_DATABASE.get(category, LEGAL_DATABASE["Other"])
                
                risk_level = "SAFE"
                risk_weight = 0
                safe_count += 1
                
                reason = "No issues identified. Clause conforms to standard legal templates."
                explanation = db_entry["consequences"]
                consequences = "Standard clause, low operational risk."
                negotiation_advice = db_entry["negotiation_advice"]
                financial_impact = "None"
                legal_impact = "Standard legal validity."
                matched_evidence = []
                detected_sentence = "N/A"
            
            analyzed_clauses.append({
                "id": clause_id,
                "number": num,
                "title": title,
                "text": text,
                "category": category,
                "confidence": confidence,
                "risk_level": risk_level,
                "risk_weight": risk_weight,
                "matched_evidence": matched_evidence,
                "detected_sentence": detected_sentence,
                "reason": reason,
                "explanation": explanation,
                "consequences": consequences,
                "rewrite": rewrite,
                "negotiation_advice": negotiation_advice,
                "severity": {
                    "financial_risk": "HIGH" if risk_level in ["CRITICAL", "HIGH"] else ("MED" if risk_level == "WARNING" else "LOW"),
                    "legal_validity": "WEAK" if risk_level == "CRITICAL" else ("MODERATE" if risk_level in ["HIGH", "WARNING"] else "STRONG"),
                    "negotiability": "HIGH" if risk_level in ["CRITICAL", "HIGH"] else ("MED" if risk_level == "WARNING" else "LOW")
                },
                "indian_law": LEGAL_DATABASE.get(category, LEGAL_DATABASE["Other"])["laws"],
                "financial_impact": financial_impact,
                "legal_impact": legal_impact
            })
            
        # Calculate overall score (0-100) using normalized scoring algorithm
        # We can calculate missing protections counts here or pass it in.
        # Let's count missing protections inside the route, but here we can calculate a base score from the clause risks.
        highest_risk = "SAFE"
        if critical_count > 0:
            highest_risk = "CRITICAL"
        elif high_count > 0:
            highest_risk = "HIGH"
        elif warning_count > 0:
            highest_risk = "WARNING"
            
        avg_confidence = 95.0
        if analyzed_clauses:
            avg_confidence = sum(c["confidence"] for c in analyzed_clauses) / len(analyzed_clauses)
        confidence_factor = avg_confidence / 100.0
        
        if highest_risk == "CRITICAL":
            base = 81
            additional = (critical_count * 5) + (high_count * 3) + (warning_count * 2)
            score = int(base + min(19, additional * confidence_factor))
        elif highest_risk == "HIGH":
            base = 61
            additional = (high_count * 4) + (warning_count * 2)
            score = int(base + min(19, additional * confidence_factor))
        elif highest_risk == "WARNING":
            base = 26
            additional = (warning_count * 3)
            score = int(base + min(34, additional * confidence_factor))
        else:
            base = 5
            additional = len(analyzed_clauses) // 2
            score = int(base + min(20, additional * confidence_factor))
            
        score = min(100, max(5, score))
        
        return analyzed_clauses, score, issues
