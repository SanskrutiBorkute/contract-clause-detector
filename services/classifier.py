# ClauseGuard AI — Semantic Clause Classification Service
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Typical text patterns for each clause category to establish semantic anchor vectors
CATEGORY_TEMPLATES = {
    "Security Deposit": [
        "tenant shall pay landlord security deposit amount forfeit return vacate normal wear tear",
        "refundable security deposit returned days after vacating premises less deductions structural damage",
        "deposit of rupees held in escrow interest-bearing landlord may apply towards tenant defaults"
    ],
    "Payment Terms": [
        "tenant shall pay rent monthly due on before grace period method bank transfer invoice payment terms",
        "monthly consideration shall be payable by client within days of invoice date recurring billing fee",
        "rent is payable in advance payment schedule bank account details check draft currency rupees"
    ],
    "Termination": [
        "either party may terminate this agreement written notice cure period material breach terminate cancel lease",
        "termination of services client provider convenience termination for cause default termination clause",
        "terminate this lease immediately upon oral notice vacate premises without court order process"
    ],
    "Lock-in": [
        "lock-in period minimum term months prior exit early termination lock-in penalty remain payable",
        "both parties agree not to terminate this agreement for a minimum duration of months lock in",
        "vacate before the lock-in expires penalty equivalent to remaining rent liquidated damages"
    ],
    "Penalty": [
        "penalty liquidated damages default breach rate of interest compensation penal charge enforce",
        "shall pay a penalty fee of rupees for non-compliance breach of obligations punitive damages",
        "interest rate of percent per day annum on defaulted obligations delay fee penalty sum"
    ],
    "Confidentiality": [
        "keep confidential non-disclosure proprietary information disclosing receiving party protect secret",
        "confidentiality agreement trade secrets disclosure exceptions public domain survival post termination",
        "shall not disclose any details of this contract to third parties confidential information"
    ],
    "Privacy": [
        "privacy policy data protection processing personal data digital personal data protection dpdp act breach",
        "user privacy data security measures compliance information technology act personal information transfer",
        "safeguard customer data privacy standard rules encrypt data regulatory compliance"
    ],
    "Liability": [
        "limitation of liability limit aggregate liability direct damages exclude indirect incidental consequential loss",
        "total liability of provider under this contract capped at fees paid in previous twelve months cap",
        "neither party is liable for special damages lost profits business interruption"
    ],
    "Unlimited Liability": [
        "unlimited liability aggregate liability shall not be limited for any damages claims breach",
        "full liability for direct and indirect damages without any financial cap unlimited responsibility",
        "tenant assumes all liabilities and holds landlord harmless without limitation"
    ],
    "Force Majeure": [
        "force majeure act of god pandemic epidemic war strike lockouts natural disaster government restriction delay perform",
        "performance suspended due to events beyond reasonable control acts of god lock-down force majeure clause",
        "neither party liable for failure to perform due to unforeseen events beyond control strike flood earthquake"
    ],
    "Jurisdiction": [
        "exclusive jurisdiction of courts in Nagpur Maharashtra Mumbai Delhi court city litigation venue",
        "any legal action proceeding shall be instituted solely in courts of state country jurisdiction",
        "consent to personal jurisdiction and venue of Nagpur courts"
    ],
    "Governing Law": [
        "governed by and construed in accordance with laws of India State of Maharashtra governing law",
        "governing law of Nagpur India legal framework applicable legislation",
        "this agreement shall be subject to the laws of India"
    ],
    "Refund": [
        "refund policy prepaid fees return money cancellation fee non-refundable refund window prorated refund",
        "client entitled to full refund if services not completed default cancellation refund terms",
        "no refunds shall be issued under any circumstances non refundable cancellation fees"
    ],
    "Warranty": [
        "warrants that services performed reasonable skill care fit for purpose merchantability warranty period remedy defects",
        "guarantee product quality warranty of title non-infringement conform to specifications standard",
        "disclaims all other warranties express or implied merchantability fitness for particular purpose"
    ],
    "Indemnity": [
        "indemnify defend hold harmless from against any third party claims liabilities damages costs fees legal bills",
        "indemnification for gross negligence willful misconduct infringement breach of law",
        "party agrees to indemnify and protect the other party against losses arising out of performance"
    ],
    "Subletting": [
        "tenant sublet assign part with possession sublease prior written consent of landlord assign lease",
        "shall not subletting or transfer tenancy rights to third party without landlord approval",
        "unreasonably withhold consent to sublet subleasing terms transfer of possession"
    ],
    "Renewal": [
        "renewal option renew agreement rent increase cap mutual consent term extension renew lease",
        "automatic renewal of contract unless written termination notice given days prior to expiry renewal terms",
        "renew this agreement for a further period of months with rent escalation of percent"
    ],
    "Inspection Rights": [
        "inspection rights landlord enter premises check condition repairs reasonable business hours advance notice",
        "right of entry for inspection and repairs landlord representatives enter anytime without notice",
        "inspect property state with minimum twenty-four hours notice inspect during office hours"
    ],
    "Notice Period": [
        "notice period written notice days calendar month prior written termination notice",
        "written notice of days in advance for exit notice duration timeline specify notice",
        "either party must provide months notice in writing before exiting agreement"
    ],
    "Arbitration": [
        "arbitration seat venue Nagpur Arbitration and Conciliation Act sole arbitrator conduct proceedings english",
        "referred to arbitration mutually appointed arbitrator arbitration award final binding legal dispute",
        "resolution through arbitration under the rules of arbitration Nagpur"
    ],
    "Dispute Resolution": [
        "dispute resolution process mediation negotiation amicable settlement steps refer court arbitration cooling-off",
        "parties shall attempt to resolve disputes through good faith negotiations prior to filing lawsuit",
        "mediation cooling-off period of days to settle disputes amicably"
    ],
    "Intellectual Property": [
        "intellectual property rights pre-existing IP copyright patent trademark proprietary designs developer ownership code transfer",
        "ownership of inventions designs copyrights developed under this agreement assignment of IP",
        "work for hire developer assigns all intellectual property rights to the client upon full payment"
    ],
    "Maintenance": [
        "maintenance costs major minor repairs structural repairs plumbing electrical landlord tenant responsibility",
        "tenant responsible for daily routine maintenance structural repair cost borne by landlord",
        "landlord repair roof exterior walls structural integrity during lease period maintenance fee"
    ],
    "Insurance": [
        "insurance policy premium cover third-party liability asset insurance tenant landlord maintain insurance",
        "carry and maintain adequate commercial liability insurance policy coverage limits",
        "building structure insurance and public liability coverage required under this lease"
    ],
    "Late Fees": [
        "late fees late payment interest percentage per month grace period delay penalty charge overdue amount",
        "accrued interest of percent on delayed invoice payment late charge penalty per day",
        "grace period of days for late rent after which late fee is applied"
    ],
    "Entry Rights": [
        "quiet enjoyment entry rights landlord entry notice secure quiet possession interference",
        "peaceful possession quiet enjoyment without interruption or disturbance from landlord",
        "landlord covenants that tenant shall peaceably hold and enjoy premises during term"
    ],
    "Default": [
        "default event cure period notice of default failure to pay breach of covenant default remedies",
        "automatic default without notice forfeiture of rights in event of non-performance",
        "cure notice required to declare defaulting party in breach of agreement"
    ],
    "Assignment": [
        "assignment of rights transfer obligations subsidiary corporate restructure consent assign contract",
        "neither party shall assign transfer this agreement without written consent of other",
        "assign leasehold rights merger acquisition assignment clause"
    ],
    "Other": [
        "severability counter parts entire agreement amendments in writing waiver headings counterparts",
        "miscellaneous terms signatures seals annexures schedule exhibits reference data",
        "force and effect other sections validity of agreement execution page"
    ]
}

