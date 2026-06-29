# ClauseGuard AI — PDF Report Routes
import os
import json
from flask import Blueprint, send_file, current_app, abort
from services.report_generator import ReportGenerator

reports_bp = Blueprint('reports', __name__)

@reports_bp.route("/download-report/<analysis_id>", methods=["GET"])
def download_pdf_report(analysis_id):
    reports_dir = os.path.join(current_app.root_path, "reports")
    json_path = os.path.join(reports_dir, f"{analysis_id}.json")
    pdf_path = os.path.join(reports_dir, f"{analysis_id}.pdf")
    
    if not os.path.exists(json_path):
        abort(404, description="Analysis session not found. Please re-upload and analyze the contract.")
        
    try:
        # Load analysis data
        with open(json_path, "r", encoding="utf-8") as json_file:
            analysis_data = json.load(json_file)
            
        # Generate the PDF if it hasn't been compiled yet
        if not os.path.exists(pdf_path):
            print(f"Generating PDF report for analysis session {analysis_id}...")
            ReportGenerator.generate_pdf(analysis_data, pdf_path)
            
        contract_name = os.path.splitext(analysis_data.get("filename", "contract.pdf"))[0]
        download_name = f"ClauseGuard_Report_{contract_name}.pdf"
        
        return send_file(
            pdf_path,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=download_name
        )
        
    except Exception as e:
        print(f"Error compiling PDF report: {e}")
        abort(500, description=f"Failed to generate PDF report: {str(e)}")
