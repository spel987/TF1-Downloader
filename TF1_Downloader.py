from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from xml.etree.ElementTree import fromstring
from json import load, dump
from os import system, path
from wget import download
from subprocess import Popen, DEVNULL
from requests import get
from colorama import Fore
from re import sub

system("title " + "TF1 Downloader")

def ascii_print():
    system("cls")
    print(f"""{Fore.LIGHTCYAN_EX} ___________ __   ______                    _                 _           
|_   _|  ___/  |  |  _  \                  | |               | |          
  | | | |_  `| |  | | | |_____      ___ __ | | ___   __ _  __| | ___ _ __ 
  | | |  _|  | |  | | | / _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
  | | | |   _| |_ | |/ / (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
  \_/ \_|   \___/ |___/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|{Fore.RESET}""")
    print("\r\n                  ~ https://github.com/Nathoune987")

def delete_temp_files():
    Popen("cd assets/dl_temp && del * /S /Q", shell=True, stdout=DEVNULL)

def click_when_available(css_selector):
   while True:
    try:
        driver.find_element(By.CSS_SELECTOR, css_selector).click()
        break
    except:
        pass

def complete_when_available(css_selector, text):
   while True:
    try:
        to_complete = driver.find_element(By.CSS_SELECTOR, css_selector)
        to_complete.send_keys(text)
        break
    except:
        pass

def download_all_segment(content_url, type):
   global total_segment_number
   segment_number = 1
   while True:
    try:
        download(f"{content_url}-{segment_number}.m4s?m", f"assets/dl_temp/{type}_{segment_number}.m4s")
        segment_number += 1
    except:
        total_segment_number = segment_number-1
        break 

def ask_firefox_path():
    global firefox_path
    firefox_path_file = open('assets/firefox_path.json', 'r', encoding='utf-8')
    firefox_path = load(firefox_path_file)

    if not firefox_path["firefox_path"]:
      actually_firefox_path = input('\r\nSpécifié le chemin d\'accès de Firefox (de base "C:\\Program Files\\Mozilla Firefox\\firefox.exe", cela ne sera plus redemandé). : ')
      firefox_path.update({"firefox_path": actually_firefox_path})

    firefox_json_write =  open('assets/firefox_path.json', 'w', encoding='utf-8')
    dump(firefox_path, firefox_json_write)
    firefox_json_write.close()

    ascii_print()

delete_temp_files()

ascii_print()

ask_firefox_path()

print("\r\nDémarrage...")

options = webdriver.FirefoxOptions()
options.binary_location = firefox_path["firefox_path"]
options.add_argument('--headless')
options.set_preference("media.volume_scale", "0.0")

driver = webdriver.Firefox(executable_path=path.abspath(r"assets/geckodriver.exe"), service_log_path=path.devnull, options=options)

driver.install_addon("assets/uBlock0_1.47.5b13.firefox.signed.xpi")

ascii_print()

input_link = input(f"\r\n{Fore.LIGHTBLUE_EX}[>] {Fore.WHITE}Entrez un lien TF1 : {Fore.CYAN}")

if "tf1.fr" in input_link:
    tf1_link = input_link
else:
  input(f"\r\n{Fore.LIGHTRED_EX}[!] Ce lien n'est pas valide, entrez un lien TF1.")
  exit(1)

print(f"\r\n{Fore.CYAN}[✓]{Fore.WHITE} Ouverture du lien (1/7)")

driver.get(tf1_link)

recovered_video_title = sub("[:/\\\*\?\"<>\|]", "", driver.find_element(By.CSS_SELECTOR, ".VideoSummary_title_o8ZzQ").text)

click_when_available(".LongButton_longButton__medium_S_9PJ")

print(f"\r\n{Fore.CYAN}[✓]{Fore.WHITE} Connexion (2/7)")

#Pour visionner un replay, il faut nécéssairement un compte TF1. Le script se connecte a un compte créé pour l'occasion
complete_when_available("#email", "jimen23366@huvacliq.com")

complete_when_available("#password", "Password1234*")

click_when_available("#popin_tc_privacy_button_3")

click_when_available(".longButton__content")

print(f"\r\n{Fore.CYAN}[✓]{Fore.WHITE} Traitement (3/7)")

while True:
  mpd_file_url = None
  for request in driver.requests:
    if ".mpd" in request.url:
      mpd_file_url = request.url
      break
  if mpd_file_url:
    driver.quit()
    break

tf1_stream_url = mpd_file_url[:mpd_file_url.rfind("/")] + "/"

tree = fromstring(get(mpd_file_url).text)

video_file_codes = []

for element in tree.findall('.//{*}SegmentTemplate'):
    media_code = element.attrib["media"].split("$")[0]
    break

for element in tree.findall('.//{*}Representation'):
    if element.attrib["id"].startswith("audio"):
        audio_file_code = element.attrib["id"]
    elif element.attrib["id"].startswith("video"):
        video_file_code = element.attrib["id"]
        video_file_codes.append(video_file_code)

video_qualities = ['234p', '270p', '360p', '480p', '576p', '720p']

qualities_and_video_codes = {video_qualities[i]: video_file_codes[i] for i in range(len(video_file_codes))}

print(f"\r\n{Fore.CYAN}[✓]{Fore.WHITE} Choisissez la qualité voulue (4/7) :\r\n")

for choice_number, available_quality in enumerate(qualities_and_video_codes.keys(), 1):
    qualities_choice = f"{choice_number}. {available_quality}"
    print(qualities_choice)

quality_choice = int(input(f"\r\n{Fore.LIGHTBLUE_EX}[>]{Fore.WHITE} Choix : "))

video_url_base = f"{tf1_stream_url}{media_code}{list(qualities_and_video_codes.values())[quality_choice-1]}"
audio_url_base = f"{tf1_stream_url}{media_code}{audio_file_code}"

print(f"\r\n{Fore.CYAN}[✓]{Fore.WHITE} Téléchargement des segments vidéos (5/7)\r\n{Fore.LIGHTCYAN_EX}")

download(f"{video_url_base}.m4s?m", "assets/dl_temp/v_0.m4s")

segment_number = 1

download_all_segment(video_url_base, "v")

print(f"\r\n\r\n{Fore.CYAN}[✓]{Fore.WHITE} Téléchargement des segments audios (6/7)\r\n{Fore.LIGHTCYAN_EX}")

download(f"{audio_url_base}.m4s?m", "assets/dl_temp/a_0.m4s")

segment_number = 1

download_all_segment(audio_url_base, "a")
   
print(f"\r\n\r\n{Fore.CYAN}[✓]{Fore.WHITE} Compilation des pistes audios et vidéos (7/7)")

all_video_segments = ""
all_audio_segments = ""

for number_segment in range(total_segment_number + 1):
    all_video_segments += f"assets/dl_temp/v_{str(number_segment)}.m4s|"
    all_audio_segments += f"assets/dl_temp/a_{str(number_segment)}.m4s|"

all_video_segments = all_video_segments.removesuffix("|")
all_audio_segments = all_audio_segments.removesuffix("|")

video_compiling = Popen(f"assets/ffmpeg.exe -i \"concat:{all_video_segments}\" -i \"concat:{all_audio_segments}\" -c copy -y \"{recovered_video_title}.mp4\" -hide_banner -loglevel error")

video_compiling.wait()

delete_temp_files()

input(f"\r\n{Fore.LIGHTGREEN_EX}\"{recovered_video_title}.mp4\" {Fore.WHITE}est disponnible.\r\nAppuyer pour quitter")

exit(1)
