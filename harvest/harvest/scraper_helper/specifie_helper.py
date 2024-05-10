from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import requests
import logging
import shutil
import re
import os

logger = logging.getLogger(__name__)


def extract_chapter_number(chapter_name: str) -> int:
    """
    Find the chapter number from the chapter name
    """
    pattern = r'(volume|chapter)\s*([0-9:]+)'
    matches = re.findall(pattern, chapter_name, flags=re.IGNORECASE)

    volume = None
    chapter = None

    for match in matches:
        keyword, value = match
        if keyword.lower() == 'volume':
            volume = int(re.sub(r'\W+', '', value))
        elif keyword.lower() == 'chapter':
            chapter = int(re.sub(r'\W+', '', value))
    try:
        return volume, chapter
    except Exception as e :
        logger.error(f"Error in extracting chapter number {e}")


def parse_url_checker(base_url:str, image_url: str) -> str:
    """
    Extract the image url from the image url
    """
    
    if image_url.startswith(base_url):
        return image_url
    else:
        return base_url + image_url

def img_downloader(url: str, save_directory: str):
    """
    Download an image from the given URL and save it to the specified directory.
    
    Parameters:
        url (str): The URL of the image to download.
        save_directory (str): The directory where the image will be saved. Default is current directory.
        
    Returns:
        str: The file path of the downloaded image.
    """
    try:
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            print(f"Downloading image url {url}")
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            save_path = os.path.join(save_directory, filename)

            with open(save_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            
            return True
        else:
            print("Failed to download image. Status code:", response.status_code)
            return False

    except Exception as e:
        print("An error occurred:", e)
        return False

def manga_download_manager(urls: list, manga_title:str, chapter_no:str):
    """
    Create directory structure for storing manga files.

    Parameters:
        urls (list): List of URLs of the images to download.
        manga_title (str): Title of the manga.
        chapter_no (str): Name of the chapter.

    Returns:
        str: Path to the chapter directory.
    """
    from django.conf import settings

    base_dir = settings.BASE_DIR
    try:
        chapter_no = str(chapter_no)
    except Exception as _:
        chapter_no = f"{manga_title}_nill"

    manga_dir = os.path.join(base_dir, "Mangafiles")
    if not os.path.exists(manga_dir):
        os.makedirs(manga_dir)
        logger.info(f"Created directory: {manga_dir}")

    manga_title_dir = os.path.join(manga_dir, manga_title)
    if not os.path.exists(manga_title_dir):
        os.makedirs(manga_title_dir)
        logger.info(f"Created directory: {manga_title_dir}")

    chapter_dir = os.path.join(manga_title_dir, chapter_no)
    if not os.path.exists(chapter_dir):
        os.makedirs(chapter_dir)
        logger.info(f"Created directory: {chapter_dir}")
    
    with ThreadPoolExecutor() as executor:
        results = executor.map(
            img_downloader,
            urls,
            [os.path.join(chapter_dir, str(i)) for i in range(len(urls))]
        )
    
    for res in results:
        if res:
            logger.info(f"img of {manga_title} for {chapter_no} downloaded")
