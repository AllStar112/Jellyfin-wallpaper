#!/usr/bin/env python3
import os
import glob
import json
from datetime import datetime

# Konfigurasi
CONFIG = {
    "wallpaper_dir": "wallpapers",
    "css_output": "wallpaper.css",
    "base_url": "https://raw.githubusercontent.com/AllStar112/Jellyfin-wallpaper/main/wallpapers/",
    "duration_per_image": 15,  # detik per gambar
    "fade_duration": 2,       # persentase untuk fade
    "overlay_opacity": 0.6,
    "exclude_files": [".DS_Store", "Thumbs.db"],
    "allowed_extensions": [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"]
}

def get_image_files():
    """Ambil semua file gambar dari folder wallpaper"""
    image_files = []
    
    for ext in CONFIG["allowed_extensions"]:
        # Cek kedua kemungkinan (lowercase dan uppercase)
        pattern = os.path.join(CONFIG["wallpaper_dir"], f"*{ext}")
        image_files.extend(glob.glob(pattern))
        image_files.extend(glob.glob(pattern.upper()))
    
    # Filter file yang dikecualikan
    image_files = [
        f for f in image_files 
        if os.path.basename(f) not in CONFIG["exclude_files"]
    ]
    
    # Urutkan secara alfabetis untuk konsistensi
    image_files.sort()
    
    return image_files

def generate_css_keyframes(image_files):
    """Generate CSS keyframes dari daftar gambar"""
    if not image_files:
        return "/* ❌ Tidak ada gambar ditemukan di folder wallpapers */\n"
    
    total_images = len(image_files)
    percentage_per_image = 100 / total_images
    fade_pct = CONFIG["fade_duration"]
    
    keyframes = []
    keyframes.append("@keyframes backgroundSlideshow {")
    
    for i, img_path in enumerate(image_files):
        filename = os.path.basename(img_path)
        # Encode spasi dalam URL
        encoded_filename = filename.replace(" ", "%20")
        image_url = f"{CONFIG['base_url']}{encoded_filename}"
        
        start_percent = i * percentage_per_image
        display_end = start_percent + percentage_per_image - fade_pct
        
        # Add keyframe untuk gambar ini
        keyframes.append(f"  /* Gambar {i+1}: {filename} */")
        keyframes.append(f"  {start_percent:.2f}% {{")
        keyframes.append(f"    background-image: url('{image_url}');")
        keyframes.append(f"  }}")
        
        keyframes.append(f"  {display_end:.2f}%, {start_percent + percentage_per_image - 0.01:.2f}% {{")
        keyframes.append(f"    background-image: url('{image_url}');")
        keyframes.append(f"  }}")
    
    # Loop kembali ke gambar pertama
    first_image = os.path.basename(image_files[0])
    encoded_first = first_image.replace(" ", "%20")
    keyframes.append(f"  100% {{")
    keyframes.append(f"    background-image: url('{CONFIG['base_url']}{encoded_first}');")
    keyframes.append(f"  }}")
    keyframes.append("}")
    
    return "\n".join(keyframes)

def generate_full_css(image_files):
    """Generate file CSS lengkap"""
    total_images = len(image_files)
    total_duration = total_images * CONFIG["duration_per_image"]
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    keyframes_css = generate_css_keyframes(image_files)
    
    css_content = f"""/* ============================================ */
/* JELLYFIN WALLPAPER SLIDESHOW CSS */
/* ============================================ */
/* 
 * Generated automatically by GitHub Actions
 * Repository: https://github.com/AllStar112/Jellyfin-wallpaper
 * Total images: {total_images}
 * Total duration: {total_duration} seconds
 * Generated at: {current_time}
 * 
 * HOW TO USE:
 * 1. Copy entire content of this file
 * 2. Go to Jellyfin Dashboard → General → Custom CSS
 * 3. Paste and Save
 */
 
{keyframes_css}

/* ============================================ */
/* MAIN BACKGROUND STYLING */
/* ============================================ */

.backgroundContainer {{
  /* Slideshow Animation */
  animation: backgroundSlideshow {total_duration}s infinite ease-in-out !important;
  
  /* Background Properties */
  background-size: cover !important;
  background-position: center !important;
  background-repeat: no-repeat !important;
  background-attachment: fixed !important;
  
  /* Improve Performance */
  image-rendering: -webkit-optimize-contrast;
  image-rendering: crisp-edges;
  backface-visibility: hidden;
}}

/* Dark Overlay for Better Readability */
.backgroundContainer::before {{
  content: "" !important;
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 100% !important;
  background: rgba(0, 0, 0, {CONFIG['overlay_opacity']}) !important;
  z-index: 0 !important;
}}

/* Ensure Content Stays on Top */
.mainDrawer,
.mainAnimatedPage,
.skinHeader,
.cardContent {{
  position: relative !important;
  z-index: 1 !important;
}}

/* Optional: Smooth transition for background changes */
@media (prefers-reduced-motion: no-preference) {{
  .backgroundContainer {{
    transition: background-image 1.5s ease-in-out !important;
  }}
}}

/* ============================================ */
/* RESPONSIVE ADJUSTMENTS */
/* ============================================ */

/* Mobile Devices */
@media (max-width: 768px) {{
  .backgroundContainer {{
    background-attachment: scroll !important;
    animation-duration: {total_duration * 0.7}s !important;
  }}
}}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {{
  .backgroundContainer::before {{
    background: rgba(0, 0, 0, {CONFIG['overlay_opacity'] + 0.1}) !important;
  }}
}}

/* Print Style (hide animation when printing) */
@media print {{
  .backgroundContainer {{
    animation: none !important;
  }}
}}
"""
    
    return css_content

def main():
    print("🚀 Generating Jellyfin Wallpaper CSS...")
    print(f"📁 Checking folder: {CONFIG['wallpaper_dir']}")
    
    # Cek apakah folder wallpapers ada
    if not os.path.exists(CONFIG["wallpaper_dir"]):
        print(f"❌ Folder '{CONFIG['wallpaper_dir']}' tidak ditemukan!")
        os.makedirs(CONFIG["wallpaper_dir"])
        print(f"✅ Folder '{CONFIG['wallpaper_dir']}' telah dibuat")
    
    # Ambil file gambar
    image_files = get_image_files()
    print(f"📸 Found {len(image_files)} image(s)")
    
    # Generate CSS
    css_content = generate_full_css(image_files)
    
    # Tulis ke file
    with open(CONFIG["css_output"], "w", encoding="utf-8") as f:
        f.write(css_content)
    
    print(f"✅ CSS generated: {CONFIG['css_output']}")
    print(f"⏱️  Total slideshow duration: {len(image_files) * CONFIG['duration_per_image']}s")
    
    # Tampilkan preview
    if image_files:
        print("\n📋 Image list:")
        for i, img in enumerate(image_files[:5]):  # Tampilkan 5 pertama
            print(f"  {i+1}. {os.path.basename(img)}")
        if len(image_files) > 5:
            print(f"  ... and {len(image_files) - 5} more")

if __name__ == "__main__":
    main()
