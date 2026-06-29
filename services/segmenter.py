# ClauseGuard AI — Clause Segmentation & Contract Type Detection Service
import re

class ClauseSegmenter:
    CONTRACT_TYPES = {
        "Rental Agreement": [r"rental\s+agreement", r"lease\s+agreement", r"tenancy\s+agreement", r"landlord", r"tenant", r"rent\s+agreement"],
        "Employment Contract": [r"employment\s+contract", r"employment\s+agreement", r"offer\s+letter", r"employer", r"employee", r"salary"],
        "NDA": [r"non-disclosure", r"nda", r"confidentiality\s+agreement", r"confidential\s+information", r"disclosing\s+party", r"receiving\s+party"],
        "Vendor Agreement": [r"vendor\s+agreement", r"supply\s+agreement", r"supplier\s+agreement", r"vendor", r"purchaser"],
        "Service Agreement": [r"service\s+agreement", r"services\s+agreement", r"service\s+provider", r"client", r"sla"],
        "Loan Agreement": [r"loan\s+agreement", r"promissory\s+note", r"borrower", r"lender", r"repayment"],
        "Purchase Agreement": [r"purchase\s+agreement", r"sales\s+contract", r"buyer", r"seller"],
        "Freelance Contract": [r"freelance\s+contract", r"freelance\s+agreement", r"independent\s+contractor"],
        "Partnership Agreement": [r"partnership\s+agreement", r"partners", r"partnership\s+deed"],
        "Consulting Agreement": [r"consulting\s+agreement", r"consultant", r"client"]
    }

    @classmethod
    def detect_contract_type(cls, text):
        """
        Detects the type of contract based on keyword patterns.
        """
        lower_text = text.lower()
        scores = {}
        for ctype, patterns in cls.CONTRACT_TYPES.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, lower_text))
                score += matches
            scores[ctype] = score
        
        # Find highest score
        best_type = max(scores, key=scores.get)
        if scores[best_type] > 0:
            return best_type
        return "Other"

    @classmethod
    def segment_clauses(cls, text):
        """
        Segments the text into a list of clauses.
        Returns a list of dicts: [{'id': str, 'number': str, 'title': str, 'text': str}]
        """
        # Clean text
        text = text.replace('\r\n', '\n').strip()
        
        # Regex to match headers like:
        # Clause 1. Rent and Payment
        # Section 2: Security Deposit
        # ARTICLE III — Confidentiality
        # 4. Term and Termination
        # 10. Miscellaneous
        # Heading followed by a colon or dot or dash, and then title text.
        header_regex = re.compile(
            r'^(?:Clause|Section|Article|Para|Paragraph)?\s*(\d+|[ivxldm]+)[:.\s\-–—\)]+\s*([^\n]{3,80})',
            re.IGNORECASE | re.MULTILINE
        )
        
        matches = list(header_regex.finditer(text))
        clauses = []
        
        if len(matches) > 1:
            for i, match in enumerate(matches):
                start_idx = match.start()
                end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(text)
                
                clause_num_raw = match.group(1).strip()
                clause_title = match.group(2).strip()
                # Start text from match.start(2) (the title match group) to prevent text cutoff
                clause_text = text[match.start(2):end_idx].strip()
                
                # Format clause number
                clause_number = f"CLAUSE {clause_num_raw.upper()}"
                
                clauses.append({
                    "id": f"clause_{i + 1}",
                    "number": clause_number,
                    "title": clause_title,
                    "text": clause_text
                })
        else:
            # Fallback segmenting by double newline / paragraphs
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            for i, para in enumerate(paragraphs):
                # Split first line as title or generate from first few words
                lines = [l.strip() for l in para.split('\n') if l.strip()]
                if not lines:
                    continue
                
                # Check if first line can be a title
                first_line = lines[0]
                if len(first_line) < 60 and (first_line.isupper() or len(lines) > 1):
                    title = first_line
                    # Keep full paragraph as body to avoid discarding the first line
                    body = para
                else:
                    words = first_line.split()
                    title = " ".join(words[:4]) + "..." if len(words) > 4 else first_line
                    body = para
                
                clauses.append({
                    "id": f"clause_{i + 1}",
                    "number": f"CLAUSE {i + 1}",
                    "title": title,
                    "text": body
                })
                
        return clauses
