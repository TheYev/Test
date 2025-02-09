import aiohttp
import asyncio
import sqlite3
import csv
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_URL = "https://jsonplaceholder.typicode.com/posts"
DB_NAME = "posts.db"
CSV_NAME = "posts.csv"

async def fetch_post(session, post_id):
    try:
        async with session.get(f"{API_URL}/{post_id}", timeout=10) as response:
            if response.status == 200:
                data = await response.json()
                logging.info(f"Fetched post {post_id}")
                return data
            else:
                logging.error(f"Error {response.status} for post {post_id}")
                return None
    except Exception as e:
        logging.error(f"Exception for post {post_id}: {e}")
        return None

async def fetch_all_posts():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_post(session, i) for i in range(1, 101)]
        return await asyncio.gather(*tasks)

def save_to_db(posts):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            body TEXT
        )
    """)
    
    cursor.executemany("""
        INSERT OR IGNORE INTO posts (id, user_id, title, body) VALUES (?, ?, ?, ?)
    """, [(p['id'], p['userId'], p['title'], p['body']) for p in posts if p])
    
    conn.commit()
    conn.close()
    logging.info("Data saved to SQLite database.")

def save_to_csv(posts):
    with open(CSV_NAME, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "user_id", "title", "body"])
        for post in posts:
            if post:
                writer.writerow([post['id'], post['userId'], post['title'], post['body']])
    logging.info("Data saved to CSV file.")

async def main():
    posts = await fetch_all_posts()
    posts = [p for p in posts if p is not None]
    save_to_db(posts)
    save_to_csv(posts)

if __name__ == "__main__":
    asyncio.run(main())
