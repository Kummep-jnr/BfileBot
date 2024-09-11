from dotenv import load_dotenv
import os
import json
import schedule
import time
import random
import asyncio
from telegram import Bot

load_dotenv()


# Initialize your bot with your token and channel ID
bot_token = os.getenv('BOT_TOKEN')
channel_id = os.getenv('API_KEY')
bot = Bot(token=bot_token)

print(f"Bot Token: {bot_token}")
print(f"API Key: {api_key}")
# Load the data from the JSON file with error handling
def load_data():
    try:
        with open('bot_data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: 'bot_data.json' file not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

# Asynchronous function to post content based on type
async def post_content(item):
    print(f"Posting content: {item}")  # Debugging output
    try:
        if item['type'] == 'text':
            await bot.send_message(chat_id=channel_id, text=item['content'])
        elif item['type'] == 'image':
            await bot.send_photo(chat_id=channel_id, photo=item['file'], caption=item.get('caption', ''))
        elif item['type'] == 'video':
            await bot.send_video(chat_id=channel_id, video=item['file'], caption=item.get('caption', ''))
        elif item['type'] == 'gif':
            await bot.send_animation(chat_id=channel_id, animation=item['file'], caption=item.get('caption', ''))
    except Exception as e:
        print(f"Failed to post content of type {item.get('type')} at {time.strftime('%Y-%m-%d %H:%M:%S')}: {e}")

# Asynchronous wrapper to ensure all scheduled tasks run on a single event loop
async def run_scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

# Function to schedule posts at specific times
def schedule_posts():
    data = load_data()
    if not data:
        print("No data available to schedule posts.")
        return

    # Randomly select 12 unique items from the data for the posts
    posts = random.sample(data, min(12, len(data)))  # Adjust to the length of data if less than 12 items

    # Corrected posting times to proper HH:MM format
    posting_times = ['08:00', '08:50', '09:57', '11:00', '11:50', '13:00', '14:55', '13:54', '15:00', '15:45', '17:00', '17:55']

    for post, post_time in zip(posts, posting_times):
        print(f"Scheduling post at {post_time}")  # Debugging output
        schedule.every().day.at(post_time).do(lambda post=post: asyncio.create_task(post_content(post)))

# Main function to start everything
def main():
    # Schedule the posts
    schedule_posts()

    # Run the scheduler in an event loop
    try:
        asyncio.run(run_scheduler())
    except RuntimeError as e:
        print(f"Runtime error in event loop: {e}")

# Entry point
if __name__ == "__main__":
    main()
