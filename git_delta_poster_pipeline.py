"""
RAJBARI RANNA - AUTOMATED GIT DELTA & AI MENU POSTER PIPELINE


"""
import os
import sys
import time
import subprocess
from PIL import Image, ImageDraw

# 1. Ensure output directory exists immediately
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCREENSHOT_PATH = os.path.join(OUTPUT_DIR, "rajbari_snapshot.png")
POSTER_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "cloud_kitchen_promo_poster.jpg")

# 2. Extract Git Delta Safely (Detects new dishes & coupons added in commits)
def get_git_delta() -> dict:
    try:
        commit_msg = subprocess.check_output(["git", "log", "-1", "--pretty=%B"], text=True).strip()
        diff_summary = subprocess.check_output(["git", "diff", "-U0", "HEAD~1", "HEAD"], text=True).strip()
        added_lines = [
            line[1:].strip() for line in diff_summary.split("\n") 
            if line.startswith("+") and not line.startswith("+++") and len(line.strip()) > 3
        ]
        if not added_lines:
            added_lines = [
                "Shorshe Ilish (Hilsa in Mustard Gravy - ₹449)",
                "Kosha Mangsho (Slow-braised Mutton - ₹399)",
                "Chingri Malai Curry (Prawns in Coconut Milk - ₹479)",
                "Use Coupon GHORE20 for 20% OFF on First Order"
            ]
        return {"commit_message": commit_msg, "added_features": added_lines[:5]}
    except Exception as e:
        print(f"[!] Git Delta notice: {e}")
        return {
            "commit_message": "New Bhoj Update: Shorshe Ilish & Kosha Mangsho Launch",
            "added_features": [
                "Shorshe Ilish (Hilsa in Mustard Gravy - ₹449)",
                "Kosha Mangsho (Slow-braised Mutton - ₹399)",
                "Chingri Malai Curry (Prawns in Coconut Milk - ₹479)",
                "Use Coupon GHORE20 for 20% OFF on First Order"
            ]
        }

# 3. Capture Snapshot Safely
def capture_snapshot(save_path: str = SCREENSHOT_PATH):
    print("[*] Capturing Rajbari Ranna website snapshot...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=options)
        driver.get("http://localhost:8000")
        time.sleep(3)  # Wait for Rajbari Ranna loader to finish
        driver.save_screenshot(save_path)
        driver.quit()
        print(f"[+] Snapshot saved: {save_path}")
    except Exception as e:
        print(f"[!] Headless Chrome notice: {e}. Generating fallback canvas...")
        img = Image.new("RGB", (1920, 1080), color=(155, 28, 49))  # Vermillion Maroon #9B1C31
        draw = ImageDraw.Draw(img)
        draw.rectangle([(50, 50), (1870, 1030)], outline=(212, 160, 23), width=4)  # Mustard Gold #D4A017
        draw.text((960, 540), "RAJBARI RANNA - AUTHENTIC BENGALI CLOUD KITCHEN", fill=(248, 244, 233), anchor="mm")
        img.save(save_path)
        print(f"[+] Fallback snapshot saved: {save_path}")

# 4. Synthesize Poster Artwork (Rajbari Ranna Authentic Royal Bengali Theme)
def render_poster(delta_info: dict, output_path: str = POSTER_OUTPUT_PATH):
    print("[*] Compositing Rajbari Ranna promotional poster...")
    width, height = 1080, 1350
    poster = Image.new("RGB", (width, height), color=(155, 28, 49))  # Vermillion Maroon #9B1C31
    draw = ImageDraw.Draw(poster)
    
    # Royal Bengali Gold & Cream Accents (Mustard Gold #D4A017, Cream #F8F4E9)
    draw.rectangle([(24, 24), (1056, 1326)], outline=(212, 160, 23), width=3)
    draw.rectangle([(36, 36), (1044, 1314)], outline=(248, 244, 233), width=1)
    
    draw.text((540, 95), "R A J B A R I   R A N N A", fill=(248, 244, 233), anchor="mm")
    draw.text((540, 140), "AUTHENTIC BENGALI CLOUD KITCHEN • TODAY'S SPECIAL BHOJ", fill=(212, 160, 23), anchor="mm")
    
    # Feature Box Container
    draw.rectangle([(70, 180), (1010, 1090)], fill=(248, 244, 233), outline=(212, 160, 23), width=2)
    draw.rectangle([(70, 180), (1010, 260)], fill=(155, 28, 49))
    draw.text((540, 220), "SUCHETAMON27 / CLOUD-KITCHEN", fill=(248, 244, 233), anchor="mm")
    
    draw.text((540, 310), f"UPDATE: {delta_info['commit_message'][:45]}", fill=(43, 24, 16), anchor="mm")
    
    # Embed Snapshot Thumbnail
    if os.path.exists(SCREENSHOT_PATH):
        try:
            thumb = Image.open(SCREENSHOT_PATH).resize((860, 360))
            poster.paste(thumb, (110, 360))
        except Exception:
            pass
            
    # Added Menu Items Bullet List
    draw.rectangle([(110, 740), (970, 1050)], fill=(255, 253, 247), outline=(212, 160, 23), width=1)
    draw.text((540, 775), "✨ TODAY'S SPECIAL BHOJ & NEW DISHES ✨", fill=(155, 28, 49), anchor="mm")
    
    features_list = "\n\n".join([f"• {feat[:65]}" for feat in delta_info['added_features'][:4]])
    draw.multiline_text((540, 920), features_list, fill=(43, 24, 16), align="center", anchor="mm", spacing=10)
    
    # Footer CTA Bar
    draw.rectangle([(70, 1140), (1010, 1230)], fill=(212, 160, 23))
    draw.text((540, 1185), "ORDER FRESH NOW ON SWIGGY, ZOMATO & WHATSAPP (+91 98765 43210)", fill=(43, 24, 16), anchor="mm")
    
    poster.save(output_path, quality=95)
    print(f"[+] Rajbari Ranna poster artwork synthesized successfully: {output_path}")

if __name__ == "__main__":
    capture_snapshot()
    delta = get_git_delta()
    render_poster(delta)
