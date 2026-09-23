# Rainmatter Context Architecture: Operational Guide

> *"What is not documented in writing does not compound in memory."*

This repository is an offline-first, local cognitive environment built for Rainmatter team members. It is designed to minimize meeting overhead, enforce disciplined underwriting standards, and enable asynchronous intellectual compounding through Gemini CLI.

---

## 1. Initial Setup (Two-Minute Configuration)

### A. Clone the Repository
Save this folder locally on your machine (e.g., `~/rainmatter/context`).

### B. Launch the Operating Environment
Navigate to the root directory and start the CLI session:
```bash
cd ~/rainmatter/context
gemini
```

### C. Automated First-Time Initialization
Upon your first launch, Gemini CLI inspects `staging/10_identity/profile.md`. If uninitialized, it prompts you for four core parameters:
1. Full name.
2. Primary sector or operational mandate at Rainmatter (Climate, Health, Fintech, Media, Foundation, Legal/Finance).
3. Two to three core quarterly research hypotheses.
4. Preferred analytical workflow (e.g., deep narrative drafting, quantitative unit-economic modeling, founder call synthesis).

Gemini CLI will autonomously populate your profile, calibrate your dashboard, and format your bi-weekly share file.

---

## 2. Structural Architecture: Inputs vs. Outputs

The workspace separates cognitive intake (**Staging**) from concrete work products (**Execution**).

```
├── Dashboard.md                 <-- Central Navigation Index & Workspace Map
├── share.md                     <-- Bi-Weekly Public Dispatch (Asynchronous Team Sync)
│
├── staging/                     <-- COGNITIVE INPUTS (Intake & Synthesis)
│   ├── 10_identity/             <-- Operational manual, working style, and mandate
│   ├── 20_curation/             <-- Searchable repository of foundational literature & mental models
│   ├── 30_notes/                <-- Unstructured call logs, founder interviews, and scratchpads
│   └── 40_research/             <-- Deep thematic studies and early sector signal radars
│
└── execution/                   <-- OPERATIONAL OUTPUTS (Artifacts & Actions)
    ├── pipeline/                <-- Dealflow tracking, stage progression, and anti-slippage SLA
    ├── memos/                   <-- Concise one-page deal evaluation memos
    ├── updates/                 <-- Portfolio company quarterly health briefs
    ├── templates/               <-- Colossus-grade HTML publication templates
    └── scripts/                 <-- Local utilities and WeasyPrint PDF compiler
```

---

## 3. Zero-Manual-Friction: The Hands-Free CLI Playbook

**You never need to manually open, format, or edit markdown files or tables.** 

Gemini CLI operates as your autonomous research associate. You simply speak or type natural commands in the terminal, and it executes the file management, table updates, and date calculations for you:

### Logging a Deal & Sourcing Call
> *"I met Founder X from Enterprise Y today. They build distributed sodium-ion batteries in Gujarat, targeting ₹3 Cr seed round on ₹18 Cr post-money. Add them to my pipeline as a P0 deal and set my next action as drafting an investment memo due this Friday."*
*(Gemini CLI automatically updates `execution/pipeline/pipeline_tracker.md` with dates, stages, and SLA tags).*

### Auditing Pipeline Follow-ups (Anti-Slippage)
> *"Check my pipeline. Who am I overdue to follow up with under our seven-day SLA?"*
*(Gemini CLI calculates elapsed days since last contact and gives you a prioritized action list).*

### Archiving a Passed Deal
> *"We decided to pass on Enterprise Z because their gross margin is negative 20% and they rely on subsidized third-party APIs. Move them from my active pipeline to the passed archive with that rationale."*
*(Gemini CLI removes the deal from the active table and logs it in the learning archive).*

### Logging a Sector Weak Signal
> *"I noticed transformer lead times across state utilities extended to 24 months. Log this as a supply-chain weak signal in my clean energy radar."*
*(Gemini CLI registers the observation in `staging/40_research/sector_signal_radar.md`).*

### Synthesizing Messy Founder Call Notes
> *"Here are my messy bullet points from my call with Founder A: [paste raw notes]. Structure this into a one-page investment memo in execution/memos/ using our template."*

### Compiling Your Bi-Weekly Asynchronous Dispatch
> *"It is the end of the sprint. Scan my notes, memos, weak signals, and pipeline actions over the past two weeks, and prepare my share.md file."*

### Generating Executive HTML & PDF Briefs
> *"Format my Enterprise Y memo into a Colossus-style HTML brief and compile it to an executive PDF."*

---

## 4. The Bi-Weekly Asynchronous Protocol

Rainmatter operates on trust and asynchronous clarity over bureaucratic status meetings. 

Every two weeks, update your **`share.md`** file with high-signal learnings, dealflow evaluations, and active portfolio interventions. These logs are synthesized into a consolidated team dispatch, maintaining organizational alignment without synchronous friction.
