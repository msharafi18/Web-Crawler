from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time as t
import re
import pandas as pd
import csv

tokenlist = []
data = []
x= 0

options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
browser = webdriver.Chrome(options=options)
browser.get("https://www.digikala.com/search/category-mobile-phone/product-list/?brands%5B0%5D=18")


scroll = 1000
while True:
    t.sleep(1)
    browser.execute_script("window.scrollTo(0,{0})".format(scroll))
    scroll += 1000
    if scroll == 5000:
        break
t.sleep(2)


pages = browser.page_source
page = BeautifulSoup(pages,"html.parser")
# print(page)

text = page.find_all("div",{"class":"product-list_ProductList__item__LiiNI"})
for i in text:
    tokenlist.append(re.findall(r"(/product/dkp-\d*)",str(i)))


for i in tokenlist:
    browser.get("https://www.digikala.com{0}/".format(i[0]))
    t.sleep(2)
    productpages = browser.page_source
    productpage = BeautifulSoup(productpages,"html.parser")
    title = productpage.find_all("h1")
    price = productpage.find_all("span",{"data-testid":"price-no-discount"})
    pdata = []
    titlere = re.findall(r">(.+)<",str(title[0]))
    pricere = re.findall(r">(.+)<",str(price[0]))
    pdata.append(titlere[0])
    pdata.append(pricere[0])
    data.append(pdata)
    x += 1
    if x == 10:
        break

print(data)


df = pd.DataFrame(data,columns=["title","price"])
print(df)

# df.to_csv("test1.csv")

# with open("products.txt", "w", encoding="utf-8") as file:
#     for item in data:
#         file.write(f"نام: {item['name']}, قیمت: {item['price']}\n")
# print("اطلاعات با موفقیت ذخیره شد!")

# with open("products.csv", "w", encoding="utf-8", newline="") as file:
#     writer = csv.DictWriter(file, fieldnames=["title", "price"])
#     writer.writeheader()  
#     writer.writerows(df) 
# file.close()

# print("اطلاعات با موفقیت ذخیره شد!")