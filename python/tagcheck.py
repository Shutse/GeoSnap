import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    
    if exif_data is not None:
        exif = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            exif[tag_name] = value
        return exif
    return None

def get_gps_info(exif_data):
    if 'GPSInfo' in exif_data:
        gps_info = {}
        for key, value in exif_data['GPSInfo'].items():
            tag_name = GPSTAGS.get(key, key)
            gps_info[tag_name] = value
        return gps_info
    return None

def convert_to_degrees(value):
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

def get_coordinates(gps_info):
    if gps_info and 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info:
        lat = convert_to_degrees(gps_info['GPSLatitude'])
        lon = convert_to_degrees(gps_info['GPSLongitude'])
        
        if gps_info.get('GPSLatitudeRef') == 'S':
            lat = -lat
        if gps_info.get('GPSLongitudeRef') == 'W':
            lon = -lon
            
        return lat, lon
    return None, None

image_path = os.path.join('..', 'tests', 'geotagged', '1.jpg')

if os.path.exists(image_path):
    exif_data = get_exif_data(image_path)
    
    if exif_data:
        print("EXIF data:")
        for tag, value in exif_data.items():
            print(f"{tag}: {value}")
        
        gps_info = get_gps_info(exif_data)
        if gps_info:
            print("\nGPS data:")
            for tag, value in gps_info.items():
                print(f"{tag}: {value}")
            
            lat, lon = get_coordinates(gps_info)
            if lat and lon:
                print(f"\ncoords: {lat}, {lon}")
        else:
            print("\nnot found: gps")
    else:
        print("not found: exif")
else:
    print("not found: file")
