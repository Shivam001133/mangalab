import logging

logger = logging.getLogger(__name__)


def chapter_no_finder(chapter_name: str) -> int:
    """
    Find the chapter number from the chapter name
    """
    chapter_name = chapter_name.strip().split()
    for data in chapter_name:
        if data.isdigit():
            try:
                return int(data)
            except ValueError:
                logger.error(f"Error: {ValueError}")