# Strong keyword signals for specific categories to boost similarity checks
KEYWORD_SIGNALS = {
    "Security Deposit": [r"security\s+deposit", r"deposit\s+of\s+₹", r"deposit\s+amount", r"forfeit.*deposit"],
    "Payment Terms": [r"monthly\s+rent", r"rent\s+shall\s+be", r"due\s+on\s+or\s+before", r"grace\s+period", r"invoice\s+within"],
    "Termination": [r"terminate\s+this\s+agreement", r"notice\s+to\s+terminate", r"right\s+to\s+terminate", r"unilateral\s+termination"],
    "Lock-in": [r"lock-in\s+period", r"lock\s+in", r"minimum\s+term", r"36\s+months\s+lock", r"24\s+months\s+lock"],
    "Penalty": [r"penalty\s+of", r"liquidated\s+damages", r"penal\s+charge", r"forfeiture\s+of\s+the\s+full"],
    "Confidentiality": [r"confidential", r"non-disclosure", r"nda", r"proprietary\s+info"],
    "Privacy": [r"privacy\s+policy", r"personal\s+data", r"dpdp", r"data\s+protection"],
    "Liability": [r"limitation\s+of\s+liability", r"indirect\s+damages", r"consequential\s+damages", r"capped\s+at\s+rent", r"liability\s+cap"],
    "Unlimited Liability": [r"unlimited\s+liability", r"liability\s+shall\s+be\s+unlimited", r"without\s+limitation.*liability"],
    "Force Majeure": [r"force\s+majeure", r"act\s+of\s+god", r"natural\s+disaster", r"pandemic", r"unforeseen\s+event"],
    "Jurisdiction": [r"jurisdiction\s+of", r"exclusive\s+jurisdiction", r"courts\s+in", r"courts\s+at"],
    "Governing Law": [r"governed\s+by", r"laws\s+of\s+india", r"governing\s+law"],
    "Refund": [r"refund", r"refundable", r"non-refundable"],
    "Warranty": [r"warrant", r"guarantee", r"quality\s+of\s+service", r"merchantability"],
    "Indemnity": [r"indemnify", r"indemnification", r"hold\s+harmless"],
    "Subletting": [r"sublet", r"sub-let", r"sublease", r"sub-lease", r"assign\s+or\s+transfer\s+possession"],
    "Renewal": [r"renewal", r"renew", r"option\s+to\s+renew", r"rent\s+increase.*renewal"],
    "Inspection Rights": [r"inspect", r"inspection", r"landlord\s+entry", r"entry\s+for\s+repairs"],
    "Notice Period": [r"notice\s+period", r"days'\s+written\s+notice", r"days\s+notice"],
    "Arbitration": [r"arbitration", r"arbitrator", r"arbitrate", r"arbitration\s+and\s+conciliation"],
    "Dispute Resolution": [r"dispute\s+resolution", r"disputes\s+arising", r"mediate", r"mediation", r"amicable\s+settlement"],
    "Intellectual Property": [r"intellectual\s+property", r"copyright", r"patent", r"trademark", r"proprietary\s+rights"],
    "Maintenance": [r"maintenance", r"structural\s+repairs", r"repairs\s+and\s+maintenance", r"plumbing", r"electrical"],
    "Insurance": [r"insurance", r"insure", r"policy\s+coverage"],
    "Late Fees": [r"late\s+fee", r"late\s+payment", r"delay\s+charge", r"interest\s+on\s+overdue"],
    "Entry Rights": [r"quiet\s+enjoyment", r"quiet\s+possession", r"peacefully\s+enjoy"],
    "Default": [r"default", r"event\s+of\s+default", r"cure\s+the\s+default"],
    "Assignment": [r"assignment\s+rights", r"assign\s+or\s+transfer\s+rights"],
}

