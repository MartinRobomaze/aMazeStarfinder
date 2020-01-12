from astropy.time import Time
from datetime import datetime
import math
from object import Object
import location


def eq_to_alt_az(ra, dec, lat, long):
    ra = ra * 15
    time = datetime.utcnow()
    time_hrs = time.hour + time.minute / 60 + time.second / 3600
    time_julian = Time(time)
    time_julian.format = 'jd'
    time_j2000 = time_julian.value - 2451545  # Get J2000 time from substracting julian time of 1.1.2000 12:00 from current julian time.

    local_sid_time = (100.46 + 0.98547 * time_j2000 + long + 15 * time_hrs) % 360

    hour_angle = local_sid_time - ra

    alt = math.degrees(math.asin(math.sin(math.radians(dec)) * math.sin(math.radians(lat)) + math.cos(math.radians(dec)) * math.cos(math.radians(lat)) * math.cos(math.radians(hour_angle))))

    a = math.acos((math.sin(math.radians(dec)) - math.sin(math.radians(alt)) * math.sin(math.radians(lat))) / (math.cos(math.radians(alt)) * math.cos(math.radians(lat))))
    a = math.degrees(a)
    az = 0

    if math.degrees(math.sin(math.radians(hour_angle))) < 0:
        az = a
    else:
        az = 360 - a

    return alt, az


messier_path = 'data/messier-objects.csv'

print('========aMaze STARFINDER========')

objects = {}

with open(messier_path, 'r') as f:
    raw_data = f.read()
    raw_data = raw_data.replace('"', '')
    data_lines = raw_data.split('\n')
    data_lines.pop(0)
    data_lines.pop()
    for data_line in data_lines:
        data = data_line.split(';')
        sky_object = Object(data[0], data[2], data[4], data[6], data[8], data[9])

        objects[sky_object.messier] = sky_object

location_successful = False

lat = 0
long = 0
choice_location = ''
lat_string = ''
long_string = ''

while not location_successful:
    print('Get location from WiFi(poor accuracy)[1] or enter it manually[2]: ')
    choice_location = input()

    if choice_location == '1':
        (lat, long) = location.Location.get_location()
    elif choice_location == '2':
        print('Enter your latitude[dg min sec]: ')
        lat_string = input()
        print('Enter your longitude[dg min sec]: ')
        long_string = input()
    else:
        print('invalid choice')
        continue

    location_successful = True

while True:
    print('Find object[1] or list messier objects[2]: ')
    choice = input()

    if choice == '1':
        print('Enter Messier index of your object: ')
        messier = input()

        print('Object info: \nname:', objects[messier].name, '\nConstellation:', objects[messier].constellation,
              '\nType:', objects[messier].type)

        ra_string = objects[messier].ra
        dec_string = objects[messier].dec
        lat_string = lat_string.split(' ')
        long_string = long_string.split(' ')
        ra_string = ra_string.split(' ')
        dec_string = dec_string.split(' ')

        if choice_location == '1':
            lat = float(lat)
            long = float(long)
        else:
            lat = float(lat_string[0]) + float(lat_string[1]) / 60 + float(lat_string[2]) / 3600
            long = float(long_string[0]) + float(long_string[1]) / 60 + float(long_string[2]) / 3600

        ra = float(ra_string[0]) + float(ra_string[1]) / 60 + float(ra_string[2]) / 3600
        dec = float(dec_string[0]) + float(dec_string[1]) / 60 + float(dec_string[2]) / 3600

        alt, az = eq_to_alt_az(ra, dec, lat, long)
        print('Position of the object[az, alt]: ', az, ', ', alt)
    elif choice == '2':
        print(objects)
        for key, sky_object in objects.items():
            print('name:', sky_object.name, '\tConstellation:', sky_object.constellation,
                  '\tType:', sky_object.type, '\tMessier index: ', sky_object.messier)

    else:
        print('Invalid choice...')
