import logging

logger = logging.getLogger(__name__)


class DomainScrape:
    def __init__(self, domain):
        self.domain = domain

    class Manhwaz:
        class Treanding:
            MANGALIST = ".item.col-4.col-md-2"
            MANGA_URL = ".img-item a::attr(href)"
            IMG_URL = ".img-item a::attr(href)"
            MANGA_TITLE = ".line-2.font-weight-bold a::text"
            CHAPTER_URL = ".btn-link::attr(href)"
            CHAPTER_NAME = ".btn-link::text"


def domain_scrape(domain):
    match domain:
        case "manhwaz.com":
            return DomainScrape.Manhwaz
        case "bato.com":
            return None
        case "mangakakalot.com":
            return None
        case _:
            logger.info("You have chosen an invalid domain")
            return None
