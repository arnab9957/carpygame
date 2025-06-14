import os
import urllib.request
import sys

def download_font():
    """Download the Orbitron font for the car game"""
    # Using Google Fonts API to download Orbitron Bold
    font_url = "https://fonts.gstatic.com/s/orbitron/v29/yMJMMIlzdpvBhQQL_SC3X9yhF25-T1nyGy6BoWgz.ttf"
    font_dir = "fonts"
    font_path = os.path.join(font_dir, "Orbitron-Bold.ttf")
    
    # Create fonts directory if it doesn't exist
    if not os.path.exists(font_dir):
        os.makedirs(font_dir)
    
    # Download the font
    try:
        print(f"Downloading Orbitron font to {font_path}...")
        urllib.request.urlretrieve(font_url, font_path)
        print("Font downloaded successfully!")
        return True
    except Exception as e:
        print(f"Error downloading font: {e}")
        
        # Try alternative URL
        try:
            alt_font_url = "https://fonts.gstatic.com/s/orbitron/v25/yMJMMIlzdpvBhQQL_SC3X9yhF25-T1nyGy6BoWgz.ttf"
            print("Trying alternative URL...")
            urllib.request.urlretrieve(alt_font_url, font_path)
            print("Font downloaded successfully with alternative URL!")
            return True
        except Exception as e2:
            print(f"Error downloading from alternative URL: {e2}")
            return False

if __name__ == "__main__":
    download_font()
