from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, get_user_model

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

import requests
from datetime import datetime

from .models import Profile
from .serializers import *
from main.serializers import *
from dnd_7th_4_backend.settings.base import env


# JWT 발급 함수
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),  # access_token 호출
        'refresh': str(refresh)
    }


# 로컬 개발용
@api_view(['POST'])
@permission_classes([AllowAny])
def managerLogin(request, format=None):
    try:
        username = request.data['username']
        password = request.data['password']
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            user = authenticate(username=username, password=password)
            data = {'username': username, 'django_token': get_tokens_for_user(user)}
            return Response(data, status=200)
    except:
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)


# 프론트 요청부분
@api_view(['GET'])
@permission_classes([AllowAny])
def front(request):
    client_id = env('kakao_client_id')
    redirect_uri = env('kakao_redirect_uri')
    response_type = "code"

    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type={response_type}"
    )


# 백엔드 처리부분
@api_view(['GET'])
@permission_classes([AllowAny])
def back(request):

    code = request.GET.get('code', None)

    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
    }
    data = {
        'grant_type': 'authorization_code',
        'client_id': env('kakao_client_id'),
        'redirect_uri': env('kakao_redirect_uri'),
        'code': code
    }

    url = 'https://kauth.kakao.com/oauth/token'

    token_req = requests.post(url, headers=headers, data=data)
    token_req_json = token_req.json()

    kakao_access_token = token_req_json.get("access_token")

    kakao_api_response = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={
            "Authorization": f"Bearer {kakao_access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        },
    )
    kakao_api_response = kakao_api_response.json()
  
    kakao_id = kakao_api_response["id"]
    nickname = kakao_api_response["properties"]["nickname"]
    profile_image = kakao_api_response["properties"]["profile_image"]
    phone_number = kakao_api_response["kakao_account"]["phone_number"]

    profile = Profile.objects.filter(kakao_id=str(kakao_id))

    if profile.exists():
        print("기존 유저")
        user = User.objects.get(username=str(kakao_id))
    else:
        print("새로운 유저")
        user = User.objects.create(username=str(kakao_id))  # unique 값으로 username 넣어야함
        user.save()
        profile = Profile.objects.create(user=user, kakao_id=str(kakao_id), nickname=nickname, profile_image=str(profile_image), phone_number=str(phone_number))
        profile.save()

    return Response({"nickname": nickname,"profile_img": profile_image, "kakao_access_token": kakao_access_token, "django_token": get_tokens_for_user(user)})


# 연결 끊기 -> 로컬 테스트용
def logout(request):
    kakao_access_token = "EcW8_CTN85mbXlR38Nru2qujG0RSfLniZa9-AP5LCisMpwAAAYKu3xw5"  # kakao access token
    data = requests.post("https://kapi.kakao.com/v1/user/unlink",
                         headers={"Authorization": f"Bearer {kakao_access_token}"},
                         )
    print(data.json())
    return Response({"data": "연결 끊기 완료"})


# 백엔드 테스트용
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        username = request.data['username']
        password = request.data['password']
        user = User.objects.get(username=username)

        if not Profile.objects.filter(user=user).exists():
            profile = Profile.objects.create(user=user, nickname=user.username, kakao_id=user.id)
            profile.save()

        if check_password(password, user.password):
            user = authenticate(username=username, password=password)
            data = {'username': username, 'django_token': get_tokens_for_user(user)}
            return Response(data, status=status.HTTP_200_OK)
    except:
        return Response({"message": "로그인 오류"}, status=status.HTTP_400_BAD_REQUEST)


