# Fix HTML structure of templates/clauseguard.html
import os

html_path = r"c:\Users\Vanshika\Desktop\Contract-Clause-Detector\templates\clauseguard.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

target_marker = """          <div class="rep-card-body" id="report-critical-clauses">
    <script>"""

restored_html = """          <div class="rep-card-body" id="report-critical-clauses">
             <!-- Critical issues list (populated dynamically) -->
          </div>
        </div>

        <div class="rep-card anim d2">
          <div class="rep-card-head">
            <div class="rep-card-title">📊 Risk Score Breakdown</div>
          </div>
          <div class="rep-card-body" id="report-score-breakdown">
             <!-- Score breakdown bars (populated dynamically) -->
          </div>
        </div>

      </div>

      <div class="rep-grid">

        <div class="rep-card anim d3">
          <div class="rep-card-head">
            <div class="rep-card-title">📋 Missing Protections</div>
            <span id="report-missing-count-badge" style="font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px;background:var(--amb-l);color:var(--amber)">0 Absent</span>
          </div>
          <div class="rep-card-body" id="report-missing-protections">
             <!-- Missing protections list (populated dynamically) -->
          </div>
        </div>

        <div class="rep-card anim d4">
          <div class="rep-card-head">
            <div class="rep-card-title">✏ AI Recommendations & Checklist</div>
          </div>
          <div class="rep-card-body" id="report-recommendations">
             <!-- AI recommendations checklist (populated dynamically) -->
          </div>
        </div>

      </div>

      <!-- Action Row -->
      <div class="rep-action-row anim d4" style="margin-top: 20px;">
        <button class="rep-btn" onclick="generateNegotiationLetter()">📝 &nbsp;AI Negotiation Letter</button>
        <button class="rep-btn" onclick="shareWithLawyer()">📤 &nbsp;Share Report</button>
        <button class="rep-btn vio" onclick="downloadReportPDF()">📥 &nbsp;Download PDF Report</button>
      </div>

    </div>
  </div>
</div>

</main>

<script>"""

if target_marker in content:
    content = content.replace(target_marker, restored_html)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("HTML structure successfully restored!")
else:
    print("Target marker not found! Check if already fixed or changed.")
