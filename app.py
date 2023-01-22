from flask import Flask, jsonify
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


app = Flask(__name__)


@app.route('/notebooks', methods=['GET'])
def search_notebooks():
    service = Service(executable_path='C:/Users/patri/PycharmProjects/webScraper/chromedriver/chromedriver.exe')
    service.start()
    chrome_driver = webdriver.Chrome(service=service)
    chrome_driver.get('https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops')
    page_source = chrome_driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    notebooks_list = []
    for notebook in soup.find_all('div', class_='col-sm-4 col-lg-4 col-md-4'):
        name = notebook.text
        price = notebook.select_one('.price').get_text()
        if 'Lenovo' in name:
            notebooks_list.append({'name': name, 'price': price})

    chrome_driver.quit()
    notebooks_list.sort(key=lambda x: float(x['price'].replace(',', '').replace('$', '')))
    return jsonify(notebooks_list)


if __name__ == '__main__':
    app.run(debug=True)