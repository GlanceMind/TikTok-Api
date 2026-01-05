import sys
import os
# Add parent directory to sys.path to import local TikTokApi package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TikTokApi import TikTokApi
import asyncio

# Set your own ms_token
ms_token = os.environ.get("ms_token", None)

async def search_video_with_comments():
    async with TikTokApi() as api:
        await api.create_sessions(
            ms_tokens=[ms_token],
            num_sessions=1,
            sleep_after=3,
            browser=os.getenv("TIKTOK_BROWSER", "chromium"),
        )
        
        search_term = "旅伴匹配"
        print(f"Searching for videos with term: {search_term}")
        
        async for video in api.search.videos(search_term, count=10, WebIdLastTime=0):
            print("=" * 40)
            print(f"Video ID: {video.id}")
            print(f"Description: {video.desc[:100]}..." if video.desc else "No description")
            print(f"Create Time: {video.create_time}")
            print(f"Author: {video.author.username if video.author else 'Unknown'}")
            
            # Construct video link
            # The author ID used in URL is author.username, but video object from search has author object.
            # Assuming author.username is the uniqueId.
            if video.author:
                video_url = f"https://www.tiktok.com/@{video.author.username}/video/{video.id}"
                print(f"Video Link: {video_url}")
            
            print("\nComments:")
            try:
                comment_count = 0
                async for comment in api.video(id=video.id).comments(count=5):
                    print(f"  - [{comment.author.username}]: {comment.text}")
                    comment_count += 1
                if comment_count == 0:
                    print("  No comments found or requests failed.")
            except Exception as e:
                print(f"  Error fetching comments: {e}")

            # Appropriate delay between processing videos
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(search_video_with_comments())
