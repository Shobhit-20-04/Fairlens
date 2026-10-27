"""
FairLens: Build High-Resolution Composite and Individual Proofs for Legal & Financial Domains.
Creates:
1. 11_nvidia_nemotron_legal_pretraining_us_only_proof.png (Side-by-side annotated composite of Page 6 and Page 7).
2. 11a_nvidia_nemotron_technical_report_page6.png (Ultra high-res full Page 6).
3. 11b_nvidia_nemotron_technical_report_page7.png (Ultra high-res full Page 7).
4. 12_nvidia_nemotron_financial_eval_us_only_proof.png (Ultra high-res full Page 37).
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import pypdfium2 as pdfium

WORKSPACE_DIR = Path("D:/fairlens")
OUTPUT_DIR = WORKSPACE_DIR / "research_papers" / "official_proof_screenshots"
PDF_PATH = WORKSPACE_DIR / "research_papers" / "08_Nemotron_and_NVIDIA" / "Nemotron-3-Ultra-550B_Technical_Report.pdf"


def build_proofs():
    pdf = pdfium.PdfDocument(str(PDF_PATH))
    scale = 2.2

    # Render Pages 6, 7, and 37
    print("--> Rendering Pages 6, 7, and 37 with PDFium vector engine...")
    img6 = pdf[5].render(scale=scale).to_pil()
    img7 = pdf[6].render(scale=scale).to_pil()
    img37 = pdf[36].render(scale=scale).to_pil()

    # Save individual high-res pages
    p6_path = OUTPUT_DIR / "11a_nvidia_nemotron_technical_report_page6.png"
    p7_path = OUTPUT_DIR / "11b_nvidia_nemotron_technical_report_page7.png"
    p37_path = OUTPUT_DIR / "12_nvidia_nemotron_financial_eval_us_only_proof.png"

    img6.save(str(p6_path))
    img7.save(str(p7_path))
    img37.save(str(p37_path))
    print(f"  -> Saved {p6_path.name} ({p6_path.stat().st_size:,} bytes)")
    print(f"  -> Saved {p7_path.name} ({p7_path.stat().st_size:,} bytes)")
    print(f"  -> Saved {p37_path.name} ({p37_path.stat().st_size:,} bytes)")

    # Build Side-by-Side Annotated Composite for PROOF 11
    banner_h = 160
    border = 20
    canvas_w = img6.width + img7.width + (border * 3)
    canvas_h = max(img6.height, img7.height) + banner_h + (border * 2)

    composite = Image.new("RGB", (canvas_w, canvas_h), (15, 23, 42)) # dark slate
    draw = ImageDraw.Draw(composite)

    # Banner Background
    draw.rectangle([(0, 0), (canvas_w, banner_h)], fill=(30, 41, 59))
    draw.line([(0, banner_h), (canvas_w, banner_h)], fill=(59, 130, 246), width=3)

    # Fonts
    font_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 34)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
    font_meta = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)

    # Banner Text
    draw.text((border + 10, 22), "NVIDIA Nemotron 3 Ultra Technical Report — Section 2.3.5 Legal Pre-Training Datasets", fill=(56, 189, 248), font=font_title)
    draw.text((border + 10, 72), "EMPIRICAL FINDING: 100% US & Canadian Legal Data (California, NY, eCFR, Caselaw, CUAD) — ZERO Indian Law (0 IPC, 0 BNS, 0 CrPC)", fill=(248, 113, 113), font=font_sub)
    draw.text((border + 10, 112), "Candidate: Shobhit (Reg No: 26MCS0057) • Institution: VIT Vellore (MASET697) • Left: Page 6 (Section Start) | Right: Page 7 (Continuation)", fill=(148, 163, 184), font=font_meta)

    # Paste Page 6
    p6_x = border
    p6_y = banner_h + border
    composite.paste(img6, (p6_x, p6_y))

    # Paste Page 7
    p7_x = img6.width + (border * 2)
    p7_y = banner_h + border
    composite.paste(img7, (p7_x, p7_y))

    # Draw Highlight Border on Section 2.3.5 on Page 6
    hl_p6_top = 1135
    hl_p6_bot = 1605
    box_p6 = [(p6_x + 70, p6_y + hl_p6_top), (p6_x + img6.width - 70, p6_y + hl_p6_bot)]
    draw.rectangle(box_p6, outline=(239, 68, 68), width=4)
    # Badge on Page 6
    draw.rectangle([(p6_x + 80, p6_y + hl_p6_top - 32), (p6_x + 600, p6_y + hl_p6_top)], fill=(239, 68, 68))
    draw.text((p6_x + 88, p6_y + hl_p6_top - 28), "SECTION 2.3.5 (PAGE 6): 4 US LEGAL DATASETS", fill=(255, 255, 255), font=font_meta)

    # Draw Highlight Border on Page 7 (Legal datasets continuation)
    hl_p7_top = 175
    hl_p7_bot = 1575
    box_p7 = [(p7_x + 70, p7_y + hl_p7_top), (p7_x + img7.width - 70, p7_y + hl_p7_bot)]
    draw.rectangle(box_p7, outline=(239, 68, 68), width=4)
    # Badge on Page 7
    draw.rectangle([(p7_x + 80, p7_y + hl_p7_top - 32), (p7_x + 670, p7_y + hl_p7_top)], fill=(239, 68, 68))
    draw.text((p7_x + 88, p7_y + hl_p7_top - 28), "CONTINUATION (PAGE 7): 8 US & CANADIAN DATASETS", fill=(255, 255, 255), font=font_meta)

    # Save Composite as Proof 11
    proof11_path = OUTPUT_DIR / "11_nvidia_nemotron_legal_pretraining_us_only_proof.png"
    composite.save(str(proof11_path))
    print(f"  -> Saved {proof11_path.name} ({proof11_path.stat().st_size:,} bytes, {composite.size})")


if __name__ == "__main__":
    build_proofs()
