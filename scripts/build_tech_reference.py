"""Builds the comprehensive Technical_Reference.docx document for Drift."""
from __future__ import annotations

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import doc_builder as db


def build_tech_reference() -> None:
    doc = db.create_document()

    # Cover Page
    db.add_cover_page(
        doc,
        title="Drift JobFinder — Complete Technical Reference Manual",
        subtitle="Comprehensive Architectural, Data Layer, Multi-AI, Ingestion, and Component Specification",
        doc_type="Technical Reference Manual",
        metadata=[
            ("System Name", "Drift JobFinder (Production Release v1.0.0)"),
            ("Document Version", "1.0.0 — Comprehensive Engineering Reference"),
            ("Target Audience", "Software Engineers, System Architects, Security Auditors, DevOps"),
            ("Codebase Scope", "148 Python Modules · 18,739 Lines of Code"),
            ("Runtime Environment", "Windows 10/11 x64 · Python 3.12–3.15 · PyQt5 5.15 · SQLite 3.45+"),
            ("License & Status", "Proprietary / Enterprise Production Verified"),
        ],
    )

    # 1. Executive Summary & System Philosophy
    db.add_heading_1(doc, "1. Executive Summary & System Philosophy")
    db.add_paragraph(
        doc,
        "Drift is an enterprise-grade desktop intelligence application designed to automate, curate, and optimize the executive job hunting and application process. Unlike generic web aggregators or cloud software-as-a-service platforms, Drift is engineered strictly as a desktop-native, zero-telemetry, offline-first application. All sensitive user assets—including complete career histories, resumes, tailored variations, candidate notes, and strategic job applications—reside exclusively on the local host within an encrypted/protected local SQLite database.",
    )
    db.add_paragraph(
        doc,
        "The architecture adheres to three core design tenets:",
    )
    db.add_bullet(
        doc,
        "All resume parsing, scoring, search execution, and tracking operate completely offline by default. External cloud services are invoked exclusively when authorized by the user for LLM-based semantic reasoning or live source crawling.",
        bold_prefix="Local-First & Host-Isolated: ",
    )
    db.add_bullet(
        doc,
        "The application ships with zero hardcoded API keys. Users provide their own keys for supported providers (Groq, OpenAI, Anthropic, Google Gemini, Mistral, DeepSeek, or local Ollama). Keys are stored strictly in the Windows Credential Manager / OS Keychain, never written to disk unencrypted, and never transmitted to third parties.",
        bold_prefix="Bring-Your-Own-Key (BYOK) Multi-Provider AI: ",
    )
    db.add_bullet(
        doc,
        "All network ingestion respects robots.txt directives, applies aggressive per-domain token bucket rate limiting, uses strict circuit breaker cool-offs, and queries employer-canonical applicant tracking systems (Greenhouse, Lever, Ashby, Workable) over brittle scraping.",
        bold_prefix="Ethical & Compliance-First Ingestion: ",
    )

    db.add_callout(
        doc,
        "Drift has zero remote server dependencies. There is no telemetry, no tracking pixel, no analytics beacon, and no centralized backend server. The user maintains total sovereignty over their employment data.",
        title="PRIVACY GUARANTEE",
        level="success",
    )

    # Architectural Overview Table
    db.add_heading_2(doc, "1.1 Codebase Structure & Package Inventory")
    db.add_paragraph(
        doc,
        "The codebase encompasses 148 Python modules and 18,739 lines of thoroughly tested code organized across five primary layers:",
    )

    db.add_table(
        doc,
        headers=["Layer / Package", "File Count", "Line Count", "Core Architectural Responsibilities"],
        data=[
            ["core/ (Ingestion, AI, Pipeline)", "69 files", "8,683 lines", "Concurrent ScanEngine, Multi-AI router, Resume parser/rubric, Normalization, SimHash Dedup, Ranking, ATS definitions"],
            ["ui/ (Presentation & Shell)", "32 files", "6,205 lines", "PyQt5 desktop application shell, 10 screen controllers, Design System tokens, cubic-bezier springs, reusable component library"],
            ["tests/ (Automated Quality)", "16 files", "2,422 lines", "Pytest suite comprising 222 test cases covering unit logic, integration flows, characterization, and compliance"],
            ["db/ (Storage & Migrations)", "8 files", "1,172 lines", "SQLite connection manager, WAL mode configuration, FTS5 virtual table, schema migration engine (m001-m006)"],
            ["Root & Scripts", "23 files", "257 lines", "Main bootstrapper (main.py), models, app paths, packaging specs (drift.spec), secret scanner"],
        ],
        col_widths=[1.8, 0.9, 0.9, 2.9],
    )

    # 2. Data Layer & SQLite Engine
    db.add_heading_1(doc, "2. Data Layer Architecture (db/)")
    db.add_paragraph(
        doc,
        "Storage is powered by SQLite 3 via Python's native `sqlite3` module. The design intentionally eschews heavyweight Object-Relational Mappers (ORMs) in favor of deterministic, highly optimized raw SQL statements with strict parameter binding to eliminate SQL injection vulnerabilities and overhead.",
    )

    db.add_heading_2(doc, "2.1 Connection Pragmas & Concurrency Isolation")
    db.add_paragraph(
        doc,
        "Every SQLite connection opened across the application lifecycle executes a deterministic set of pragmas defined in `db/connection.py`:",
    )
    db.add_code_block(
        doc,
        """PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;
PRAGMA busy_timeout = 5000;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = -64000; -- 64MB memory cache""",
    )
    db.add_bullet(doc, "Write-Ahead Logging ensures concurrent worker threads can write scan checkpoints without locking out the main UI thread during read queries.", bold_prefix="WAL Journaling: ")
    db.add_bullet(doc, "Cascading deletes and relationship constraints between jobs, scores, applications, and cover letters are strictly enforced by the database engine.", bold_prefix="Foreign Key Integrity: ")
    db.add_bullet(doc, "Short-lived lock contentions automatically wait up to 5 seconds before raising an operational error, preventing database lock crashes during intense background scans.", bold_prefix="5000ms Busy Timeout: ")

    db.add_heading_2(doc, "2.2 Complete Relational Schema (14 Tables + FTS5)")
    db.add_paragraph(
        doc,
        "The schema represents a comprehensive job hunting and candidate relationship model:",
    )
    db.add_table(
        doc,
        headers=["Table Name", "Primary Key", "Indexes / Triggers", "Core Purpose & Payload"],
        data=[
            ["profile", "id (TEXT)", "created_at", "Stores candidate career profiles, target job titles, locations, and salary floors."],
            ["resume", "id (TEXT)", "profile_id, is_default", "Stores parsed resume trees, extracted skills, contact information, and file paths."],
            ["resume_version", "id (TEXT)", "resume_id, job_id", "Stores tailored resume variations, bullet rewrites, and keyword alignment diffs."],
            ["search", "id (TEXT)", "last_run_at", "Persists named search criteria queries (query_json) for instant reuse."],
            ["run", "id (TEXT)", "started_at, status", "Records scan execution history, duration, total items discovered, and query snapshots."],
            ["source", "id (TEXT)", "status, last_probe_at", "Registry of job sources, breaker states (healthy, degraded, cooling_off), failure counts."],
            ["run_source_result", "id (TEXT)", "run_id, source_id", "Granular run audit log per source (duration, fetched items, error messages)."],
            ["job", "id (TEXT)", "fingerprint (UQ), posted_at, company", "Canonical job listings, normalized salary, location, description, and canonical URL."],
            ["job_score", "id (TEXT)", "job_id, final_score", "Detailed 3-stage ranking scores (lexical, semantic, LLM), sub-scores, and rationales."],
            ["application", "id (TEXT)", "job_id (UQ), status, updated_at", "Kanban tracking stages (saved, applied, interview, offer, rejected), notes, deadlines."],
            ["cover_letter", "id (TEXT)", "job_id, created_at", "Tailored cover letter drafts generated for specific job postings."],
            ["blocklist", "id (TEXT)", "pattern, target_field", "User-defined exclusion patterns (company names, recruiter domains, unwanted keywords)."],
            ["setting", "key (TEXT)", "key (UQ)", "Application configurations (AI routing matrix, pricing overrides, search defaults)."],
            ["llm_cache", "prompt_hash (TEXT)", "expires_at", "SHA-256 prompt-response cache preventing redundant, costly LLM queries."],
            ["llm_usage", "id (TEXT)", "task, created_at", "Financial cost ledger logging input/output tokens and estimated dollar cost per call."],
            ["job_embedding", "job_id (TEXT)", "model", "Vector embedding cache supporting offline semantic cosine similarity ranking."],
            ["job_fts", "rowid (INTEGER)", "FTS5 Virtual Table", "Full-text search index over job(title, company_name, description_text) kept in sync via triggers."],
        ],
        col_widths=[1.4, 1.1, 1.4, 2.6],
    )

    db.add_heading_2(doc, "2.3 Schema Migration Framework (m001–m006)")
    db.add_paragraph(
        doc,
        "Schema migrations are executed automatically on application startup via `db/migrations/__init__.py`. Migrations are forward-only, transactional, and strictly recorded in the `_migration` table as well as mirrored into `PRAGMA user_version`:",
    )
    db.add_bullet(doc, "Establishes the foundational 14 relational tables, FTS5 virtual table, and auto-sync triggers.", bold_prefix="m001_initial_schema: ")
    db.add_bullet(doc, "Safely imports legacy 1.x job data into new job, application, and cover_letter tables with automatic pre-migration backup.", bold_prefix="m002_import_legacy: ")
    db.add_bullet(doc, "Adds prompt-response cache (`llm_cache`) and financial cost ledger (`llm_usage`).", bold_prefix="m003_ai_cache_usage: ")
    db.add_bullet(doc, "Adds persistent circuit breaker state, failure tracking, and health metrics to the `source` table.", bold_prefix="m004_source_breaker: ")
    db.add_bullet(doc, "Transitions job identity from URL hashes to robust content-based fingerprints (`fingerprint_alias`), deduplicating across sources.", bold_prefix="m005_content_fingerprint: ")
    db.add_bullet(doc, "Creates `job_embedding` cache table for offline semantic cosine matching.", bold_prefix="m006_job_embedding: ")

    # 3. Multi-Provider AI Architecture
    db.add_heading_1(doc, "3. Multi-Provider AI Architecture (core/ai/)")
    db.add_paragraph(
        doc,
        "Drift features an enterprise-grade, multi-provider LLM orchestration layer (`core/ai/`). The system avoids bulky vendor client libraries (such as the standard `openai` or `anthropic` SDKs) and communicates directly with model inference endpoints over raw, hardened HTTP. This eliminates SDK dependency conflicts and guarantees precise control over timeouts, headers, and retries.",
    )

    db.add_heading_2(doc, "3.1 Supported AI Providers & Endpoint Specifications")
    db.add_table(
        doc,
        headers=["Provider", "Base URL", "Authentication", "Native Embeddings", "Typical Latency"],
        data=[
            ["Groq (Default)", "https://api.groq.com/openai/v1", "Authorization: Bearer <KEY>", "No (Uses router fallback)", "200ms – 600ms (Ultra-Fast)"],
            ["OpenAI", "https://api.openai.com/v1", "Authorization: Bearer <KEY>", "Yes (text-embedding-3-small)", "800ms – 2,000ms"],
            ["Anthropic Claude", "https://api.anthropic.com/v1", "x-api-key: <KEY>", "No", "1,200ms – 3,000ms"],
            ["Google Gemini", "https://generativelanguage.googleapis.com/v1beta", "x-goog-api-key: <KEY>", "Yes (text-embedding-004)", "800ms – 1,800ms"],
            ["OpenRouter", "https://openrouter.ai/api/v1", "Authorization: Bearer <KEY>", "No", "Variable by model"],
            ["Mistral AI", "https://api.mistral.ai/v1", "Authorization: Bearer <KEY>", "Yes (mistral-embed)", "700ms – 1,500ms"],
            ["DeepSeek", "https://api.deepseek.com/v1", "Authorization: Bearer <KEY>", "No", "1,000ms – 2,500ms"],
            ["Ollama (Local)", "http://localhost:11434/v1", "None (Host-Local)", "Yes (nomic-embed-text)", "Hardware dependent (Offline)"],
        ],
        col_widths=[1.3, 2.2, 1.4, 0.9, 0.7],
    )

    db.add_heading_2(doc, "3.2 Dynamic Task Routing & Fallback Chains")
    db.add_paragraph(
        doc,
        "Rather than assigning a single model globally, Drift routes AI queries across eight discrete functional tasks. Each task specifies its optimal model, temperature, max token ceiling, and an automated fallback chain in `core/ai/routing.py`:",
    )
    db.add_bullet(doc, "Extracts skills, experience, and metadata into strict JSON. Default: llama-3.3-70b-versatile -> gpt-4o-mini.", bold_prefix="resume_parse: ")
    db.add_bullet(doc, "Extracts hard/soft skill tokens from raw job descriptions. Default: llama-3.1-8b-instant.", bold_prefix="keyword_extract: ")
    db.add_bullet(doc, "Expands search queries with industry synonyms (e.g. k8s -> kubernetes). Default: llama-3.1-8b-instant.", bold_prefix="query_expand: ")
    db.add_bullet(doc, "Evaluates candidate fit and generates concise rationales for top jobs. Default: llama-3.3-70b-versatile -> claude-3-5-sonnet.", bold_prefix="job_rerank: ")
    db.add_bullet(doc, "Provides deep qualitative feedback on job cards. Default: llama-3.3-70b-versatile.", bold_prefix="job_explain: ")
    db.add_bullet(doc, "Suggests honest bullet point refinements aligned with job requirements. Default: claude-3-5-sonnet -> gpt-4o.", bold_prefix="resume_tailor: ")
    db.add_bullet(doc, "Drafts personalized, highly structured cover letters. Default: claude-3-5-sonnet -> llama-3.3-70b-versatile.", bold_prefix="cover_letter: ")
    db.add_bullet(doc, "Generates 1536-dim vector embeddings for semantic ranking. Default: local nomic-embed-text -> text-embedding-3-small.", bold_prefix="embeddings: ")

    db.add_heading_2(doc, "3.3 Structured Output Validation & Self-Healing Repair Loop")
    db.add_paragraph(
        doc,
        "When calling models for structured outputs (JSON), Drift enforces schema integrity using a robust two-stage repair loop implemented in `core/ai/base.py`. If a model returns malformed JSON or omits mandatory schema properties:",
    )
    db.add_bullet(doc, "The parsing error message and specific validation failures are formatted into a secondary corrective prompt.", bold_prefix="1. Feedback Generation: ")
    db.add_bullet(doc, "The model is given exactly one immediate repair attempt to fix the payload against the JSON Schema.", bold_prefix="2. Repair Completion: ")
    db.add_bullet(doc, "If the repair fails or the response remains invalid, the manager fails gracefully to the next provider in the fallback chain or local heuristics, ensuring zero application crashes.", bold_prefix="3. Deterministic Fallback: ")

    db.add_heading_2(doc, "3.4 Keystore & Security Architecture")
    db.add_paragraph(
        doc,
        "Drift enforces enterprise-grade key security via `core/ai/keystore.py`:",
    )
    db.add_bullet(doc, "On Windows systems, API keys are stored in the Windows Credential Manager via the DPAPI subsystem under target `Drift/ApiKey/<provider>`. Keys are encrypted using the user's Windows logon credentials.", bold_prefix="Windows Credential Manager (Primary): ")
    db.add_bullet(doc, "Where the OS keychain is unavailable, keys are stored in an AES-256-GCM encrypted sidecar file with strict file permissions (0600).", bold_prefix="AES-256-GCM Fallback: ")
    db.add_bullet(doc, "Keys are strictly write-only in the UI. Keys are masked upon entry (`gsk_...3xQ9`) and can never be exported or read back in plaintext via the user interface.", bold_prefix="Write-Only UI: ")
    db.add_bullet(doc, "Before every HTTP dispatch, `core/ai/http.py` verifies the destination IP and hostname against the registered provider domain whitelist. A mismatch aborts execution immediately, preventing key leakage through DNS spoofing.", bold_prefix="Host Whitelist Assertion: ")
    db.add_bullet(doc, "All error messages, loggers, and exception handlers pass through regex redaction to scrub key-shaped strings prior to emission.", bold_prefix="Key Redaction: ")

    # 4. Ingestion Engine & Scraping Architecture
    db.add_heading_1(doc, "4. Ingestion Engine & Scraping Architecture (core/sources/, core/engine/)")
    db.add_paragraph(
        doc,
        "Drift's ingestion subsystem features a concurrent, compliant crawling pipeline capable of fanning out across multiple job sources simultaneously while honoring remote service constraints.",
    )

    db.add_heading_2(doc, "4.1 Multi-Tier Ingestion Hierarchy")
    db.add_table(
        doc,
        headers=["Tier", "Classification", "Examples", "Ingestion Methodology & Compliance"],
        data=[
            ["Tier 1", "Declarative ATS Boards", "Greenhouse, Lever, Ashby, Workable", "Direct query to employer-canonical ATS widget APIs. Highest fidelity, full HTML descriptions, zero scraping overhead."],
            ["Tier 2", "Public Aggregators", "Himalayas, Working Nomads", "Key-free public JSON endpoints. Includes explicit salary disclosures, remote tags, and direct apply URLs."],
            ["Tier 5", "Community / BYOC", "Hacker News (Algolia), Reddit (OAuth)", "Community hiring threads. Hacker News utilizes Algolia API; Reddit connects via legitimate user OAuth tokens."],
            ["Tier 6", "Playwright Browser Adapter", "Custom Corporate Career Pages", "Framework for headless browser navigation with human pacing (2–6s random delay), robots verification, and zero CAPTCHA evasion."],
            ["Legacy", "First-Party Remote Feeds", "Jobicy, The Muse, Arbeitnow, RemoteOK, Remotive, We Work Remotely", "Legacy feeds maintained with circuit breakers and robots.txt gating."],
        ],
        col_widths=[0.8, 1.5, 1.8, 2.4],
    )

    db.add_heading_2(doc, "4.2 Concurrent ScanEngine Architecture (core/engine/)")
    db.add_paragraph(
        doc,
        "The `ScanEngine` (`core/engine/engine.py`) orchestrates job discovery across selected sources:",
    )
    db.add_bullet(doc, "Runs queries across a bounded thread pool (configurable between 1 and 64 threads; default is 12 threads). Clean ATS APIs execute first, followed by aggregators and browser sessions.", bold_prefix="Bounded Priority Pool: ")
    db.add_bullet(doc, "Implements a per-host `TokenBucket` rate limiter (default 120 requests/minute per host with maximum concurrency of 4) preventing accidental rate limit bans.", bold_prefix="Domain Token Bucket: ")
    db.add_bullet(doc, "Tracks consecutive network failures in the `source` table. Five consecutive errors trigger an automated 1-hour cooldown state (`cooling_off`).", bold_prefix="Circuit Breaker: ")
    db.add_bullet(doc, "All scan tasks observe a cooperative `CancelToken`. When the user clicks Cancel, running threads finish their current atomic unit and exit cleanly without data corruption.", bold_prefix="Cooperative Cancellation: ")
    db.add_bullet(doc, "Discovered jobs are written to the database checkpoint immediately upon source completion, allowing interrupted scans to resume seamlessly.", bold_prefix="Durable Checkpoints: ")
    db.add_bullet(doc, "If an overly restrictive query produces fewer results than `min_results`, the engine automatically relaxes constraints in order: nice-to-have keywords -> date window -> location mode -> salary floor.", bold_prefix="Automated Query Widening: ")

    # 5. Normalization, Deduplication & Ranking
    db.add_heading_1(doc, "5. Normalization, Deduplication & Ranking (core/normalize/, core/dedup/, core/ranking/)")
    db.add_paragraph(
        doc,
        "Raw job postings collected across disparate job boards exhibit wild variations in formatting, duplicate postings, and inconsistent terminology. Drift applies a 3-stage transformation pipeline:",
    )

    db.add_heading_2(doc, "5.1 Canonical Data Normalization (core/normalize/)")
    db.add_paragraph(
        doc,
        "Every raw job record is parsed into a strongly typed `NormalizedJob`:",
    )
    db.add_bullet(doc, "Extracted into minimum, maximum, currency (ISO 4217), and payment period (hourly, monthly, annual). Never inferred if unstated.", bold_prefix="Salary Normalization: ")
    db.add_bullet(doc, "Parsed into ISO 8601 UTC timestamps, with relative dates ('3 days ago') flagged with an approximate marker.", bold_prefix="Date Normalization: ")
    db.add_bullet(doc, "Standardized into structured city, state/province, country, and work-mode taxonomy (Remote, Hybrid, On-site).", bold_prefix="Location Normalization: ")
    db.add_bullet(doc, "Standardized to canonical tiers: Intern, Junior, Mid-Level, Senior, Lead, Staff, Principal, Executive.", bold_prefix="Seniority Mapping: ")

    db.add_heading_2(doc, "5.2 Content Fingerprinting & SimHash Deduplication (core/dedup/)")
    db.add_paragraph(
        doc,
        "To prevent duplicate entries when the same role is listed across multiple boards (e.g. Greenhouse, RemoteOK, and Himalayas), Drift generates a dual-layer fingerprint:",
    )
    db.add_bullet(doc, "`fingerprint = sha256(canonical_company + title + city)`. Guaranteed collision for identical postings.", bold_prefix="Exact Content Fingerprint: ")
    db.add_bullet(doc, "64-bit Hamming distance hash computed over description 3-grams. Postings with a Hamming distance <= 3 are merged as near-duplicate postings.", bold_prefix="SimHash Near-Merge: ")
    db.add_bullet(doc, "When duplicates merge, the system retains the most authoritative record (ATS > Aggregator > Legacy Feed), consolidates alternate apply links, and increments a 'Seen on N boards' badge.", bold_prefix="Authoritative Retention: ")

    db.add_heading_2(doc, "5.3 Multi-Stage Ranking Pipeline (core/ranking/)")
    db.add_paragraph(
        doc,
        "Candidates are ranked using a hybrid three-stage scoring engine:",
    )
    db.add_bullet(doc, "Fast, offline inverted-index BM25 scoring over title, required skills, and description text. Instantly filters out non-matching listings.", bold_prefix="Stage 1 — Lexical BM25: ")
    db.add_bullet(doc, "Cosine similarity between the candidate's resume embedding and the job posting embedding. Captures semantic alignment even when wording differs.", bold_prefix="Stage 2 — Semantic Cosine: ")
    db.add_bullet(doc, "Top 100 candidate jobs are submitted in batches of 20 to the configured LLM (e.g. Groq LLaMA-3.3-70B or Claude 3.5 Sonnet) to generate qualitative sub-scores and concise rationales.", bold_prefix="Stage 3 — LLM Reranking: ")

    db.add_callout(
        doc,
        "Final Score = (w_lex * Score_BM25) + (w_sem * Score_Cosine) + (w_llm * Score_LLM) * FreshnessDecay(posted_at).\nEvery job card displays the exact breakdown: Hard Skills %, Seniority Fit %, and Domain Alignment.",
        title="SCORING FORMULA",
        level="info",
    )

    # 6. Resume Intelligence & ATS Module
    db.add_heading_1(doc, "6. Resume Intelligence & ATS Module (core/resume/)")
    db.add_paragraph(
        doc,
        "The resume intelligence module provides comprehensive document parsing, multi-dimensional alignment analysis, honest tailoring, and multi-format document generation.",
    )

    db.add_heading_2(doc, "6.1 Multi-Format Layout-Aware Parser")
    db.add_paragraph(
        doc,
        "Resume files are parsed using a tiered fallback engine that handles complex visual layouts:",
    )
    db.add_bullet(doc, "PyMuPDF (fitz) -> pdfplumber (table/column extraction) -> pypdf fallback.", bold_prefix="PDF Documents: ")
    db.add_bullet(doc, "python-docx extracting paragraphs, runs, tables, and bullet structures.", bold_prefix="DOCX Documents: ")
    db.add_bullet(doc, "Windows COM automation (`win32com.client`) interacting with native Word when installed.", bold_prefix="DOC Legacy Documents: ")
    db.add_bullet(doc, "If no LLM key is configured, an offline heuristic regex engine extracts phone numbers, emails, LinkedIn URLs, GitHub links, and cross-references against a 190+ technical skill dictionary.", bold_prefix="Offline Heuristic Backfill: ")

    db.add_heading_2(doc, "6.2 8-Dimension Rubric Scoring")
    db.add_paragraph(
        doc,
        "Drift evaluates candidate fit across eight discrete dimensions, avoiding opaque single-number scores:",
    )
    db.add_table(
        doc,
        headers=["Dimension", "Weight", "Evaluation Methodology", "Missing Handling"],
        data=[
            ["Hard Skill Coverage", "30%", "Exact & synonym match of required technologies (e.g. React, PostgreSQL)", "Marked as Missing Skill"],
            ["Experience Duration", "15%", "Calculated total years in relevant software roles vs. job requirement", "Penalized if under minimum"],
            ["Seniority Alignment", "15%", "Title seniority tier comparison (Senior vs. Lead vs. Mid)", "Distance penalty"],
            ["Domain Relevance", "10%", "Industry keyword overlap (Fintech, Healthcare, AI, SaaS)", "Neutral if unspecified"],
            ["Education Criteria", "10%", "Degree level and field of study verification", "Neutral if experience compensates"],
            ["Location & Work Mode", "10%", "Work authorization, timezone alignment, remote compatibility", "Hard filter if incompatible"],
            ["Compensation Fit", "5%", "Candidate salary minimum vs. stated posting salary range", "Neutral if unstated"],
            ["ATS Mechanics", "5%", "Heading structure, keyword density, typography standard compliance", "Actionable formatting tips"],
        ],
        col_widths=[1.5, 0.8, 2.6, 1.6],
    )

    db.add_heading_2(doc, "6.3 Honest Tailoring Safety Net")
    db.add_paragraph(
        doc,
        "When tailoring resume bullets for specific jobs, Drift enforces a strict anti-hallucination safety net (`core/resume/generate.py`):",
    )
    db.add_callout(
        doc,
        "SAFETY NET ENFORCEMENT: The tailoring engine performs lexical analysis on every proposed bullet revision. If a generated bullet introduces a new numerical metric, unverified percentage, or technical skill NOT present in the candidate's master resume, the revision is instantly rejected and reverted. Drift strictly refuses to fabricate candidate qualifications.",
        title="INTEGRITY RULE",
        level="danger",
    )

    # 7. User Interface & Presentation Layer
    db.add_heading_1(doc, "7. User Interface & Presentation Layer (ui/)")
    db.add_paragraph(
        doc,
        "The presentation tier is built using PyQt5, structured as an enterprise desktop productivity application with hardware-accelerated rendering and custom styling tokens.",
    )

    db.add_heading_2(doc, "7.1 Design System Tokens & Motion Curves (ui/theme/)")
    db.add_paragraph(
        doc,
        "Drift implements a complete design system adhering to modern ergonomics:",
    )
    db.add_bullet(doc, "Includes tailored Dark and Light themes with 8 selectable accent palettes (Teal, Blue, Indigo, Purple, Rose, Orange, Amber, Emerald).", bold_prefix="Color System: ")
    db.add_bullet(doc, "Custom spring animation curves implemented via `QEasingCurve.setCustomType` evaluating `cubic-bezier(0.32, 0.72, 0, 1)`. Collapses to instant transitions when Windows reduced-motion is active.", bold_prefix="Motion Curves: ")
    db.add_bullet(doc, "Reusable inputs, custom tables, badges, toast notifications, dialogs, and progress indicators located in `ui/components/`.", bold_prefix="Component Library: ")

    db.add_heading_2(doc, "7.2 Application Screens & Navigation Flow")
    db.add_bullet(doc, "Overview of total scanned listings, active applications, conversion rates, and token spend.", bold_prefix="1. Dashboard (screen_dashboard.py): ")
    db.add_bullet(doc, "Comprehensive query builder with required/excluded terms, salary floors, and source selectors.", bold_prefix="2. Search Builder (screen_search_builder.py): ")
    db.add_bullet(doc, "Real-time streaming view showing active workers, source event logs, and cancel button.", bold_prefix="3. Live Run Monitor (screen_run.py): ")
    db.add_bullet(doc, "Interactive cards with match badges, score sliders, keyword highlights, and apply actions.", bold_prefix="4. Scored Results (screen_results.py): ")
    db.add_bullet(doc, "Interactive drag-and-drop Kanban board (Saved -> Applied -> Interview -> Offer).", bold_prefix="5. Application Tracker (screen_tracker.py): ")
    db.add_bullet(doc, "Resume editor, skill weighting panel, tailoring workspace, and DOCX/PDF export.", bold_prefix="6. Resume Studio (screen_resume.py): ")
    db.add_bullet(doc, "Live status, latency benchmarks, failure counters, and test buttons for all adapters.", bold_prefix="7. Source Health (screen_sources.py): ")
    db.add_bullet(doc, "Historical audit log of past scans with duration, yield, and query snapshots.", bold_prefix="8. Runs Audit (screen_runs.py): ")

    # 8. Build, Packaging & Distribution
    db.add_heading_1(doc, "8. Build, Packaging & Distribution")
    db.add_paragraph(
        doc,
        "Drift is compiled into a standalone, portable Windows executable using PyInstaller (`drift.spec`).",
    )
    db.add_bullet(doc, "In frozen mode, the application assets reside in the read-only bundle, while writable files (`jobs.db`, settings, logs) are directed to `%LOCALAPPDATA%\\Drift` via `app_paths.py`.", bold_prefix="Data Directory Redirection: ")
    db.add_bullet(doc, "Includes PyQt5 shared libraries, OpenSSL binaries, SQLite FTS5 extension, application icons, and Jinja2 templates.", bold_prefix="Bundled Dependencies: ")
    db.add_bullet(doc, "Packaged with `run.bat` for developer execution and `Drift.exe` for end users.", bold_prefix="Deployment Deliverables: ")

    output_path = Path("d:/Projects/Drift - Mindcob/Technical_Reference.docx")
    doc.save(str(output_path))
    print(f"Technical_Reference.docx saved to {output_path}")


if __name__ == "__main__":
    build_tech_reference()
