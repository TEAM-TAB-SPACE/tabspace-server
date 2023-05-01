# tabspace-server
온라인 강의 플랫폼 탭스페이스 서버

배포url: https://tab.tabspace.site

기술스택: NEXT.js(프론트엔드) + Django(백엔드)
장고 라이브러리: rest_framework, rest_framework_simplejwt, corsheaders, django_crontab, storages

주요 구현 사항:
- 오늘의 강의 기능 구현

: 전체 강의 목록을 한 달 평일 수에 맞춰 스케줄링 자동화(서버 예약 작업 : 매달 1일 자정, 국경일 API 사용)

: 오늘의 강의 상태 업데이트(서버 예약 작업: 평일 자정)

- 학습관리 시스템(LMS) 구현

: 강의 진도율 계산 알고리즘 구현 

: 강의 카테고리 별 강의 수강률 기반 능력 신장률 계산 알고리즘 구현 (오각형 그래프)

: 출석률 계산 알고리즘 구현(오늘의 강의 모두 수강 시 출석/ 서버 예약 작업: 화-토 자정)

- 과제 제출/다운로드/삭제 구현(AWS S3)

시연영상:
![탭스페이스_시연영상_light](https://user-images.githubusercontent.com/120891914/235433716-7d29536b-bbfe-45aa-83fd-794b2d8f4b4d.gif)

<img width="100%" src="https://ds3h3lok6dodu.cloudfront.net/video/탭스페이스_시연영상_light.gif"/>

서버 아키텍처:
![image](https://user-images.githubusercontent.com/120891914/235428839-6124c0d5-0b51-449e-be0f-d2490ba98096.png)

데이터베이스 구조
![models](https://user-images.githubusercontent.com/120891914/235426965-0f6fc32d-8c17-48b9-8844-c4194645c6b3.png)
