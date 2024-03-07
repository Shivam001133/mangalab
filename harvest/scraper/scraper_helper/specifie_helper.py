import logging
import re 

logger = logging.getLogger(__name__)


def chapter_no_finder(chapter_name: str) -> int:
    """
    Find the chapter number from the chapter name
    """
    chapter_name = chapter_name.strip().split()
    for data in chapter_name:
        if data.isdigit():
            try:
                cleaned_string = re.sub(r'\W+', '', data)
                return int(cleaned_string)
            except ValueError as e:
                logger.error(f"Error: {data} - {e}")
    # rather than return 0 change it 
    return 0
