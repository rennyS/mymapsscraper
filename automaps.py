import requests
import xml.etree.ElementTree as ET
import pandas as pd
kml_url = ''


def download_kml(url, save_to='temp_kml'):
    # Download the KMZ file from googlemymaps
    response = requests.get(url)
    with open(save_to,'wb') as file:
        file.write(response.content)
    return save_to



def parse_kml_to_dataframe(kml_file, desired_keys=None):
    # If no specific keys provided, consider all keys
    if desired_keys is None:
        desired_keys = ['Approximate Attendance','Start Time','Date of Protest', 'City', 'Postcode']

    # Parse the KML file
    tree = ET.parse(kml_file)
    root = tree.getroot()
    
    # Namespace may be required for finding elements
    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    # Initialize an empty list to hold the parsed data
    data = []

    # Iterate through each Placemark
    for placemark in root.findall('.//kml:Placemark', namespace):
        placemark_data = {}

        # Extract simple properties
        placemark_data['Name'] = placemark.find('kml:name', namespace).text if placemark.find('kml:name', namespace) is not None else None
        placemark_data['Address'] = placemark.find('kml:address', namespace).text if placemark.find('kml:address', namespace) is not None else None

        
        # Extract ExtendedData only for desired keys
        for data_element in placemark.findall('.//kml:ExtendedData/kml:Data', namespace):
            key = data_element.get('name')
            if key in desired_keys or not desired_keys:
                value = data_element.find('kml:value', namespace).text if data_element.find('kml:value', namespace) is not None else None
                placemark_data[key] = value
        
        # Add the dictionary to our list of data
        data.append(placemark_data)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)
    return df
    
def correct_attendance(value):
    # Corrects "Oct-50" to "10-50"
    if value == "Oct-50":
        return "10-50"
    if value =="1-Oct":
        return "1-10"
    return value

# Assuming 'df' is your DataFrame after parsing the KML
# Apply correction to the 'Approximate Attendance' column


# Now, df has the corrected values for "Approximate Attendance"


# URL of the KMZ file to be downloaded and parsed

kml_file = download_kml(kml_url)

desired_keys = ['Approximate Attendance','Start Time','Date of Protest', 'City', 'Postcode']
# Call the parsing function with the list of desired keys
df = parse_kml_to_dataframe(kml_file, desired_keys)
df['Approximate Attendance'] = df['Approximate Attendance'].apply(correct_attendance)
df['Approximate Attendance'] = df['Approximate Attendance'].fillna('N/A')
# Proceed to save the DataFrame to CSV as before
csv_file_path = 'filtered_data.csv'
df.to_csv(csv_file_path, index=False)

print(f"Filtered data saved to {csv_file_path}")
