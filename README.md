# BD-eCommerce-Scraper

* A web application to get product information like product title, price, image, URL, site etc. from multiple e-commerce sites.

[Live App](https://bd-ecommerce-scraper.afjol-77.repl.co/) <br>
<br>

![screenshot](https://github.com/Afjol-77/BD-eCommerce-Scraper/blob/main/media/screenshot.png?raw=true)

---

**Features:**
* Scrap for individual ecommerce site as well as multiple sites
* Search any keyword
* All products will be sorted by price in ascending order
* Data can be downloaded as JSON/CSV file 

**Used Technologies:** 
* Django 4
* Bootstrap 5


## How to run this app on your machine? <br>
### 1. Extract and open the project, then install the requirements.txt using pip
```
pip install -r requirements.txt
```
### 2. Create a .env file under 'scraper' directory and put your secret key, database url
```
MY_SECRET_KEY=
DATABASE_URL=
```

### 3. For migrations, type this on your terminal
```
python manage.py makemigrations
python manage.py migrate
```

### 4. Run the server using the following command
```
python manage.py runserver
```

Your Django project is **LIVE** now on your localhost. <br>
Open your browser and type **127.0.0.1:8000** on address bar.<br>
<br>
___
### THANK YOU!

