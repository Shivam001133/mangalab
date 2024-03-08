import logging
import re 

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


