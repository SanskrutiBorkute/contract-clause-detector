# ClauseGuard AI — Predatory Clause Rules & Detection Algorithms
import re
from utils.legal_db import LEGAL_DATABASE

def get_detected_sentence(text, keywords):
    """
    Helper to extract the specific sentence containing any of the matched keywords.
    """
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for sent in sentences:
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', sent.lower()):
                return sent.strip()
    # Fallback to searching raw substring if word boundary fails
    for sent in sentences:
        for kw in keywords:
            if kw.lower() in sent.lower():
                return sent.strip()
    return text.strip()

def check_security_deposit_risk(text):
    lower_text = text.lower()
    matched_ev = []
    
    # 1. Check excessive deposit (more than 3 months)
    months_match = re.search(r'(\d+)\s*(?:month|month\'s|months|months\')', lower_text)
    excessive = False
    months = 0
    if months_match:
        months = int(months_match.group(1))
        if months > 3:
            excessive = True
            matched_ev.append(f"{months} months")
            
    # 2. Check forfeit for normal wear and tear
    wear_tear_forfeit = "wear" in lower_text and "tear" in lower_text and ("forfeit" in lower_text or "deduct" in lower_text or "not refundable" in lower_text)
    if wear_tear_forfeit:
        matched_ev.append("wear and tear")
        if "forfeit" in lower_text: matched_ev.append("forfeit")
        if "not refundable" in lower_text: matched_ev.append("not refundable")
        
    sole_discretion = "sole discretion" in lower_text and ("forfeit" in lower_text or "deposit" in lower_text)
    if sole_discretion:
        matched_ev.append("sole discretion")
        
    # 3. Return delay
    return_delay = False
    delay_match = re.search(r'(\d+)\s*days', lower_text)
    if delay_match:
        days = int(delay_match.group(1))
        if days > 45:
            return_delay = True
            matched_ev.append(f"{days} days")
            
    if wear_tear_forfeit or (sole_discretion and excessive):
        det_sent = get_detected_sentence(text, ["wear", "tear", "forfeit", "discretion"])
        return {
            "flagged": True,
            "risk_level": "CRITICAL",
            "risk_weight": 20,
            "matched_evidence": matched_ev,
            "detected_sentence": det_sent,
            "reason": "Deposit forfeiture allowed for normal wear and tear or at landlord's sole discretion.",
            "explanation": "The clause allows the landlord to forfeit your deposit for 'normal wear and tear' or under subjective criteria. In Indian tenancy law, normal wear and tear is the landlord's liability; the tenant is only responsible for willful or negligent damages.",
            "consequences": "You could lose your entire deposit (₹[Amount]) at the end of the term even if you maintain the property in excellent condition, with no immediate legal recourse.",
            "rewrite_template": "The Tenant shall pay a security deposit of ₹[Amount] (equivalent to 2 months' rent). The Landlord shall refund the security deposit in full within 30 days of the Tenant vacating, subject only to deductions for reasonable costs of repair of actual damage beyond normal wear and tear.",
            "negotiation_advice": "Demand that the phrase 'normal wear and tear excepted' be explicitly added, and that any deductions require written itemized repair bills.",
            "financial_impact": "Full deposit amount at risk (up to ₹[Amount]).",
            "legal_impact": "Unenforceable in court, but difficult to recover without litigation."
        }
    elif excessive:
        det_sent = get_detected_sentence(text, [f"{months} month", "months"])
        return {
            "flagged": True,
            "risk_level": "HIGH",
            "risk_weight": 15,
            "matched_evidence": matched_ev,
            "detected_sentence": det_sent,
            "reason": f"Excessive security deposit amount of {months} months' rent.",
            "explanation": f"The security deposit is set to {months} months' rent. Under Model Tenancy Act, 2021, and prevailing rent control practices in major Indian cities, the deposit for residential premises is capped at 2 months, and commercial is usually 3-6 months.",
            "consequences": "Ties up substantial working capital (₹[Amount]) interest-free for the entire lease period.",
            "rewrite_template": "The Tenant shall pay a security deposit of ₹[Amount] (equivalent to 2-3 months' rent). The Landlord shall refund the deposit within 30 days of vacating.",
            "negotiation_advice": "Propose reducing the deposit to a standard 2 to 3 months of rent.",
            "financial_impact": f"Excess cash lockup of {months-3} months rent.",
            "legal_impact": "Legally contestable under the Model Tenancy Act."
        }
    elif return_delay:
        det_sent = get_detected_sentence(text, ["days"])
        return {
            "flagged": True,
            "risk_level": "WARNING",
            "risk_weight": 8,
            "matched_evidence": matched_ev,
            "detected_sentence": det_sent,
            "reason": "Unreasonable delay in returning security deposit (>45 days).",
            "explanation": "The landlord has specified a long window to return the deposit. Standard legal practice dictates returning the deposit within 30 days of handing over possession.",
            "consequences": "You will face cash flow delays and lose interest on your money for months after vacating.",
            "rewrite_template": "The Landlord shall refund the security deposit to the Tenant within 30 days of the Tenant vacating and delivering possession.",
            "negotiation_advice": "Insist that the deposit must be returned within 30 days of vacating.",
            "financial_impact": "Delayed cash flow post-vacating.",
            "legal_impact": "Legally weak. 30 days is the standard statutory limit."
        }
        
    return None

