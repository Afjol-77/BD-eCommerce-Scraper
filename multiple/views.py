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
def multiple(request):
	return render(request, "multiple/multiple.html")


def evaly_dataset(request):
	if 'keyword' in request.GET:
		keyword = request.GET['keyword']
	
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
			multiple_result.append(object)

	time.sleep(1)

def bdshop_dataset(request):
	if 'keyword' in request.GET:
		keyword = request.GET['keyword']
	
	for i in range(1,10):
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
			multiple_result.append(object)

	time.sleep(1)


def gadgetandgear_dataset(request):
	if 'keyword' in request.GET:
		keyword = request.GET['keyword']

	
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
			multiple_result.append(object)
	time.sleep(1)

evaly_title = []
evaly_price = []
evaly_image = []
evaly_url = []
evaly_site = []
bdshop_title = []
bdshop_price = []
bdshop_image = []
bdshop_url = []
bdshop_site = []
gng_title = []
gng_price = []
gng_image = []
gng_url = []
gng_site = []
multiple_result= []


def multiple_dataset(request):
	evaly_dataset(request)
	gadgetandgear_dataset(request)
	bdshop_dataset(request)

	sorted_result = sorted(multiple_result, key=lambda d: d['Price'])
	for i in sorted_result:
		i['Price'] = "Tk "+ str(i['Price'])
	final = json.dumps(sorted_result, indent=2)

	with open("media/multiple_dataset.json", "w") as outfile:
		outfile.write(final)

	evaly_dict = {"Product Title":evaly_title ,"Price": evaly_price, "Image": evaly_image, "Product URL": evaly_url, "Site": evaly_site}
	evaly_df = pd.DataFrame(evaly_dict)
	gng_dict = {"Product Title":gng_title ,"Price": gng_price, "Image": gng_image, "Product URL": gng_url, "Site": gng_site}
	gng_df = pd.DataFrame(gng_dict)
	bdshop_dict = {"Product Title":bdshop_title ,"Price": bdshop_price, "Image": bdshop_image, "Product URL": bdshop_url, "Site": bdshop_site}
	bdshop_df = pd.DataFrame(bdshop_dict)

	temp_df1 = pd.concat([evaly_df, gng_df])
	temp_df2 = pd.concat([temp_df1, bdshop_df])
	sorted_df = temp_df2.sort_values(by=['Price'], ascending=True)
	sorted_df = sorted_df.reset_index(drop=True)
	sorted_df['Price'] = 'Tk ' + sorted_df['Price'].astype(str)
	sorted_df.to_csv("media/multiple_dataset.csv")

	return render(request, "multiple/multiple_dataset.html")