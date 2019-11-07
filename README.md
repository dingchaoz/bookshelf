## Zhengli

Zhengli---Catalogue and organize your book collection based off images shot from your camera. We are offering an API service
that uses data science to automatically detect and recognize books that it finds in user submitted images of bookshelves. 

Future Features:
Organize books by genre and categories.

## How to use Zhengli
```
git clone https://github.com/dingchaoz/bookshelf.git
docker build -t zhengli .
docker run --rm -p 5000:8080 shelf 
```
then send a book shelf image to the service
```
curl -X POST -H 'content-type: application/json' --data '{"file":"IMG_20190904_155939359.jpg"}' http://127.0.0.1:5000/api
```
sample information returned about the books from the shelf image
```

```

## How does Zhengli work?
At a high level, Zhengli uses a combination of computer vision, image processing, and natural language processing to detect books in images of bookshelves. Breaking it down a little further, these are the main steps involved. A more detailed description of each step in the algorithm is presented in the following sections.

Zhengli's algorithm:

Detect all instances of book shapes in the image
Split books into individual one by its spine
Detect all instances of text in each book image
Spell correct text detected
Extract book title, publisher, author from detected text associated with a book
Perform a search on the book, titile and publisher for a match on open library API
Validate the book using its original camera image and its image on open library website
Get the ISBN number from the book
Get the Deway Decimal number and other
Return the following information about the books: title, author, publisher, publishing date, ISBN, deway decimal number.


### Create virtual environment

Each project is self contained and has requires specific in a `requirements.txt`
To make things isolated, for each project you will create a separate
python virtual environment. This allows us to separate our dependancies and track them.

You will need to have python 3.7.4 in your path.

If it is your first time in a project:
```
python -m venv .venv
source .venv/bin/activate
cd bookshelf
pip install -r requirements.txt
```
To install the our book organizing library(package named as zhengli for now), run:
```
pip install -e .
```
Confirm zhengli is installed correctly, run the following in Python terminal:
```
import zhengli
from zhengli.core import dewey_decimal_api
```

## WARNING that this line should only be run when a completely new virual environment is created:
```
python -m venv .venv
```
## Recreate virtual environment with the same name will wipe out all previous installed packages.
After virtual venv is created, we only need to run the following line to enter the virtual venv to use it:
```
source .venv/bin/activate
```
If there a requirements.txt need to be created or updated:
```
pip freeze > requirements.txt
```
Or when you add a new dependency to your project you can manually add it to the
`requirements.txt` file.

To exit virtual environment in terminal
```
deactivate
```

