from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "social-preview.png"

WIDTH = 1200
HEIGHT = 630


def add_text(page, x, y, text, fontsize, fontname="helv", color=(1, 1, 1)):
    page.insert_text(
        (x, y),
        text,
        fontname=fontname,
        fontsize=fontsize,
        color=color,
        overlay=True,
    )


def main():
    doc = fitz.open()
    page = doc.new_page(width=WIDTH, height=HEIGHT)

    background = fitz.Rect(0, 0, WIDTH, HEIGHT)
    page.draw_rect(background, color=(0.06, 0.09, 0.13), fill=(0.06, 0.09, 0.13), overlay=True)

    page.draw_rect(fitz.Rect(0, 0, WIDTH, 120), color=(0.78, 0.36, 0.23), fill=(0.78, 0.36, 0.23), overlay=True)
    page.draw_circle((1000, 110), 220, color=(0.83, 0.66, 0.33), fill=(0.83, 0.66, 0.33), overlay=True)
    page.draw_circle((1120, 520), 170, color=(0.13, 0.18, 0.24), fill=(0.13, 0.18, 0.24), overlay=True)

    add_text(page, 70, 95, "RICCARDO CAPANNA", 28, "hebo", (0.97, 0.97, 0.97))
    add_text(page, 70, 220, "Regulated AI Commercial Ops Cockpit", 34, "hebo", (0.96, 0.96, 0.96))
    add_text(page, 70, 270, "AI Adoption, Governance, Workflow Design", 24, "helv", (0.89, 0.90, 0.92))
    add_text(page, 70, 330, "Stakeholder maps, training plans, guardrails,", 20, "helv", (0.84, 0.86, 0.89))
    add_text(page, 70, 362, "prompt-structured workflows, and no-code automation.", 20, "helv", (0.84, 0.86, 0.89))

    pill = fitz.Rect(70, 430, 420, 478)
    page.draw_rect(pill, color=(0.83, 0.66, 0.33), fill=(0.83, 0.66, 0.33), overlay=True)
    add_text(page, 92, 462, "Case Study for AI Adoption Reviewers", 17, "hebo", (0.08, 0.09, 0.11))

    footer = fitz.Rect(70, 535, 720, 575)
    page.draw_rect(footer, color=(0.13, 0.18, 0.24), fill=(0.13, 0.18, 0.24), overlay=True)
    add_text(page, 92, 560, "Portfolio: errer441122.github.io/regulated-ai-governance-cockpit", 14, "helv", (0.94, 0.94, 0.94))

    pix = page.get_pixmap(alpha=False)
    pix.save(str(OUTPUT))
    doc.close()


if __name__ == "__main__":
    main()
