# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose
from w3lib.html import remove_tags


# Removes commas from data collected to store integers
def remove_commas(text):
    text = text.replace(',', '')
    return text


# Allows the data collected to be modified
class CovidWebscraperItem(Item):

    country_name = Field(
    )

    # Recoveries contain spaces and commas when collected
    total_recoveries = Field(
        input_processor=MapCompose(remove_tags, remove_commas)
    )

    # Active cases contain commas when large
    total_active_cases = Field(
        input_processor=MapCompose(remove_commas)
    )

    # Large populations contain commas when collected
    population = Field(
        input_processor=MapCompose(remove_commas)
    )