# 카카오톡 알림 설정
class KakaoAlarmView(APIView):
    permission_classes = (AllowAny,)

    # 만약 사용자의 alarm이 on -> off로 off 였으면 on으로 변경
    def post(self, request):
        print('/accout/kakao_alarm : GET -----------------------------')
        try:
            # 받은 데이터
            user = request.user.profile
            
            # 카카오톡 알림 설정하기
            if user.kakao_alarm:
                user.kakao_alarm = False
            else:
                user.kakao_alarm = True
            user.save()

            return Response({"data": ProfileKakaoAlarmSerializers(user).data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f'/accout/kakao_alarm : Error {e} -----------------------------')
            return Response({"message": "요청을 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST)


# 카카오톡 지역 설정
class KakaoRegionView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            print('/account/alarm/region : POST ——————————————')
            # 받은 데이터
            city = request.data["city"]  # 시
            district = request.data["district"]  # 군, 구
            user = request.user.profile # 사용자
            region = Region.objects.filter(city=city, district=district)
            
            if len(region) == 0:
                return Response({'data': '', 'message': f'{city}, {district}에 대한 자원이 존재하지 않습니다.'}, status=status.HTTP_204_NO_CONTENT)
            region = region[0]
            
            if user.kakao_region == region:
                return Response({"message": "이미 저장된 데이터 요청이 들어왔습니다."}, status=status.HTTP_409_CONFLICT)
            else:
                # 알림 지역 갱신하기
                user.kakao_region = region
                user.save()

                data = {}
                data['사용자id'] = user.id
                data['등록된지역'] = RegionSeriallizer(user.kakao_region).data
                return Response({"data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f'/account/alarm/region : Error {e} -----------------------------')
            return Response({"message": "요청을 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST)


# 사용자 지역 생성 및 삭제
class RegionView(APIView):
    permission_classes = (AllowAny,)

    # 도착한 city, district를 사용자 지역으로 생성
    def post(self, request):
        print('/account/region : POST ——————————————')
        try:
            # 받은 데이터
            city = request.data["city"]  # 시
            district = request.data["district"]  # 군, 구
        except Exception as e:
            print(f'/account/alarm/regio : Error {e} -----------------------------')
            return Response({"message": "1-1 요청을 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = request.user.profile # 사용자
        except Exception as e:
            print(f'/account/alarm/regio : Error {e} -----------------------------')
            return Response({"message": "1-2-1 요청을 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            region = Region.objects.filter(city=city, district=district)

        except Exception as e:
            print(f'/account/alarm/regio : Error {e} -----------------------------')
            return Response({"message": "1-2-2 요청을 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            
            if len(region) == 0:
                return Response({'data': '', 'message': f'{city}, {district}에 대한 자원이 존재하지 않습니다.'}, status=status.HTTP_204_NO_CONTENT)
            region = region[0]
            
            try:
                # 이미 user와 region에 대한 데이터가 존재하는 경우
                user_region = User_Region.objects.get(region=region, user=user)
                return Response({"message": "이미 저장된 데이터 요청이 들어왔습니다."}, status=status.HTTP_409_CONFLICT)
            except User_Region.DoesNotExist:

                # user_region 데이터 생성
                user_region = User_Region(user=user, region=region)
                user_region.save()

                data = {}
                data['사용자id'] = user.id
                data['지역'] = RegionSeriallizer(region).data
                return Response({"data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f'/account/alarm/regio : Error {e} -----------------------------')
            return Response({"message": "2 요청을 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST)

    # 도착한 city, district를 사용자 지역 목록에서 삭제
    def delete(self, request):
        print('/account/region : DELETE ——————————————')
        try:
            # 받은 데이터
            city = request.GET.get('city', '')  # 시
            district = request.GET.get('district', '')  # 군, 구

            user = request.user.profile
            region = get_object_or_404(Region, city=city, district=district)

            try:
                # 지역 목록에서 삭제
                user_region = User_Region.objects.get(region=region, user=user)
                user_region.delete()
                return Response({'message': "삭제가 완료되었습니다"}, status=status.HTTP_200_OK)
            except User_Region.DoesNotExist:
                # 요청한 데이터가 사용자에게 등록이 되어 있지 않았던 경우
                return Response({'data': '', 'message': f'{city}, {district}에 대한 자원이 존재하지 않습니다. '}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            print(f'/account/region : Error {e} -----------------------------')
            return Response({"message": "요청을 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST)


# 등록 지역 목록 API 반환
class RegisterRegionView(APIView):

    def get(self, request):
        imgs = {
            "맑음": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%A7%80%EC%97%AD%EB%AA%A9%EB%A1%9D+%EC%9D%BC%EB%9F%AC%EC%8A%A4%ED%8A%B8/%EC%A7%80%EC%97%AD%EB%AA%A9%EB%A1%9D_%EB%A7%91%EC%9D%8C.png",
            "구름많음": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%A7%80%EC%97%AD%EB%AA%A9%EB%A1%9D+%EC%9D%BC%EB%9F%AC%EC%8A%A4%ED%8A%B8/%EC%A7%80%EC%97%AD%EB%AA%A9%EB%A1%9D_%EA%B5%AC%EB%A6%84%EB%A7%8E%EC%9D%8C.png",
            "흐림": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%A7%80%EC%97%AD%EB%AA%A9%EB%A1%9D+%EC%9D%BC%EB%9F%AC%EC%8A%A4%ED%8A%B8/%EC%A7%80%EC%97%AD%EB%AA%A9%EB%A1%9D_%EB%A7%A4%EC%9A%B0%ED%9D%90%EB%A6%BC.png",
            "약한비": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%A7%80%EC%97%AD%EB%AA%A9%EB%A1%9D+%EC%9D%BC%EB%9F%AC%EC%8A%A4%ED%8A%B8/%EC%A7%80%EC%97%AD%EB%AA%A9%EB%A1%9D_%EC%95%BD%ED%95%9C+%EB%B9%84.png",
            "중간비": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%A7%80%EC%97%AD%EB%AA%A9%EB%A1%9D+%EC%9D%BC%EB%9F%AC%EC%8A%A4%ED%8A%B8/%EC%A7%80%EC%97%AD%EB%AA%A9%EB%A1%9D_%EC%A4%91%EA%B0%84+%EB%B9%84.png",
            "강한비": "https://weathercomment.s3.ap-northeast-2.amazonaws.com/%EC%A7%80%EC%97%AD%EB%AA%A9%EB%A1%9D+%EC%9D%BC%EB%9F%AC%EC%8A%A4%ED%8A%B8/%EC%A7%80%EC%97%AD%EB%AA%A9%EB%A1%9D_%EA%B0%95%ED%95%9C+%EB%B9%84.png"
        }

        try:
            profile = request.user.profile
            user_regions = User_Region.objects.filter(user=profile)
            res = dict()
            for user_region in user_regions:
                city = user_region.region.city
                district = user_region.region.district
                region = user_region.region

                api1 = Api1.objects.get(region=region)
                temperature = api1.T1H  # 현재 기온
                PTY = api1.PTY  # 강수 형태(코드값으로 받음)

                ## 강수 형태 -> 없음(맑음, 구름많음, 흐림) / 있음(비) 기준으로 1차 판별

                # 강수 형태 "없음" -> "하늘상태"로 판별
                if PTY == "0":
                    api2 = Api2.objects.get(region=region)
                    h = int(datetime.now().strftime("%H"))  # 현재 시각
                    field = f'info_{h}'
                    str = (api2.serializable_value(field)).replace(" ", "")
                    f_list = str.split('/')
                    SKY = f_list[1]  # 현재 하늘 상태
                    img_url = imgs[SKY]

                # 강수 형태 있음 -> "비"
                else:
                    rn1 = api1.RN1
                    rn1 = rn1.replace("mm", "")
                    rn1 = float(rn1)  # data-type 맞추기
                    if rn1 >= 15:
                        img_url = imgs["강한비"]
                    elif 3 <= rn1 < 15:
                        img_url = imgs["중간비"]
                    else:
                        img_url = imgs["약한비"]

                d = {"지역": city + " " + district,
                      "이미지url": img_url,
                      "현재기온": temperature}
                res[f'{len(res)}'] = d

            return Response({"data": res}, status=status.HTTP_200_OK)

        except:
            return Response({"data": ""}, status=status.HTTP_200_OK)