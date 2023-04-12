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
def evaly(request):
    return render(request,'evaly/evaly.html')

def evaly_dataset(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
    evaly_title = []
    evaly_price = []
    evaly_image = []
    evaly_url = []
    evaly_site = []
    evaly_result= []
    
    for i in range(1,10):
        site_url = "https://evaly.com.bd/search?page="+str(i)+"&term="+keyword
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
        box = soup.find("div", class_="flex gap-4")

        titles = box.find_all("p", class_ ="font-medium text-base line-clamp-2 hover:underline h-[47px]")
        prices = box.find_all("p",class_ ="text-sm font-medium text-gray-800 md:text-lg")
        images = box.find_all("img")
        urls = box.find_all("a")

        for j in  range(0, len(titles)):
            title = titles[j].text
            price = int(prices[j].text[1:])
            image = images[j].get("src")
            url = urls[j].get("href")
            f_url = "https://evaly.com.bd"+url
            site = "Evaly"
            evaly_title.append(title)
            evaly_price.append(price)
            evaly_image.append(image)
            evaly_url.append(f_url)
            evaly_site.append(site)
            object = {}
            object["Product Title"] = title
            object["Price"] = price
            object["Image"] = image
            object["Product URL"] = f_url
            object["Site"] = site
            evaly_result.append(object)

    time.sleep(1)



    sorted_result = sorted(evaly_result, key=lambda d: d['Price'])
    for i in sorted_result:
        i['Price'] = "Tk "+str(i['Price'])
    final = json.dumps(sorted_result, indent=2)

    with open("media/evaly_dataset.json", "w") as outfile:
        outfile.write(final)


    evaly_dict = {"Product Title":evaly_title ,"Price": evaly_price, "Image": evaly_image, "Product URL": evaly_url, "Site": evaly_site}
    evaly_df = pd.DataFrame(evaly_dict)
    sorted_df = evaly_df.sort_values(by=['Price'], ascending=True)
    sorted_df = sorted_df.reset_index(drop=True)
    sorted_df['Price'] = 'Tk ' + sorted_df['Price'].astype(str)
    sorted_df.to_csv("media/evaly_dataset.csv")
    
    return render(request, "evaly/evaly_dataset.html")