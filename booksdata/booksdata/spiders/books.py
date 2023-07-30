import scrapy
from pathlib import Path
import csv

# from pymongo import MongoClient
# import datetime

# client = MongoClient("mongodb+srv://admin:admin12345@scrapy-mongo.dvljlbg.mongodb.net/")
# db = client.scrapy

# def data_in_mongo(title,price,image,inStock,rating,page):
#     collection = db[page]
#     doc = {"title":title,"price":price,"image":image,"rating":rating,"inStock":inStock,
#     "date": datetime.datetime.now(tz=datetime.timezone.utc),
# }
#     inserted= collection.insert_one(doc)
#     return inserted.inserted_id


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]


    def start_requests(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.csv"

        self.log(f"Saved file {filename}")

        cards = response.css(".product_pod")
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["title", "price", "image", "inStock", "rating"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for card in cards:
                title = card.css("h3>a::text").get()
                price = card.css(".product_price .price_color::text").get()
                rating = card.css(".star-rating").attrib["class"].split(" ")[1]

                availability = card.css(".availability")
                inStock = len(availability.css(".icon-ok")) > 0

                image = card.css(".image_container img")
                image = image.attrib["src"].replace(
                    "../../../../media", "https://books.toscrape.com/media"
                )
              # data_in_mongo(title,price,image,inStock,rating,page)  mongo db code

                writer.writerow(
                    {"title": title, "price": price, "image": image, "inStock": inStock, "rating": rating}
                )

    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     # filename = f"quotes-{page}.html"

    #     filename = f"quotes-{page}.csv"


    #     # Path(filename).write_bytes(response.body)
    #     self.log(f"Saved file {filename}")
    #     # a=response.css(".product_pod").get()
    #     # b = a.css("a").text
    #     # print(b)
    #     cards = response.css(".product_pod")
    #     with open(filename, "w", newline="", encoding="utf-8") as csvfile:
    #         fieldnames = ["title", "price", "image", "inStock", "rating"]
    #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #         writer.writeheader()
    #     for card in cards:
    #         title=card.css("h3>a::text").get()
    #         price=card.css(".product_price .price_color::text").get()
    #         rating=card.css(".star-rating").attrib['class'].split(' ')[1]
    #         # print(rating)
            
    #         availability=card.css(".availability")
    #         # print(availibility)
    #         if len(availability.css(".icon-ok"))>0:
    #             inStock=True
    #         else:
    #             inStock=False

    #         image=card.css(".image_container img")
    #         image=image.attrib["src"].replace("../../../../media","https://books.toscrape.com/media")
    #         writer.writerow(
    #                 {"title": title, "price": price, "image": image, "inStock": inStock, "rating": rating}
    #             )