"""
Generates visual screenshots and presentation cards for the 5 test cases.
Saves high-resolution PNGs in the `screenshots/` directory for the report.
"""

import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

def create_card_screenshot(test_file: str, output_image: str):
    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data["test_case_metadata"]
    projects = data["projects"]

    fig, ax = plt.subplots(figsize=(12, 14), dpi=150)
    fig.patch.set_facecolor("#f8fafc")
    ax.set_facecolor("#f8fafc")
    ax.axis("off")

    # Header Banner
    header_box = patches.FancyBboxPatch(
        (0.03, 0.90), 0.94, 0.08,
        boxstyle="round,pad=0.015,rounding_size=0.02",
        facecolor="#4f46e5", edgecolor="none"
    )
    ax.add_patch(header_box)

    ax.text(0.06, 0.945, f"💡 Project Idea Generator - Test Case #{meta['id']}", 
            fontsize=16, fontweight="bold", color="white", va="center")
    ax.text(0.06, 0.915, f"Domain: {meta['domain']}  |  Level: {meta['skill_level']}  |  Time: {meta['time_limit']}", 
            fontsize=10.5, color="#e0e7ff", va="center")

    # Draw 5 Project Cards
    y_start = 0.86
    card_height = 0.145
    gap = 0.022

    diff_colors = {
        "Beginner": ("#dcfce7", "#15803d"),
        "Intermediate": ("#dbeafe", "#1d4ed8"),
        "Advanced": ("#fef3c7", "#b45309")
    }

    for idx, p in enumerate(projects):
        y_pos = y_start - (idx * (card_height + gap))
        
        # Card Background
        card = patches.FancyBboxPatch(
            (0.03, y_pos - card_height), 0.94, card_height,
            boxstyle="round,pad=0.01,rounding_size=0.015",
            facecolor="#ffffff", edgecolor="#cbd5e1", linewidth=1.2
        )
        ax.add_patch(card)

        # Difficulty Badge
        bg_col, txt_col = diff_colors.get(p.get("difficulty", "Intermediate"), ("#dbeafe", "#1d4ed8"))
        badge = patches.FancyBboxPatch(
            (0.05, y_pos - 0.032), 0.13, 0.022,
            boxstyle="round,pad=0.005,rounding_size=0.008",
            facecolor=bg_col, edgecolor="none"
        )
        ax.add_patch(badge)
        ax.text(0.115, y_pos - 0.021, p.get("difficulty", "Intermediate").upper(),
                fontsize=8, fontweight="bold", color=txt_col, ha="center", va="center")

        # Time Badge
        time_badge = patches.FancyBboxPatch(
            (0.19, y_pos - 0.032), 0.15, 0.022,
            boxstyle="round,pad=0.005,rounding_size=0.008",
            facecolor="#f3e8ff", edgecolor="none"
        )
        ax.add_patch(time_badge)
        ax.text(0.265, y_pos - 0.021, f"⏱ {p.get('estimated_time', '')}",
                fontsize=8, fontweight="bold", color="#7e22ce", ha="center", va="center")

        # Title & Tagline
        ax.text(0.05, y_pos - 0.052, f"#{p['id']}  {p['title']}", 
                fontsize=11.5, fontweight="bold", color="#1e293b", va="center")
        ax.text(0.05, y_pos - 0.073, f'"{p["tagline"]}"', 
                fontsize=8.5, fontstyle="italic", color="#64748b", va="center")

        # Modules Summary
        mods = p.get("key_modules", [])
        mod_names = "  •  ".join([m.get("module_name", "") for m in mods[:3]])
        ax.text(0.05, y_pos - 0.096, f"Modules: {mod_names}", 
                fontsize=8, color="#334155", va="center")

        # Tools & Stack
        tools = p.get("tools_and_technologies", {})
        tool_list = []
        for cat in ["frontend", "backend", "ai_or_apis"]:
            tool_list.extend(tools.get(cat, []))
        tool_str = " | ".join(tool_list[:5])
        ax.text(0.05, y_pos - 0.116, f"Stack: {tool_str}", 
                fontsize=8, color="#0f766e", fontweight="bold", va="center")

        # Winning Tip
        tip = p.get("evaluation_winning_tip", "")
        if len(tip) > 85:
            tip = tip[:82] + "..."
        ax.text(0.05, y_pos - 0.134, f"🏆 10-Mark Tip: {tip}", 
                fontsize=7.8, color="#7c3aed", fontstyle="italic", va="center")

    # Footer
    ax.text(0.5, 0.015, "Generative AI Mini Project &bull; Evaluation Topic #49: Project Idea Generator",
            fontsize=8.5, color="#94a3b8", ha="center", va="center")

    os.makedirs(os.path.dirname(output_image), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_image, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close()
    print(f"Generated screenshot: {output_image}")

def generate_all():
    samples_dir = os.path.join(os.path.dirname(__file__), "sample_outputs")
    screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    files = [
        ("test_case_1_healthcare_telemedicine.json", "test_case_1_healthcare.png"),
        ("test_case_2_cybersecurity_threat_detection.json", "test_case_2_cybersecurity.png"),
        ("test_case_3_edtech_personalized_learning.json", "test_case_3_edtech.png"),
        ("test_case_4_fintech_fraud_detection.json", "test_case_4_fintech.png"),
        ("test_case_5_environmental_sustainability.json", "test_case_5_sustainability.png"),
    ]

    for jf, img in files:
        json_path = os.path.join(samples_dir, jf)
        if os.path.exists(json_path):
            create_card_screenshot(json_path, os.path.join(screenshots_dir, img))

if __name__ == "__main__":
    generate_all()
