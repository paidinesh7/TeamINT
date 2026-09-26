#!/usr/bin/env python3
"""
=============================================================================
TEAMINT BI-WEEKLY DISPATCH AGGREGATOR & MAGAZINE COMPILER
=============================================================================
Parses individual team member share.md files from execution/dispatches/,
deduplicates dealflow, aggregates weak signals, compiles an institutional
Colossus-style HTML magazine, and renders a print-ready executive PDF.

Usage:
    python aggregate_dispatches.py [dispatches_directory] [output_html] [output_pdf]
=============================================================================
"""

import sys
import os
import re
import glob

# Try importing WeasyPrint for PDF generation
try:
    import weasyprint
    HAS_WEASYPRINT = True
except ImportError:
    HAS_WEASYPRINT = False


def parse_dispatch_file(file_path):
    """Parses an individual team member dispatch markdown file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract member name
    name_match = re.search(r"# Bi-Weekly Dispatch:\s*([^\n\r]+)", content)
    member_name = name_match.group(1).strip() if name_match else os.path.splitext(os.path.basename(file_path))[0]

    # Extract sector / mandate
    sector_match = re.search(r"\*\s*Sector\s*/\s*Mandate:\s*\*?\s*\[?([^\n\r\]]+)\]?", content, re.IGNORECASE)
    sector = sector_match.group(1).strip() if sector_match else "General"

    # Extract sections using regex
    curations = []
    signals = []
    deals = []
    interventions = []
    priorities = []

    # Section 1: Curations & Signals
    sec1_match = re.search(r"## 1\. High-Signal Curations & Emerging Patterns(.*?)(?=## 2\.|$)", content, re.DOTALL)
    if sec1_match:
        sec1_text = sec1_match.group(1)
        
        # Primary literature
        lit_matches = re.findall(r"\*\s*\*\*\[([^\]]+)\]\(([^)]*)\)\*\*:(.*?)(?=\*\s*\*\*\[|\n###|\Z)", sec1_text, re.DOTALL)
        for title, url, body in lit_matches:
            curations.append({
                "title": title.strip(),
                "url": url.strip(),
                "body": body.strip(),
                "member": member_name
            })
            
        # Weak signals
        sig_match = re.search(r"### Weak Signals & Structural Inflections(.*?)(?=\Z|##)", sec1_text, re.DOTALL)
        if sig_match:
            sig_lines = re.findall(r"\*\s*\*\*\[?([^\]:\*]+)\]?\*\*:\s*([^\n\r]+)", sig_match.group(1))
            for domain, desc in sig_lines:
                signals.append({
                    "domain": domain.strip(),
                    "description": desc.strip(),
                    "member": member_name
                })

    # Section 2: Dealflow Table
    sec2_match = re.search(r"## 2\. Dealflow & Sourcing Velocity(.*?)(?=## 3\.|$)", content, re.DOTALL)
    if sec2_match:
        sec2_text = sec2_match.group(1)
        table_rows = re.findall(r"^\|\s*\*\*([^\*\|]+)\*\*\s*\|\s*([^\|]+)\|\s*([^\|]+)\|\s*([^\|]+)\|\s*([^\|]+)\|\s*([^\|]+)\|", sec2_text, re.MULTILINE)
        for name, d_sector, stage, model, verdict, thesis in table_rows:
            if "Company A" in name or "Company B" in name:
                continue  # skip default placeholders if unmodified
            deals.append({
                "name": name.strip(),
                "sector": d_sector.strip(),
                "stage": stage.strip(),
                "model": model.strip(),
                "verdict": verdict.strip(),
                "thesis": thesis.strip(),
                "member": member_name
            })

    # Section 3: Portfolio Interventions
    sec3_match = re.search(r"## 3\. Portfolio Interventions & Support(.*?)(?=## 4\.|$)", content, re.DOTALL)
    if sec3_match:
        sec3_text = sec3_match.group(1)
        int_matches = re.findall(r"\*\s*\*\*\[?([^\]:\*]+)\]?\*\*:\s*(.*?)(?=\*\s*\*\*\[?|\Z)", sec3_text, re.DOTALL)
        for company, details in int_matches:
            if "Portfolio Company 1" in company or "Portfolio Company 2" in company:
                continue
            clean_details = re.sub(r"\s*\*Intervention:\*\s*", "", details).strip()
            interventions.append({
                "company": company.strip(),
                "details": clean_details,
                "member": member_name
            })

    # Section 4: Operational Priorities
    sec4_match = re.search(r"## 4\. Operational Priorities(.*?)(?=\Z)", content, re.DOTALL)
    if sec4_match:
        sec4_text = sec4_match.group(1)
        prio_lines = re.findall(r"\d+\.\s*\*\*\[?([^\]:\*]+)\]?\*\*:\s*([^\n\r]+)", sec4_text)
        for p_title, p_desc in prio_lines:
            priorities.append({
                "title": p_title.strip(),
                "desc": p_desc.strip(),
                "member": member_name
            })

    return {
        "name": member_name,
        "sector": sector,
        "curations": curations,
        "signals": signals,
        "deals": deals,
        "interventions": interventions,
        "priorities": priorities
    }


def generate_colossus_html(parsed_members, sprint_period="Current Sprint"):
    """Generates an institutional Colossus-grade HTML publication combining all dispatches."""
    all_curations = []
    all_signals = []
    all_deals = []
    all_interventions = []
    all_priorities = []

    for m in parsed_members:
        all_curations.extend(m["curations"])
        all_signals.extend(m["signals"])
        all_deals.extend(m["deals"])
        all_interventions.extend(m["interventions"])
        all_priorities.extend(m["priorities"])

    # Build Dealflow Table Rows
    deal_rows_html = ""
    for d in all_deals:
        verdict_class = "verdict-pursue" if "pursue" in d["verdict"].lower() else "verdict-pass"
        deal_rows_html += f"""
        <tr>
            <td><strong>{d['name']}</strong></td>
            <td>{d['sector']}</td>
            <td>{d['stage']}</td>
            <td>{d['model']}</td>
            <td><span class="badge {verdict_class}">{d['verdict']}</span></td>
            <td>{d['thesis']}</td>
            <td><em>{d['member']}</em></td>
        </tr>
        """
    if not deal_rows_html:
        deal_rows_html = "<tr><td colspan='7' style='text-align: center; color: #718096;'>No active pipeline deals logged this sprint.</td></tr>"

    # Build Signals HTML
    signals_html = ""
    for s in all_signals:
        signals_html += f"""
        <div class="signal-card">
            <div class="signal-meta"><strong>{s['domain']}</strong> &bull; Logged by {s['member']}</div>
            <div class="signal-desc">{s['description']}</div>
        </div>
        """
    if not signals_html:
        signals_html = "<p style='color: #718096;'>No weak signals registered this sprint.</p>"

    # Build Interventions HTML
    interventions_html = ""
    for i in all_interventions:
        interventions_html += f"""
        <div class="intervention-item">
            <strong>{i['company']}</strong>: {i['details']}
            <span class="author-tag">— {i['member']}</span>
        </div>
        """
    if not interventions_html:
        interventions_html = "<p style='color: #718096;'>No portfolio interventions logged this sprint.</p>"

    # Build Priorities HTML
    priorities_html = ""
    for p in all_priorities:
        priorities_html += f"""
        <li style="margin-bottom: 8px;">
            <strong>{p['title']}</strong> ({p['member']}): {p['desc']}
        </li>
        """
    if not priorities_html:
        priorities_html = "<li style='color: #718096;'>No upcoming priorities specified.</li>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Team Fortnightly Dispatch — {sprint_period}</title>
    <style>
        @page {{
            size: A4;
            margin: 18mm 20mm;
            @bottom-right {{
                content: "Page " counter(page) " of " counter(pages);
                font-family: 'Inter', -apple-system, sans-serif;
                font-size: 8pt;
                color: #718096;
            }}
            @bottom-left {{
                content: "Team Intelligence Executive Dispatch — Confidential";
                font-family: 'Inter', -apple-system, sans-serif;
                font-size: 8pt;
                color: #718096;
                font-weight: 500;
            }}
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #2D3748;
            line-height: 1.6;
            font-size: 9.8pt;
            margin: 0;
            padding: 0;
        }}

        .header-container {{
            border-bottom: 3px solid #0F2942;
            padding-bottom: 18px;
            margin-bottom: 25px;
        }}

        .category-tag {{
            font-size: 8.5pt;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #2F855A;
            margin-bottom: 6px;
        }}

        .title {{
            font-size: 22pt;
            color: #0F2942;
            margin: 0 0 8px 0;
            font-weight: 800;
            line-height: 1.15;
            letter-spacing: -0.5px;
        }}

        .subtitle {{
            font-size: 10.5pt;
            color: #4A5568;
            margin: 0;
            font-style: italic;
            font-weight: 400;
            line-height: 1.5;
        }}

        .metadata {{
            margin-top: 12px;
            font-size: 8pt;
            color: #718096;
            font-weight: 500;
        }}

        .metrics-grid {{
            display: flex;
            gap: 15px;
            margin: 20px 0;
        }}

        .metric-box {{
            flex: 1;
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            padding: 12px 15px;
            border-radius: 4px;
            text-align: center;
        }}

        .metric-num {{
            font-size: 18pt;
            font-weight: 800;
            color: #0F2942;
            line-height: 1.2;
        }}

        .metric-label {{
            font-size: 7.5pt;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #718096;
            font-weight: 600;
            margin-top: 4px;
        }}

        h2 {{
            font-size: 13pt;
            color: #0F2942;
            margin-top: 25px;
            margin-bottom: 10px;
            border-bottom: 1px solid #CBD5E0;
            padding-bottom: 4px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 8.5pt;
        }}

        th {{
            background-color: #0F2942;
            color: white;
            font-weight: 600;
            text-align: left;
            padding: 6px 8px;
            border: 1px solid #0F2942;
        }}

        td {{
            padding: 6px 8px;
            border: 1px solid #E2E8F0;
            vertical-align: top;
        }}

        tr:nth-child(even) {{
            background-color: #F8FAFC;
        }}

        .badge {{
            display: inline-block;
            padding: 2px 6px;
            font-size: 7.5pt;
            font-weight: 700;
            border-radius: 3px;
            text-transform: uppercase;
        }}

        .verdict-pursue {{
            background-color: #DEF7EC;
            color: #03543F;
        }}

        .verdict-pass {{
            background-color: #FDE8E8;
            color: #9B1C1C;
        }}

        .signal-card {{
            border-left: 3px solid #2F855A;
            background-color: #F0FDF4;
            padding: 10px 14px;
            margin-bottom: 10px;
            border-radius: 0 4px 4px 0;
        }}

        .signal-meta {{
            font-size: 8pt;
            color: #2F855A;
            font-weight: 600;
            margin-bottom: 3px;
        }}

        .signal-desc {{
            font-size: 9pt;
            color: #2D3748;
        }}

        .intervention-item {{
            padding: 8px 12px;
            border-bottom: 1px solid #EDF2F7;
            font-size: 9pt;
        }}

        .author-tag {{
            color: #718096;
            font-style: italic;
            font-size: 8pt;
            margin-left: 5px;
        }}
    </style>
</head>
<body>

    <div class="header-container">
        <div class="category-tag">Institutional Synthesis &bull; Fortnightly Review</div>
        <h1 class="title">Team Fortnightly Dispatch</h1>
        <p class="subtitle">Consolidated operational review synthesizing dealflow velocity, cross-pollinated sector weak signals, and active enterprise interventions.</p>
        <div class="metadata">
            Period: {sprint_period} &bull; Participating Members: {len(parsed_members)} &bull; Architecture: TeamINT
        </div>
    </div>

    <div class="metrics-grid">
        <div class="metric-box">
            <div class="metric-num">{len(all_deals)}</div>
            <div class="metric-label">Deals Evaluated</div>
        </div>
        <div class="metric-box">
            <div class="metric-num">{len(all_signals)}</div>
            <div class="metric-label">Weak Signals Logged</div>
        </div>
        <div class="metric-box">
            <div class="metric-num">{len(all_interventions)}</div>
            <div class="metric-label">Interventions Executed</div>
        </div>
        <div class="metric-box">
            <div class="metric-num">{len(all_priorities)}</div>
            <div class="metric-label">Priorities in Flight</div>
        </div>
    </div>

    <h2>1. Consolidated Dealflow & Sourcing Matrix</h2>
    <table>
        <thead>
            <tr>
                <th>Company</th>
                <th>Sector</th>
                <th>Stage</th>
                <th>Business Model</th>
                <th>Verdict</th>
                <th>Underwriting Thesis</th>
                <th>Lead</th>
            </tr>
        </thead>
        <tbody>
            {deal_rows_html}
        </tbody>
    </table>

    <h2>2. Cross-Pollinated Weak Signals & Structural Inflections</h2>
    {signals_html}

    <h2>3. Portfolio & Enterprise Interventions</h2>
    {interventions_html}

    <h2>4. Active Fortnightly Priorities Across Team</h2>
    <ul style="padding-left: 20px;">
        {priorities_html}
    </ul>

</body>
</html>
"""
    return html


