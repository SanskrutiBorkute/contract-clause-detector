# ClauseGuard AI — Legal Reference Database

LEGAL_DATABASE = {
    "Security Deposit": {
        "name": "Security Deposit",
        "default_rewrite": "The Tenant shall pay a security deposit of ₹[Amount] (equivalent to 2-3 months' rent). The Landlord shall hold this deposit in trust. Within 30 days of the Tenant vacating the premises, the Landlord shall refund the security deposit in full, subject only to deductions for reasonable costs of repair of actual damage beyond normal wear and tear. An itemized statement of such repairs and costs shall be provided to the Tenant.",
        "laws": ["Model Tenancy Act, 2021 — Section 11", "Transfer of Property Act, 1882 — Section 108", "Maharashtra Rent Control Act, 1999"],
        "negotiation_advice": "Request that the deposit amount be reduced to 2 to 3 months of rent, which is standard. Ensure a clause is explicitly added stating that the deposit cannot be forfeited for 'normal wear and tear' (like paint fading, normal wall scuffs) and must be returned within 30 days.",
        "consequences": "An excessive security deposit ties up your capital. Without explicit protections, landlords can arbitrarily keep your deposit by claiming minor scuffs or paint fading constitutes damage, and delay refunds for months or years."
    },
    "Payment Terms": {
        "name": "Payment Terms & Rent",
        "default_rewrite": "Rent shall be paid monthly on or before the 5th day of each calendar month. A grace period of 5 days shall be allowed. In the event of late payment, the Tenant shall pay interest at a reasonable rate not exceeding 10% per annum on the overdue amount.",
        "laws": ["Indian Contract Act, 1872 — Section 73 (Reasonable Compensation)", "Model Tenancy Act, 2021 — Section 9"],
        "negotiation_advice": "Check for a grace period (standard is 5 days). If there is a late payment penalty, verify that the rate is reasonable (annualized, not daily) and not unconscionable.",
        "consequences": "Vague payment terms can lead to disputed deadlines. High daily penalties (e.g. ₹500/day or 2% daily interest) constitute legal penalties, which are generally unenforceable under Indian contract law but cause severe harassment."
    },
    "Termination": {
        "name": "Termination",
        "default_rewrite": "Either party may terminate this agreement by giving at least 30 days' written notice to the other party. If either party commits a material breach of this agreement, the non-breaching party may terminate this agreement if the breach is not cured within 15 days of written notice.",
        "laws": ["Indian Contract Act, 1872 — Section 73", "Transfer of Property Act, 1882 — Section 106", "Model Tenancy Act, 2021 — Section 21"],
        "negotiation_advice": "Request that termination rights be mutual. If the landlord has a 24-hour or immediate termination clause, insist on at least a 30-day written notice and a cure period (e.g. 15 days) to correct any alleged lease violations.",
        "consequences": "One-sided immediate termination clauses can force your business to evict or stop operations overnight, leading to massive financial losses, loss of goodwill, and legal vulnerability."
    },
    "Lock-in": {
        "name": "Lock-In Period",
        "default_rewrite": "Both parties agree to a lock-in period of [Months] months. If either party terminates the agreement prior to the expiration of this period, they shall be liable to pay a penalty equivalent to the rent of the remaining months of the lock-in period, up to a maximum of 3 months' rent as liquidated damages.",
        "laws": ["Indian Contract Act, 1872 — Section 74 (Liquidated Damages vs Penalty)", "Supreme Court of India rulings on Lock-in Enforceability"],
        "negotiation_advice": "Negotiate a shorter lock-in period (e.g., 6-12 months). Ensure the penalty for early exit is capped at a maximum of 1-3 months of rent, rather than paying out the entire remaining lock-in period. Forfeiture of deposit in addition to lock-in penalty should be rejected.",
        "consequences": "Extremely long lock-in periods with double penalties are considered punitive under Indian contract law. Courts will only award actual proven damages, not a flat penalty, but landlords may try to freeze your deposit."
    },
    "Penalty": {
        "name": "Penalty Clauses",
        "default_rewrite": "If either party fails to perform any obligation, the other party shall be entitled to recover actual damages. Any liquidated damages specified herein represent a genuine pre-estimate of loss and shall be capped at a reasonable sum.",
        "laws": ["Indian Contract Act, 1872 — Section 74"],
        "negotiation_advice": "Ensure penalties are reciprocal and represent a realistic estimate of damage. Unreasonable penalties (like double rent or forfeiture of all assets) should be struck down or heavily reduced.",
        "consequences": "Uncapped or exorbitant penalty clauses can create huge, unpredictable liabilities. Section 74 of the Indian Contract Act states that courts will not enforce penal clauses and will only award reasonable compensation."
    },
    "Confidentiality": {
        "name": "Confidentiality",
        "default_rewrite": "Each party shall keep confidential all non-public information disclosed by the other party. This obligation shall survive for a period of 2 years after the termination of this agreement. Confidential information does not include information that is publicly known or independently developed.",
        "laws": ["Information Technology Act, 2000", "Indian Contract Act, 1872 — Section 27 (Restraint of Trade / Survival)"],
        "negotiation_advice": "Insist that confidentiality obligations be reciprocal. Ensure there are standard exceptions (e.g., information that is already public, received from a third party, or required to be disclosed by law). Limit the survival period to 2-3 years post-termination.",
        "consequences": "Unbalanced or permanent confidentiality clauses expose your business to litigation if standard business details are shared. Employees and contractors could face injunctions or damages."
    },
    "Privacy": {
        "name": "Privacy & Data Protection",
        "default_rewrite": "Both parties agree to process personal data in compliance with the Digital Personal Data Protection (DPDP) Act, 2023. Each party shall implement appropriate technical and organizational measures to protect personal data from unauthorized access or breach.",
        "laws": ["Digital Personal Data Protection (DPDP) Act, 2023", "Information Technology Act, 2000 — Section 43A"],
        "negotiation_advice": "Ensure data protection clauses align with the DPDP Act, 2023. Limit liability for data breaches if the breach occurred due to factors beyond reasonable control, and include mutual indemnification for regulatory fines.",
        "consequences": "Non-compliance with data privacy laws in India can result in heavy regulatory penalties. Unbalanced data processing clauses can leave you solely responsible for joint data breaches."
    },
    "Liability": {
        "name": "Limitation of Liability",
        "default_rewrite": "Neither party shall be liable to the other for any indirect, incidental, or consequential damages. The aggregate liability of either party under this agreement shall be limited to the total amount actually paid under this agreement in the 12 months preceding the claim.",
        "laws": ["Indian Contract Act, 1872 — Section 73"],
        "negotiation_advice": "Ensure there is a mutual cap on liability (e.g., equivalent to the contract value or 12 months' rent). Expressly exclude indirect, special, or consequential damages (such as lost profits or business interruption).",
        "consequences": "Without a limitation of liability clause, a business can face claims for indirect losses or unlimited damages, which could lead to complete financial bankruptcy in case of a dispute."
    },
    "Unlimited Liability": {
        "name": "Unlimited Liability",
        "default_rewrite": "Except in cases of gross negligence, willful misconduct, or breach of confidentiality, the liability of either party for any claims arising under this agreement shall be capped at the total fees paid under this agreement.",
        "laws": ["Indian Contract Act, 1872 — Section 73 (Direct Damages Only)"],
        "negotiation_advice": "Strenuously object to any clause where you assume unlimited liability. Limit unlimited liability exceptions only to fraud, willful misconduct, or gross negligence, and place a financial cap on all standard contract breaches.",
        "consequences": "Unlimited liability clauses expose your business and personal assets to unlimited claims, nullifying the protection of a limited liability company or partnership."
    },
    "Force Majeure": {
        "name": "Force Majeure",
        "default_rewrite": "Neither party shall be liable for any failure or delay in performing obligations due to events beyond its reasonable control, including acts of God, war, pandemic, government restrictions, or natural disasters. If a Force Majeure event continues for more than 45 days, either party may terminate this agreement upon written notice.",
        "laws": ["Indian Contract Act, 1872 — Section 56 (Frustration of Contract)"],
        "negotiation_advice": "Ensure the clause includes modern events like pandemics, lockdowns, and government orders. Add a provision that rent or service obligations are suspended or reduced proportionally during the force majeure period.",
        "consequences": "Without a modern Force Majeure clause, you may remain legally obligated to pay full rent or perform services even during a government-mandated lockdown or natural disaster, leading to severe cash flow crises."
    },
    "Jurisdiction": {
        "name": "Jurisdiction",
        "default_rewrite": "This agreement shall be subject to the exclusive jurisdiction of the courts located in [City], India.",
        "laws": ["Code of Civil Procedure, 1908 — Section 20", "Indian Contract Act, 1872 — Section 28"],
        "negotiation_advice": "Choose the city where your business is based, or a mutually convenient central city. Never agree to a jurisdiction in a foreign country or a distant state for a local contract, as it increases dispute costs exponentially.",
        "consequences": "An unfavorable jurisdiction clause forces you to hire lawyers and travel to a distant city or country to defend or file any lawsuit, rendering minor disputes too expensive to contest."
    },
    "Governing Law": {
        "name": "Governing Law",
        "default_rewrite": "This agreement shall be governed by and construed in accordance with the laws of India.",
        "laws": ["Indian Contract Act, 1872"],
        "negotiation_advice": "Ensure the governing law is specified as Indian law, particularly for domestic transactions. Foreign governing laws are costly to interpret and contest.",
        "consequences": "Vague or foreign governing laws create extreme uncertainty and require foreign legal experts to resolve disputes, adding immense overhead."
    },
    "Refund": {
        "name": "Refund Policy",
        "default_rewrite": "In the event of cancellation or termination of services by the Service Provider, the Client shall be entitled to a pro-rata refund of any prepaid fees for uncompleted services within 14 business days.",
        "laws": ["Consumer Protection Act, 2019 — Unfair Trade Practices", "Indian Contract Act, 1872"],
        "negotiation_advice": "Strikethrough 'strict no-refund' clauses in service or purchase agreements. Insist on a prorated refund if the service provider terminates the contract early, defaults, or fails to deliver.",
        "consequences": "'No refund' clauses are frequently challenged in Consumer Courts under the Consumer Protection Act as 'unfair contracts.' However, resolving this requires consumer court filings, so proactive negotiation is best."
    },
    "Warranty": {
        "name": "Warranties & Guarantees",
        "default_rewrite": "The Provider warrants that the services/goods shall be performed/supplied with reasonable skill and care, in accordance with industry standards. The Provider shall remedy any defects or non-conformity at its own cost within 15 days of notice.",
        "laws": ["Sale of Goods Act, 1930 — Sections 14-16 (Implied Conditions/Warranties)"],
        "negotiation_advice": "Ensure the provider gives standard warranties of quality and compliance. If you are the provider, limit warranties to a specified period (e.g. 90 days) and disclaim all other implied warranties.",
        "consequences": "Disclaiming all warranties allows vendors to deliver subpar goods or buggy software without liability. For service providers, too broad a warranty can lead to endless unpaid re-work requests."
    },
    "Indemnity": {
        "name": "Indemnity",
        "default_rewrite": "Each party shall indemnify and hold harmless the other party from and against any third-party claims, damages, or liabilities arising out of the indemnifying party's gross negligence, willful misconduct, or breach of applicable law under this agreement.",
        "laws": ["Indian Contract Act, 1872 — Section 124 & 125"],
        "negotiation_advice": "Indemnity must be mutual. Limit indemnity claims to direct third-party claims arising from gross negligence or legal breaches. Avoid broad indemnification for standard contract breaches, which can bypass the duty to mitigate damages.",
        "consequences": "A one-sided, broad indemnity clause can force your business to pay for all of the other party's legal bills, claims, and damages even if they were partially at fault or could have avoided the loss."
    },
    "Subletting": {
        "name": "Sub-letting Rights",
        "default_rewrite": "The Tenant shall not sublet, assign, or part with the possession of the premises without the prior written consent of the Landlord, which consent shall not be unreasonably withheld, conditioned, or delayed.",
        "laws": ["Transfer of Property Act, 1882 — Section 108(j)", "Model Tenancy Act, 2021"],
        "negotiation_advice": "Negotiate to add the phrase 'consent shall not be unreasonably withheld, conditioned, or delayed'. This prevents the landlord from blocking corporate restructuring or sublease requests arbitrarily.",
        "consequences": "An absolute ban on subletting or transferring possession can prevent your company from transferring the lease to a subsidiary or selling the business (if the lease is an asset)."
    },
    "Renewal": {
        "name": "Renewal Options",
        "default_rewrite": "This agreement may be renewed upon mutual written consent of both parties, at least 30 days prior to the expiration of the term. The rent increase upon renewal shall be capped at a mutually agreed rate not exceeding 5-8%.",
        "laws": ["Transfer of Property Act, 1882", "Model Tenancy Act, 2021"],
        "negotiation_advice": "Avoid automatic renewals that lock you in without active approval. Add a cap on the rent increase upon renewal (standard in India is 5% to 8% per annum) to prevent arbitrary spikes.",
        "consequences": "Uncapped renewal terms allow landlords to hike rent by 30% or 50% upon renewal, forcing you to relocate your business and waste fit-out investments."
    },
    "Inspection Rights": {
        "name": "Inspection & Landlord Entry",
        "default_rewrite": "The Landlord or their authorized representatives shall have the right to enter the premises to inspect the condition or perform necessary repairs, provided they give the Tenant at least 24 hours' prior written notice and schedule entry during reasonable business hours (9 AM - 6 PM).",
        "laws": ["Model Tenancy Act, 2021 — Section 15 (Entry of Landlord)", "Indian Constitution — Article 21 (Right to Privacy)"],
        "negotiation_advice": "Strictly object to entry 'at any time without notice'. Insist on a minimum 24-hour advance written notice, entry only during normal business hours, and the presence of a tenant representative.",
        "consequences": "Allowing unrestricted landlord entry violates your right to quiet enjoyment, compromises business privacy, poses safety risks, and can lead to disruptions of commercial operations."
    },
    "Notice Period": {
        "name": "Notice Period",
        "default_rewrite": "Either party may terminate this agreement by providing the other party with a minimum of 30 days' written notice.",
        "laws": ["Transfer of Property Act, 1882 — Section 106"],
        "negotiation_advice": "Notice periods should be symmetric. Ensure the notice period is realistic (standard is 30 days for rentals, 30-90 days for commercial or employment agreements).",
        "consequences": "Short notice periods (like 24 hours or 7 days) can disrupt operations and leave your business stranded without an alternative location or vendor."
    },
    "Arbitration": {
        "name": "Arbitration",
        "default_rewrite": "Any dispute arising out of this agreement shall be referred to arbitration in accordance with the Arbitration and Conciliation Act, 1996. The seat and venue of arbitration shall be Nagpur, India, and the proceedings shall be conducted in English.",
        "laws": ["Arbitration and Conciliation Act, 1996 (Amended 2015 & 2019)"],
        "negotiation_advice": "Ensure the seat of arbitration is convenient. Check that arbitrator fees are split equally and that the arbitrator must be appointed mutually, not unilaterally by one party.",
        "consequences": "Unilateral arbitrator appointment has been ruled illegal by the Supreme Court of India. Balanced arbitration clauses speed up dispute resolution without high litigation costs."
    },
    "Dispute Resolution": {
        "name": "Dispute Resolution Process",
        "default_rewrite": "In the event of a dispute, the parties shall first attempt to resolve the matter amicably through mediation or negotiation within 30 days. If unresolved, the dispute may then be referred to arbitration or competent courts.",
        "laws": ["Arbitration and Conciliation Act, 1996", "Commercial Courts Act, 2015 (Pre-institution Mediation)"],
        "negotiation_advice": "Ensure there is a mandatory 'cooling-off' period of 15 to 30 days for amicable settlement/mediation before any party can rush to court or file for arbitration.",
        "consequences": "Without a structured step-by-step dispute resolution process, parties can immediately file aggressive lawsuits for minor issues, running up legal costs."
    },
    "Intellectual Property": {
        "name": "Intellectual Property Rights",
        "default_rewrite": "Each party shall retain all right, title, and interest in its pre-existing intellectual property. Any intellectual property developed solely or jointly under this agreement shall belong exclusively to the party that paid for its creation, upon full payment of fees.",
        "laws": ["Indian Copyright Act, 1957", "Patents Act, 1970"],
        "negotiation_advice": "Verify that IP transfer only occurs upon 'full payment' of agreed fees. If you are hiring a developer/designer, ensure all IP transfers automatically. If you are the provider, protect your core templates and background IP.",
        "consequences": "Vague IP clauses can lead to disputes where you pay for development but do not legally own the software or designs, preventing you from licensing, patenting, or selling the product."
    },
    "Maintenance": {
        "name": "Maintenance & Repair Cost",
        "default_rewrite": "The Landlord shall be responsible for all structural repairs, major plumbing, and electrical issues. The Tenant shall be responsible for routine daily upkeep, minor repairs costing under ₹2,000, and damage caused by their negligence.",
        "laws": ["Model Tenancy Act, 2021 — Section 15 (Second Schedule list of repairs)", "Transfer of Property Act, 1882 — Sec. 108"],
        "negotiation_advice": "Insist that structural maintenance (leaks, wall cracks, wiring, lift maintenance) is the landlord's responsibility. The tenant should only cover minor consumables (bulbs, cleaning) and damages caused directly by tenant negligence.",
        "consequences": "Forcing the tenant to pay for structural repairs (e.g. replacing a rusted water tank or fixing leaking roofs) is financially exploitative and can run into lakhs of rupees."
    },
    "Insurance": {
        "name": "Insurance Obligations",
        "default_rewrite": "Each party shall maintain appropriate insurance coverage for their respective interests under this agreement. The Tenant shall maintain insurance for their personal property/equipment, and the Landlord shall maintain building structure insurance.",
        "laws": ["Insurance Act, 1938"],
        "negotiation_advice": "Check that you are not forced to insure the entire building structure or take out excessive policy covers. Keep policy requirements limited to standard business liability and your own equipment.",
        "consequences": "Absence of clear insurance division can result in disputes over who pays for damages during natural disasters, fires, or structural collapse."
    },
    "Late Fees": {
        "name": "Late Fees",
        "default_rewrite": "Any payments not received by the due date shall bear interest at the rate of 1% per month (12% per annum) calculated from the due date until paid, with a grace period of 5 business days.",
        "laws": ["Indian Contract Act, 1872 — Section 74"],
        "negotiation_advice": "Strike out flat daily penalty sums (e.g., '₹1,000 per day for delay'). Ask for a reasonable percentage-based late interest rate (e.g. 1% to 1.5% per month) to avoid punitive interest charges.",
        "consequences": "Exorbitant daily late fees quickly accumulate and act as a tool for financial coercion during disputes, despite being legally weak in court."
    },
    "Entry Rights": {
        "name": "Quiet Enjoyment & Entry",
        "default_rewrite": "Subject to the Tenant paying the rent and performing their obligations, the Tenant shall quietly hold and enjoy the premises during the tenancy without interruption by the Landlord.",
        "laws": ["Transfer of Property Act, 1882 — Section 108(c)"],
        "negotiation_advice": "Ensure the contract contains a 'covenant of quiet enjoyment'. This legally bars the landlord from locking the gate, shutting off utilities, or interfering with daily business operations.",
        "consequences": "Without quiet enjoyment protections, landlords can cut electricity, block customer entry, or lock the premises during minor disputes, destroying business operations."
    },
    "Default": {
        "name": "Default Clauses",
        "default_rewrite": "In the event of default by either party, the non-defaulting party shall provide a written notice of default. The defaulting party shall have 15 days from receipt of notice to cure the default before legal remedies are pursued.",
        "laws": ["Indian Contract Act, 1872"],
        "negotiation_advice": "Always demand a written 'Notice of Default' and a minimum 15-day cure period. Avoid clauses that declare automatic default and immediate forfeiture of rights without notice.",
        "consequences": "Automatic default clauses trigger immediate cancellation or forfeiture of deposits for minor admin slip-ups, leaving you zero opportunity to resolve the issue."
    },
    "Assignment": {
        "name": "Assignment Rights",
        "default_rewrite": "Neither party shall assign or transfer its rights or obligations under this agreement without the prior written consent of the other party, which consent shall not be unreasonably withheld or delayed.",
        "laws": ["Indian Contract Act, 1872 — Assignment principles"],
        "negotiation_advice": "Add the caveat that consent to assign or transfer 'shall not be unreasonably withheld, conditioned, or delayed', especially if you plan to structure, sell, or merge your business.",
        "consequences": "An absolute transfer ban blocks mergers, acquisitions, or standard corporate reorganizations, as you cannot legally assign your rights to the new entity."
    },
    "Other": {
        "name": "General Clauses",
        "default_rewrite": "This agreement constitutes the entire understanding between the parties and supersedes all prior discussions or agreements. Any amendments must be made in writing and signed by both parties.",
        "laws": ["Indian Contract Act, 1872", "Indian Evidence Act, 1872 — Section 91 & 92 (Exclusion of oral agreement)"],
        "negotiation_advice": "Ensure there is an 'Entire Agreement' and 'Written Amendment' clause. This prevents any party from claiming there was a separate verbal agreement or side promise that overrides the contract.",
        "consequences": "Without a written amendment clause, parties can claim oral alterations, leading to conflicting claims and prolonged, expensive litigation in court."
    }
}