def check_termination_risk(text):
    lower_text = text.lower()
    matched_ev = []
    
    # 1. 24 hours notice or immediate/oral notice
    immediate = False
    if "24 hours" in lower_text or "24-hour" in lower_text:
        immediate = True
        matched_ev.append("24 hours")
    if "immediate" in lower_text:
        immediate = True
        matched_ev.append("immediate")
    if "oral" in lower_text:
        immediate = True
        matched_ev.append("oral")
    if "without notice" in lower_text or "without prior notice" in lower_text:
        immediate = True
        matched_ev.append("without notice")
        
    # 2. One-sided termination (only landlord can terminate)
    one_sided = ("landlord may terminate" in lower_text or "lessor may terminate" in lower_text) and not ("tenant may terminate" in lower_text or "lessee may terminate" in lower_text or "either party" in lower_text or "mutual" in lower_text)
    if one_sided:
        matched_ev.append("one-sided")
    
    if immediate:
        det_sent = get_detected_sentence(text, ["24 hours", "immediate", "oral", "without notice"])
        return {
            "flagged": True,
            "risk_level": "CRITICAL",
            "risk_weight": 20,
            "matched_evidence": matched_ev,
            "detected_sentence": det_sent,
            "reason": "Immediate eviction or termination without notice / on oral notice.",
            "explanation": "This clause gives the landlord the right to terminate the lease immediately or with extremely short notice (e.g. 24 hours) or on verbal/oral communication without court intervention.",
            "consequences": "Your business can be forced onto the street overnight, disrupting operations, causing major financial losses, and giving you no time to locate alternative premises.",
            "rewrite_template": "Either party may terminate this agreement by giving at least 30 days' written notice to the other party.",
            "negotiation_advice": "Insist on a minimum 30-day (or 60-day for commercial leases) written notice period for convenience, and a 15-day cure period for breaches.",
            "financial_impact": "Complete loss of business continuity and fit-out investments.",
            "legal_impact": "Unconstitutional and illegal. Eviction requires due process of law."
        }
    elif one_sided:
        det_sent = get_detected_sentence(text, ["terminate"])
        return {
            "flagged": True,
            "risk_level": "HIGH",
            "risk_weight": 15,
            "matched_evidence": matched_ev,
            "detected_sentence": det_sent,
            "reason": "One-sided termination right favoring only the Landlord.",
            "explanation": "The clause grants termination rights exclusively to the landlord, while locking in the tenant or providing no corresponding right for the tenant to terminate for convenience or breach.",
            "consequences": "You are bound to the contract, but the landlord can exit whenever they choose, creating a massive imbalance of power.",
            "rewrite_template": "Either party may terminate this agreement by providing 30 days' written notice to the other party.",
            "negotiation_advice": "Request that all termination rights be made mutual (reciprocal) for both parties.",
            "financial_impact": "High operational vulnerability.",
            "legal_impact": "Adjudicated as an 'unfair contract' under the Consumer Protection Act, but costly to challenge."
        }
        
    return None