class ClauseClassifier:
    def __init__(self):
        # Flatten categories and texts for training the vectorizer
        self.categories = list(CATEGORY_TEMPLATES.keys())
        corpus = []
        self.cat_indices = []
        
        for idx, cat in enumerate(self.categories):
            templates = CATEGORY_TEMPLATES[cat]
            for t in templates:
                corpus.append(t)
                self.cat_indices.append(idx)
        
        # Fit vectorizer
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.vectors = self.vectorizer.fit_transform(corpus)

    def classify(self, clause_text):
        """
        Classifies clause_text into one of the 29 categories using semantic TF-IDF cosine similarity + rules.
        Returns predicted category (str) and confidence score (int, 0-100).
        """
        lower_clause = clause_text.lower()
        clause_vector = self.vectorizer.transform([lower_clause])
        
        # Calculate cosine similarity with all anchor templates
        similarities = cosine_similarity(clause_vector, self.vectors)[0]
        
        # Aggregate similarity scores per category (average of templates)
        cat_scores = np.zeros(len(self.categories))
        for idx, sim in enumerate(similarities):
            cat_idx = self.cat_indices[idx]
            # Accumulate maximum similarity
            if sim > cat_scores[cat_idx]:
                cat_scores[cat_idx] = sim
        
        # Apply keyword boosts
        for idx, cat in enumerate(self.categories):
            if cat in KEYWORD_SIGNALS:
                boost = 0.0
                for pattern in KEYWORD_SIGNALS[cat]:
                    if re.search(pattern, lower_clause):
                        boost += 0.25 # add 25% boost for every keyword matched
                cat_scores[idx] += boost
        
        # Find best category
        best_idx = np.argmax(cat_scores)
        best_score = cat_scores[best_idx]
        best_category = self.categories[best_idx]
        
        # Calculate confidence score
        # Base confidence from raw cosine similarity + boosts
        confidence = int(min(99, max(50, best_score * 100)))
        
        # If score is very low, fall back to "Other"
        if best_score < 0.02:
            return "Other", 90
            
        return best_category, confidence

