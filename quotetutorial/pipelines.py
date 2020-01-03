# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3


class QuotetutorialPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_tables()

    def create_connection(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect("myquotes.db")
        except sqlite3.Error as e:
            print(e)

        if self.conn:
            self.curr = self.conn.cursor()

    def create_tables(self):
        self.curr.execute(
            """
            DROP TABLE IF EXISTS quotes_tb;
            """
        )
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS quotes_tb(
                id integer PRIMARY KEY,
                title text,
                author text
            );
            """
        )
        self.curr.execute(
            """
            DROP TABLE IF EXISTS tags_tb;
            """
        )
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS tags_tb(
                id integer PRIMARY KEY,
                quote_id integer NOT NULL,
                tag text NOT NULL
            )
            """
        )

    def store_quote(self, title, author):
        sql = """
            insert into quotes_tb (title, author)
            values (?,?)
        """
        self.curr.execute(sql, (title, author))
        return self.curr.lastrowid

    def store_tags(self, quote_id, tags: list):
        sql = """
        insert into tags_tb (quote_id, tag)
        values (?,?)
        """
        for tag in tags:
            self.curr.execute(sql, (quote_id, tag))

    def process_item(self, item, spider):
        quote_id = self.store_quote(item["title"][0], item["author"][0])
        self.store_tags(quote_id, item["tags"])
        # print("Pipeline : " + item["title"][0])
        self.conn.commit()
        return item

    # def store_db(self, item):

    #     self.curr.execute(
    #         """insert into quotes_tb values (?,?,?)""",
    #         (item["title"][0], item["author"][0], ",".join(item["tags"])),
    #     )
    #     self.conn.commit()
    #     # print("*** SQL: " + sql)
