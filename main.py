import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_books():
    books = []

    for page_num in range(1, 50):
        url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to get page: {url}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        book_elements = soup.find_all('article', class_='product_pod')

        for book_element in book_elements:
            book = parse_book_element(book_element)
            if book is not None:
                books.append(book)
                print(book['title'])

    return books

def parse_book_element(book_element):
    try:
        image_element = book_element.find('img')
        title = image_element['alt']

        rating_element = book_element.find('p')
        rating = rating_element['class'][1]

        price_element = book_element.find('p', class_='price_color')
        price = float(price_element.text[1:])

        return {'title': title, 'rating': rating, 'price': price}
    except Exception as e:
        print(f"Failed to parse book element. Error: {e}")
        return None

def save_to_csv(books):
    df = pd.DataFrame(books)
    df.to_csv('books.csv', index=False)

def main():
    books = scrape_books()
    save_to_csv(books)

if __name__ == "__main__":
    main()
