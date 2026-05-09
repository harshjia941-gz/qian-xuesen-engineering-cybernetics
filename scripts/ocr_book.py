#!/usr/bin/env python3
"""OCR for 工程控制论 1100-page scanned PDF using tesseract chi_sim"""

import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
import sys

PDF_PATH = "/Users/harshai/Documents/qian-xuesen-engineering-cybernetics/sources/工程控制论-上、下-钱学森-宋健.pdf"
OUTPUT_DIR = Path("/Users/harshai/Documents/qian-xuesen-engineering-cybernetics/book-ocr")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Convert PDF to images in batches of 50 pages
BATCH_SIZE = 50
START_PAGE = 1
END_PAGE = 1100  # or adjust

for batch_start in range(START_PAGE, END_PAGE + 1, BATCH_SIZE):
    batch_end = min(batch_start + BATCH_SIZE - 1, END_PAGE)
    batch_label = f"pages_{batch_start:04d}-{batch_end:04d}"
    output_file = OUTPUT_DIR / f"{batch_label}.txt"
    
    # Skip if already done
    if output_file.exists() and output_file.stat().st_size > 0:
        print(f"[SKIP] {batch_label} — already exists")
        continue
    
    print(f"[OCR] {batch_label} — converting {batch_start}-{batch_end}...", flush=True)
    
    try:
        images = convert_from_path(
            PDF_PATH, 
            first_page=batch_start, 
            last_page=batch_end,
            dpi=300,
            thread_count=2
        )
    except Exception as e:
        print(f"[ERROR] PDF conversion failed for {batch_label}: {e}", flush=True)
        continue
    
    texts = []
    for i, img in enumerate(images):
        page_num = batch_start + i
        try:
            text = pytesseract.image_to_string(
                img, lang='chi_sim', config='--psm 6'
            )
            texts.append(f"=== PAGE {page_num} ===\n{text}\n")
        except Exception as e:
            print(f"  [WARN] Page {page_num}: {e}", flush=True)
            texts.append(f"=== PAGE {page_num} ===\n[OCR FAILED: {e}]\n")
    
    full_text = "\n".join(texts)
    output_file.write_text(full_text, encoding='utf-8')
    print(f"[DONE] {batch_label} — {len(full_text)} chars", flush=True)

print(f"\n[DONE] All pages OCR'd. Output in {OUTPUT_DIR}")
