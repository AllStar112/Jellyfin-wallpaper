#!/usr/bin/env python3
"""
JELLYFIN WALLPAPER CSS GENERATOR
Generate CSS dengan format PERSIS seperti template
3 detik gambar + 1 detik transisi
"""

import os
import glob

# ========= CONFIG =========
REPO_OWNER = "AllStar112"
REPO_NAME = "Jellyfin-wallpaper"
BRANCH = "main"
WALLPAPER_DIR = "wallpapers"
CSS_OUTPUT = "wallpaper.css"

# TIMING: 3 detik gambar, 1 detik transisi
DISPLAY_SECONDS = 3  # Waktu gambar full tampil
FADE_SECONDS = 1     # Waktu transisi ke gambar berikutnya
# ==========================

def get_jsdelivr_url(filename):
    """Generate jsDelivr URL untuk gambar"""
    encoded_name = filename.replace(" ", "%20")
    return f"https://cdn.jsdelivr.net/gh/{REPO_OWNER}/{REPO_NAME}@{BRANCH}/{WALLPAPER_DIR}/{encoded_name}"

def calculate_percentages(num_images):
    """
    Hitung persentase dengan format PERSIS seperti template:
    - Format: X%, Y% { ... }  (dua persentase, sama seperti contoh)
    - Contoh di template: 0%, 28% { ... } dan 33%, 61% { ... }
    """
    percentages = []
    
    # Total waktu per gambar (tampil + transisi)
    total_per_image = DISPLAY_SECONDS + FADE_SECONDS
    
    for i in range(num_images):
        # Start persentase untuk gambar ini
        start_pct = (i * total_per_image * 100) / (num_images * total_per_image)
        
        # Akhir dari display time (sebelum fade out)
        display_end_pct = start_pct + (DISPLAY_SECONDS * 100) / (num_images * total_per_image)
        
        # Format PERSIS seperti template: "start_pct%, display_end_pct%"
        percentages.append({
            'start': round(start_pct, 2),
            'display_end': round(display_end_pct, 2),
            'display_range': f"{start_pct:.2f}%, {display_end_pct:.2f}%"
        })
    
    return percentages

def main():
    print("🔄 Generating CSS dengan format template...")
    
    # 1. Get semua gambar
    images = []
    for ext in ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif']:
        pattern = os.path.join(WALLPAPER_DIR, f'*{ext}')
        images.extend(glob.glob(pattern))
        images.extend(glob.glob(pattern.upper()))
    
    if not images:
        print("❌ ERROR: Tidak ada gambar di folder 'wallpapers/'")
        return
    
    # Sort dan ambil nama file saja
    images = sorted([os.path.basename(img) for img in images])
    num_images = len(images)
    
    print(f"📸 Found {num_images} images: {', '.join(images)}")
    
    # 2. Hitung persentase PERSIS seperti template
    percentages = calculate_percentages(num_images)
    
    # 3. Hitung total waktu animasi
    total_seconds = num_images * (DISPLAY_SECONDS + FADE_SECONDS)
    
    # 4. Build CSS PERSIS seperti template
    css_lines = []
    
    # HEADER - PERSIS
    css_lines.append("/* Background Slideshow untuk .backgroundContainer */")
    css_lines.append("@keyframes backgroundSlideshow {")
    
    # KEYFRAMES - FORMAT PERSIS SEPERTI TEMPLATE
    for i, img in enumerate(images):
        url = get_jsdelivr_url(img)
        pct = percentages[i]
        
        # Format: "X%, Y% { background-image: url(...); }"
        css_lines.append(f"  {pct['display_range']} {{")
        css_lines.append(f"    background-image: url('{url}');")
        css_lines.append(f"  }}")
    
    # AKHIR - LOOP KE GAMBAR PERTAMA (PERSIS seperti baris 100% di template)
    first_url = get_jsdelivr_url(images[0])
    css_lines.append(f"  100% {{")
    css_lines.append(f"    background-image: url('{first_url}');")
    css_lines.append(f"  }}")
    
    css_lines.append("}")
    css_lines.append("")
    
    # BACKGROUND CONTAINER - PERSIS SEPERTI TEMPLATE
    css_lines.append("/* Hanya terapkan ke .backgroundContainer */")
    css_lines.append(".backgroundContainer {")
    css_lines.append(f"  animation: backgroundSlideshow {total_seconds}s infinite ease-in-out !important;")
    css_lines.append("  background-size: cover !important;")
    css_lines.append("  background-position: center !important;")
    css_lines.append("  background-repeat: no-repeat !important;")
    css_lines.append("  background-attachment: fixed !important;")
    css_lines.append(f"  transition: background-image {FADE_SECONDS}s ease-in-out !important;")  # 1s transisi
    css_lines.append("}")
    css_lines.append("")
    
    # OVERLAY - PERSIS SEPERTI TEMPLATE
    css_lines.append("/* Efek overlay agar konten tetap terbaca */")
    css_lines.append(".backgroundContainer::before {")
    css_lines.append('  content: "" !important;')
    css_lines.append("  position: absolute !important;")
    css_lines.append("  top: 0 !important;")
    css_lines.append("  left: 0 !important;")
    css_lines.append("  width: 100% !important;")
    css_lines.append("  height: 100% !important;")
    css_lines.append("  background: rgba(0, 0, 0, 0.6) !important;")
    css_lines.append("  z-index: 0 !important;")
    css_lines.append("}")
    
    # 5. Write to file
    with open(CSS_OUTPUT, 'w', encoding='utf-8') as f:
        f.write("\n".join(css_lines))
    
    print(f"✅ CSS generated: {CSS_OUTPUT}")
    print(f"⏱️  Total duration: {total_seconds}s ({num_images} gambar × {DISPLAY_SECONDS+1}s)")
    
    # Show timing details
    print(f"\n📊 Timing details:")
    for i, (img, pct) in enumerate(zip(images, percentages)):
        print(f"  Gambar {i+1} ({img}): {pct['display_range']}")
    
    return True

if __name__ == "__main__":
    main()
