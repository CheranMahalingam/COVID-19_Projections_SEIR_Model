# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

# Stores data in a database


class CovidWebscraperPipeline(object):

    # Creates connection to database and creates a table
    def __init__(self):
        self.create_connection()
        self.create_table()

    # Initializes database
    def create_connection(self):
        self.conn = sqlite3.connect('case_data.db')
        self.curr = self.conn.cursor()

    # Creates a table to store data and removes table if it already exists
    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS cases_tb""")
        self.curr.execute("""CREATE TABLE cases_tb(
                        country_name text,
                        total_recoveries integer,
                        total_active_cases integer,
                        population integer
                        )""")

    # Calls on stored_db function to store webscraped items
    def process_item(self, item, spider):
        self.stored_db(item)
        return item

    # Inserts webscraped items into the database
    def stored_db(self, item):
        self.curr.execute("""INSERT INTO cases_tb VALUES (?, ?, ?, ?)""", (
            item['country_name'][0],
            item['total_recoveries'][0],
            item['total_active_cases'][0],
            item['population'][0]
        ))
        self.conn.commit()
