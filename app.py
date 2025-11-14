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
    competitor_index = np.clip(np.random.normal(1.0,0.1,n_months),0.8,1.3) # 1.0±0.1 정규분포, 0.8~1.3 클립 경쟁 강도 지수

    base_sales = (
        10 * tv_ad_spend + # TV 광고비 10배 영향
        15 * online_ad_spend + # 온라인 광고비 15배 영향
        200 * is_promotion + # 모션 광고 200배 영향
        50 * holiday_cnt + # 휴일 50배 영향
        800 * (price_index - 1.0) + # 물가 800배 영향
        400 * (competitor_index - 1.0) + # 경쟁 400배 영향
        1500 * np.cos(2 * np.pi * months / 12) + # 연말 1500배 영향 (12월 최대값)
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
        "competitor_index": competitor_index,
        "sales": np.round(base_sales,0) # 최종 매출
    })
    return df

def train_model(df):
    # 특징 변수(독립변수) 선택
    X = df[[
        "months", "is_promotion", "tv_ad_spend", "online_ad_spend", "price_index", "holiday_cnt", "competitor_index"
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

@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        # 폼 데이터 가져오기
        months = request.form.getlist('month')
        tv_ad_spends = request.form.getlist('tv_ad_spend')
        online_ad_spends = request.form.getlist('online_ad_spend')
        price_indices = request.form.getlist('price_index')
        holiday_cnts = request.form.getlist('holiday_cnt')
        competitor_indices = request.form.getlist('competitor_index')
        
        # make_data()로 가상 데이터 생성 (기본값 60개)
        df = make_data()
        # 생성된 데이터의 80%로 모델 학습
        model = train_model(df)
        
        num_rows = len(months)
        
        # 프로모션 여부: 첫 번째 행은 'is_promotion', 나머지는 'is_promotion_1', 'is_promotion_2' ...
        is_promotions = []
        # 첫 번째 행의 프로모션 여부
        first_promotion = request.form.get('is_promotion', '0')
        is_promotions.append(first_promotion)
        
        # 나머지 행들의 프로모션 여부 (행 수 기준으로 순서대로 가져오기)
        for i in range(1, num_rows):
            promotion_key = f'is_promotion_{i}'
            promotion_value = request.form.get(promotion_key, '0')  # None이면 기본값 '0' 사용
            is_promotions.append(promotion_value)
        
        for i in range(num_rows):
            month = int(months[i])
            is_promotion = int(is_promotions[i])
            tv_ad_spend = float(tv_ad_spends[i])
            online_ad_spend = float(online_ad_spends[i])
            price_index = float(price_indices[i])
            holiday_cnt = int(holiday_cnts[i])
            competitor_index = float(competitor_indices[i])
            
            X_new = np.array([[month, is_promotion, tv_ad_spend, online_ad_spend, price_index, holiday_cnt, competitor_index]])
            pred_sales = round(model.predict(X_new)[0], 0)
            try:
                db.insert_data(month, is_promotion, tv_ad_spend, online_ad_spend, price_index, holiday_cnt, competitor_index, pred_sales)
            except Exception as e:
                print(f"데이터 삽입 실패: {e}")
        return redirect(url_for('list_data'))
    
    return render_template('add_data.html')

if __name__ == '__main__':
    app.run(debug=True)