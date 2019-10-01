# google_api_image_scrape.py
import io
import csv


def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
         content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    if len(texts) > 0:
        text = response.text_annotations[0].description
    else:
        text = None

    return text

def write_csv_file(input_from_cloud, output_file):

    csv_file = output_file
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for x in input_from_cloud:
                writer.writerows("".join(x))

    except IOError:
        print("I/O error")


def get_book_titles_from_image(input_file_name, outpule_file_name='books.csv'):
    shelves = [detect_test(x) for x in input_file_name]
    write_csv_file(shelves, "books.csv")
