import xml.etree.ElementTree as ET
import pandas as pd
import base64


class KMLParser:

    def __init__(self, kml_filepath):
        self.kml_filepath = kml_filepath

    def parse_kml_to_dataframe(self):
        # Parse the KML file
        root = ET.parse(self.kml_filepath).getroot()
        namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
        data = []

        # Iterate through each Placemark
        for placemark in root.findall('.//kml:Placemark', namespace):
            placemark_dict = {}

            # Extract the name
            #placemark_dict['Name'] = placemark.find('kml:name', namespace).text



            # Extract the extended data
            extended_data = placemark.find('kml:ExtendedData', namespace)
            schema_data = extended_data.find('kml:SchemaData', namespace)
            for simple_data in schema_data.findall('kml:SimpleData', namespace):
                placemark_dict[simple_data.attrib['name']] = simple_data.text

            # Extract the coordinates

            data.append(placemark_dict)

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # Decode any columns with Base64-encoded names
        for column in df.columns:
            if column.startswith('str:'):
                try:
                    decoded_column_name = base64.b64decode(column[4:]).decode('utf-8')
                    df.rename(columns={column: decoded_column_name}, inplace=True)
                except:
                    pass

        return df
# Create an instance of the KMLParser class
parser = KMLParser('')

# Call the parse_kml_to_dataframe function
df = parser.parse_kml_to_dataframe()

df.to_csv('parsed.csv.txt', index=False)
