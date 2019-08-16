import re

import requests

url = 'https://openlibrary.org/api/books?bibkeys=ISBN:9780980200447&jscmd=data&format=json'

response = requests.get(url)

print('All info about this book is{}'.format(response.text))

dewey_pattern = re.compile('(\d{3}/.\d)')

dewey_decimal_of_the_book = dewey_pattern.findall(response.text)[0]

print('Dewey decimal code of the book is {}'.format(dewey_decimal_of_the_book))
