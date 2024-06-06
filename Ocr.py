import os
import pytesseract
from PIL import Image
import re
import pymongo

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def ocr_images(folder_name='data'):

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["menu_database"]
    collection = db["menu_collection"]

    image_files = [f for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))]
    all_items = []
    all_prices = []

    for image_file in image_files:
        try:
            image_path = os.path.join(folder_name, image_file)
            with Image.open(image_path) as img:
                # Perform OCR on the image to extract text
                text = pytesseract.image_to_string(img)

                items = []
                prices = []

                # Split the text into lines and process each line
                lines = text.split('\n')
                for line in lines:
                    if re.search('[a-zA-Z]', line):
                        items.append(line.strip())
                    # Check if line contains any digit character, if yes, consider it as a price
                    if re.search('\d', line):
                        prices.append(line.strip())

                all_items.extend(items)
                all_prices.extend(prices)        

        except Exception as e:
            print(f"Error processing image {image_file}: {e}")

    print("All Items:", all_items)
    print("All Prices:", all_prices) 

    # Insert all_items and all_prices into MongoDB
    menu_data = {"items": all_items, "prices": all_prices}
    collection.insert_one(menu_data)

    print("Data inserted into MongoDB.")       

ocr_images(folder_name='data')
