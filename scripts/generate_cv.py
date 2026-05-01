from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "CV.pdf"

PAGE_WIDTH, PAGE_HEIGHT = fitz.paper_size("a4")
MARGIN_X = 42
CONTENT_WIDTH = PAGE_WIDTH - (MARGIN_X * 2)

REGULAR_FONT_PATH = Path(r"C:\Windows\Fonts\calibri.ttf")
BOLD_FONT_PATH = Path(r"C:\Windows\Fonts\calibrib.ttf")


def load_font(page, alias, font_path, fallback_name):
    if font_path.exists():
        page.insert_font(fontname=alias, fontfile=str(font_path))
        return fitz.Font(fontfile=str(font_path)), alias, str(font_path)
    return fitz.Font(fallback_name), fallback_name, None


def wrap_text(text, font, size, max_width):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        candidate = word if not current else f"{current} {word}"
        if font.text_length(candidate, fontsize=size) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def draw_lines(page, x, y, lines, size, font_name, font_file, color=(0, 0, 0), leading=1.22):
    for line in lines:
        kwargs = {
            "fontname": font_name,
            "fontsize": size,
            "color": color,
            "overlay": True,
        }
        if font_file:
            kwargs["fontfile"] = font_file
        page.insert_text((x, y), line, **kwargs)
        y += size * leading
    return y


def draw_paragraph(page, x, y, text, width, size, font, font_name, font_file, spacing_after=5):
    lines = wrap_text(text, font, size, width)
    y = draw_lines(page, x, y, lines, size, font_name, font_file)
    return y + spacing_after


def draw_bullets(page, x, y, bullets, width, size, font, font_name, font_file, spacing_after=6):
    bullet_radius = 2.1
    indent = 16
    text_width = width - indent

    for bullet in bullets:
        lines = wrap_text(bullet, font, size, text_width)
        bullet_y = y - (size * 0.28)
        page.draw_circle((x + 6, bullet_y), bullet_radius, color=(0, 0, 0), fill=(0, 0, 0), overlay=True)
        y = draw_lines(page, x + indent, y, lines, size, font_name, font_file)
        y += spacing_after

    return y


def draw_section_heading(page, x, y, text, size, font_name, font_file):
    kwargs = {
        "fontname": font_name,
        "fontsize": size,
        "color": (0, 0, 0),
        "overlay": True,
    }
    if font_file:
        kwargs["fontfile"] = font_file
    page.insert_text((x, y), text.upper(), **kwargs)
    return y + (size * 1.45)


def add_link(page, rect, url):
    page.insert_link({"kind": fitz.LINK_URI, "from": rect, "uri": url})