def main():
    dispatches_dir = sys.argv[1] if len(sys.argv) > 1 else "execution/dispatches"
    output_html = sys.argv[2] if len(sys.argv) > 2 else "execution/dispatches/fortnightly_executive_dispatch.html"
    output_pdf = sys.argv[3] if len(sys.argv) > 3 else "execution/dispatches/fortnightly_executive_dispatch.pdf"

    if not os.path.isabs(dispatches_dir):
        # Resolve relative to script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        vault_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
        dispatches_dir = os.path.join(vault_root, dispatches_dir)
        output_html = os.path.join(vault_root, output_html)
        output_pdf = os.path.join(vault_root, output_pdf)

    print(f"Scanning for team dispatches in: {dispatches_dir}")
    md_files = glob.glob(os.path.join(dispatches_dir, "*.md"))

    if not md_files:
        print(f"❌ No markdown dispatch files found in: {dispatches_dir}")
        print("Please place member share.md files into execution/dispatches/ to aggregate.")
        return

    print(f"Found {len(md_files)} member dispatch(es):")
    parsed_members = []
    for f in md_files:
        print(f"  • Parsing: {os.path.basename(f)}")
        parsed_members.append(parse_dispatch_file(f))

    # Generate unified HTML
    html_content = generate_colossus_html(parsed_members)
    os.makedirs(os.path.dirname(os.path.abspath(output_html)), exist_ok=True)
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Generated Executive HTML Dispatch: {output_html}")

    # Compile to PDF
    if HAS_WEASYPRINT:
        try:
            print("Compiling Executive PDF via WeasyPrint...")
            weasyprint.HTML(filename=output_html).write_pdf(output_pdf)
            print(f"✅ Generated Executive PDF Dispatch: {output_pdf}")
        except Exception as e:
            print(f"⚠️ WeasyPrint compilation notice: {e}")
    else:
        print("ℹ️ WeasyPrint not installed. HTML dispatch generated successfully.")


if __name__ == "__main__":
    main()
