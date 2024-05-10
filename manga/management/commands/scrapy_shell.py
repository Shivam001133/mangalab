# runscrapyshell.py
from django.core.management.base import BaseCommand
from scrapy.cmdline import execute

class Command(BaseCommand):
    help = 'Runs the Scrapy shell'

    def handle(self, *args, **options):
        execute(['scrapy', 'shell'])