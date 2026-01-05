import sys
import os
import json
# Add parent directory to sys.path to import local TikTokApi package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TikTokApi import TikTokApi
import asyncio

# Load full cookies from tiktok_cookies.json (preferred method)
def load_cookies():
    """Load complete TikTok cookies from JSON file"""
    cookies_file = os.path.join(os.path.dirname(__file__), '..', 'tiktok_cookies.json')
    
    if os.path.exists(cookies_file):
        with open(cookies_file, 'r') as f:
            cookies = json.load(f)
            print(f"✓ Loaded {len(cookies)} cookies from {cookies_file}")
            return cookies
    else:
        # Fallback to ms_token from environment variable
        ms_token = os.environ.get("ms_token")
        if ms_token:
            print("⚠ Using ms_token from environment (full cookies recommended)")
            return {"msToken": ms_token}
        else:
            print("⚠ No cookies found. Will attempt to auto-generate.")
            return None

# Load cookies
cookies = load_cookies()

# Load proxies from Webshare file
def load_proxies():
    """Load proxies from Webshare 10 proxies.txt file"""
    proxies_file = os.path.join(os.path.dirname(__file__), '..', 'proxies.txt')
    proxies = []
    
    if os.path.exists(proxies_file):
        with open(proxies_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                
                # Parse format: IP:PORT:USERNAME:PASSWORD
                parts = line.split(':')
                if len(parts) == 4:
                    ip, port, username, password = parts
                    proxy = {
                        "server": f"http://{ip}:{port}",
                        "username": username,
                        "password": password,
                    }
                    proxies.append(proxy)
        
        print(f"✓ Loaded {len(proxies)} proxies from {proxies_file}")
        return proxies
    else:
        # Fallback to original proxy configuration
        print("⚠ Webshare proxies file not found, using default proxy")
        PROXY_TUNNEL = os.environ.get("PROXY_TUNNEL", "l273.kdlfps.com:18866")
        PROXY_USERNAME = os.environ.get("PROXY_USERNAME", "f2179606115")
        PROXY_PASSWORD = os.environ.get("PROXY_PASSWORD", "vwpbtnlp")
        
        return [{
            "server": f"http://{PROXY_TUNNEL}",
            "username": PROXY_USERNAME,
            "password": PROXY_PASSWORD,
        }]

# Load proxies
proxies = load_proxies()

async def search_video_with_comments():
    """Search for videos and fetch comments with proxy support and retry logic"""
    
    max_retries = 3
    retry_delay = 5  # seconds
    
    # Try different browsers - webkit first (less detected), then chromium as fallback
    browsers_to_try = [
        os.getenv("TIKTOK_BROWSER", "webkit"),  # Default: webkit (often less detected)
        "chromium",  # Fallback to chromium
    ]
    
    for browser_type in browsers_to_try:
        for attempt in range(1, max_retries + 1):
            try:
                print(f"\n{'='*60}")
                print(f"Browser: {browser_type} | Attempt {attempt}/{max_retries}")
                print(f"{'='*60}")
                print("Creating TikTok API session with proxy and anti-detection measures...")
                
                async with TikTokApi() as api:
                    # Minimal configuration - matching official TikTok-Api examples
                    # Complex parameters can actually trigger MORE detection!
                    await api.create_sessions(
                        cookies=[cookies] if cookies else None,
                        num_sessions=1,
                        sleep_after=3,  # Official examples use 3 seconds
                        proxies=proxies,
                        browser=browser_type,
                        headless=False,  # Critical for avoiding detection
                        # No context_options - let browser use defaults
                        # No override_browser_args - avoid detection triggers
                    )
                    
                    print("✓ Session created successfully!")
                    print(f"  Using browser: {browser_type}")
                    print(f"  Proxy pool: {len(proxies)} proxies available")
                    if cookies:
                        print(f"  Cookies: {len(cookies)} loaded")
                        print(f"  msToken: {'✓' if 'msToken' in cookies else '✗'}")
                    else:
                        print(f"  Cookies: Auto-generating")
                    
                    search_term = "旅伴匹配"
                    print(f"\nSearching for videos with term: {search_term}")
                    
                    video_count = 0
                    async for video in api.search.videos(search_term, count=10, WebIdLastTime=0):
                        video_count += 1
                        print("\n" + "=" * 60)
                        print(f"Video #{video_count}")
                        print("=" * 60)
                        print(f"Video ID: {video.id}")
                        print(f"Description: {video.desc[:100]}..." if video.desc else "No description")
                        print(f"Create Time: {video.create_time}")
                        print(f"Author: {video.author.username if video.author else 'Unknown'}")
                        
                        if video.author:
                            video_url = f"https://www.tiktok.com/@{video.author.username}/video/{video.id}"
                            print(f"Video Link: {video_url}")
                        
                        print("\nFetching Comments:")
                        try:
                            comment_count = 0
                            async for comment in api.video(id=video.id).comments(count=5):
                                comment_count += 1
                                comment_text = comment.text[:100] if len(comment.text) > 100 else comment.text
                                print(f"  #{comment_count}. [{comment.author.username}]: {comment_text}")
                            
                            if comment_count == 0:
                                print("  ⚠ No comments found (video may have no comments or request failed)")
                            else:
                                print(f"\n  ✓ Successfully fetched {comment_count} comments")
                                
                        except Exception as e:
                            error_str = str(e)
                            print(f"  ✗ Error fetching comments: {e}")
                            
                            # Provide specific troubleshooting for "empty response"
                            if "empty response" in error_str.lower():
                                print("\n  ⚠ TikTok detected bot activity. Suggestions:")
                                print("    1. Ensure ms_token is set (export ms_token=YOUR_TOKEN)")
                                print("    2. Proxy IP may be blacklisted - try different proxy")
                                print("    3. Add delays between requests")
                                print("    4. Current browser will try next attempt or webkit fallback")

                        # Appropriate delay between processing videos
                        await asyncio.sleep(3)
                    
                    if video_count == 0:
                        print("\n⚠ No videos found. This might indicate:")
                        print("  - Search term has no results")
                        print("  - TikTok is blocking the requests")
                        print("  - Proxy/IP is restricted")
                    else:
                        print(f"\n✓ Successfully processed {video_count} videos")
                    
                    # If we get here, everything succeeded
                    print(f"\n{'='*60}")
                    print(f"✓ Completed successfully with {browser_type}")
                    print(f"{'='*60}")
                    return
                    
            except Exception as e:
                error_msg = str(e)
                print(f"\n✗ {browser_type} Attempt {attempt} failed: {error_msg}")
                
                if attempt < max_retries:
                    wait_time = retry_delay * attempt
                    print(f"⏳ Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    print(f"\n✗ {browser_type} failed after {max_retries} attempts")
                    if browser_type != browsers_to_try[-1]:
                        print(f"→ Will try next browser: {browsers_to_try[browsers_to_try.index(browser_type)+1]}")
                    break
        
        # If we successfully returned, we won't reach here
        # This means all attempts with this browser failed, try next browser
    
    # If all browsers failed
    print(f"\n❌ All browsers failed after {max_retries} attempts each.")
    print("\n🔧 Troubleshooting checklist:")
    print("  1. ✓ Verify proxy: python3 proxy_demo.py")
    print("  2. ✓ Set ms_token: export ms_token=YOUR_MS_TOKEN")
    print("     (Get from browser cookies after visiting tiktok.com)")
    print("  3. ✓ Check TikTokApi/tiktok.py has both bug fixes applied")
    print("  4. ✓ Try a different proxy service (current proxy may be blacklisted)")
    print("  5. ✓ Verify proxy supports browser/HTTPS connections")
    raise Exception("Failed to fetch data after trying all browsers and retries")

if __name__ == "__main__":
    asyncio.run(search_video_with_comments())
