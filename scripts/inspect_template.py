import pptx
from pptx.util import Inches, Pt

prs = pptx.Presentation(r'C:\Users\KIIT\Downloads\0bbeb81d157f41dbb44b96a154bf5bfd (3).pptx')
print(f"Slide dimensions: {prs.slide_width.inches:.3f} x {prs.slide_height.inches:.3f} inches")

for i, slide in enumerate(prs.slides):
    print(f"\n==========================================")
    print(f"SLIDE {i+1} (shapes: {len(slide.shapes)})")
    print(f"==========================================")
    for s in slide.shapes:
        left = s.left.inches if s.left is not None else 0
        top = s.top.inches if s.top is not None else 0
        width = s.width.inches if s.width is not None else 0
        height = s.height.inches if s.height is not None else 0
        print(f"Shape: '{s.name}' | Type: {s.shape_type} | Bounds: L={left:.2f}, T={top:.2f}, W={width:.2f}, H={height:.2f}")
        if s.has_text_frame:
            for p_idx, p in enumerate(s.text_frame.paragraphs):
                p_text = p.text.strip()
                if p_text:
                    print(f"   P[{p_idx}]: '{p_text}'")
        if s.has_table:
            t = s.table
            print(f"   Table ({len(t.rows)}x{len(t.columns)}):")
            for r_idx, r in enumerate(t.rows):
                row_txt = [c.text.strip() for c in r.cells]
                print(f"     Row {r_idx}: {row_txt}")
