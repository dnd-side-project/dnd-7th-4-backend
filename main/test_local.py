# 로컬 db data input 용

import csv
import os
import django
import sys

# 현재 디렉토리 경로 표시
os.chdir(".")
print("Current dir=", end=""), print(os.getcwd())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR=", end=""), print(BASE_DIR)

sys.path.append(BASE_DIR)

# 프로젝트명.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_7th_4_backend.settings")
django.setup()

from main.models import *

# csv 파일 경로
CSV_PATH = '../region.csv'

# encoding 설정 필요
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        # print(row['구분'], row['행정구역코드'], row['1단계'], row['2단계'],
        #       row['격자 X'], row['격자 Y'],
        #       row['경도(시)'], row['경도(분)'], row['경도(초)'],
        #       row['위도(시)'], row['위도(분)'], row['위도(초)'],
        #       row['경도(초/100)'], row['위도(초/100)'],
        #       row['미세먼지API'], row['중기육상예보구역'], row['중기기온예보구역'], row['전일종관관측코드'])

        Region.objects.create(
            country=row['country'],
            div_code=row['div_code'],
            city=row['city'],
            district=row['district'],
            cor_x=row['cor_x'],
            cor_y=row['cor_y'],
            lon_h=row['lon_h'],
            lon_m=row['lon_m'],
            lon_s=row['lon_s'],
            lat_h=row['lat_h'],
            lat_m=row['lat_m'],
            lat_s=row['lat_s'],
            longitude=row['longitude'],
            latitude=row['latitude'],
            api4_code=row['api4_code'],
            api5_code=row['api5_code'],
            api6_code=row['api6_code'],
            api10_code=row['api10_code']
        )
