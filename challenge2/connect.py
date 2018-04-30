import sqlite3

conn = sqlite3.connect("reddit.db")
# conn.text_factory = lambda x: str(x, 'latin1')
query_sub =  """
SELECT s.id, s.name, c.body FROM subreddits s JOIN comments c ON s.id = c.subreddit_id LIMIT 30
"""

for id, name, body in conn.execute(query_sub):
    print(id, name, body.encode())