"""HTML to PDF conversion via wkhtmltopdf."""

import os
import subprocess
from pathlib import Path
from datetime import datetime


OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", Path(__file__).parent.parent.parent / "output"))


def ensure_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_html(html: str, name: str) -> Path:
    """Save HTML to output directory, return path."""
    ensure_output_dir()
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{name}-{ts}.html"
    path = OUTPUT_DIR / filename
    path.write_text(html, encoding="utf-8")
    return path


def html_to_pdf(html_path: Path) -> Path:
    """Convert HTML file to PDF using wkhtmltopdf."""
    pdf_path = html_path.with_suffix(".pdf")
    env = os.environ.copy()
    env["QT_QPA_PLATFORM"] = "offscreen"
    result = subprocess.run(
        [
            "wkhtmltopdf",
            "--quiet",
            "--enable-local-file-access",
            "--orientation", "Landscape",
            "--page-size", "A4",
            "--margin-top", "0",
            "--margin-bottom", "0",
            "--margin-left", "0",
            "--margin-right", "0",
            "--disable-smart-shrinking",
            str(html_path),
            str(pdf_path),
        ],
        env=env,
        capture_output=True,
        timeout=30,
    )
    if not pdf_path.exists():
        raise RuntimeError(f"PDF generation failed: {result.stderr.decode()}")
    return pdf_path


def render(html: str, name: str) -> tuple[Path, Path]:
    """Save HTML, zip it for WhatsApp delivery, and convert to PDF. Returns (html_path, zip_path)."""
    html_path = save_html(html, name)
    pdf_path = html_to_pdf(html_path)
    # Create zip for WhatsApp (it blocks raw .html files)
    zip_path = html_path.with_suffix(".zip")
    import zipfile
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(html_path, html_path.name)
    return html_path, zip_path
