import os
import sys
import requests
import argparse
import snscrape.modules.twitter as sntwitter
from tqdm import tqdm

def download_file(url, folder):
    local_filename = url.split("?")[0].split("/")[-1]
    local_path = os.path.join(folder, local_filename)
    if os.path.exists(local_path):
        print(f"Skipped (exists): {local_filename}")
        return local_path
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        with open(local_path, 'wb') as f, tqdm(
            desc=local_filename,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in r.iter_content(chunk_size=1024):
                size = f.write(chunk)
                bar.update(size)
        print(f"Downloaded: {local_filename}")
        return local_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def save_tweet_text(tweet, folder, tweet_id):
    filename = os.path.join(folder, f"tweet_{tweet_id}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(tweet.content)
    print(f"Saved tweet text: tweet_{tweet_id}.txt")

def main(username, limit, outdir):
    folder = outdir if outdir else f"{username}_media"
    os.makedirs(folder, exist_ok=True)

    scraper = sntwitter.TwitterUserScraper(username)
    count = 0

    for tweet in scraper.get_items():
        if limit and count >= limit:
            break

        media = tweet.media
        if not media:
            count += 1
            continue

        # Save tweet text for each tweet with media
        save_tweet_text(tweet, folder, tweet.id)

        for m in media:
            url = None
            if hasattr(m, 'fullUrl'):  # photo or video
                url = m.fullUrl
            elif hasattr(m, 'videoUrl'):  # video
                url = m.videoUrl
            elif hasattr(m, 'previewUrl'):  # GIFs etc.
                url = m.previewUrl

            if url:
                download_file(url, folder)

        count += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download all media (images/videos) from a Twitter user with tweet text.")
    parser.add_argument("username", help="Twitter username (without @)")
    parser.add_argument("--limit", type=int, default=0, help="Max number of tweets to scan (0 = no limit)")
    parser.add_argument("--output", type=str, default=None, help="Output folder (default: <username>_media)")

    args = parser.parse_args()
    main(args.username, args.limit, args.output)
