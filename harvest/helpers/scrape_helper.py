import re
from harvest_routes.models import Harvester, ScrapingHarvest


def scraping_info(domain_name):
    """
    This function is used to scrape the domain
    """
    domain = Harvester.objects.get(domain_name=domain_name)
    return ScrapingHarvest.objects.filter(
        is_active=True, harvest=domain
    ).first()


def extract_chapter_no(chapter_title):
    """
    Extract chapter number from chapter title
    """
    seatch_str = r"\bchapter\s+(\d+)"
    match = re.search(seatch_str, chapter_title, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def extract_manga_title(title):
    """
    Extract manga title from the title
    """
    title_list = title.split("~")
    title_list = [title.strip() for title in title_list if title.strip()]
    if title_list:
        return title_list[0], title_list
    return None, []
