import requests as r
import bs4
from datetime import datetime
import time
import schedule
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    product_list = ['B0CHWWW471', 'B0CHX1W1XY', 'B09G9BL5CP','B0CFVBQBB7']
    base_url = 'https://www.amazon.in'
    url = 'https://www.amazon.in/dp/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
    }
    base_response = r.get(base_url, headers=headers)
    cookies = base_response.cookies

    products = []
    for prod in product_list:
        product_reponse = r.get(url + prod, headers=headers, cookies=cookies)
        soup = bs4.BeautifulSoup(product_reponse.text, features='lxml')
        price_lines = soup.find_all(class_="a-price-whole")
        head_lines = soup.find_all(class_='a-size-large product-title-word-break')

        final_price = str(price_lines[0])
        final_head = str(head_lines[0])
        final_price = final_price.replace('<span class="a-price-whole">', '')
        final_price = final_price.replace('<span class="a-price-decimal">.</span></span>', '')
        final_head = final_head.replace('<span class="a-size-large product-title-word-break" id="productTitle">', '')
        final_head = final_head.replace('</span>', '')
        final_head = final_head.strip()

        products.append({'url': url + prod, 'name': final_head, 'cost': final_price})

    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)