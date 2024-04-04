import requests
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import os
import pandas as pd



def download_and_extract_kmz(url, extract_to='temp_kml'):
    # Download the KMZ file from googlemymaps
    response = requests.get(url)
    kmz_filename = 'temp.kmz'
    with open(kmz_filename, 'wb') as file:
        file.write(response.content)

    # Extract the KMZ file to temp folder
    with ZipFile(kmz_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    # Cleanup the downloaded KMZ file
    os.remove(kmz_filename)
    return extract_to

def parse_kml_to_dataframe(directory):
    # Find the KML file in the specified directory
    kml_path = None
    for filename in os.listdir(directory):
        if filename.endswith('.kml'):
            kml_path = os.path.join(directory, filename)
            break

    if not kml_path:
        raise FileNotFoundError("No KML file found in the specified directory.")

    # Parse the KML file
    tree = ET.parse(kml_path)
    root = tree.getroot()
    
    # Namespace may be required for finding elements
    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    # create empty list to prepare for data
    data = []

    # Go through each Placemark in the KML file (pin location)
    for placemark in root.findall('.//kml:Placemark', namespace):
        # Initialize a dictionary to store the placemark's data
        placemark_data = {}

        # Extract properties of each element in the placemark if not blank
        placemark_data['Name'] = placemark.find('kml:name', namespace).text if placemark.find('kml:name', namespace) is not None else None
        placemark_data['Address'] = placemark.find('kml:address', namespace).text if placemark.find('kml:address', namespace) is not None else None
        placemark_data['Description'] = placemark.find('kml:description', namespace).text if placemark.find('kml:description', namespace) is not None else None
        
        # Extract the extended data
        for data_element in placemark.findall('.//kml:ExtendedData/kml:Data', namespace):
            # Use the 'name' attribute of the <Data> tag as the key
            key = data_element.get('name')
            # Use the text of the <value> tag as the value
            value = data_element.find('kml:value', namespace).text if data_element.find('kml:value', namespace) is not None else None
            placemark_data[key] = value
        
        # Add the dictionary to our list of data
        data.append(placemark_data)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)
    return df

# URL of the KMZ file to be downloaded and parsed
url = 'URL OF KMZ'
directory = download_and_extract_kmz(url)
df = parse_kml_to_dataframe(directory)

# Specify the path to save the CSV file
csv_file_path = os.path.join(directory, 'parsed_data.csv')
df.to_csv(csv_file_path, index=False)

print(f"Data saved to {csv_file_path}")