def main():
    doc = fitz.open()
    page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)

    regular_font, regular_name, regular_file = load_font(page, "cv_regular", REGULAR_FONT_PATH, "helv")
    bold_font, bold_name, bold_file = load_font(page, "cv_bold", BOLD_FONT_PATH, "helv-bold")

    name = "RICCARDO CAPANNA"
    title = "AI Adoption & GenAI Transformation | Process Analysis | Governance | Business-Technology Translator"
    contact_line_1 = "Email: errer441122@gmail.com | Phone: +39 3425873190"
    contact_line_2 = "Bologna, Italy | Portfolio: https://errer441122.github.io/regulated-ai-governance-cockpit/ | GitHub: https://github.com/errer441122"

    profile = (
        "Final-year Communication Sciences and Digital Media student with hands-on portfolio work in GenAI "
        "adoption, process analysis and governance for regulated environments. I design use-case discovery "
        "flows, stakeholder maps, training plans, adoption KPIs and human-in-the-loop guardrails, translating "
        "AI capabilities into practical workflows for business, compliance and technical stakeholders. Interested "
        "in AI transformation, responsible GenAI adoption and consulting-oriented implementation projects."
    )

    education_lines = [
        "Universita degli Studi Guglielmo Marconi (UniMarconi)",
        "Laurea Triennale in Scienze della Comunicazione e Media Digitali",
        "2023 - Present | Currently in the third year | Expected graduation: 2026",
    ]

    selected_project_title = "Regulated AI Commercial Ops Cockpit - AI Adoption & Governance Case Study"
    selected_project_bullets = [
        "Designed an AI adoption case study for a simulated regulated-enterprise workflow, covering stakeholder mapping, phased rollout, training by audience, adoption KPIs and governance guardrails.",
        "Built a GenAI account brief simulator using structured prompt logic, approved-data framing and human-review positioning.",
        "Created a process analysis layer with 20 accounts, 16 opportunities and 9 sales stages, including weighted scoring, stage exit criteria, bottleneck diagnostics and Sales-to-CS handoff logic.",
        "Produced consulting-style deliverables: governance checklist, training plan, adoption metrics, use-case prioritization logic and methodology/limitations section.",
    ]

    applied_ai_bullets = [
        "Built and deployed BESTIK, an AI intelligence pipeline using LangChain/LangGraph, FAISS/SQLite memory, Docker and cloud deployment to turn public data into structured reports, performance views and Telegram notifications.",
        "Focused on workflow reliability, quality gates, human oversight and repeatable reporting rather than fully autonomous decision-making.",
        "Built and documented agentic and conditional workflow prototypes using n8n, Zapier, Power Automate basics and Copilot Studio concepts, with a focus on human oversight, context handling and operational reliability.",
        "Use LLMs to structure research, synthesize regulatory information, generate operational templates, and prepare workshop or training materials for business adoption workflows.",
    ]

    skill_bullets = [
        "AI Adoption & Governance: stakeholder mapping, use-case intake, training planning, adoption KPIs, human-in-the-loop guardrails, EU AI Act awareness.",
        "Process Analysis & Commercial Ops: CRM workflow design, pipeline governance, weighted forecasting, bottleneck analysis, Sales-to-CS handoff.",
        "Prompt Engineering & Automation: prompt structuring, task decomposition, output validation, agentic workflows, persistent memory, context management, local databases, Power Automate, Copilot Studio.",
        "Data, Reporting & Communication: Excel / Google Sheets, Google Analytics, performance visualizations, clear documentation, structured writing, presentation.",
    ]

    role_match_bullets = [
        "Interested in AI Adoption, GenAI transformation and consulting-oriented implementation work in regulated or process-heavy environments.",
        "Natural bridge between business communication, AI tooling and operational thinking: useful for use-case discovery, workflow improvement, training support and cross-functional coordination.",
        "Languages: English: B2 (upper-intermediate) | Italian native",
        "Earliest start date: 01/05/2026 | Internship availability: 5-6 months | Open to remote: Yes",
    ]

    y = 44
    y = draw_lines(page, MARGIN_X, y, [name], 22, bold_name, bold_file, leading=1.0)
    y += 6
    y = draw_paragraph(page, MARGIN_X, y, title, CONTENT_WIDTH, 11.4, bold_font, bold_name, bold_file, spacing_after=4)
    contact_y_1 = y
    contact_lines_1 = wrap_text(contact_line_1, regular_font, 9.2, CONTENT_WIDTH)
    y = draw_lines(page, MARGIN_X, y, contact_lines_1, 9.2, regular_name, regular_file, color=(0.23, 0.23, 0.23))
    y += 2
    contact_y_2 = y
    contact_lines_2 = wrap_text(contact_line_2, regular_font, 9.2, CONTENT_WIDTH)
    y = draw_lines(page, MARGIN_X, y, contact_lines_2, 9.2, regular_name, regular_file, color=(0.23, 0.23, 0.23))
    y += 10

    email_text = "Email: errer441122@gmail.com"
    phone_text = "Phone: +39 3425873190"
    email_x = MARGIN_X
    phone_prefix = "Email: errer441122@gmail.com | "
    phone_x = MARGIN_X + regular_font.text_length(phone_prefix, fontsize=9.2)
    portfolio_text = "Portfolio: https://errer441122.github.io/regulated-ai-governance-cockpit/"
    github_text = "GitHub: https://github.com/errer441122"
    portfolio_x = MARGIN_X + regular_font.text_length("Bologna, Italy | ", fontsize=9.2)
    github_prefix = "Bologna, Italy | Portfolio: https://errer441122.github.io/regulated-ai-governance-cockpit/ | "
    github_x = MARGIN_X + regular_font.text_length(github_prefix, fontsize=9.2)
    add_link(page, fitz.Rect(email_x, contact_y_1 - 9, email_x + regular_font.text_length(email_text, fontsize=9.2), contact_y_1 + 2), "mailto:errer441122@gmail.com")
    add_link(page, fitz.Rect(phone_x, contact_y_1 - 9, phone_x + regular_font.text_length(phone_text, fontsize=9.2), contact_y_1 + 2), "tel:+393425873190")
    add_link(page, fitz.Rect(portfolio_x, contact_y_2 - 9, portfolio_x + regular_font.text_length(portfolio_text, fontsize=9.2), contact_y_2 + 2), "https://errer441122.github.io/regulated-ai-governance-cockpit/")
    add_link(page, fitz.Rect(github_x, contact_y_2 - 9, github_x + regular_font.text_length(github_text, fontsize=9.2), contact_y_2 + 2), "https://github.com/errer441122")

    page.draw_line((MARGIN_X, y), (PAGE_WIDTH - MARGIN_X, y), color=(0.72, 0.72, 0.72), width=0.8)
    y += 16

    y = draw_section_heading(page, MARGIN_X, y, "Profile", 10.2, bold_name, bold_file)
    y = draw_paragraph(page, MARGIN_X, y, profile, CONTENT_WIDTH, 9.1, regular_font, regular_name, regular_file, spacing_after=9)

    y = draw_section_heading(page, MARGIN_X, y, "Education", 10.2, bold_name, bold_file)
    y = draw_lines(page, MARGIN_X, y, [education_lines[0]], 9.1, bold_name, bold_file)
    y = draw_lines(page, MARGIN_X, y, [education_lines[1]], 9.1, regular_name, regular_file)
    y = draw_lines(page, MARGIN_X, y, [education_lines[2]], 9.1, regular_name, regular_file)
    y += 8

    y = draw_section_heading(page, MARGIN_X, y, "Selected Project", 10.2, bold_name, bold_file)
    y = draw_lines(page, MARGIN_X, y, wrap_text(selected_project_title, bold_font, 9.4, CONTENT_WIDTH), 9.4, bold_name, bold_file)
    y += 4
    y = draw_bullets(page, MARGIN_X, y, selected_project_bullets, CONTENT_WIDTH, 8.85, regular_font, regular_name, regular_file, spacing_after=4.5)

    y = draw_section_heading(page, MARGIN_X, y, "Applied AI, Automation and Digital Projects", 10.2, bold_name, bold_file)
    y = draw_bullets(page, MARGIN_X, y, applied_ai_bullets, CONTENT_WIDTH, 8.85, regular_font, regular_name, regular_file, spacing_after=4.5)

    y = draw_section_heading(page, MARGIN_X, y, "Relevant Skills", 10.2, bold_name, bold_file)
    y = draw_bullets(page, MARGIN_X, y, skill_bullets, CONTENT_WIDTH, 8.8, regular_font, regular_name, regular_file, spacing_after=4.2)

    y = draw_section_heading(page, MARGIN_X, y, "Role Match and Availability", 10.2, bold_name, bold_file)
    y = draw_bullets(page, MARGIN_X, y, role_match_bullets, CONTENT_WIDTH, 8.9, regular_font, regular_name, regular_file, spacing_after=4.2)

    doc.save(str(OUTPUT), garbage=4, deflate=True)
    doc.close()


if __name__ == "__main__":
    main()