def check_lock_in_risk(text):
    lower_text = text.lower()
    matched_ev = []
    
    # Check excessive lock-in (e.g., 36 months / 3 years or more)
    long_lock = False
    if "36" in lower_text or "three years" in lower_text or "3 years" in lower_text:
        long_lock = True
        matched_ev.append("36 months")
    if "five years" in lower_text or "60" in lower_text:
        long_lock = True
        matched_ev.append("60 months")
        
    # Double penalty (liquidated damages + forfeiture of deposit)
    double_penalty = "forfeit" in lower_text and ("penalty" in lower_text or "liquidated damages" in lower_text or "remaining months" in lower_text)
    if double_penalty:
        matched_ev.append("double penalty")
        if "forfeit" in lower_text: matched_ev.append("forfeit")
        if "penalty" in lower_text: matched_ev.append("penalty")
    
    if double_penalty:
        det_sent = get_detected_sentence(text, ["forfeit", "penalty", "remaining"])
        return {
            "flagged": True,
            "risk_level": "CRITICAL",
            "risk_weight": 20,
            "matched_evidence": matched_ev,
            "detected_sentence": det_sent,
            "reason": "Double penalty for early termination (deposit forfeiture AND rent penalty).",
            "explanation": "This clause imposes a double penalty for exiting early: it forfeits your security deposit AND demands payment of rent for the remaining lock-in period. This is penal and legally unconscionable.",
            "consequences": "Exiting early could cost you your entire deposit plus a cash payment of several lakhs of rupees, creating severe financial distress.",
            "rewrite_template": "If either party terminates the agreement prior to the lock-in, they shall pay a capped penalty equivalent to a maximum of 2 months' rent as liquidated damages, with no forfeiture of the deposit.",
            "negotiation_advice": "Negotiate to cap the early termination liability at a maximum of 1 or 2 months' rent as liquidated damages, with NO forfeiture of deposit.",
            "financial_impact": "Combined loss of deposit and cash penalty.",
            "legal_impact": "Invalid under Section 74 of the Indian Contract Act. Courts do not enforce double penalties."
        }
    elif long_lock:
        det_sent = get_detected_sentence(text, ["lock", "months", "years"])
        return {
            "flagged": True,
            "risk_level": "HIGH",
            "risk_weight": 15,
            "matched_evidence": matched_ev,
            "detected_sentence": det_sent,
            "reason": "Excessively long lock-in period (3 years or more).",
            "explanation": "A lock-in period of 36 months or more is excessively long for small businesses. It prevents you from adjusting to business downturns or relocating if the premises prove unsuitable.",
            "consequences": "Legally binds you to pay rent for years even if your business fails or needs to scale down.",
            "rewrite_template": "Both parties agree to a lock-in period of 12 months, after which exit is allowed with 2 months' notice.",
            "negotiation_advice": "Ask to reduce the lock-in period to 12 months, or add a clause allowing exit with a notice period after the first 6-12 months.",
            "financial_impact": "Long-term fixed rent liability.",
            "legal_impact": "Valid if signed, but courts will only award actual proven landlord damages upon exit."
        }
        
    return None

def check_inspection_risk(text):
    lower_text = text.lower()
    matched_ev = []
    
    # Entry at any time without prior notice
    no_notice_entry = "any time" in lower_text and ("without notice" in lower_text or "no notice" in lower_text or "without prior notice" in lower_text or "without warning" in lower_text)
    if no_notice_entry:
        matched_ev.append("any time")
        matched_ev.append("without notice")
        
    if no_notice_entry:
        det_sent = get_detected_sentence(text, ["time", "notice"])
        return {
            "flagged": True,
            "risk_level": "HIGH",
            "risk_weight": 15,
            "matched_evidence": matched_ev,
            "detected_sentence": det_sent,
            "reason": "Landlord reserves entry rights at any time without prior notice.",
            "explanation": "The clause permits the landlord to enter the leased property at any hour without notifying you. This violates the legal covenant of 'quiet enjoyment' and your right to privacy.",
            "consequences": "Disrupts business operations, compromises trade secrets/customer privacy, and presents safety concerns.",
            "rewrite_template": "The Landlord shall have the right to enter the premises to inspect or repair, provided they give the Tenant at least 24 hours' prior written notice and schedule entry during reasonable business hours.",
            "negotiation_advice": "Insist on 'minimum 24 hours' prior written notice' and 'entry only during normal business hours' and 'in the presence of the Tenant'.",
            "financial_impact": "Operational disruption and privacy breach.",
            "legal_impact": "Violates the Model Tenancy Act, Section 15, and Article 21 of the Indian Constitution."
        }
        
    return None

