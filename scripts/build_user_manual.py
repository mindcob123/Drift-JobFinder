"""Builds the comprehensive User_Manual.docx document for Drift."""
from __future__ import annotations

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import doc_builder as db


def build_user_manual() -> None:
    doc = db.create_document()

    # Cover Page
    db.add_cover_page(
        doc,
        title="Drift JobFinder — End-User Operational Manual",
        subtitle="Complete Step-by-Step Guide to Installation, Search Automation, AI Matching, and Application Tracking",
        doc_type="User Operational Manual",
        metadata=[
            ("Application Name", "Drift JobFinder"),
            ("Application Version", "1.0.0 Production Release"),
            ("Target Audience", "Job Seekers, Software Professionals, Engineering Leaders, General Users"),
            ("Supported Operating Systems", "Microsoft Windows 10 & Windows 11 (64-bit)"),
            ("Document Release Date", "October 2026"),
            ("Document Classification", "Official End-User Manual"),
        ],
    )

    # 1. Welcome & Overview
    db.add_heading_1(doc, "1. Welcome & Introduction to Drift")
    db.add_paragraph(
        doc,
        "Welcome to Drift JobFinder! Drift is an intelligent desktop career assistant created to transform how software engineers, designers, product managers, and knowledge workers discover, evaluate, and track employment opportunities.",
    )
    db.add_paragraph(
        doc,
        "Most job search tools today are commercial web aggregators designed to optimize recruiter clicks, promote sponsored ads, and track user behavioral profiles. Drift takes the opposite approach:",
    )
    db.add_bullet(
        doc,
        "Drift runs 100% on your local PC. Your resume, job applications, interview notes, and search queries are stored strictly in an encrypted local database on your hard drive. No remote server tracks your job hunting.",
        bold_prefix="Complete Privacy: ",
    )
    db.add_bullet(
        doc,
        "Rather than scraping stale aggregator listings, Drift queries employer-canonical Applicant Tracking Systems (such as Greenhouse, Lever, Ashby, and Workable) directly to retrieve genuine, open roles before they are flooded with applicants.",
        bold_prefix="Direct ATS Feeds: ",
    )
    db.add_bullet(
        doc,
        "Drift scores every job listing against your specific career history across 8 transparent dimensions, explaining exactly why a job fits or what skills are missing.",
        bold_prefix="Explainable Match Scoring: ",
    )
    db.add_bullet(
        doc,
        "Drift helps tailor resume bullet points to match job descriptions, but enforces a strict safety net: it will never invent fake skills, false qualifications, or exaggerated metrics.",
        bold_prefix="Honest AI Assistance: ",
    )
    db.add_bullet(
        doc,
        "Includes a full Kanban board to track your application lifecycle from 'Saved' to 'Interview' to 'Offer'.",
        bold_prefix="Integrated Application Tracker: ",
    )

    # 2. Installation & Getting Started
    db.add_heading_1(doc, "2. System Requirements & Installation")
    db.add_paragraph(
        doc,
        "Drift is designed as a lightweight, high-performance Windows desktop application.",
    )

    db.add_heading_2(doc, "2.1 System Requirements")
    db.add_table(
        doc,
        headers=["Component", "Minimum Requirement", "Recommended Specification"],
        data=[
            ["Operating System", "Microsoft Windows 10 (64-bit)", "Microsoft Windows 11 (64-bit)"],
            ["Processor", "Dual-Core 1.8 GHz 64-bit CPU", "Quad-Core Intel i5/i7/i9 or AMD Ryzen"],
            ["Memory (RAM)", "4 GB RAM", "8 GB RAM or higher"],
            ["Disk Space", "300 MB free space", "1 GB free space (for caching & local database)"],
            ["Display Resolution", "1280 x 720 pixels", "1920 x 1080 (Full HD) or higher"],
            ["Internet Connection", "Broadband connection", "Stable broadband (for crawling job boards)"],
        ],
        col_widths=[1.5, 2.5, 2.5],
    )

    db.add_heading_2(doc, "2.2 Launching Drift")
    db.add_paragraph(
        doc,
        "You can launch Drift in one of two ways depending on how you received the software:",
    )
    db.add_bullet(
        doc,
        "Double-click `Drift.exe` located in your installation directory or Desktop shortcut. The application initializes immediately without requiring any third-party runtime or installer.",
        bold_prefix="Method A — Standalone Executable (Recommended): ",
    )
    db.add_bullet(
        doc,
        "If running from the source checkout, double-click `run.bat` or run `python main.py` in your terminal. The batch script automatically verifies your virtual environment, loads configuration files, and launches the application shell.",
        bold_prefix="Method B — Developer Batch Script: ",
    )

    db.add_heading_2(doc, "2.3 Where Your Data Lives")
    db.add_paragraph(
        doc,
        "All user data is stored safely in a dedicated folder in your Windows user profile:",
    )
    db.add_code_block(
        doc,
        r"C:\Users\<YourUsername>\AppData\Local\Drift\jobs.db",
    )
    db.add_paragraph(
        doc,
        "This file contains your entire application history, saved searches, custom resume versions, and application notes. Backing up this single `jobs.db` file guarantees that your entire job search history is safely preserved.",
    )

    # 3. Initial Configuration & AI Setup
    db.add_heading_1(doc, "3. Initial Configuration & AI Setup")
    db.add_paragraph(
        doc,
        "When you first open Drift, navigating to the **Settings** tab allows you to configure your preferred AI provider, visual theme, and scan parameters.",
    )

    db.add_heading_2(doc, "3.1 Connecting an AI Provider (Bring-Your-Own-Key)")
    db.add_paragraph(
        doc,
        "Drift ships without hardcoded API keys to protect your privacy and ensure you maintain full control over usage costs. You can connect any of the following providers:",
    )
    db.add_table(
        doc,
        headers=["Provider", "Pricing / Free Tier", "Setup Instructions"],
        data=[
            ["Groq (Recommended)", "Free tier available with high rate limits", "Visit console.groq.com, generate a free API key (starts with 'gsk_'), and paste it into Drift."],
            ["Google Gemini", "Generous free tier", "Visit aistudio.google.com, create a free Gemini API key, and enter it into Drift."],
            ["OpenAI", "Pay-as-you-go credit", "Visit platform.openai.com, generate an API key (starts with 'sk-'), and paste it into Drift."],
            ["Anthropic Claude", "Pay-as-you-go credit", "Visit console.anthropic.com, generate an API key (starts with 'sk-ant-'), and enter it into Drift."],
            ["Ollama (100% Offline)", "Completely Free & Local", "Install Ollama locally (ollama.ai), run 'ollama run llama3', and select Ollama in Drift. Requires no internet or keys."],
        ],
        col_widths=[1.5, 1.8, 3.2],
    )

    db.add_callout(
        doc,
        "SECURITY NOTICE: Your API keys are stored securely in the Windows Credential Manager (DPAPI) under your Windows account. They are never written in plaintext to disk, never logged, and never transmitted anywhere except directly to the provider's official API.",
        title="SECURITY",
        level="success",
    )

    db.add_heading_2(doc, "3.2 Theme & Accent Customization")
    db.add_paragraph(
        doc,
        "Drift supports modern high-contrast aesthetics designed for long work sessions. In **Settings -> Appearance**, you can toggle between **Dark Mode** (slate charcoal background) and **Light Mode** (clean white background), and choose from 8 accent colors: Teal, Blue, Indigo, Purple, Rose, Orange, Amber, or Emerald.",
    )

    # 4. Resume Studio & Career Profile
    db.add_heading_1(doc, "4. Resume Studio & Career Profile")
    db.add_paragraph(
        doc,
        "The **Resume Studio** is the intelligence core of Drift. By uploading your resume, Drift builds a comprehensive understanding of your technical skills, experience depth, and career preferences.",
    )

    db.add_heading_2(doc, "4.1 Uploading Your Master Resume")
    db.add_bullet(doc, "Click on the **Résumés** tab in the left navigation sidebar.", bold_prefix="Step 1: ")
    db.add_bullet(doc, "Click **Upload Résumé** and select your resume file (.PDF, .DOCX, or .DOC).", bold_prefix="Step 2: ")
    db.add_bullet(doc, "Drift's layout-aware parser extracts your contact info, career timeline, education, and technical skills in seconds.", bold_prefix="Step 3: ")
    db.add_bullet(doc, "Review the extracted information in the visual editor. You can edit any field, add missing skills, or assign importance weights (1x to 3x) to specific technologies you want to prioritize.", bold_prefix="Step 4: ")

    db.add_heading_2(doc, "4.2 Honest Resume Tailoring")
    db.add_paragraph(
        doc,
        "When you discover a high-priority job listing, you can generate a tailored version of your resume aligned with that specific posting:",
    )
    db.add_bullet(doc, "Click **Tailor Résumé** from any job card or in the Resume Studio.", bold_prefix="1. Select Job: ")
    db.add_bullet(doc, "Drift analyzes the employer's required keywords and suggests subtle rephrasings of your existing bullet points to highlight matching experience.", bold_prefix="2. Review Diff: ")
    db.add_bullet(doc, "The side-by-side diff viewer shows exact revisions. You can approve or reject each bullet individually.", bold_prefix="3. Approve Changes: ")
    db.add_bullet(doc, "Click **Export** to generate a clean, ATS-compliant `.docx`, `.pdf`, or `.txt` document ready to submit.", bold_prefix="4. Export: ")

    db.add_callout(
        doc,
        "ANTI-HALLUCINATION PROMISE: Drift will never invent skills, experience, or metrics you do not possess. If a suggestion introduces a number or skill not present in your original resume, the system automatically rejects it.",
        title="HONESTY GUARANTEE",
        level="warning",
    )

    # 5. Building & Running Job Searches
    db.add_heading_1(doc, "5. Building & Running Job Searches")
    db.add_paragraph(
        doc,
        "Drift offers both a fast Quick Search and an Advanced Search Builder to discover roles matching your exact requirements.",
    )

    db.add_heading_2(doc, "5.1 Advanced Search Builder")
    db.add_paragraph(
        doc,
        "Access the Search Builder by clicking **Search** in the sidebar. You can configure:",
    )
    db.add_bullet(doc, "Enter primary titles (e.g. 'Senior Python Engineer', 'Full Stack Tech Lead').", bold_prefix="Role Titles: ")
    db.add_bullet(doc, "Keywords that MUST appear in the description (e.g. 'PostgreSQL', 'Docker').", bold_prefix="Required Keywords: ")
    db.add_bullet(doc, "Keywords that boost a job's score but aren't strictly required (e.g. 'FastAPI', 'PyQt').", bold_prefix="Nice-to-Have Keywords: ")
    db.add_bullet(doc, "Terms to reject automatically (e.g. 'Java', 'Clearance Required', 'Staffing Agency').", bold_prefix="Excluded Keywords: ")
    db.add_bullet(doc, "Select Remote Only, Hybrid, or On-site with specific city/country filters.", bold_prefix="Location Mode: ")
    db.add_bullet(doc, "Specify your minimum desired salary (e.g. '$140,000 USD/year'). Listings below this threshold will be filtered out unless 'Include unstated salary' is checked.", bold_prefix="Compensation Floor: ")
    db.add_bullet(doc, "Choose which job boards to search (Greenhouse, Lever, Ashby, Workable, Himalayas, etc.).", bold_prefix="Source Selection: ")

    db.add_heading_2(doc, "5.2 Executing a Live Scan & The Run Monitor")
    db.add_paragraph(
        doc,
        "Once you click **Start Search**, Drift transitions to the **Live Run Monitor** screen:",
    )
    db.add_bullet(doc, "The progress bar shows overall scan completion and total unique jobs discovered.", bold_prefix="Live Progress: ")
    db.add_bullet(doc, "Each job board shows its real-time state: Queued -> In Progress -> Completed with item counts.", bold_prefix="Per-Source Status: ")
    db.add_bullet(doc, "You can click **Cancel** at any time. The scan stops safely without losing any discovered jobs.", bold_prefix="Safe Cancellation: ")
    db.add_bullet(doc, "Discovered jobs appear immediately as sources finish; you do not have to wait for the entire scan to complete.", bold_prefix="Live Streaming: ")

    # 6. Evaluating Results & Match Scoring
    db.add_heading_1(doc, "6. Evaluating Results & Match Scoring")
    db.add_paragraph(
        doc,
        "After a scan completes, Drift presents discovered roles on the **Jobs** screen, ranked from highest match to lowest match.",
    )

    db.add_heading_2(doc, "6.1 Understanding Match Scores & Badges")
    db.add_paragraph(
        doc,
        "Each job card features a prominent color-coded match badge:",
    )
    db.add_bullet(doc, "Outstanding alignment across technical skills, seniority, and domain experience.", bold_prefix="90% – 100% (Green / Top Match): ")
    db.add_bullet(doc, "Solid fit with most core skills present; minor skill gaps or seniority variance.", bold_prefix="75% – 89% (Blue / Strong Match): ")
    db.add_bullet(doc, "Moderate match; candidate meets base qualifications but lacks some preferred tools.", bold_prefix="60% – 74% (Amber / Potential Fit): ")
    db.add_bullet(doc, "Weak match or significant mismatch in required qualifications.", bold_prefix="Below 60% (Gray / Low Fit): ")

    db.add_heading_2(doc, "6.2 The 8-Dimension Rubric Breakdown")
    db.add_paragraph(
        doc,
        "Clicking on the score badge opens the **Rubric Breakdown Dialog**. This reveals exact sub-scores across Hard Skills, Experience Years, Seniority, Domain Knowledge, Education, Work Mode, Salary, and ATS Formatting, accompanied by a one-sentence AI rationale explaining the evaluation.",
    )

    db.add_heading_2(doc, "6.3 Essential Job Actions")
    db.add_bullet(doc, "Opens the employer's official job application page in your default web browser.", bold_prefix="Apply Now: ")
    db.add_bullet(doc, "Saves the job directly into your Kanban Application Tracker under 'Saved'.", bold_prefix="Save Job: ")
    db.add_bullet(doc, "Hides this posting and prevents it from appearing in any future searches.", bold_prefix="Dismiss: ")
    db.add_bullet(doc, "Uses AI to generate a personalized, tailored cover letter highlighting your relevant achievements.", bold_prefix="Cover Letter: ")

    # 7. Application Tracker (Kanban Pipeline)
    db.add_heading_1(doc, "7. The Application Tracker (Kanban Pipeline)")
    db.add_paragraph(
        doc,
        "The **Applications** screen provides an interactive Kanban board to organize your active job applications.",
    )

    db.add_heading_2(doc, "7.1 Pipeline Stages")
    db.add_bullet(doc, "Interesting roles you have bookmarked for review.", bold_prefix="Saved: ")
    db.add_bullet(doc, "Applications you have formally submitted to the employer.", bold_prefix="Applied: ")
    db.add_bullet(doc, "Initial recruiter screenings or phone calls scheduled.", bold_prefix="Screening: ")
    db.add_bullet(doc, "Active technical interviews, hiring manager rounds, or onsite presentations.", bold_prefix="Interview: ")
    db.add_bullet(doc, "Formal written offers received awaiting negotiation.", bold_prefix="Offer: ")
    db.add_bullet(doc, "Closed applications (archived with full notes).", bold_prefix="Rejected / Withdrawn: ")

    db.add_heading_2(doc, "7.2 Managing Application Cards")
    db.add_paragraph(
        doc,
        "You can drag and drop cards between columns as your status progresses. Clicking any card opens the details drawer where you can:",
    )
    db.add_bullet(doc, "Log recruiter names, email addresses, and interview dates.", bold_prefix="Add Notes: ")
    db.add_bullet(doc, "Schedule upcoming follow-up tasks (e.g. 'Send thank-you email on Thursday').", bold_prefix="Set Deadlines: ")
    db.add_bullet(doc, "Record stated compensation brackets and equity grant details.", bold_prefix="Salary Tracking: ")
    db.add_bullet(doc, "Click **Export Applications** to download your complete tracker as a spreadsheet-ready CSV or JSON file.", bold_prefix="Spreadsheet Export: ")

    # 8. Dashboard, Analytics & Health
    db.add_heading_1(doc, "8. Dashboard, Analytics & Source Health")
    db.add_heading_2(doc, "8.1 Dashboard Metrics")
    db.add_paragraph(
        doc,
        "The **Dashboard** home screen aggregates key analytics regarding your job search velocity:",
    )
    db.add_bullet(doc, "Total unique job listings discovered across all runs.", bold_prefix="Total Jobs Scanned: ")
    db.add_bullet(doc, "Number of applications currently in progress.", bold_prefix="Active Pipeline: ")
    db.add_bullet(doc, "Percentage of applications advancing to screening and interview stages.", bold_prefix="Conversion Rate: ")
    db.add_bullet(doc, "Real-time ledger of AI tokens consumed and estimated API expenditure.", bold_prefix="Token Spend: ")

    db.add_heading_2(doc, "8.2 Source Health Manager")
    db.add_paragraph(
        doc,
        "The **Sources** screen monitors the real-time operational health of all job adapters. You can view response latency, success rates, and last verified scan dates. If an external service experiences network downtime, Drift marks it as 'Degraded' and cools off automatically without slowing down your other searches. You can click **Test** on any source to run an immediate diagnostic probe.",
    )

    # 9. Troubleshooting & FAQ
    db.add_heading_1(doc, "9. Troubleshooting & Frequently Asked Questions (FAQ)")

    db.add_heading_2(doc, "9.1 Frequently Asked Questions")
    db.add_paragraph(
        doc,
        "Q: Why did a scan return zero results?\n"
        "A: Overly restrictive filters are the most common cause. Try relaxing salary minimums, broadening required keywords, or selecting 'Include unstated salary'. Drift's automated widening will also suggest relaxed criteria if results fall below your minimum threshold.",
    )
    db.add_paragraph(
        doc,
        "Q: Can I use Drift completely offline without any internet connection?\n"
        "A: Yes! You can browse previously scanned jobs, edit your resume, organize your Kanban tracker, export documents, and run local keyword matching without an internet connection. To run offline semantic AI ranking, connect local Ollama.",
    )
    db.add_paragraph(
        doc,
        "Q: How do I back up my data?\n"
        r"A: Simply copy the file `jobs.db` from `%LOCALAPPDATA%\Drift\` (or `db/jobs.db` in your installation folder) to an external drive or cloud backup. To restore, place the file back into the same directory.",
    )

    db.add_heading_2(doc, "9.2 Common Error Resolutions")
    db.add_table(
        doc,
        headers=["Symptom / Error", "Root Cause", "Recommended Resolution"],
        data=[
            ["'Invalid API Key' Notification", "Key was mistyped, revoked, or expired on the provider console.", "Navigate to Settings -> AI Providers, re-enter your key, and click 'Test Connection'."],
            ["'Database Locked' Warning", "Another instance of Drift or an external SQLite browser is holding a lock.", "Close any secondary Drift windows or SQLite management tools. The database will auto-unlock in 5 seconds."],
            ["Source shows 'Cooling Off'", "Target job board returned multiple 429 rate limit or 5xx server errors.", "Drift's circuit breaker paused the source for 1 hour to prevent IP bans. It will automatically re-enable."],
            ["Resume upload shows 'Low Text Quality'", "Resume is a scanned image or flattened graphic without selectable text.", "Save your resume directly as a PDF from Microsoft Word or Google Docs so text is machine-readable."],
        ],
        col_widths=[1.8, 2.0, 2.7],
    )

    output_path = Path("d:/Projects/Drift - Mindcob/User_Manual.docx")
    doc.save(str(output_path))
    print(f"User_Manual.docx saved to {output_path}")


if __name__ == "__main__":
    build_user_manual()
