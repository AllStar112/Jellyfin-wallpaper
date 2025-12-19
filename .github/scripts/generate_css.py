#!/usr/bin/env python3
"""
JELLYFIN WALLPAPER CSS GENERATOR

"""

import os
import glob

# ========= CONFIG =========
GITHUB_USER = "AllStar112"
REPO_NAME = "Jellyfin-wallpaper"
BRANCH = "main"
WALLPAPERS_FOLDER = "wallpapers"
CSS_OUTPUT = "wallpaper.css"

DISPLAY_SECONDS = 5  # detik gambar
FADE_SECONDS = 1.5     # detik transisi
DISPLAY_RATIO = 0.75
# ==========================

def get_jsdelivr_url(filename):
    """Generate jsDelivr URL"""
    encoded = filename.replace(" ", "%20")
    return f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@{BRANCH}/{WALLPAPERS_FOLDER}/{encoded}"

def calculate_percentages(num_images):
    """
    Hitung persentase PERSIS SEPERTI TEMPLATE:
    Template untuk 3 gambar: 
    0%, 28%     (gambar 1)
    33%, 61%    (gambar 2) 
    66%, 94%    (gambar 3)
    100%        (loop ke gambar 1)
    
    Pola: 
    - Gap antar gambar: 33-28=5%, 66-61=5%
    - Range gambar: 28-0=28%, 61-33=28%, 94-66=28%
    """
    percentages = []
    
    # Untuk 3 gambar di template: 28% display, 5% gap
    # Kita sesuaikan dengan 3s display + 1s fade
    
    if num_images == 3:
        # Khusus 3 gambar, pakai angka template
        return [
            {"start": 0, "end": 28},
            {"start": 33, "end": 61},
            {"start": 66, "end": 94}
        ]
    else:
        # Untuk gambar lain, hitung otomatis
        # Total: 100% / num_images = segment per gambar
        # Display: 75% dari segment, Fade: 25% dari segment
        for i in range(num_images):
            segment = 100 / num_images
            start = i * segment
            display_end = start + (segment * DISPLAY_RATIO)  # 75% untuk display
            
            percentages.append({
                "start": round(start, 2),
                "end": round(display_end, 2)
            })
        
        return percentages

def main():
    print("🚀 Generating CSS with exact template structure...")
    
    # 1. Get semua gambar
    images = []
    for ext in ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif']:
        pattern = os.path.join(WALLPAPERS_FOLDER, f'*{ext}')
        images.extend(glob.glob(pattern))
        images.extend(glob.glob(pattern.upper()))
    
    if not images:
        print("❌ ERROR: No images in 'wallpapers/' folder!")
        # Create empty CSS file
        with open(CSS_OUTPUT, 'w') as f:
            f.write("/* No images found in wallpapers folder */")
        return
    
    # Sort dan ambil nama file
    images = sorted([os.path.basename(img) for img in images])
    num_images = len(images)
    
    print(f"📸 Found {num_images} images")
    
    # 2. Hitung persentase
    percentages = calculate_percentages(num_images)
    
    # 3. Hitung total waktu (3s + 1s per gambar)
    total_seconds = num_images * (DISPLAY_SECONDS + FADE_SECONDS)
    
    # 4. Build CSS PERSIS SEPERTI TEMPLATE
    css_lines = []
    
    # HEADER - PERSIS
    css_lines.append("/* Background Slideshow untuk .backgroundContainer */")
    css_lines.append("@keyframes backgroundSlideshow {")
    
    # KEYFRAMES - FORMAT PERSIS: "X%, Y% { background-image: url(...); }"
    for i, (img, pct) in enumerate(zip(images, percentages)):
        url = get_jsdelivr_url(img)
        
        # Format PERSIS: "X%, Y% {"
        css_lines.append(f"  {pct['start']:.2f}%, {pct['end']:.2f}% {{")
        css_lines.append(f"    background-image: url('{url}');")
        css_lines.append(f"  }}")
    
    # AKHIR - LOOP KE GAMBAR PERTAMA (PERSIS seperti baris 100%)
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
    
    # 5. Save to file
    with open(CSS_OUTPUT, 'w', encoding='utf-8') as f:
        f.write("\n".join(css_lines))

    total_per_image = DISPLAY_SECONDS + FADE_SECONDS
    print(f"✅ CSS generated: {CSS_OUTPUT}")
    print(f"⏱️  Total duration: {total_seconds}s ({num_images} gambar × {total_per_image}s)")
    
    # Show timing
    print(f"\n📊 Timing (PERSIS seperti template):")
    for i, (img, pct) in enumerate(zip(images, percentages)):
        print(f"  Gambar {i+1}: {pct['start']:.2f}%, {pct['end']:.2f}% → {img}")
    
    return True

if __name__ == "__main__":
    main()
