# ClauseGuard AI — Missing Clause Rules & Templates

MISSING_RULES = {
    "Rental Agreement": {
        "Governing Law": {
            "name": "Governing Law Clause",
            "why_missing": "The agreement is missing a Governing Law clause. Without specifying the applicable state and local laws, any dispute will face legal ambiguity regarding which tenancy and rent control statutes apply, causing delays and unpredictable judicial rulings.",
            "remedy": "Add: 'This agreement shall be governed by and construed in accordance with the laws of India and the state in which the property is located.'"
        },
        "Force Majeure": {
            "name": "Force Majeure Clause",
            "why_missing": "No Force Majeure protection is present. If a lockdown, natural disaster, fire, or government restriction prevents you from occupying or operating from the premises, you remain legally obligated to pay 100% of the rent and late fees.",
            "remedy": "Add: 'Neither party shall be liable for failure to perform if prevented by acts of God, pandemics, lockdowns, or disasters. During such periods, rent obligations shall be suspended or proportionally reduced.'"
        },
        "Dispute Resolution": {
            "name": "Dispute Resolution Clause",
            "why_missing": "There is no structured dispute resolution path. If a conflict arises over maintenance, deposit, or rent, either party can immediately drag the other into a lengthy, expensive court battle without trying mediation first.",
            "remedy": "Add: 'In case of any dispute, the parties shall first attempt to resolve the issue amicably through good-faith negotiations or mediation within 30 days.'"
        },
        "Confidentiality": {
            "name": "Confidentiality Clause",
            "why_missing": "No confidentiality terms protect the tenant's business operations or landlord's sensitive property/commercial info from being disclosed to third parties.",
            "remedy": "Add: 'Both parties agree to maintain the confidentiality of the terms of this lease and any proprietary business details disclosed during the tenancy.'"
        },
        "Notice Period": {
            "name": "Notice Period Clause",
            "why_missing": "A notice period for terminating the lease is missing. This can lead to arguments over whether a party can terminate immediately or what constitutes reasonable notice before vacating.",
            "remedy": "Add: 'Either party may terminate this agreement by providing the other party with at least 30 days' written notice.'"
        },
        "Renewal": {
            "name": "Renewal & Escalation Cap",
            "why_missing": "There is no renewal escalation cap. At the end of the tenancy term, the landlord has complete leverage to demand an exorbitant rent hike (e.g. 30%) or force a sudden, expensive eviction.",
            "remedy": "Add: 'The Tenant shall have the option to renew the lease with an annual rent escalation capped at a maximum of 5% to 8%.'"
        },
        "Refund": {
            "name": "Security Deposit Refund Protection",
            "why_missing": "No refund timeline or rules cover the security deposit. The landlord could withhold your deposit indefinitely after you vacate, using arbitrary justifications without returning your funds.",
            "remedy": "Add: 'The Landlord shall refund the security deposit in full within 30 days of the Tenant handing over possession, subject only to documented repairs beyond wear and tear.'"
        },
        "Indemnity": {
            "name": "Tenant Indemnity Protection",
            "why_missing": "No clause protects the tenant from claims arising from building structural defects, landlord's negligence, or third-party injuries on the property.",
            "remedy": "Add: 'The Landlord shall indemnify and hold the Tenant harmless against any claims, losses, or damages arising from structural failures, landlord's gross negligence, or title disputes.'"
        },
        "Liability": {
            "name": "Limitation of Liability",
            "why_missing": "There is no limitation on the tenant's liability, leaving the tenant exposed to unlimited financial damages for accidental fires or structural accidents that occur on the property.",
            "remedy": "Add: 'The Tenant's total liability for damage to the premises shall be capped at a maximum equivalent to 6 months' rent, excluding cases of gross negligence or willful misconduct.'"
        }
    },
    "Employment Contract": {
        "Governing Law": {
            "name": "Governing Law Clause",
            "why_missing": "Missing Governing Law clause. If salary, exit terms, or non-competes are disputed, there is zero clarity on which state's labor courts have jurisdiction, causing procedural delays.",
            "remedy": "Add: 'This contract shall be governed by and construed in accordance with the laws of India and the state of employment.'"
        },
        "Force Majeure": {
            "name": "Force Majeure Clause",
            "why_missing": "Missing Force Majeure clause. Under extreme circumstances (natural disasters, pandemics), the employer could terminate employment instantly or withhold pay without a defined legal framework.",
            "remedy": "Add: 'Performance of duties and payment of salary may be modified or suspended mutually in the event of continuous force majeure occurrences.'"
        },
        "Dispute Resolution": {
            "name": "Dispute Resolution Clause",
            "why_missing": "Without a dispute resolution process, internal issues (appraisals, harassment, contract breaches) may result in immediate litigation or public labor disputes rather than confidential mediation.",
            "remedy": "Add: 'Any dispute arising under this contract shall first be referred to the internal HR Grievance Committee, followed by mutual mediation before legal action.'"
        },
        "Confidentiality": {
            "name": "Confidentiality Clause",
            "why_missing": "No confidentiality protection is present. The employee can share sensitive trade secrets, source code, customer lists, and business strategies with competitors without violating the contract.",
            "remedy": "Add: 'The Employee shall not disclose any confidential information, trade secrets, or client data of the Employer during or after the term of employment.'"
        },
        "Notice Period": {
            "name": "Notice Period Clause",
            "why_missing": "No exit notice period is defined. The employee can walk out on a critical project with zero warning, or the employer can fire the employee instantly without severance.",
            "remedy": "Add: 'Either party may terminate employment by giving 30 days' written notice or salary in lieu of notice.'"
        },
        "Renewal": {
            "name": "Renewal Option Clause",
            "why_missing": "For fixed-term contracts, the lack of renewal terms means employment simply lapses, creating job insecurity for the employee and operational disruptions for the employer.",
            "remedy": "Add: 'This contract may be extended or renewed upon mutual written agreement of both parties at least 15 days prior to expiry.'"
        },
        "Refund": {
            "name": "Refund / Compensation Clause",
            "why_missing": "Missing clear terms on final settlement timelines, potentially leading to the employer delaying severance, unpaid bonuses, or expense refunds post-termination.",
            "remedy": "Add: 'Upon termination, the Employer shall release all due salary, gratuity, and expense refunds within 15 days of the employee's final working day.'"
        },
        "Indemnity": {
            "name": "Employee Indemnification Clause",
            "why_missing": "Without an indemnity limit, the employee could be held personally liable for company losses or third-party lawsuits arising from standard business decisions.",
            "remedy": "Add: 'The Employer shall defend and indemnify the Employee against any third-party claims or liabilities arising out of the performance of their standard duties.'"
        },
        "Liability": {
            "name": "Limitation of Employee Liability",
            "why_missing": "No liability cap protects the employee. The company could sue the employee for unlimited damages if a coding bug or business mistake causes financial loss.",
            "remedy": "Add: 'Except in cases of fraud or willful misconduct, the Employee's liability for any loss caused to the Employer shall be capped at a maximum of 3 months' basic salary.'"
        }
    },
    "NDA": {
        "Governing Law": {
            "name": "Governing Law Clause",
            "why_missing": "Missing Governing Law. Confidentiality breaches involve complex legal actions; without a defined governing law, pursuing an injunction is extremely complicated.",
            "remedy": "Add: 'This agreement shall be governed by and construed in accordance with the laws of India.'"
        },
        "Force Majeure": {
            "name": "Force Majeure Clause",
            "why_missing": "No Force Majeure protection. If a party is forced to disclose information due to government orders or regulatory disasters, they could technically be held in breach of the NDA.",
            "remedy": "Add: 'No party shall be in breach for disclosures required by law, regulatory authorities, or orders of competent courts, provided prior notice is given.'"
        },
        "Dispute Resolution": {
            "name": "Dispute Resolution & Jurisdiction",
            "why_missing": "No specific dispute resolution mechanism is present, making it difficult to quickly obtain an injunction or damages in the event of a leaks/breach of confidentiality.",
            "remedy": "Add: 'Any dispute arising out of this NDA shall be referred to arbitration under the Arbitration and Conciliation Act, with Nagpur designated as the seat.'"
        },
        "Confidentiality": {
            "name": "Core Confidentiality Definition",
            "why_missing": "The NDA lacks a clear definition of what constitutes confidential information and what exceptions apply (e.g. public info, independent discovery), making the NDA vague and legally vulnerable.",
            "remedy": "Add: 'Confidential Information includes all proprietary data marked as confidential, excluding information that becomes public through no fault of the receiving party.'"
        },
        "Notice Period": {
            "name": "NDA Duration / Expiry Notice",
            "why_missing": "The agreement lacks a defined duration or survival period, meaning the confidentiality obligations could be deemed indefinite (which courts dislike) or terminate instantly upon contract end.",
            "remedy": "Add: 'The obligations of confidentiality shall remain in force for a period of 3 years from the date of disclosure, surviving any termination of this agreement.'"
        },
        "Renewal": {
            "name": "Renewal / Term Extension Option",
            "why_missing": "Missing extension terms, which could lead to confidential discussions continuing after the NDA has expired without active legal protection.",
            "remedy": "Add: 'The term of this NDA may be extended in writing by mutual consent to cover ongoing discussions.'"
        },
        "Refund": {
            "name": "Return of Confidential Materials",
            "why_missing": "No clause mandates the return or destruction of confidential files, allowing the receiving party to retain local copies of sensitive code, designs, or data indefinitely.",
            "remedy": "Add: 'Upon written request, the receiving party shall return or destroy all physical and digital copies of confidential materials within 10 days.'"
        },
        "Indemnity": {
            "name": "Breach Indemnification Clause",
            "why_missing": "No indemnity is specified for confidentiality breaches. If the receiving party leaks proprietary trade secrets, the disclosing party has to prove actual damages in court, which is highly difficult.",
            "remedy": "Add: 'The receiving party shall indemnify the disclosing party for any direct losses, damages, or legal expenses arising from an unauthorized disclosure of confidential info.'"
        },
        "Liability": {
            "name": "Limitation of Liability (NDA)",
            "why_missing": "No liability cap is present. While disclosures should have strong remedies, a receiving party faces unlimited punitive damages for accidental or non-willful disclosures.",
            "remedy": "Add: 'Except in cases of gross negligence or willful disclosure, the total liability under this NDA shall be capped at a reasonable mutually agreed sum.'"
        }
    },
    "Service Agreement": {
        "Governing Law": {
            "name": "Governing Law Clause",
            "why_missing": "No Governing Law is specified, creating significant complications if the client and service provider operate in different states and a service delivery dispute occurs.",
            "remedy": "Add: 'This agreement shall be governed by and construed in accordance with the laws of India.'"
        },
        "Force Majeure": {
            "name": "Force Majeure Clause",
            "why_missing": "No Force Majeure protection. If internet shutdowns, lockdowns, or grid failures prevent service delivery, the provider will be in default and face heavy breach penalties.",
            "remedy": "Add: 'Neither party shall be liable for service delays or failures caused by events beyond reasonable control, including natural disasters and government mandates.'"
        },
        "Dispute Resolution": {
            "name": "Dispute Resolution Clause",
            "why_missing": "Without a dispute resolution path, minor scope disagreements can trigger immediate contract termination and litigation, rather than structured mediation.",
            "remedy": "Add: 'The parties shall attempt to resolve service disputes through mutual discussion for 15 days, followed by arbitration in accordance with the Arbitration Act.'"
        },
        "Confidentiality": {
            "name": "Confidentiality Protection",
            "why_missing": "No confidentiality terms protect client databases or provider background code/templates from being shared with third parties or competitors during service execution.",
            "remedy": "Add: 'Both parties shall protect any proprietary or confidential data shared during the course of services and shall not disclose it without written consent.'"
        },
        "Notice Period": {
            "name": "Termination Notice Period",
            "why_missing": "No notice period is defined for exiting. The client can cancel the project instantly without paying for completed milestones, or the provider can drop the client without handoff.",
            "remedy": "Add: 'Either party may terminate this agreement for convenience by providing 30 days' written notice to the other party.'"
        },
        "Renewal": {
            "name": "Renewal Option",
            "why_missing": "Missing renewal terms, meaning services will terminate abruptly at the end of the term, requiring drafting a completely new contract to continue operations.",
            "remedy": "Add: 'This agreement may be renewed for successive terms upon written agreement and review of pricing terms at least 30 days prior to expiration.'"
        },
        "Refund": {
            "name": "Refund & Payment Terms Protection",
            "why_missing": "Missing refund policy. If services are terminated early or not delivered, there is no obligation for the provider to return prepaid fees, which constitutes an unfair trade practice.",
            "remedy": "Add: 'If this agreement is terminated by the Client due to Provider default, the Provider shall refund all prepaid fees for uncompleted milestones within 14 days.'"
        },
        "Indemnity": {
            "name": "Indemnification Clause",
            "why_missing": "Missing mutual indemnity. A party could face heavy losses from intellectual property infringement claims or service defaults caused entirely by the other party.",
            "remedy": "Add: 'Each party shall indemnify and hold the other harmless from third-party claims arising from patent/copyright infringement or willful misconduct under this agreement.'"
        },
        "Liability": {
            "name": "Limitation of Liability Cap",
            "why_missing": "No limitation of liability exists. The service provider could be sued for unlimited consequential damages or lost client profits if a service outage or bug occurs.",
            "remedy": "Add: 'The aggregate liability of either party for any breach of this agreement shall be capped at the total fees paid under this agreement in the 12 months preceding the claim.'"
        }
    }
}

# General standard list if contract type is not specifically mapped
DEFAULT_MISSING = {
    "Termination": {
        "name": "Termination Clause",
        "why_missing": "No clause defines the termination procedure for the agreement.",
        "remedy": "Add a standard termination notice clause."
    },
    "Dispute Resolution": {
        "name": "Dispute Resolution Clause",
        "why_missing": "No mechanism is present to resolve conflicts outside of expensive court litigation.",
        "remedy": "Add mutual negotiation and mediation clauses."
    },
    "Governing Law": {
        "name": "Governing Law & Jurisdiction",
        "why_missing": "No governing legal framework is specified.",
        "remedy": "Insert Indian governing law and local exclusive jurisdiction clauses."
    }
}
