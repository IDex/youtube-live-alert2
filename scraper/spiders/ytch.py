import json
import re
import datetime

import scrapy
import yaml
import munch
import pathlib
from appdirs import user_config_dir

config_path = list(pathlib.Path(__file__).parent.parent.parent.resolve().glob('config.yml'))[0]

class YtchSpider(scrapy.Spider):
    name = "ytch"
    start_urls = list(
        munch.Munch.fromDict(
            yaml.safe_load(
                (
                    (
                        config_path
                    ).read_text()
                )
            )
        ).channels.values()
    )
    start_urls = [x + "/live" for x in start_urls]

    def parse(self, response):
        """Parse live stream details if channel is streaming."""
        res = [
            re.findall(r'(".*?"):(".*?"|\[.*?\]|true|false)', x)
            for x in re.findall(r'videoDetails":{(.*?)}', response.text)
        ]
        if not res:
            return
        res = res[0]
        res = "{%s}" % ",".join([":".join(x) for x in res][:-1])
        res = json.loads(res)
        res["keywords"] = ", ".join(res["keywords"])
        res["scraped_time"] = datetime.datetime.now()
        res = dict(table="youtube_streams", value=res, key="videoId")
        return res