def check_maintenance_risk(text):
    lower_text = text.lower()
    matched_ev = []
    
    # Tenant responsible for all repairs, including structural
    all_repairs = ("all repairs" in lower_text or "structural repairs" in lower_text or "structural" in lower_text) and ("tenant" in lower_text or "lessee" in lower_text) and ("solely responsible" in lower_text or "responsible for" in lower_text or "bear" in lower_text)
    if all_repairs:
        matched_ev.append("all repairs")
        if "structural" in lower_text: matched_ev.append("structural")
        matched_ev.append("tenant responsible")
        
    if all_repairs:
        det_sent = get_detected_sentence(text, ["repairs", "structural", "responsible"])
        return {
            "flagged": True,
            "risk_level": "HIGH",
            "risk_weight": 15,
            "matched_evidence": matched_ev,
            "detected_sentence": det_sent,
            "reason": "Tenant is made responsible for all structural repairs and major maintenance.",
            "explanation": "The clause shifts the burden of structural maintenance (like foundation, leaking roofs, external walls, major plumbing lines) entirely onto the tenant. By law, structural maintenance is the landlord's duty.",
            "consequences": "You could be forced to pay hundreds of thousands of rupees to fix leaking roofs, structural cracks, or electrical mains wiring that you do not own.",
            "rewrite_template": "The Landlord shall be responsible for all structural repairs, major plumbing, and electrical issues. The Tenant shall only be responsible for routine daily upkeep and minor repairs.",
            "negotiation_advice": "Negotiate to explicitly separate structural repairs (Landlord's cost) from routine day-to-day minor maintenance (Tenant's cost, e.g. bulbs, minor painting).",
            "financial_impact": "High capital expenditure risk on landlord's asset.",
            "legal_impact": "Contests standard legal conventions, but binding if explicitly agreed in contract."
        }
        
    return None

def check_liability_risk(text):
    lower_text = text.lower()
    matched_ev = []
    
    # Unlimited liability or landlord zero liability
    unlimited = "unlimited liability" in lower_text or "shall not be limited" in lower_text or "agree to accept all liability" in lower_text
    if unlimited:
        matched_ev.append("unlimited liability")
        
    zero_landlord = ("landlord shall not be liable" in lower_text or "lessor shall not be liable" in lower_text) and ("any" in lower_text or "howsoever caused" in lower_text or "injury" in lower_text or "damage" in lower_text)
    if zero_landlord:
        matched_ev.append("zero landlord liability")
        
    if unlimited:
        det_sent = get_detected_sentence(text, ["unlimited", "liability"])
        return {
            "flagged": True,
            "risk_level": "CRITICAL",
            "risk_weight": 20,
            "matched_evidence": matched_ev,
            "detected_sentence": det_sent,
            "reason": "Unlimited liability assumed by the Tenant.",
            "explanation": "You are agreeing to assume unlimited liability for any issues under the contract. In commercial transactions, liability should always be capped at a reasonable sum to protect the business.",
            "consequences": "A single lawsuit or claim could bankrupt your business and expose your personal assets to seizure.",
            "rewrite_template": "Neither party shall be liable for indirect or consequential damages. The aggregate liability of either party under this agreement shall be limited to the total fees paid under this agreement.",
            "negotiation_advice": "Strenuously demand a mutual cap on liability (e.g. capped at the total amount paid under the contract, or 12 months' rent).",
            "financial_impact": "Unlimited financial exposure.",
            "legal_impact": "Exposes the business to devastating judgements."
        }
    elif zero_landlord:
        det_sent = get_detected_sentence(text, ["liable", "negligence", "damage"])
        return {
            "flagged": True,
            "risk_level": "HIGH",
            "risk_weight": 15,
            "matched_evidence": matched_ev,
            "detected_sentence": det_sent,
            "reason": "Landlord disclaims all liability, even for negligence.",
            "explanation": "The landlord is disclaiming all liability for injuries, damage to your assets, or accidents on the property, even if caused by the landlord's gross negligence (like poorly maintained wiring or structural collapse).",
            "consequences": "If a short circuit occurs due to old wiring and burns your inventory, you cannot claim compensation from the landlord.",
            "rewrite_template": "The Landlord shall remain liable for damages or injuries arising from their gross negligence, willful misconduct, or structural failures.",
            "negotiation_advice": "Add an exception stating that the landlord remains liable for losses arising from their gross negligence, willful misconduct, or failure to perform structural repairs.",
            "financial_impact": "Loss of assets and inventory without recourse.",
            "legal_impact": "Legally contestable under the Consumer Protection Act and general tort law."
        }
        
    return None

