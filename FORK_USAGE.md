# TikTok-Api Custom Fork Usage

This fork contains enhancements to the TikTok-Api library, specifically for better handling of video search results and accessing associated comments.

**Original Repository**: [davidteather/TikTok-Api](https://github.com/davidteather/TikTok-Api)
**Fork Repository**: [GlanceMind/TikTok-Api](https://github.com/GlanceMind/TikTok-Api)
**Feature Branch**: `feat/search-video`

## Installation

You can install this specific version directly from GitHub using pip:

```bash
pip install git+https://github.com/GlanceMind/TikTok-Api.git@feat/search-video
```

Or clone the repository and install locally:

```bash
git clone git@github.com:GlanceMind/TikTok-Api.git
cd TikTok-Api
git checkout feat/search-video
pip install .
```

## New Features

### 1. Enhanced Video Search

The `api.search.videos` method now returns detailed `SearchVideo` objects which include:
- `id`: Video ID
- `desc`: Video description (caption)
- `create_time`: Video creation timestamp
- `author`: Author information
- `stats`: Video statistics (diggCount, shareCount, etc.)

**Example Usage:**

```python
async for video in api.search.videos("keyword", count=10):
    print(video.id)
    print(video.desc)
    print(video.create_time)
```

### 2. Streamlined Comments Access

You can easily search for videos and then fetch their comments using the standard `api.video().comments()` method.

**Example Usage:**

```python
async for video in api.search.videos("keyword", count=10):
    # Fetch comments for the found video
    async for comment in api.video(id=video.id).comments(count=5):
        print(f"Comment by {comment.author.username}: {comment.text}")
```

## Included Examples

- **`examples/search_video_example.py`**: demonstrates basic video search and printing detailed info.
- **`examples/search_video_with_comments_example.py`**: demonstrates searching videos and retrieving their comments with appropriate delays.
