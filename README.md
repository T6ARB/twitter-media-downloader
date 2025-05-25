# Twitter Media Downloader

A Python CLI tool to download **all images and videos** from a Twitter user’s tweets, with the tweet text saved alongside.

---

## Features

- Download photos, videos, and GIFs from a Twitter account  
- Save media files in a folder named `<username>_media` (or custom folder)  
- Save the tweet text in `.txt` files next to media files  
- Option to limit number of tweets to scan  
- Progress bar during downloads (using tqdm)  
- Simple command-line usage  

---

## Installation

**Clone the Repository:**
```bash
    git clone https://github.com/T6ARB/twitter-media-downloader.git
```   
```bash
pip install -r requirements.txt
```

---

## Usage

```bash
python twitter_media_downloader.py <username> [--limit N] [--output /path/to/folder]
```

- `<username>`: Twitter handle without `@`  
- `--limit N`: Optional, limits scanning to last N tweets (default 0 = no limit)  
- `--output`: Optional, specify output directory (default: `<username>_media`)

Example:

```bash
python twitter_media_downloader.py nasa --limit 100 --output ./nasa_media
```