def check_late_fees_risk(text):
    lower_text = text.lower()
    matched_ev = []
    
    # Check for daily interest or high annual rate or daily penalty
    daily_interest = "per day" in lower_text or "per-day" in lower_text or "daily" in lower_text or "interest" in lower_text and ("1%" in lower_text or "2%" in lower_text or "3%" in lower_text or "4%" in lower_text or "5%" in lower_text)
    high_rate = False
    pct_match = re.search(r'(\d+)\s*%', lower_text)
    if pct_match:
        val = int(pct_match.group(1))
        if val > 18:
            high_rate = True
            matched_ev.append(f"{val}% interest")
            
    hold_over_penalty = "two times" in lower_text or "2 times" in lower_text or "double the rent" in lower_text or "double rent" in lower_text or "double the monthly" in lower_text
    
    if daily_interest or high_rate or hold_over_penalty or "penalty" in lower_text:
        if daily_interest:
            matched_ev.append("daily interest/late fee")
        if hold_over_penalty:
            matched_ev.append("double rent penalty")
        det_sent = get_detected_sentence(text, ["interest", "penalty", "daily", "late", "two times", "2 times", "double"])
        return {
            "flagged": True,
            "risk_level": "WARNING",
            "risk_weight": 8,
            "matched_evidence": matched_ev,
            "detected_sentence": det_sent,
            "reason": "High late payment penalty or daily interest/double rent charges.",
            "explanation": "The interest rate or penalty for late payments / holding over is excessively high or charged on a double basis. Under Indian Contract Act, Section 74, unreasonable penalties are considered penal in nature and are generally unenforceable.",
            "consequences": "Even a short delay of a few days or holding over could lead to a massive accumulated penalty.",
            "rewrite_template": "In case of delay in payment or holding over, the Tenant shall pay interest on the overdue amount at a reasonable rate of 1% per month (12% per annum) after a grace period of 5 days.",
            "negotiation_advice": "Request a grace period of 5-10 days and cap the late payment interest at 12% per annum.",
            "financial_impact": "Accumulating daily penalties.",
            "legal_impact": "Unenforceable under Section 74 of the Indian Contract Act."
        }
    return None

def run_predatory_rules(category, text):
    """
    Orchestrates specialized predatory check functions based on the clause category.
    Returns details dict if flagged, else None.
    """
    if category == "Security Deposit":
        return check_security_deposit_risk(text)
    elif category == "Termination" or category == "Notice Period":
        return check_termination_risk(text)
    elif category == "Lock-in":
        return check_lock_in_risk(text)
    elif category == "Inspection Rights" or category == "Entry Rights":
        return check_inspection_risk(text)
    elif category == "Maintenance":
        return check_maintenance_risk(text)
    elif category == "Liability" or category == "Unlimited Liability":
        return check_liability_risk(text)
    elif category == "Late Fees" or category == "Penalty" or category == "Payment Terms":
        return check_late_fees_risk(text)
    
    # General fallback for unilateral discretionary clauses
    lower_text = text.lower()
    if "discretion" in lower_text and ("sole" in lower_text or "unilateral" in lower_text) and ("forfeit" in lower_text or "terminate" in lower_text or "penalty" in lower_text):
        det_sent = get_detected_sentence(text, ["discretion", "sole", "unilateral"])
        return {
            "flagged": True,
            "risk_level": "WARNING",
            "risk_weight": 8,
            "matched_evidence": ["sole discretion", "unilateral"],
            "detected_sentence": det_sent,
            "reason": "Unilateral discretion given to one party.",
            "explanation": "This clause gives the landlord or other party the absolute right to make decisions (like forfeiting deposits, charging penalties, or terminating) without your consent or verification.",
            "consequences": "Enables one-sided enforcement of terms without mediation.",
            "rewrite_template": "Any decisions regarding forfeitures, defaults, or termination must be made mutually in writing based on objective, documented evidence.",
            "negotiation_advice": "Request that all discretionary actions be based on 'mutual written agreement' or subject to independent arbitration.",
            "financial_impact": "Medium risk of cash losses.",
            "legal_impact": "Valid but highly unfavorable."
        }
        
    return None
