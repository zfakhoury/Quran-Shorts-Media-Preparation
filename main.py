import random, os, shutil, json, requests, subprocess
from dotenv import load_dotenv
from PIL import Image, ImageOps
from tabulate import tabulate
from quran_reciter_data import reciters, ayat_count

load_dotenv()

def download_audio(reciter_id, surah_number, ayah_number):
    # Load recitation data from recitation.js
    with open('/Users/m3evo/Development/Python/Quran-Shorts-Media-Preparation/recitations.json', 'r', encoding='utf-8') as file:
        recitation_data = file.read()

    # Parse JSON data
    recitation_data = recitation_data[recitation_data.index('{'):recitation_data.rindex('}') + 1]
    recitation_data = json.loads(recitation_data)

    # Construct URL for the audio file
    reciter_info = recitation_data[str(reciter_id)]
    subfolder = reciter_info['subfolder']
    filename = f"{surah_number:03d}{ayah_number:03d}.mp3"
    url = f"https://www.everyayah.com/data/{subfolder}/{filename}"

    # Download the audio file
    response = requests.get(url)
    if response.status_code == 200:
        # Save the audio file
        file_path = os.path.join("/Users/m3evo/YT Media/Temp Media/", filename)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"{filename}")
    else:
        print(f"Audio {response.status_code}")


def invert_image(surat, ayat):
    image = Image.open(f"/Users/m3evo/YT Media/Ayats/{surat}_{ayat}.png").convert('RGBA')
    r, g, b, a = image.split()
    r, g, b = map(ImageOps.invert, (r, g, b))
    inverted_image = Image.merge(image.mode, (r, g, b, a))
    inverted_image.save(f"/Users/m3evo/YT Media/Temp Media/{surat}_{ayat}.png", 'PNG')
    print(f"{surat}_{ayat}.png")


def download_pexels_video():
    random_page = random.randint(1, 10)  # Assuming there are 10 pages
    url = f"https://api.pexels.com/videos/search?query=landscape&page={random_page}"

    headers = {
        'Authorization': os.environ['PEXELS_TOKEN']
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    videos = data.get('videos', [])
    if videos:
        selected_video = random.choice(videos)
        download_link = selected_video['video_files'][0]['link']
        
        folder_path = "/Users/m3evo/YT Media/Temp Media/"
        video_path = os.path.join(folder_path, f"{selected_video['id']}.mp4")

        # Download the video
        with open(video_path, 'wb') as video_file:
            video_file.write(requests.get(download_link).content)
            print(f"Background video: {selected_video['id']}.mp4")
    else:
        print("No videos found on this page.")


def surat_calligraphy(surat):
    if 1 < surat < 9:
        surat = f'00{surat}'
    elif 10 < surat < 99:
        surat = f'0{surat}'
    
    folder_path = "/Users/m3evo/YT Media/Surah Calligraphy/"
    calligraphy = f"{surat}.png"

    return folder_path + calligraphy, calligraphy


def valid_interval(surat, first_ayat, last_ayat, reciter_id):
    state = False
    if str(reciter_id) in reciters:
        if 1 <= surat <= 114:
            if 1 <= first_ayat <= ayat_count[surat-1] and 1 <= last_ayat <= ayat_count[surat-1]:
                state = True
    return state


def construct_reciters_table():
    num_cols = 3
    num_rows = -(-len(reciters) // num_cols)  # Equivalent to ceil(len(data) / num_cols)

    table_data = [[] for _ in range(num_rows)]
    for idx, (key, value) in enumerate(reciters.items()):
        table_data[idx % num_rows].extend([key, value])

    headers = ["ID", "Reciter"] * num_cols
    print(f'{tabulate(table_data, headers=headers, tablefmt="grid")}\n')


construct_reciters_table()
reciter_id = int(input("Reciter ID: "))
surat = int(input("Surat: "))
first_ayat = int(input("First ayat: "))
last_ayat = int(input("Last ayat: "))

if valid_interval(surat, first_ayat, last_ayat, reciter_id):
    for i in range(0, last_ayat - first_ayat + 1):
        print("")
        invert_image(surat, first_ayat + i)
        download_audio(reciter_id, surat, first_ayat + i)

    download_pexels_video()
    calligraphy_path, calligraphy = surat_calligraphy(surat)
    shutil.copyfile(calligraphy_path, f"/Users/m3evo/YT Media/Temp Media/{calligraphy}")
    subprocess.run(['open', "/Users/m3evo/YT Media/Temp Media/"])

else:
    print('Incorrect input.')
