import os
import zipfile
from pathlib import Path

def create_zip():
    project_dir = Path(r"c:\Users\KIIT\Desktop\fake-news-detection")
    zip_path = Path(r"c:\Users\KIIT\Desktop\fake-news-detection.zip")
    
    exclude_dirs = {'.git', '__pycache__', '.pytest_cache', '.ipynb_checkpoints', 'venv', '.venv', 'env', '.env', 'scratch'}
    exclude_exts = {'.pyc', '.pyo', '.pyd'}
    
    print(f"Creating zip file at: {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for root, dirs, files in os.walk(project_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                ext = Path(file).suffix.lower()
                if ext in exclude_exts or file.endswith('.tmp'):
                    continue
                
                full_path = Path(root) / file
                rel_path = full_path.relative_to(project_dir)
                
                # Exclude the zip file itself if located inside
                if full_path == zip_path:
                    continue
                
                zipf.write(full_path, arcname=str(rel_path))
                
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"Zip created successfully! Size: {size_mb:.2f} MB")

if __name__ == "__main__":
    create_zip()
