import pptx

prs = pptx.Presentation(r'C:\Users\KIIT\Downloads\0bbeb81d157f41dbb44b96a154bf5bfd (3).pptx')
s2 = prs.slides[1]
for sh in s2.shapes:
    print(f"Shape: '{sh.name}' ({sh.shape_type}) L={sh.left.inches:.2f}, T={sh.top.inches:.2f}, W={sh.width.inches:.2f}, H={sh.height.inches:.2f}")
    if sh.has_text_frame:
        for p in sh.text_frame.paragraphs:
            print(f"   p: '{p.text}'")
            for r in p.runs:
                print(f"      run: '{r.text}', font={r.font.name}, size={r.font.size}")
    if sh.has_table:
        t = sh.table
        print(f"   Table: {len(t.rows)} rows x {len(t.columns)} cols")
        for r_idx, r in enumerate(t.rows):
            print(f"      row {r_idx}: {[c.text for c in r.cells]}")
