"""
Packages all required deliverables for Google Drive submission:
Drive_Upload_Package/
├── Report.pdf (2-page procedure report)
├── Code.zip (full project code, without API keys or venv)
├── github_link.txt (GitHub repository URL)
└── screenshots/ (5 output screenshots)
"""

import os
import shutil
import zipfile

def package_drive_files():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(base_dir, "Drive_Upload_Package")
    
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir, exist_ok=True)

    # 1. github_link.txt
    gh_link_path = os.path.join(dist_dir, "github_link.txt")
    with open(gh_link_path, "w", encoding="utf-8") as f:
        f.write("https://github.com/shahidshaikh181807-design/MultiModal_Generative_AI_Studio\n")
    print(f"Created: {gh_link_path}")

    # 2. Copy Report.pdf
    src_pdf = os.path.join(base_dir, "Report.pdf")
    if os.path.exists(src_pdf):
        shutil.copy2(src_pdf, os.path.join(dist_dir, "Report.pdf"))
        print(f"Copied: Report.pdf to {dist_dir}")
    else:
        print("Warning: Report.pdf not found. Run generate_pdf_report.py first.")

    # 3. Copy screenshots/
    src_screenshots = os.path.join(base_dir, "screenshots")
    dst_screenshots = os.path.join(dist_dir, "screenshots")
    if os.path.exists(src_screenshots):
        shutil.copytree(src_screenshots, dst_screenshots)
        print(f"Copied: screenshots/ to {dist_dir}")

    # 4. Create Code.zip (Strictly WITHOUT .env, venv, or __pycache__)
    code_zip_path = os.path.join(dist_dir, "Code.zip")
    
    exclude_dirs = {".git", "venv", ".venv", "env", "__pycache__", "Drive_Upload_Package", ".gemini"}
    exclude_files = {".env", "Code.zip"}

    with zipfile.ZipFile(code_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(base_dir):
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file in exclude_files or file.endswith(".pyc"):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                zf.write(full_path, rel_path)

    print(f"Created: Code.zip (size: {os.path.getsize(code_zip_path) / 1024:.1f} KB)")
    print(f"\nAll files successfully packaged inside:\n{dist_dir}")

if __name__ == "__main__":
    package_drive_files()
