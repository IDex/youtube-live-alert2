import datetime
import subprocess
import time
import webbrowser

import dataset
import pathlib


def main():
    db_file = list(pathlib.Path(__file__).parent.parent.resolve().glob('result.db'))[0]
    print(db_file)
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = dataset.connect(f"sqlite:///{db_file}")
    t = db["youtube_streams"]
    print(f"Starting youtube tracking. Database contents: {len(list(t.all()))}")
    if "seen" not in t.columns:
        t.create_column("seen", db.types.boolean)
    while True:
        subprocess.run("scrapy crawl ytch".split())
        for url in db.query(
            f"select videoId from youtube_streams where seen is null and isLive = 1"
        ):
            url = url["videoId"]
            print(url)
            webbrowser.open(f"https://www.youtube.com/watch?v={url}")
            t.update(dict(videoId=url, seen=1), keys=("videoId"))
        time.sleep(60)


if __name__ == "__main__":
    main()
