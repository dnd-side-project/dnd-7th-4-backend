from django.db import models

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # 최초 생성일
    updated_at = models.DateTimeField(auto_now=True)  # 최초 수정일

# API6 -시도별 실시간 측정정보
class Api6(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    sidoName = models.CharField(max_length=2) # 시도명
    stationName = models.CharField(max_length=10) # 측정소명

    pm10Grade1h = models.IntegerField(null=True, default=0) # 미세먼지 등급
    pm25Grade1h = models.IntegerField(null=True, default=0) # 고농도 미세먼지 등급
    
    pm10Value24 = models.IntegerField(null=True, default=0) # 미세먼지 24시간 예측 등급
    pm25Value24 = models.IntegerField(null=True, default=0) # 고농도 24시간 예측 미세먼지 등급

    def __str__(self):
        return str(self.id)

#  행정구역
class Region(models.Model):
    country = models.CharField(max_length=10)  # 나라
    div_code = models.CharField(max_length=10)  # 행정구역 코드
    city = models.CharField(max_length=20)  # 시, 도 (1단계)
    district = models.CharField(max_length=20)  # 군, 구  (2단계)

    cor_x = models.IntegerField()  # x좌표
    cor_y = models.IntegerField()  # y좌표

    lon_h = models.IntegerField()  # 경도(시)
    lon_m = models.IntegerField()  # 경도(분)
    lon_s = models.FloatField()  # 경도(초)

    lat_h = models.IntegerField()  # 위도(시)
    lat_m = models.IntegerField()  # 위도(분)
    lat_s = models.FloatField()  # 위도(초)

    longitude = models.FloatField()  # 경도(초/100)
    latitude = models.FloatField()  # 위도(초/100)

    api4_code = models.CharField(max_length=20)  # 중기육상예보 api code
    api5_code = models.CharField(max_length=20)  # 중기기온예보 api code
    api6_code = models.CharField(max_length=20)  # 시도별 실시간 측정정보 api code
    api6_station = models.CharField(max_length=20, null=True, default='') # 측정소 데이터
    api10_code = models.IntegerField()  # 종관관측예보 api code

    # FK
    api6_id = models.ForeignKey(Api6, on_delete=models.CASCADE,null=True, default='')

    def __str__(self):
        return self.div_code  # 행정 구역 코드값을 대표값으로

class Api1(Base):
    base_date = models.CharField(max_length=10)
    base_time = models.CharField(max_length=10)
    PTY = models.CharField(max_length=10)  # 강수형태
    REH = models.CharField(max_length=10)  # 습도
    RN1 = models.CharField(max_length=10)  # 1시간 강수량
    T1H = models.CharField(max_length=10)  # 기온
    UUU = models.CharField(max_length=10)  # 동서바람성분
    VEC = models.CharField(max_length=10)  # 풍향
    VVV = models.CharField(max_length=10)  # 남북바람성분
    WSD = models.CharField(max_length=10)  # 풍속

    region = models.OneToOneField(Region, on_delete=models.CASCADE)

# API2 - 초단기 예보 조회
class Api2(Base):
    info_0 = models.TextField()  # 00시에 대한 (기온)/ (하늘상태)/ (강수형태)/ (1시간 강수량) 정보
    info_1 = models.TextField()  # 01시에 대한 (기온)/ (하늘상태)/ (강수형태)/ (1시간 강수량) 정보
    info_2 = models.TextField()
    info_3 = models.TextField()
    info_4 = models.TextField()
    info_5 = models.TextField()
    info_6 = models.TextField()
    info_7 = models.TextField()
    info_8 = models.TextField()
    info_9 = models.TextField()
    info_10 = models.TextField()
    info_11 = models.TextField()
    info_12 = models.TextField()
    info_13 = models.TextField()
    info_14 = models.TextField()
    info_15 = models.TextField()
    info_16 = models.TextField()
    info_17 = models.TextField()
    info_18 = models.TextField()
    info_19 = models.TextField()
    info_20 = models.TextField()
    info_21 = models.TextField()
    info_22 = models.TextField()
    info_23 = models.TextField()

    region = models.OneToOneField(Region, on_delete=models.CASCADE)  # x,y 좌표랑 1:1 mapping


# API2 - 단기예보조회
class Api3(Base):
    info_0 = models.TextField()  # 00시에 대한 (기온)/ (하늘상태)/ (강수형태)/ (1시간 강수량) 정보
    info_1 = models.TextField()
    info_2 = models.TextField()
    info_3 = models.TextField()
    info_4 = models.TextField()
    info_5 = models.TextField()
    info_6 = models.TextField()
    info_7 = models.TextField()
    info_8 = models.TextField()
    info_9 = models.TextField()
    info_10 = models.TextField()
    info_11 = models.TextField()
    info_12 = models.TextField()
    info_13 = models.TextField()
    info_14 = models.TextField()
    info_15 = models.TextField()
    info_16 = models.TextField()
    info_17 = models.TextField()
    info_18 = models.TextField()
    info_19 = models.TextField()
    info_20 = models.TextField()
    info_21 = models.TextField()
    info_22 = models.TextField()
    info_23 = models.TextField()
    info_24 = models.TextField()
    info_25 = models.TextField()
    info_26 = models.TextField()
    info_27 = models.TextField()
    info_28 = models.TextField()
    info_29 = models.TextField()
    info_30 = models.TextField()
    info_31 = models.TextField()
    info_32 = models.TextField()
    info_33 = models.TextField()
    info_34 = models.TextField()
    info_35 = models.TextField()
    info_36 = models.TextField()
    info_37 = models.TextField()
    info_38 = models.TextField()
    info_39 = models.TextField()
    info_40 = models.TextField()
    info_41 = models.TextField()
    info_42 = models.TextField()
    info_43 = models.TextField()
    info_44 = models.TextField()
    info_45 = models.TextField()
    info_46 = models.TextField()
    info_47 = models.TextField()

    info_day0_MAX = models.TextField(null=True, default='')  # 오늘 최고기온
    info_day0_MIN = models.TextField(null=True, default='')  # 오늘 최저기온
    info_day1_MAX = models.TextField(null=True, default='')  # 내일 최고기온
    info_day1_MIN = models.TextField(null=True, default='')  # 내일 최저기온
    info_day2_MAX = models.TextField(null=True, default='')  # 모래 최고기온
    info_day2_MIN = models.TextField(null=True, default='')  # 모래 최저기온
    info_day3_MAX = models.TextField(null=True, default='')  # 글피 최고기온
    info_day3_MIN = models.TextField(null=True, default='')  # 글피 최저기온

    region = models.OneToOneField(Region, on_delete=models.CASCADE)  # x,y 좌표랑 1:1 mapping


# API4 - 중기육상예보조회
class Api4(Base):
    regId = models.CharField(max_length=20)    # 중기육상지역코드 (10개)
    tmFc = models.CharField(max_length=20)     # 관측된 날짜 + 시간

    rnSt3Am = models.CharField(max_length=10)  # 3일 후 오전 강수 확률
    rnSt3Pm = models.CharField(max_length=10)  # 3일 후 오후 강수 확률
    rnSt4Am = models.CharField(max_length=10)  # 4일 후 오전 강수 확률
    rnSt4Pm = models.CharField(max_length=10)  # 4일 후 오후 강수 확률
    rnSt5Am = models.CharField(max_length=10)  # 5일 후 오전 강수 확률
    rnSt5Pm = models.CharField(max_length=10)  # 5일 후 오후 강수 확률
    rnSt6Am = models.CharField(max_length=10)  # 6일 후 오전 강수 확률
    rnSt6Pm = models.CharField(max_length=10)  # 6일 후 오후 강수 확률
    rnSt7Am = models.CharField(max_length=10)  # 7일 후 오전 강수 확률
    rnSt7Pm = models.CharField(max_length=10)  # 7일 후 오후 강수 확률
    rnSt8 = models.CharField(max_length=10)    # 8일 후 강수 확률
    rnSt9 = models.CharField(max_length=10)    # 9일 후 강수 확률
    rnSt10 = models.CharField(max_length=10)   # 10일 후 강수 확률

    wf3Am = models.CharField(max_length=20)    # 3일 후 오전 날씨 예보
    wf3Pm = models.CharField(max_length=20)    # 3일 후 오후 날씨 예보
    wf4Am = models.CharField(max_length=20)    # 4일 후 오전 날씨 예보
    wf4Pm = models.CharField(max_length=20)    # 4일 후 오후 날씨 예보
    wf5Am = models.CharField(max_length=20)    # 5일 후 오전 날씨 예보
    wf5Pm = models.CharField(max_length=20)    # 5일 후 오후 날씨 예보
    wf6Am = models.CharField(max_length=20)    # 6일 후 오전 날씨 예보
    wf6Pm = models.CharField(max_length=20)    # 6일 후 오후 날씨 예보
    wf7Am = models.CharField(max_length=20)    # 7일 후 오전 날씨 예보
    wf7Pm = models.CharField(max_length=20)    # 7일 후 오후 날씨 예보
    wf8 = models.CharField(max_length=20)      # 8일 후 날씨 예보
    wf9 = models.CharField(max_length=20)      # 9일 후 날씨 예보
    wf10 = models.CharField(max_length=20)     # 10일 후 날씨 예보


# API5 - 중기기온조회
class Api5(Base):
    regId = models.CharField(max_length=20)   # 중기기온지역코드
    tmFc = models.CharField(max_length=20)  # 관측된 날짜 + 시간

    taMin3 = models.CharField(max_length=10)  # 3일 후 예상 최저 기온
    taMax3 = models.CharField(max_length=10)  # 3일 후 예상 최고 기온
    taMin4 = models.CharField(max_length=10)  # 4일 후 예상 최저 기온
    taMax4 = models.CharField(max_length=10)  # 4일 후 예상 최고 기온
    taMin5 = models.CharField(max_length=10)  # 5일 후 예상 최저 기온
    taMax5 = models.CharField(max_length=10)  # 5일 후 예상 최고 기온
    taMin6 = models.CharField(max_length=10)  # 6일 후 예상 최저 기온
    taMax6 = models.CharField(max_length=10)  # 6일 후 예상 최고 기온
    taMin7 = models.CharField(max_length=10)  # 7일 후 예상 최저 기온
    taMax7 = models.CharField(max_length=10)  # 7일 후 예상 최고 기온
    taMin8 = models.CharField(max_length=10)  # 8일 후 예상 최저 기온
    taMax8 = models.CharField(max_length=10)  # 8일 후 예상 최고 기온
    taMin9 = models.CharField(max_length=10)  # 9일 후 예상 최저 기온
    taMax9 = models.CharField(max_length=10)  # 9일 후 예상 최고 기온
    taMin10 = models.CharField(max_length=10)  # 10일 후 예상 최저 기온
    taMax10 = models.CharField(max_length=10)  # 10일 후 예상 최고 기온

    # 중기기온코드 지역이 거의 x,y 지역좌표랑 개수가 같아서 1:1로 매핑시킴
    region = models.OneToOneField(Region, on_delete=models.CASCADE)

# API7 -일몰 일출 데이터
class Api7(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    today_sunrise = models.IntegerField() # 오늘 일출
    today_sunset = models.IntegerField() # 오늘 일몰
    tomorrow_sunrise = models.IntegerField(null=True, default=0) # 내일 일출
    tomorrow_sunset = models.IntegerField(null=True, default=0) # 내일 일몰

    # FK
    region_id = models.OneToOneField(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.div_code  # 행정 구역 코드값을 대표값으로

#API8 - 자외선 지수 API
class Api8(Base):

    today = models.IntegerField()  # 오늘 예측값
    tomorrow = models.IntegerField()  # 내일 예측값

    div_code = models.CharField(max_length=10)  # 행정구역 코드

#API9 - 체감온도 API
class Api9(Base):
    temperature = models.CharField(max_length=1500, null=True, default='')

    base_time = models.CharField(max_length=10, null=True, default='')

    div_code = models.CharField(max_length=10)  # 행정구역 코드