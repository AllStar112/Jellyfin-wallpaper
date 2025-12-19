#!/usr/bin/env python3
import os
import glob
from datetime import datetime

# ========== KONFIGURASI ==========
REPO_OWNER = "AllStar112"
REPO_NAME = "Jellyfin-wallpaper"
BRANCH = "main"
# =================================

def generate_jsdelivr_url(filename):
    """Generate jsDelivr URL dari filename"""
    # Format: https://cdn.jsdelivr.net/gh/user/repo@branch/path
    encoded_name = filename.replace(" ", "%20")
    return f"https://cdn.jsdelivr.net/gh/{REPO_OWNER}/{REPO_NAME}@{BRANCH}/wallpapers/{encoded_name}"

def main():
    print("🔍 Scanning wallpapers folder...")
    
    # Cari semua file gambar
    image_extensions = ['jpg', 'jpeg', 'png', 'webp', 'bmp', 'gif', 'JPG', 'JPEG', 'PNG']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(f"wallpapers/*.{ext}"))
    
    if not image_files:
        print("⚠️ No images found! Creating placeholder CSS...")
        css_content = "/* No wallpapers found in wallpapers/ folder */"
    else:
        image_files.sort()
        total_images = len(image_files)
        
        print(f"📸 Found {total_images} images:")
        for img in image_files:
            print(f"  → {os.path.basename(img)}")
        
        # ========== GENERATE CSS ==========
        # 1. Keyframes
        keyframes = ["@keyframes backgroundSlideshow {"]
        
        for i, img_path in enumerate(image_files):
            filename = os.path.basename(img_path)
            url = generate_jsdelivr_url(filename)
            
            # Hitung persentase
            total_percent = 100
            fade_time = 2  # 2% untuk fade effect
            
            # Start position untuk gambar ini
            start_pct = (i / total_images) * total_percent
            # End position (sebelum fade ke gambar berikutnya)
            end_pct = ((i + 1) / total_images) * total_percent - fade_time
            
            # Keyframe untuk fade in
            keyframes.append(f"  {start_pct:.2f}% {{ background-image: url('{url}'); }}")
            # Keyframe untuk tampil penuh
            keyframes.append(f"  {end_pct:.2f}% {{ background-image: url('{url}'); }}")
        
        # Loop kembali ke gambar pertama
        first_url = generate_jsdelivr_url(os.path.basename(image_files[0]))
        keyframes.append(f"  100% {{ background-image: url('{first_url}'); }}")
        keyframes.append("}")
        
        # 2. Durasi animasi
        duration_per_image = 15  # detik
        total_duration = total_images * duration_per_image
        
        # 3. Gabungkan semua
        keyframes_css = "\n".join(keyframes)
        
        css_content = f"""/* ============================================ */
/* JELLYFIN WALLPAPER SLIDESHOW - AUTO GENERATED */
/* ============================================ */
/* Repo: https://github.com/{REPO_OWNER}/{REPO_NAME} */
/* Images: {total_images} • Duration: {total_duration}s */
/* Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} */
/* ============================================ */

{keyframes_css}

/* MAIN STYLES */
.backgroundContainer {{
  animation: backgroundSlideshow {total_duration}s infinite ease-in-out !important;
  background-size: cover !important;
  background-position: center !important;
  background-repeat: no-repeat !important;
  background-attachment: fixed !important;
}}

/* Overlay */
.backgroundContainer::before {{
  content: "" !important;
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 100% !important;
  background: rgba(0, 0, 0, 0.6) !important;
  z-index: 0 !important;
}}

/* Mobile */
@media (max-width: 768px) {{
  .backgroundContainer {{
    background-attachment: scroll !important;
    animation-duration: {total_duration * 0.7}s !important;
  }}
}}
"""
    
    # Tulis ke file
    with open("wallpaper.css", "w", encoding="utf-8") as f:
        f.write(css_content)
    
    print(f"✅ wallpaper.css generated with {total_images if image_files else 0} images")

if __name__ == "__main__":
    main()
