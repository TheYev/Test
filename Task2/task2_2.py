import os
import json
import argparse
import xml.etree.ElementTree as ET
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_product(product):
    try:
        product['id'] = int(product['id'])
        product['price'] = float(product['price'])
        if product['id'] <= 0 or product['price'] <= 0:
            raise ValueError("ID and price weill be biger then 0.")
        return True
    except (ValueError, KeyError, TypeError) as e:
        logging.error(f"Validation error {product}: {e}")
        return False

def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        product = {child.tag: child.text for child in root}
        if validate_product(product):
            return product
    except ET.ParseError as e:
        logging.error(f"XML parse error {file_path}: {e}")
    return None

def process_files(input_dir, output_dir):
    print(input_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".xml"):
            file_path = os.path.join(input_dir, file_name)
            product = parse_xml(file_path)
            if product:
                json_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.json")
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(product, f, indent=4)
                logging.info(f"Saved: {json_file}")

def main():
    parser = argparse.ArgumentParser(description="Convert XML to JSON")
    parser.add_argument("--input-dir", required=True, help="Directory with XML files")
    parser.add_argument("--output-dir", required=True, help="Directory with JSON files")
    args = parser.parse_args()
    
    process_files(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()
