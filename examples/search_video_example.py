import sys
import os
# Add parent directory to sys.path to import local TikTokApi package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TikTokApi import TikTokApi
import asyncio

# Set your own ms_token, needs to have done a search before for this to work
# You can get this from your browser cookies after visiting TikTok and searching
ms_token = os.environ.get("ms_token", None)

async def search_videos():
    async with TikTokApi() as api:
        await api.create_sessions(
            ms_tokens=[ms_token],
            num_sessions=1,
            sleep_after=3,
            browser=os.getenv("TIKTOK_BROWSER", "chromium"),
        )
        
        search_term = "旅伴匹配"  # User's keyword from the request
        
        print(f"Searching for videos with term: {search_term}")
        
        # Searching for videos
        # You can pass additional parameters like WebIdLastTime as seen in the URL
        async for video in api.search.videos(search_term, count=10, WebIdLastTime=0):
            print(f"Found video: {video.id}")
            print(f"Description: {video.desc}")
            print(f"create time: {video.create_time}")
            if video.stats:
                print(f"Stats: {video.stats}")
            print(f"Author: {video.author.username if video.author else 'Unknown'}")
            print("-" * 20)

if __name__ == "__main__":
    asyncio.run(search_videos())
