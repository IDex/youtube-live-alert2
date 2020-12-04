# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import dataset
import pathlib


class ScraperPipeline:
    def open_spider(self, spider):
        db_path = list(pathlib.Path(__file__).parent.parent.resolve().glob('result.db'))[0]
        self.db = dataset.connect(f"sqlite:///{db_path}")

    def process_item(self, item, spider):
        self.db[item["table"]].upsert(
            item["value"],
            [item["key"]],
        )
        return item
