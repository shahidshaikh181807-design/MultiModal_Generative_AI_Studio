"""
Generates a formal 2-page A4 PDF Procedure Report for Drive submission.
Course: Generative AI Mini Project
Problem Statement #49: Project Idea Generator
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748b"))
        # Header (on page 2)
        if self._pageNumber > 1:
            self.drawString(36, 810, "Generative AI Mini Project Procedure Report — PS #49: Project Idea Generator")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, 804, 559, 804)
        
        # Footer
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 38, 559, 38)
        self.drawString(36, 26, "Student: Shahid Shaikh | Roll No / PS: 49 | B.Tech CSE (Gen AI)")
        self.drawRightString(559, 26, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename: str):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#1e1b4b"),
        alignment=1
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#4338ca"),
        alignment=1
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=5,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=10.5,
        textColor=colors.HexColor("#334155")
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=3
    )

    story = []

    # Title & Subtitle Banner
    story.append(Paragraph("PROJECT PROCEDURE REPORT: PROJECT IDEA GENERATOR", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Final-Year Generative AI Mini Project (10-Mark Academic Evaluation)", subtitle_style))
    story.append(Spacer(1, 4))

    # Header Meta Table
    meta_data = [
        [
            Paragraph("<b>Student Name:</b> Shahid Shaikh", body_style),
            Paragraph("<b>Problem Statement No:</b> PS #49", body_style)
        ],
        [
            Paragraph("<b>Class / Branch:</b> LY B.Tech CSE (Gen AI)", body_style),
            Paragraph("<b>Roll Number:</b> Topic / Roll #49", body_style)
        ],
        [
            Paragraph("<b>Subject:</b> Generative AI (23 CSE4004)", body_style),
            Paragraph("<b>GitHub:</b> github.com/shahidshaikh181807-design/MultiModal_Generative_AI_Studio", body_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[260, 263])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 4))

    # 1. Problem Statement
    story.append(Paragraph("1. Problem Statement", section_heading))
    p1_text = (
        "Students struggle to pick project topics that strike the right balance between academic rigor and time feasibility. "
        "The <b>Project Idea Generator</b> automates this by taking a student's chosen <b>domain</b>, <b>skill level</b>, "
        "and <b>available timeframe</b>, and generating <b>5 distinct, well-scoped project proposals</b> with structured modules, "
        "recommended tools, difficulty ratings, and viva presentation tips displayed as responsive cards."
    )
    story.append(Paragraph(p1_text, body_style))
    story.append(Spacer(1, 4))

    # 2. Tools & Model
    story.append(Paragraph("2. Tools, Libraries & LLM Models Used", section_heading))
    tools_data = [
        [Paragraph("<b>Component</b>", body_bold), Paragraph("<b>Technology / Framework Used</b>", body_bold), Paragraph("<b>Role / Purpose</b>", body_bold)],
        [Paragraph("Programming Language", body_style), Paragraph("Python 3.13.2", body_style), Paragraph("Core backend logic, API integration, data parsing", body_style)],
        [Paragraph("UI Framework", body_style), Paragraph("Streamlit 1.57.0 with Custom CSS", body_style), Paragraph("Responsive 5-card layout, badges, expanders", body_style)],
        [Paragraph("Primary LLM Engine", body_style), Paragraph("Google Gemini 2.5 Flash (`google-genai` SDK)", body_style), Paragraph("High-speed structured JSON generation (temperature 0.7)", body_style)],
        [Paragraph("Alternative Models", body_style), Paragraph("Groq (LLaMA-3.3-70B) & OpenAI (GPT-4o mini)", body_style), Paragraph("Multi-provider flexibility with OpenAI-compatible API", body_style)],
        [Paragraph("Offline Fallback Engine", body_style), Paragraph("Built-in Deterministic Synthesizer", body_style), Paragraph("Guarantees 100% test reliability with zero API downtime", body_style)]
    ]
    t_tools = Table(tools_data, colWidths=[120, 180, 223])
    t_tools.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#ede9fe")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#c4b5fd")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_tools)
    story.append(Spacer(1, 4))

    # 3. Procedure
    story.append(Paragraph("3. Step-by-Step Implementation Procedure", section_heading))
    steps = [
        "<b>Step 1 — Environment Setup:</b> Initialized local environment with Python 3.13, configured Git repository, created `.gitignore` to protect API keys, and authored `requirements.txt`.",
        "<b>Step 2 — API Key & Multi-Provider Architecture:</b> Configured Google AI Studio API key (`GEMINI_API_KEY`) and designed an extensible client supporting Gemini, Groq, and an offline fallback engine.",
        "<b>Step 3 — Prompt Engineering & Schema Enforcement:</b> Formulated system instructions setting the persona of an Academic Advisor and enforced strict JSON output with schema validation (5 projects, modules, stack, difficulty).",
        "<b>Step 4 — Core Logic (`generator.py` & `prompts.py`):</b> Built dynamic prompt compilers, response sanitizers, regex JSON extractors, and automated schema parsers.",
        "<b>Step 5 — Streamlit Web UI (`app.py`):</b> Developed an interactive web interface with domain dropdowns, skill level sliders, timeframe selectors, glassmorphic card layouts, badges, and JSON export.",
        "<b>Step 6 — Automated Testing:</b> Authored `test_generator.py` and validated output conformity across 5 diverse domains (Healthcare, Cybersecurity, EdTech, FinTech, Sustainability).",
        "<b>Step 7 — GitHub Deployment:</b> Pushed version-controlled code to GitHub (`main` branch) and linked to Streamlit Community Cloud."
    ]
    for s in steps:
        story.append(Paragraph(f"• {s}", body_style))
        story.append(Spacer(1, 1.5))
    story.append(Spacer(1, 3))

    # 4. Prompt Used
    story.append(Paragraph("4. Prompt Design & Iterative Improvement", section_heading))
    prompt_snippet = (
        "<b>System Prompt:</b> <i>'You are an expert Academic Project Advisor. Generate exactly 5 innovative, practical, "
        "and highly scoring project ideas based on domain, skill level, and timeframe. Output strictly a valid JSON array "
        "with id, title, tagline, difficulty, problem_statement, key_modules (3+), tools_and_technologies, and evaluation_winning_tip.'</i><br/>"
        "<b>Prompt Improvement Made:</b> Initially, the LLM returned markdown conversational text and wrapped JSON in ```json code fences, "
        "causing parse errors. Improved it by adding explicit schema constraints (`response_mime_type='application/json'`), "
        "zero markdown preamble instructions, and an automated regex-based fallback extractor (`re.search(r'\\[\\s*\\{.*\\}\\s*\\]')`)."
    )
    story.append(Paragraph(prompt_snippet, body_style))

    # PAGE BREAK TO PAGE 2
    story.append(PageBreak())

    # --- PAGE 2 ---
    # 5. Results & Testing
    story.append(Paragraph("5. Experimental Results (Tested Across 5 Engineering Domains)", section_heading))
    story.append(Paragraph("The system was tested against 5 distinct test scenarios to verify scoping, modularity, and schema conformity:", body_style))
    story.append(Spacer(1, 3))

    results_data = [
        [Paragraph("<b>Test Case</b>", body_bold), Paragraph("<b>Inputs (Domain, Level, Time)</b>", body_bold), Paragraph("<b>Sample Generated Project & Modules</b>", body_bold), Paragraph("<b>Status</b>", body_bold)],
        [Paragraph("<b>TC 1</b>", body_style), Paragraph("Healthcare & Telemedicine<br/>Beginner | 1-2 Weeks", body_style), Paragraph("<b>Smart Healthcare Assistant & Predictive Dashboard</b><br/>• Data Ingestion &bull; LLM Analysis Engine &bull; Streamlit UI", body_style), Paragraph("<font color='#16a34a'><b>PASSED</b></font>", body_style)],
        [Paragraph("<b>TC 2</b>", body_style), Paragraph("Cybersecurity & Threat<br/>Intermediate | 1 Month", body_style), Paragraph("<b>Real-Time Cybersecurity Anomaly & Alert System</b><br/>• Packet Stream Simulator &bull; ML Anomaly Detector &bull; Alert Dispatcher", body_style), Paragraph("<font color='#16a34a'><b>PASSED</b></font>", body_style)],
        [Paragraph("<b>TC 3</b>", body_style), Paragraph("EdTech & Learning<br/>Advanced | 3 Months", body_style), Paragraph("<b>Interactive EdTech Knowledge Bot with Citations</b><br/>• Vector DB Indexer &bull; Hybrid Semantic RAG &bull; Quiz Generator", body_style), Paragraph("<font color='#16a34a'><b>PASSED</b></font>", body_style)],
        [Paragraph("<b>TC 4</b>", body_style), Paragraph("FinTech & Fraud<br/>Intermediate | 1-2 Weeks", body_style), Paragraph("<b>Financial Transaction Anomaly Detection & Scoring</b><br/>• CSV Stream Parser &bull; Isolation Forest Model &bull; Risk Cards", body_style), Paragraph("<font color='#16a34a'><b>PASSED</b></font>", body_style)],
        [Paragraph("<b>TC 5</b>", body_style), Paragraph("Sustainability & Energy<br/>Beginner | 2-3 Weeks", body_style), Paragraph("<b>Smart Solar & Weather Telemetry Visualizer</b><br/>• OpenWeather API Ingestion &bull; KPI Dash &bull; Anomaly Flags", body_style), Paragraph("<font color='#16a34a'><b>PASSED</b></font>", body_style)]
    ]
    t_results = Table(results_data, colWidths=[38, 145, 290, 50])
    t_results.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_results)
    story.append(Spacer(1, 4))

    # Embedded Screenshot of UI
    story.append(Paragraph("<b>Visual Deliverable: Generated Project Cards UI (Test Case 1):</b>", body_style))
    story.append(Spacer(1, 2))
    
    img_path = os.path.join(os.path.dirname(__file__), "screenshots", "test_case_1_healthcare.png")
    if os.path.exists(img_path):
        # Fit inside A4 width (~520pt) with nice height
        story.append(Image(img_path, width=520, height=195))
        story.append(Spacer(1, 4))

    # 6. Challenges Faced & Solutions
    story.append(Paragraph("6. Challenges Faced and Technical Solutions", section_heading))
    challenges = [
        ("LLM Output Inconsistency", "LLMs occasionally returned markdown code fences (```json) or conversational preamble. Fixed by combining JSON schema constraints in API calls with a regex pattern extractor that isolates outermost JSON arrays (`[...]`)."),
        ("Overly Ambitious Scope for Beginners", "Initial prompts generated multi-tenant enterprise architectures for 1-week beginner projects. Fixed by parameterizing prompt constraints to strictly bound in-scope deliverables vs. out-of-scope backlog items."),
        ("UI Card Rendering in Dark Mode", "Streamlit dark mode caused unreadable text contrast on static white cards. Fixed by writing adaptive CSS with glassmorphic semi-transparent backgrounds (`rgba(30, 41, 59, 0.82)`), blur filters, and high-contrast typography.")
    ]
    for c_title, c_sol in challenges:
        story.append(Paragraph(f"• <b>{c_title}:</b> {c_sol}", body_style))
        story.append(Spacer(1, 1.5))
    story.append(Spacer(1, 3))

    # 7. Conclusion & Future Scope
    story.append(Paragraph("7. Conclusion & Future Enhancements", section_heading))
    conc_text = (
        "<b>What Works:</b> The system successfully synthesizes 5 complete, feasible, and modular project ideas tailored to domain, "
        "skill level, and duration. All features (card UI, tech stack chips, expandable modules, presentation tips, JSON download) function seamlessly.<br/>"
        "<b>What Doesn't / Current Limitations:</b> Requires internet/API access for live LLM inference (mitigated by our smart offline fallback engine).<br/>"
        "<b>Future Improvement:</b> Add an automated GitHub Starter Repo Generator that scaffolds the selected project card's complete directory structure, README, and starter boilerplate code with one click."
    )
    story.append(Paragraph(conc_text, body_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report.pdf successfully created at: {filename}")

if __name__ == "__main__":
    out_pdf = os.path.join(os.path.dirname(__file__), "Report.pdf")
    build_pdf(out_pdf)
