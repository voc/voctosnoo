import sqlite3
from time import sleep

import feedparser
import praw

class Bot:
    def __init__(self, subreddit="mediacccde", feed="https://media.ccc.de/podcast-hq.xml", database_file="threads.db", reddit_args={}):
        reddit = praw.Reddit(**reddit_args)
        self.subreddit = reddit.subreddit(subreddit)
        self.feed = feed

        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS threads(id,link,title,thread_id)")
        self.conn.commit()

    def submit_post_for_entry(self, entry):
        while True:
            try:
                return self.subreddit.submit(entry.title, url=entry.link)
            except praw.exceptions.APIException as e:
                if e.field == "ratelimit":
                    sleep(60)
                else:
                    raise e

    def process_feed(self):
        feed = feedparser.parse( self.feed )

        for entry in sorted(feed.entries, key=lambda e: e.updated):
            print(entry.enclosures[0].href)
            self.cursor.execute("SELECT id FROM threads WHERE id = ?", (entry.id,))
            data=self.cursor.fetchall()
            if len(data)==0:
                print("Creating thread for {}".format(entry.id))
                thread = self.submit_post_for_entry(entry)
                self.cursor.execute("INSERT INTO threads(id,link,title,thread_id) VALUES(?,?,?,?)", (entry.id, entry.link, entry.title, 1))
                self.conn.commit()

    def run(self, interval=300):
        while True:
            self.process_feed()
            sleep(interval)