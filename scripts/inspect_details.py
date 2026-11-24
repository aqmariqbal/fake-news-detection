import pptx

prs = pptx.Presentation(r'C:\Users\KIIT\Downloads\0bbeb81d157f41dbb44b96a154bf5bfd (3).pptx')
for idx, slide in enumerate(prs.slides):
    print(f'=== SLIDE {idx+1} ===')
    for s in slide.shapes:
        if s.has_text_frame:
            for p in s.text_frame.paragraphs:
                if p.text.strip():
                    runs_info = [f"'{r.text}' (font={r.font.name}, size={r.font.size})" for r in p.runs]
                    print(f"   Shape '{s.name}': p.text='{p.text}' | runs: {runs_info}")
