# 홈쇼핑 매출 예측 프로그램

Flask 기반 웹 애플리케이션으로 홈쇼핑 매출을 예측하고 시각화하는 프로그램입니다.

## 주요 기능

- **매출 예측**: 월, 프로모션 여부, 광고비, 물가지수, 휴일 일수, 경쟁 강도 등을 입력하여 예상 매출을 예측
- **데이터 입력**: 여러 행의 데이터를 한 번에 입력 가능 (동적 행 추가)
- **데이터 목록**: 저장된 예측 데이터를 테이블 형식으로 조회
- **데이터 시각화**: Chart.js를 사용한 막대 그래프로 예상 매출 시각화
- **상세 정보**: 차트에서 각 막대에 마우스를 올리면 해당 예측의 모든 입력 정보 표시

## 기술 스택

- **Backend**: Flask, Python 3
- **Database**: MySQL
- **Machine Learning**: scikit-learn (LinearRegression)
- **Data Processing**: pandas, numpy
- **Frontend**: HTML, CSS, JavaScript
- **Visualization**: Chart.js

## 프로젝트 구조

```
homeshopping-sales-prediction/
├── app.py                 # Flask 애플리케이션 메인 파일
├── db.py                  # 데이터베이스 연결 및 CRUD 함수
├── templates/             # HTML 템플릿
│   ├── layout.html        # 기본 레이아웃
│   ├── index.html         # 메인 페이지
│   ├── add_data.html      # 데이터 입력 페이지
│   ├── list_data.html     # 데이터 목록 페이지
│   └── chart_data.html    # 데이터 그래프 페이지
├── static/
│   ├── css/
│   │   └── style.css      # 스타일시트
│   └── js/
│       ├── add_data.js    # 입력 행 추가 JavaScript
│       └── chart_data.js  # 차트 시각화 JavaScript
└── README.md
```

## 설치 및 실행

### 필요 조건

- Python 3.x
- MySQL Server
- 필요한 Python 패키지:
  ```
  Flask
  mysql-connector-python
  numpy
  pandas
  scikit-learn
  ```

### 설치 방법

1. 저장소 클론 또는 다운로드

2. Python 패키지 설치
   ```bash
   pip install flask mysql-connector-python numpy pandas scikit-learn
   ```

3. MySQL 데이터베이스 설정
   - `db.py` 파일의 `base_config`에서 MySQL 연결 정보 수정 (host, user, password)
   - MySQL 서버가 실행 중인지 확인
   - `db.py` 실행하여 데이터베이스와 테이블 자동 생성
     ```bash
     python db.py
     ```
   - 실행 시 `homeshopping` 데이터베이스와 `homeshopping_sales` 테이블이 자동으로 생성됩니다.

4. 애플리케이션 실행
   ```bash
   python app.py
   ```

5. 브라우저에서 접속
   ```
   http://localhost:5000
   ```

## 사용 방법

### 1. 데이터 입력
- "데이터 입력" 메뉴에서 예측에 필요한 정보 입력
- 월, 프로모션 여부, TV 광고비, 온라인 광고비, 물가 지수, 휴일 일수, 경쟁 강도 입력
- "입력 행 추가" 버튼으로 여러 행 추가 가능
- "데이터 저장" 버튼으로 예측 실행 및 저장

### 2. 데이터 목록
- "데이터 목록" 메뉴에서 저장된 모든 예측 데이터 조회

### 3. 데이터 그래프
- "데이터 그래프" 메뉴에서 예상 매출을 막대 그래프로 시각화
- 각 막대에 마우스를 올리면 상세 입력 정보 확인 가능

## 예측 모델

- **모델 타입**: 선형 회귀 (Linear Regression)
- **학습 데이터**: 60개의 가상 데이터 생성
- **학습/테스트 분할**: 80% 학습, 20% 테스트
- **입력 변수**:
  - 월 (1-12)
  - 프로모션 여부 (0: 비프로모션, 1: 프로모션)
  - TV 광고비 (만원)
  - 온라인 광고비 (만원)
  - 물가 지수
  - 휴일 일수
  - 경쟁 강도 지수

## 데이터베이스 스키마

```sql
CREATE TABLE homeshopping_sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    month INT,
    is_promotion TINYINT,
    tv_ad_spend DOUBLE,
    online_ad_spend DOUBLE,
    price_index DOUBLE,
    holiday_cnt INT,
    competitor_index DOUBLE,
    sales DOUBLE
)
```

## 주요 파일 설명

- **app.py**: Flask 라우트, 모델 학습 및 예측 로직
- **db.py**: MySQL 데이터베이스 연결 및 CRUD 작업
- **add_data.js**: 입력 행 동적 추가 기능
- **chart_data.js**: Chart.js를 사용한 차트 시각화
- **style.css**: 전역 스타일시트
