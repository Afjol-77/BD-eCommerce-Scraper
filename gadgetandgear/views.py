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
def gadgetandgear(request):
    return render(request, "gadgetandgear/gadgetandgear.html")

def gadgetandgear_dataset(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
    gng_title = []
    gng_price = []
    gng_image = []
    gng_url = []
    gng_site = []
    gng_result= []
    
    for i in range(1,10):
        site_url = "https://gadgetandgear.com/search?keyword="+keyword+"&page="+str(i)
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
        box = soup.find("div", class_="col-12 mt-3 px-lg-0")

        titles = box.find_all("p", class_ ="product-name d-block mb-0")
        prices = box.find_all("p",class_ ="product-price text-bold mb-0")
        images = box.find_all("img")
        urls = box.find_all("a")

        for j in  range(0, len(titles)):
            title = titles[j].text
            price = prices[j].text.strip()
            price = price.translate({ord('\n'): None})
            pos = 0
            cnt = 0
            for k in range(0, len(price)-1):
                if price[k] == 'T':
                    cnt += 1
                if cnt == 2:
                    pos = k
                    break
            if cnt == 2:
                price = price[:pos]
            price = price.translate({ord(','): None})
            price = price[4:]
            price = int(float(price))
            image = images[j].get("data-src")
            url = urls[j].get("href")
            site = "GadgetandGear"
            
            gng_title.append(title)
            gng_price.append(price)
            gng_image.append(image)
            gng_url.append(url)
            gng_site.append(site)
            object = {}
            object["Product Title"] = title
            object["Price"] = price
            object["Image"] = image
            object["Product URL"] = url
            object["Site"] = site
            gng_result.append(object)

    time.sleep(1)



    sorted_result = sorted(gng_result, key=lambda d: d['Price'])
    for i in sorted_result:
        i['Price'] = "Tk "+str(i['Price'])
    final = json.dumps(sorted_result, indent=2)

    with open("media/gng_dataset.json", "w") as outfile:
        outfile.write(final)


    gng_dict = {"Product Title":gng_title ,"Price": gng_price, "Image": gng_image, "Product URL": gng_url, "Site": gng_site}
    gng_df = pd.DataFrame(gng_dict)
    sorted_df = gng_df.sort_values(by=['Price'], ascending=True)
    sorted_df = sorted_df.reset_index(drop=True)
    sorted_df['Price'] = 'Tk ' + sorted_df['Price'].astype(str)
    sorted_df.to_csv("media/gng_dataset.csv")
    
    return render(request, "gadgetandgear/gadgetandgear_dataset.html")