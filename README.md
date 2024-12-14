# Quran-Shorts-Media-Preparation

This repository showcases my workflow to automate the preparation of media files for my Quran shorts on <https://www.youtube.com/@islamic-vibes-33/shorts>

## Dependencies

Before running the scripts, ensure you have the following dependencies installed:

- Python 3.x
- `requests`
- `Pillow`
- `beautifulsoup4`
- `python-dotenv`
- `tabulate`
- `inkscape`

You can install the required Python libraries using pip:

```sh
pip install requests Pillow beautifulsoup4 python-dotenv tabulate
```

Inkscape is a standalone application and needs to be installed separately. You can download and install it from the [Inkscape website](https://inkscape.org).

## Preparing prerequisite media - required for initial setup only

Before we run `main.py`, we need to have the images locally on our machine for the script to run correctly.

### 1. Download all ayats of every surah

- Open <https://everyayah.com/data/quranpngs/>, download the `000_images.zip` file and extract the data
- Open `main.py`, navigate to `invert_image` function and set the correct path to the extracted folder

### 2. Download calligraphy styling of every surah

- Open `prepare_surah_calligraphy.py` and adjust the output directory where the images will be saved

### 3. Preparing Pexels API key

Pexels is a platform that contains free high quality images and videos shared by creators.

- Create an account on <https://www.pexels.com/join-consumer/>
- Request an API key from <https://www.pexels.com/api/new/> and use it in your code
- Make sure to set the download directory to your desired location

Read [Pexels' API documentaion](https://www.pexels.com/api/documentation/) if needed.

## Running `main.py`

Once the above steps were completed, you are set to save time by automatically generating media files for Quran videos.
Don't forget to edit all the paths in the file.
