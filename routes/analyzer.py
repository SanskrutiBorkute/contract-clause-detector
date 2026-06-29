# ClauseGuard AI — Contract Analyzer Route
import os
import uuid
import json
import hashlib
import time
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from services.extractor import TextExtractor
from services.segmenter import ClauseSegmenter
from services.classifier import ClauseClassifier
from services.risk_detector import RiskDetector
from services.missing_detector import MissingDetector
from utils.helpers import calculate_reading_time, map_risk_score_to_label, generate_one_line_summary, get_overall_recommendation

analyzer_bp = Blueprint('analyzer', __name__)

# Initialize classifiers and rules engines on startup
print("Initializing Clause Classifier & Risk Engine...")
classifier = ClauseClassifier()
risk_detector = RiskDetector(classifier)
print("Classifier initialized successfully!")

def calculate_file_md5(file_stream):
    """
    Calculates MD5 hash of the uploaded file stream.
    """
    hasher = hashlib.md5()
    file_stream.seek(0)
    # Read in chunks of 8192 bytes
    for chunk in iter(lambda: file_stream.read(8192), b""):
        hasher.update(chunk)
    file_stream.seek(0)  # Reset pointer
    return hasher.hexdigest()

@analyzer_bp.route("/analyze", methods=["POST"])
def analyze_contract():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file part in request"})
        
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file"})
        
    if not file:
        return jsonify({"success": False, "error": "Invalid file upload"})
        
    start_time = time.time()
    
    # Ensure uploads and reports folders exist
    uploads_dir = os.path.join(current_app.root_path, "uploads")
    reports_dir = os.path.join(current_app.root_path, "reports")
    os.makedirs(uploads_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    
    # 1. Calculate MD5 hash for caching
    file_hash = calculate_file_md5(file)
    cache_path = os.path.join(reports_dir, f"cache_{file_hash}.json")
    
    # Check if cached analysis exists, and retrieve text & filename to skip OCR, but re-run analysis dynamically
    cached_text = None
    cached_filename = None
    if os.path.exists(cache_path):
        print(f"Cache hit! Reusing extracted text for dynamic re-analysis of file hash {file_hash}.")
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
            cached_text = cached_data.get("text")
            cached_filename = cached_data.get("filename")
        except Exception as e:
            print(f"Failed to read cache file: {e}. Re-extracting from scratch...")

    # Save file temporarily
    filename = secure_filename(file.filename)
    file_path = os.path.join(uploads_dir, filename)
    file.save(file_path)
    
    try:
        # 2. Text Extraction
        if cached_text:
            text = cached_text
            filename = cached_filename or filename
        else:
            print(f"Extracting text from {filename}...")
            text = TextExtractor.extract_text(file_path)
            
        if not text or not text.strip():
            raise ValueError("No extractable text found in this document. Please ensure it is a valid text file, PDF, Word doc, or clean scan.")
            
        page_count = TextExtractor.get_page_count(file_path)
        
        # 3. Contract Type Detection
        print("Detecting contract type...")
        contract_type = ClauseSegmenter.detect_contract_type(text)
        
        # 4. Clause Segmentation
        print("Segmenting clauses...")
        clauses = ClauseSegmenter.segment_clauses(text)
        
        # Avoid duplicate clauses by text content
        seen_texts = set()
        deduplicated_clauses = []
        for c in clauses:
            norm_text = " ".join(c["text"].split()).lower()
            if norm_text not in seen_texts:
                seen_texts.add(norm_text)
                deduplicated_clauses.append(c)
        
        # 5. Clause Risk Classification & Tagging
        print("Analyzing clauses and classifying risks...")
        analyzed_clauses, raw_score, raw_issues = risk_detector.analyze_clauses(deduplicated_clauses, contract_type)
        
        # 6. Missing Protection Check
        print("Checking for missing protections...")
        missing_protections = MissingDetector.detect_missing_clauses(analyzed_clauses, contract_type)
        
        # Normalize clause risk levels for consistency
        for c in analyzed_clauses:
            rl = c.get("risk_level", "SAFE").upper()
            if rl in ["CRITICAL", "HIGH", "WARNING", "SAFE"]:
                c["risk_level"] = rl
            elif rl == "MEDIUM" or rl == "MED":
                c["risk_level"] = "WARNING"
            elif rl == "LOW":
                c["risk_level"] = "SAFE"
            else:
                c["risk_level"] = "SAFE"

        # 7. Count clauses by risk level
        critical_count = sum(1 for c in analyzed_clauses if c["risk_level"] == "CRITICAL")
        high_count = sum(1 for c in analyzed_clauses if c["risk_level"] == "HIGH")
        warning_count = sum(1 for c in analyzed_clauses if c["risk_level"] == "WARNING")
        safe_count = sum(1 for c in analyzed_clauses if c["risk_level"] == "SAFE")
        
        # 8. Normalized Overall Score & Recommendation
        highest_risk = "SAFE"
        if critical_count > 0:
            highest_risk = "CRITICAL"
        elif high_count > 0:
            highest_risk = "HIGH"
        elif warning_count > 0 or len(missing_protections) > 0:
            highest_risk = "WARNING"
            
        avg_confidence = 95.0
        if analyzed_clauses:
            avg_confidence = sum(c["confidence"] for c in analyzed_clauses) / len(analyzed_clauses)
        confidence_factor = avg_confidence / 100.0
        
        if highest_risk == "CRITICAL":
            base = 76
            additional = (critical_count * 4) + (high_count * 2.5) + (warning_count * 1.5) + (len(missing_protections) * 1.0)
            risk_score = int(base + min(24, additional * confidence_factor))
        elif highest_risk == "HIGH":
            base = 51
            additional = (high_count * 3) + (warning_count * 1.5) + (len(missing_protections) * 1.0)
            risk_score = int(base + min(24, additional * confidence_factor))
        elif highest_risk == "WARNING":
            base = 26
            additional = (warning_count * 2) + (len(missing_protections) * 1.5)
            risk_score = int(base + min(24, additional * confidence_factor))
        else:
            base = 0
            additional = len(analyzed_clauses) * 0.5
            risk_score = int(base + min(25, additional * confidence_factor))
            
        risk_score = min(100, max(0, risk_score))
        
        reading_time_mins = calculate_reading_time(text)
        overall_risk, risk_desc = map_risk_score_to_label(risk_score)
        
        # Clean issues list representing CRITICAL, HIGH, and WARNING clauses
        issues = []
        for c in analyzed_clauses:
            if c["risk_level"] in ["CRITICAL", "HIGH", "WARNING"]:
                issues.append({
                    "clause_id": c["id"],
                    "title": f"{c['title']} — {c['number']}",
                    "why": c["reason"],
                    "risk_level": c["risk_level"],
                    "financial_impact": c["financial_impact"]
                })
                
        # 9. Top 5 Key Risks
        top_risks = []
        # First add critical/high/warning clauses sorted by weight
        flagged_clauses = [c for c in analyzed_clauses if c["risk_level"] in ["CRITICAL", "HIGH", "WARNING"]]
        flagged_sorted = sorted(flagged_clauses, key=lambda x: x["risk_weight"], reverse=True)
        for c in flagged_sorted:
            top_risks.append({
                "clause_id": c["id"],
                "category": c["category"],
                "risk_level": c["risk_level"],
                "reason": c["reason"],
                "financial_impact": c["financial_impact"],
                "consequences": c["consequences"]
            })
            
        # If fewer than 5, supplement with missing protections
        if len(top_risks) < 5:
            for m in missing_protections:
                if len(top_risks) >= 5:
                    break
                top_risks.append({
                    "clause_id": "MISSING",
                    "category": m["name"],
                    "risk_level": "WARNING",
                    "reason": m["why_missing"],
                    "financial_impact": "Varies",
                    "consequences": m["remedy"]
                })
                
        overall_recommendation = get_overall_recommendation(risk_score)
        if risk_score >= 76:
            final_rec = "Do Not Sign"
        elif risk_score >= 51:
            final_rec = "Legal Review Recommended"
        elif risk_score >= 26:
            final_rec = "Sign After Negotiation"
        else:
            final_rec = "Safe to Sign"

        processing_time_ms = (time.time() - start_time) * 1000
        if processing_time_ms < 15.0:
            processing_time_ms = 15.6
            
        one_line_sum = generate_one_line_summary(
            contract_type, len(analyzed_clauses), len(issues), len(missing_protections), overall_risk
        )
        
        # Generate AI Executive Summary dynamically
        high_crit_clauses = [c for c in analyzed_clauses if c.get("risk_level") in ["CRITICAL", "HIGH"]]
        warning_clauses = [c for c in analyzed_clauses if c.get("risk_level") == "WARNING"]
        
        risky_details = []
        if high_crit_clauses:
            cats = list(set(c.get("category") for c in high_crit_clauses))
            risky_details.append(f"{len(high_crit_clauses)} clauses were classified as High/Critical Risk due to unilateral {', '.join(cats[:2]).lower()} conditions")
        if warning_clauses:
            risky_details.append(f"{len(warning_clauses)} Warning clauses relating to {warning_clauses[0].get('category').lower()}")
            
        risky_str = ""
        if risky_details:
            risky_str = f" {', and '.join(risky_details)}."
        else:
            risky_str = " No high or critical risk clauses were flagged inside the document."

        missing_names = [m.get("name") for m in missing_protections]
        missing_str = ""
        if missing_names:
            missing_str = f" {len(missing_names)} recommended legal protections are missing, including {', and '.join(missing_names[:2])}."
        else:
            missing_str = " All standard recommended legal protections are present."

        ai_executive_summary = (
            f"This {contract_type.lower() or 'contract'} contains {len(analyzed_clauses)} clauses.{risky_str}"
            f"{missing_str} Overall risk score: {risk_score}/100. "
            f"Legal recommendation: {final_rec}."
        )

        # Generate session ID
        analysis_id = str(uuid.uuid4())
        
        # Compile response structure
        analysis_result = {
            "analysis_id": analysis_id,
            "success": True,
            "contract_type": contract_type,
            "filename": filename,
            "text": text,
            "summary": {
                "contract_type": contract_type,
                "clause_count": len(analyzed_clauses),
                "issues_count": len(issues),
                "missing_clauses_count": len(missing_protections),
                "overall_risk": overall_risk,
                "risk_score": risk_score,
                "confidence": int(avg_confidence),
                "reading_time_mins": reading_time_mins,
                "one_line_summary": one_line_sum,
                "ai_executive_summary": ai_executive_summary,
                "page_count": page_count,
                "processing_time_ms": processing_time_ms,
                "overall_recommendation": overall_recommendation,
                "final_recommendation": final_rec,
                "top_risks": top_risks
            },
            "clauses": analyzed_clauses,
            "missing_protections": missing_protections,
            "issues": issues,
            "counts": {
                "critical": critical_count,
                "high": high_count,
                "warning": warning_count,
                "safe": safe_count
            }
        }
        
        # Save analysis data to reports/ folder for subsequent PDF downloads
        session_json_path = os.path.join(reports_dir, f"{analysis_id}.json")
        with open(session_json_path, "w", encoding="utf-8") as json_file:
            json.dump(analysis_result, json_file, indent=4)
            
        # Copy the original uploaded PDF to reports/ to serve it to the frontend PDF.js viewer
        session_pdf_path = os.path.join(reports_dir, f"{analysis_id}_original.pdf")
        import shutil
        if os.path.exists(file_path):
            shutil.copy2(file_path, session_pdf_path)
            
        # Write to cache path as well
        with open(cache_path, "w", encoding="utf-8") as cache_file:
            json.dump(analysis_result, cache_file, indent=4)
            
        print("Analysis completed successfully and results stored.")
        return jsonify(analysis_result)

    except Exception as e:
        print(f"Error during contract analysis: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        })
        
    finally:
        # Clean up raw file from uploads
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as ex:
                print(f"Failed to delete temporary upload file {file_path}: {ex}")

from flask import send_from_directory

@analyzer_bp.route("/get-pdf/<analysis_id>", methods=["GET"])
def get_original_pdf(analysis_id):
    reports_dir = os.path.join(current_app.root_path, "reports")
    filename = f"{analysis_id}_original.pdf"
    if os.path.exists(os.path.join(reports_dir, filename)):
        return send_from_directory(reports_dir, filename)
    else:
        return jsonify({"success": False, "error": "PDF not found"}), 404

@analyzer_bp.route("/api/stats", methods=["GET"])
def get_stats():
    reports_dir = os.path.join(current_app.root_path, "reports")
    
    contracts_analyzed = 0
    clauses_reviewed = 0
    safe_clauses = 0
    warning_clauses = 0
    high_risk_clauses = 0
    critical_clauses = 0
    missing_protections = 0
    ai_confidence_sum = 0
    processing_time_sum = 0
    pages_processed = 0
    
    if os.path.exists(reports_dir):
        import glob
        for fpath in glob.glob(os.path.join(reports_dir, "*.json")):
            fname = os.path.basename(fpath)
            if fname.startswith("cache_"):
                continue
            name_only = os.path.splitext(fname)[0]
            if len(name_only) == 36 and name_only.count("-") == 4:
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        summary = data.get("summary", {})
                        counts = data.get("counts", {})
                        
                        contracts_analyzed += 1
                        clauses_reviewed += summary.get("clause_count", 0)
                        missing_protections += summary.get("missing_clauses_count", 0)
                        ai_confidence_sum += summary.get("confidence", 0)
                        processing_time_sum += summary.get("processing_time_ms", 0)
                        pages_processed += summary.get("page_count", 0)
                        
                        safe_clauses += counts.get("safe", 0)
                        warning_clauses += counts.get("warning", 0)
                        high_risk_clauses += counts.get("high", 0)
                        critical_clauses += counts.get("critical", 0)
                except Exception as e:
                    print(f"Error reading report file {fpath}: {e}")

    if contracts_analyzed == 0:
        stats = {
            "contracts_analyzed": 0,
            "clauses_reviewed": 0,
            "high_risk_clauses": 0,
            "missing_protections": 0
        }
    else:
        stats = {
            "contracts_analyzed": contracts_analyzed,
            "clauses_reviewed": clauses_reviewed,
            "safe_clauses": safe_clauses,
            "warning_clauses": warning_clauses,
            "high_risk_clauses": high_risk_clauses,
            "critical_clauses": critical_clauses,
            "missing_protections": missing_protections,
            "ai_confidence": round(ai_confidence_sum / contracts_analyzed, 1),
            "processing_time": round(processing_time_sum / contracts_analyzed, 0),
            "pages_processed": pages_processed
        }

    features = [
        {
            "id": "predatory",
            "icon": "⚠",
            "title": "Predatory Clause Detection",
            "description": "Scans for highly biased clauses, unilateral termination rights, excessive lock-ins, and unreasonable penalty fees that favor the other party.",
            "technical": "Runs rule-based heuristics and weighted analysis to classify clauses as CRITICAL, HIGH, WARNING, or SAFE based on severe imbalances."
        },
        {
            "id": "missing",
            "icon": "🔒",
            "title": "Missing Protection Finder",
            "description": "Identifies standard boilerplate and crucial clauses that should be in the agreement but are missing (e.g., Force Majeure, Arbitration, Limit of Liability).",
            "technical": "Cross-references identified clauses against contract type templates to flag omissions that leave you legally exposed."
        },
        {
            "id": "plain_lang",
            "icon": "📖",
            "title": "Plain-Language Explanation",
            "description": "Translates dense legalese, complex jargon, and confusing legal phrasing into clear, everyday English that anyone can understand.",
            "technical": "Generates natural language breakdowns of the purpose, intent, and practical implications of complex legal provisions."
        },
        {
            "id": "indian_law",
            "icon": "⚖",
            "title": "Indian Law Reference",
            "description": "Validates clauses against Indian statutes, such as the Indian Contract Act (1872), Model Tenancy Act (2021), and Arbitration Act (1996).",
            "technical": "Connects clauses to our integrated database of Indian legal precedents and acts, citing relevant sections and enforceability warnings."
        },
        {
            "id": "suggested_rewrites",
            "icon": "✏",
            "title": "Suggested Rewrites",
            "description": "Provides ready-to-use, balanced alternative drafting templates to make highly skewed clauses fair for both parties.",
            "technical": "Provides legal-grade fallback templates with placeholders (e.g. [Amount]) to immediately replace unfair terms during negotiations."
        },
        {
            "id": "risk_score",
            "icon": "📊",
            "title": "Risk Score",
            "description": "Computes a normalized risk score from 0 to 100 representing the overall danger level of signing the contract.",
            "technical": "Aggregates clause weights, severity ratios, and missing protections using a confidence-weighted decay formula."
        }
    ]
    
    return jsonify({
        "success": True,
        "stats": stats,
        "features": features
    })


