import mysql.connector

base_config = {
    "host": "localhost",   # MySQL 서버 주소 (로컬)
    "user": "root",        # MySQL 계정
    "password": "1234"     # MySQL 비밀번호
}

# 사용할 데이터베이스 이름
DB_NAME = "homeshopping"

table_name = "homeshopping_sales"

# 커넥션과 커서 반환하는 함수
def get_conn():
    return mysql.connector.connect(**base_config, database=DB_NAME)

def create_database():
    conn = mysql.connector.connect(**base_config)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    conn.commit()
    cursor.close()
    conn.close()

def create_table():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
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
                    )""")
    conn.commit()
    cursor.close()
    conn.close()

def get_all_data():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def insert_data(month, is_promotion, tv_ad_spend, online_ad_spend, price_index, holiday_cnt, competitor_index, sales):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} (month, is_promotion, tv_ad_spend, online_ad_spend, price_index, holiday_cnt, competitor_index, sales) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (month, is_promotion, tv_ad_spend, online_ad_spend, price_index, holiday_cnt, competitor_index, sales))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    try:
        create_database()
    except mysql.connector.Error as err:
        print(f"Database creation failed: {err}")
    try:
        create_table()
    except mysql.connector.Error as err:
        print(f"Table creation failed: {err}")