from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import db

app = Flask(__name__)

def make_data(n_months=60, seed=85):
    np.random.seed(seed) # 랜덤 시드 고정
    months = np.tile(np.arange(1,13), n_months // 12 + 1)[:n_months] # 12개월 반복
    is_promotion = np.random.choice([0,1], size=n_months, p=[0.65,0.35]) # 65% 확률로 0, 35% 확률로 1
    tv_ad_spend = np.random.normal(250,30,n_months) # 250±30 정규분포 TV 광고비
    online_ad_spend = np.random.normal(120,20,n_months) # 120±20 정규분포 온라인 광고비
    price_index = 1.0+np.random.normal(0.05,0.02,n_months) # 1.0±0.05 정규분포 물가상승 효과
    holiday_cnt = np.random.randint(0,5,n_months) # 0~4 정수 랜덤 휴일
    competiter_index = np.clip(np.random.normal(1.0,0.1,n_months),0.8,1.3) # 1.0±0.1 정규분포, 0.8~1.3 클립 경쟁 강도 지수
    
    base_sales = (
        10 * tv_ad_spend + # TV 광고비 10배 영향
        15 * online_ad_spend + # 온라인 광고비 15배 영향
        200 * is_promotion + # 모션 광고 200배 영향
        50 * holiday_cnt + # 휴일 50배 영향
        800 * (price_index - 1.0) + # 물가 800배 영향
        400 * (competiter_index - 1.0) + # 경쟁 400배 영향
        1500 * np.sin(2 * np.pi * months / 12) + # 연말 1500배 영향
        np.random.normal(0,200,n_months) # 약간의 잡음
    )
    
    # df 형태로 정리
    df = pd.DataFrame({
        "months": months,
        "is_promotion": is_promotion,
        "tv_ad_spend": np.round(tv_ad_spend,1),
        "online_ad_spend": np.round(online_ad_spend,1),
        "price_index": np.round(price_index,3),
        "holiday_cnt": holiday_cnt,
        "competiter_index": competiter_index,
        "sales": np.round(base_sales,0) # 최종 매출
    })
    return df

def train_model(df):
    # 특징 변수(독립변수) 선택
    X = df[[
        "months", "is_promotion", "tv_ad_spend", "online_ad_spend", "price_index", "holiday_cnt", "competiter_index"
    ]]
    y = df["sales"]

    # 훈련 데이터와 테스트 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # 모델 생성
    model = LinearRegression()
    model.fit(X_train, y_train)
    print("훈련 성공")

    return model

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list_data')
def list_data():
    list_data = db.get_all_data()
    return render_template('list_data.html', list_data=list_data)

if __name__ == '__main__':
    app.run(debug=True)