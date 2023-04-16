import time
import requests
from threading import Thread
import os
import lxml
import pandas as pd
from bs4 import BeautifulSoup
import json


from django.shortcuts import render
import os

# Create your views here.
def bdshop(request):
    return render(request, "bdshop/bdshop.html")

def bdshop_dataset(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
    bdshop_title = []
    bdshop_price = []
    bdshop_image = []
    bdshop_url = []
    bdshop_site = []
    bdshop_result= []
    
    for i in range(1,2):
        site_url = "https://www.bdshop.com/catalogsearch/result/index/?p="+str(i)+"&q="+keyword
        r = requests.head(site_url, allow_redirects=True)
        if r.status_code != 200:
            break
    
        while True:
            try:
                webpage = requests.get(site_url).text
                break
            except:
                time.sleep(10)
          
        soup = BeautifulSoup(webpage, "lxml")

        titles = soup.find_all("h2", class_ ="product name product-item-name")
        prices = soup.find_all("span", {"data-price-type": "finalPrice"})
        images = soup.find_all("span", class_="main-photo")
        urls = soup.find_all("a", class_="product-item-link")

        for j in  range(0, len(titles)):
            title = titles[j].text.replace("&nbsp;", " ")
            price = prices[j].text[1:]
            price = price.translate({ord(','): None})
            price = int(float(price))
            image = images[j].find("img", class_="product-image-photo").get("src")
            url = urls[j].get("href")
            site = "BD Shop"
            bdshop_title.append(title)
            bdshop_price.append(price)
            bdshop_image.append(image)
            bdshop_url.append(url)
            bdshop_site.append(site)
            object = {}
            object["Product Title"] = title
            object["Price"] = price
            object["Image"] = image
            object["Product URL"] = url
            object["Site"] = site
            bdshop_result.append(object)

    time.sleep(0.2)



    sorted_result = sorted(bdshop_result, key=lambda d: d['Price'])
    for i in sorted_result:
        i['Price'] = "Tk "+str(i['Price'])
    final = json.dumps(sorted_result, indent=2)

    with open("media/bdshop_dataset.json", "w") as outfile:
        outfile.write(final)


    bdshop_dict = {"Product Title":bdshop_title ,"Price": bdshop_price, "Image": bdshop_image, "Product URL": bdshop_url, "Site": bdshop_site}
    bdshop_df = pd.DataFrame(bdshop_dict)
    sorted_df = bdshop_df.sort_values(by=['Price'], ascending=True)
    sorted_df = sorted_df.reset_index(drop=True)
    sorted_df['Price'] = 'Tk ' + sorted_df['Price'].astype(str)
    sorted_df.to_csv("media/bdshop_dataset.csv")
    
    return render(request, "bdshop/bdshop_dataset.html")
