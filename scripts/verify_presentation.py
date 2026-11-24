import pptx
from pathlib import Path

pptx_path = Path(r"c:\Users\KIIT\Desktop\Fake_News_Detection_Synopsis_Presentation.pptx")
print(f"File exists: {pptx_path.exists()}, Size: {pptx_path.stat().st_size:,} bytes")

prs = pptx.Presentation(str(pptx_path))
print(f"\n==========================================")
print(f"TOTAL SLIDES: {len(prs.slides)}")
print(f"==========================================")

for idx, slide in enumerate(prs.slides):
    slide_num = idx + 1
    shapes = list(slide.shapes)
    tables = [s for s in shapes if s.has_table]
    text_samples = []
    for s in shapes:
        if s.has_text_frame:
            for p in s.text_frame.paragraphs:
                t = p.text.strip().replace("\n", " ")
                if t:
                    text_samples.append(t[:60])
    
    print(f"\n--- SLIDE {slide_num:02d} (Shapes: {len(shapes)}, Tables: {len(tables)}) ---")
    if tables:
        t = tables[0].table
        print(f"   [TABLE]: {len(t.rows)} rows x {len(t.columns)} cols")
        for r_idx, r in enumerate(list(t.rows)[:2]):
            print(f"      Row {r_idx}: {[c.text.strip().replace(chr(10), ' ') for c in r.cells]}")
    for sample in text_samples[:4]:
        print(f"   [TEXT]: {sample}")
