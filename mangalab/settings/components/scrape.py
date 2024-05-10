from mangalab.settings.components.get_env import SELENIUM_HOST

if SELENIUM_HOST:
    SELENIUM_HOST = 'selenium'
else:
    SELENIUM_HOST = 'localhost'