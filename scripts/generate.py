import os
import glob

# ========================
# KONFIGURASI
# ========================
GITHUB_USERNAME = 'AllStar112'
GITHUB_REPO = 'Jellyfin-wallpaper'
wallpaper_dir = 'wallpapers'
output_file = 'generated/wallpapers.css'

# ========================
# CARI SEMUA FILE GAMBAR
# ========================
image_extensions = ('*.jpg', '*.jpeg', '*.png', '*.webp', '*.gif')
image_files = []

for ext in image_extensions:
    image_files.extend(glob.glob(os.path.join(wallpaper_dir, ext)))

# Urutkan berdasarkan nama
image_files.sort()
image_files = [f for f in image_files if os.path.isfile(f)]

print(f"🔍 Found {len(image_files)} wallpaper files")

# ========================
# HITUNG DURASI
# ========================
if not image_files:
    print("❌ No image files found!")
    css = """.backgroundContainer {
    background-color: #000 !important;
    background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                     url('https://raw.githubusercontent.com/AllStar112/Jellyfin-wallpaper/main/Zero_Two_noDark.gif') !important;
    background-size: cover !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
    background-position: center center !important;
}"""
else:
    # 3 detik tampil + 1 detik transisi = 4 detik per foto
    total_seconds = len(image_files) * 4
    percent_per_image = 100 / len(image_files)
    
    # ========================
    # BUAT CSS
    # ========================
    css = f""".backgroundContainer,
.layout-desktop .backgroundContainer,
.layout-tv .backgroundContainer,
#loginPage .backgroundContainer {{
    background-color: #000 !important;
    background-size: cover !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
    background-position: center center !important;
    
    /* {len(image_files)} wallpapers × 4 seconds = {total_seconds}s */
    animation: slideshow {total_seconds}s infinite !important;
    animation-timing-function: ease-in-out !important;
}}

@keyframes slideshow {{
"""
    
    # ========================
    # GENERATE KEYFRAMES
    # ========================
    for i, image_file in enumerate(image_files):
        filename = os.path.basename(image_file)
        url = f'https://cdn.jsdelivr.net/gh/{GITHUB_USERNAME}/{GITHUB_REPO}/wallpapers/{filename}'
        
        start_percent = i * percent_per_image
        display_end = start_percent + (percent_per_image * 0.75)
        
        # FASE TAMPIL (3 detik)
        css += f"""
    /* {filename} */
    {start_percent:.2f}%, {display_end:.2f}% {{
        background-image: 
            linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
            url('{url}') !important;
    }}
    """
        
        # FASE TRANSISI (1 detik)
        if i < len(image_files) - 1:
            next_file = os.path.basename(image_files[i + 1])
            next_url = f'https://cdn.jsdelivr.net/gh/{GITHUB_USERNAME}/{GITHUB_REPO}/wallpapers/{next_file}'
            
            css += f"""
    /* Transition: {filename} → {next_file} */
    {display_end:.2f}%, {start_percent + percent_per_image:.2f}% {{
        background-image: 
            linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
            url('{next_url}'),
            linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
            url('{url}') !important;
    }}
    """
        else:
            # Loop: foto terakhir ke foto pertama
            first_file = os.path.basename(image_files[0])
            first_url = f'https://cdn.jsdelivr.net/gh/{GITHUB_USERNAME}/{GITHUB_REPO}/wallpapers/{first_file}'
            
            css += f"""
    /* Loop: {filename} → {first_file} */
    {display_end:.2f}%, 100% {{
        background-image: 
            linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
            url('{first_url}'),
            linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
            url('{url}') !important;
    }}
    """
    
    css += "\n}"

# ========================
# SIMPAN FILE
# ========================
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(css)

print(f"✅ Generated CSS to: {output_file}")
print(f"📊 Total wallpapers: {len(image_files)}")
print(f"⏱️  Animation: {len(image_files)*4} seconds total")
print(f"🌐 CSS URL: https://cdn.jsdelivr.net/gh/{GITHUB_USERNAME}/{GITHUB_REPO}/generated/wallpapers.css")
