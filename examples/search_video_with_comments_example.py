import sys
import os
# Add parent directory to sys.path to import local TikTokApi package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TikTokApi import TikTokApi
import asyncio

# Set your own ms_token
ms_token = os.environ.get("ms_token", None)

# Proxy configuration from proxy_demo.py
PROXY_TUNNEL = os.environ.get("PROXY_TUNNEL", "l273.kdlfps.com:18866")
PROXY_USERNAME = os.environ.get("PROXY_USERNAME", "f2179606115")
PROXY_PASSWORD = os.environ.get("PROXY_PASSWORD", "vwpbtnlp")

# Format proxy for Playwright
proxy_config = {
    "server": f"http://{PROXY_TUNNEL}",
    "username": PROXY_USERNAME,
    "password": PROXY_PASSWORD,
}

async def search_video_with_comments():
    """Search for videos and fetch comments with proxy support and retry logic"""
    
    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempt {attempt}/{max_retries}: Creating TikTok API session with proxy...")
            
            async with TikTokApi() as api:
                # Optimized configuration based on successful community solutions
                await api.create_sessions(
                    ms_tokens=[ms_token],
                    num_sessions=1,
                    sleep_after=5,  # Increased to allow more time for ms_token generation
                    proxies=[proxy_config],
                    timeout=180000,  # 180 seconds (3 minutes) for slow proxies
                    browser=os.getenv("TIKTOK_BROWSER", "chromium"),
                    headless=True,  # Set to True for remote servers without display
                    override_browser_args=[
                        '--disable-blink-features=AutomationControlled',  # Avoid detection
                        '--disable-dev-shm-usage',  # Overcome limited resource problems
                        '--no-sandbox',  # Required for root/server environments
                        '--disable-setuid-sandbox',
                        '--disable-gpu',  # Disable GPU for headless
                    ],
                    suppress_resource_load_types=['image', 'media', 'font'],  # Speed up loading
                )
                
                print("✓ Session created successfully!")
                
                search_term = "旅伴匹配"
                print(f"Searching for videos with term: {search_term}")
                
                async for video in api.search.videos(search_term, count=10, WebIdLastTime=0):
                    print("=" * 40)
                    print(f"Video ID: {video.id}")
                    print(f"Description: {video.desc[:100]}..." if video.desc else "No description")
                    print(f"Create Time: {video.create_time}")
                    print(f"Author: {video.author.username if video.author else 'Unknown'}")
                    
                    # Construct video link
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
                
                # If we get here, everything succeeded
                return
                
        except Exception as e:
            error_msg = str(e)
            print(f"✗ Attempt {attempt} failed: {error_msg}")
            
            if attempt < max_retries:
                wait_time = retry_delay * attempt  # Exponential backoff
                print(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                print(f"\n❌ Failed after {max_retries} attempts.")
                print("\nTroubleshooting tips:")
                print("1. Verify proxy is working: python3 proxy_demo.py")
                print("2. Check if TikTokApi/tiktok.py has the timeout bug fix")
                print("3. Try increasing timeout further or using a different proxy")
                raise

if __name__ == "__main__":
    asyncio.run(search_video_with_comments())
