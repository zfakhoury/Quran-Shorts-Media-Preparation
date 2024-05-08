# Python script explaining how the images of the surah calligraphy 
# folder in the repository were made

import os, subprocess, requests
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def download_surah_calligraphy():
    url = 'https://quranonline.net'
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all PNG links
    png_links = soup.find_all('img', {'src': lambda x: x.endswith('.svg')})

    # Directory to save the PNG files
    output_directory = '/Users/m3evo/YT Media/Surah Calligraphy'
    os.makedirs(output_directory, exist_ok=True)

    # Download each PNG file
    for link in png_links:
        # Get the absolute URL of the PNG file
        abs_url = urljoin(url, link['src'])
        
        # Extract the filename from the URL
        filename = abs_url.split('/')[-1]
        
        # Download the PNG file
        with open(os.path.join(output_directory, filename), 'wb') as f:
            f.write(requests.get(abs_url).content)
            print(f"Downloaded: {filename}")


def svg_to_png():
    # Directory containing SVG files
    svg_directory = '/Users/m3evo/YT Media/Surah Calligraphy'

    # Directory to save PNG files
    output_directory = '/Users/m3evo/YT Media/Surah Calligraphy'
    os.makedirs(output_directory, exist_ok=True)

    # Convert SVG files to PNG
    for filename in os.listdir(svg_directory):
        if filename.endswith('.svg'):
            svg_path = os.path.join(svg_directory, filename)
            png_path = os.path.join(output_directory, filename[:-4] + '.png')  # Change extension to PNG
            
            # Use inkscape to convert SVG to PNG
            subprocess.run(['inkscape', svg_path, '--export-type=png', '--export-filename=' + png_path, '--export-width=1600', '--export-height=1000'])
            
            print(f"Converted: {filename}")


def remove_background():
    png_directory = '/Users/m3evo/YT Media/Surah Calligraphy'
    output_directory = '/Users/m3evo/YT Media/Surah Calligraphy'

    for filename in os.listdir(png_directory):
        if filename.endswith('.png'):
            png_path = os.path.join(png_directory, filename)
            png_no_bg_path = os.path.join(output_directory, filename)
            
            png_image = Image.open(png_path)
            png_image = png_image.convert("RGBA")
            datas = png_image.getdata()
            
            # Create new pixel data with transparent background
            new_data = []
            for item in datas:
                # Keep white pixels (adjust tolerance as needed)
                if item[0] > 240 and item[1] > 240 and item[2] > 240:
                    new_data.append(item)
                else:
                    new_data.append((255, 255, 255, 0))  # Make non-white pixels transparent
            
            # Update image with new pixel data
            png_image.putdata(new_data)
            
            # Save image with transparent background
            png_image.save(png_no_bg_path, "PNG")
            
            print(f"Processed: {filename}")


download_surah_calligraphy()
svg_to_png()
remove_background()
