from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Contract Clause Detector Running"

@app.route("/analyze", methods=["POST"])
def analyze():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]

    text = ""

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        risk_score = 0
        issues = []
        missing_clauses = []

        lower_text = text.lower()
        print(lower_text[:3000])

        if "termination" not in lower_text:
            missing_clauses.append("Termination Clause")

        if "dispute" not in lower_text:
            missing_clauses.append("Dispute Resolution Clause")

        if "refund" not in lower_text:
            missing_clauses.append("Refund Policy Clause")

            missing_clauses.append("Governing Law Clause")

        if "security deposit" in lower_text:
            risk_score += 20
            issues.append("Large Security Deposit Clause")

           
        if "forfeit" in lower_text:
            risk_score += 20
            issues.append("Deposit Forfeiture Clause")

        if "without notice" in lower_text:
            risk_score += 25
            issues.append("Termination Without Notice")

        if "sole discretion" in lower_text:
            risk_score += 20
            issues.append("One-Sided Authority Clause")

        if "penalty" in lower_text:
            risk_score += 15
            issues.append("Penalty Clause")

        if "lock-in" in lower_text:
            risk_score += 15
            issues.append("Long Lock-In Period")

        if "renewal" in lower_text:
            risk_score += 10
            issues.append("Automatic Renewal Clause")

        if "late fee" in lower_text:
            risk_score += 10
            issues.append("Late Fee Clause")

        if "landlord" in lower_text and "notice" not in lower_text:
            risk_score += 15
            issues.append("Landlord Rights Without Notice")

        return jsonify({
            "success": True,
            "risk_score": risk_score,
            "issues": issues,
            "missing_clauses": missing_clauses,
            "text": text[:1000]
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)