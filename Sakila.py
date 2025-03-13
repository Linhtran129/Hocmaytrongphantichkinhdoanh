from flask import Flask
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)

# Thông tin kết nối
config = {
    'user': 'root',
    'password': '@Obama123',
    'host': 'localhost',
    'database': 'sakila',
}

# Kết nối với MySQL
conn = mysql.connector.connect(**config)

def queryDataset(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    return df

# Truy vấn dữ liệu từ các bảng
sql_customer = "SELECT * FROM customer"
sql_rental = "SELECT * FROM rental"
sql_inventory = "SELECT * FROM inventory"
sql_film = "SELECT * FROM film"

df_customer = queryDataset(conn, sql_customer)
df_rental = queryDataset(conn, sql_rental)
df_inventory = queryDataset(conn, sql_inventory)
df_film = queryDataset(conn, sql_film)

print(df_customer)
print(df_rental)
print(df_inventory)
print(df_film)

# Kết hợp dữ liệu từ bảng Rental và Inventory
df_rental_inventory = pd.merge(df_rental, df_inventory, on='inventory_id')

# Kết hợp thêm thông tin từ bảng Film
df_rental_inventory_film = pd.merge(df_rental_inventory, df_film, on='film_id')

# Kết hợp thông tin khách hàng
df_final = pd.merge(df_rental_inventory_film, df_customer, on='customer_id', suffixes=('_rental', '_customer'))

# Kiểm tra giá trị thiếu
print(df_final.isnull().sum())

# Loại bỏ các cột không cần thiết
df_final = df_final[['customer_id', 'rental_id', 'film_id', 'rental_date',
                     'return_date', 'title', 'rental_duration', 'rental_rate', 'original_language_id']]

# Tính số lần thuê phim của mỗi khách hàng
customer_rental_count = df_final.groupby('customer_id').size().reset_index(name='rental_count')

# Tính tổng chi phí thuê phim của mỗi khách hàng
customer_rental_cost = df_final.groupby('customer_id')['rental_rate'].sum().reset_index(name='total_rental_cost')

# Kết hợp thông tin
df_clustering = pd.merge(customer_rental_count, customer_rental_cost, on='customer_id')

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df_clustering_scaled = scaler.fit_transform(df_clustering[['rental_count', 'total_rental_cost']])

inertia = []
K = range(1, 10)
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(df_clustering_scaled)
    inertia.append(kmeans.inertia_)

plt.plot(K, inertia, 'bx-')
plt.xlabel('Số cụm (k)')
plt.ylabel('Inertia')
plt.title('Phương pháp Elbow')
plt.show()


kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(df_clustering_scaled)
df_clustering['Cluster'] = kmeans.labels_

print(df_clustering.groupby('Cluster').mean())

plt.scatter(df_clustering['rental_count'], df_clustering['total_rental_cost'], c=df_clustering['Cluster'], cmap='viridis')
plt.xlabel('Số lần thuê phim')
plt.ylabel('Tổng chi phí thuê phim')
plt.title('Gom cụm khách hàng')
plt.show()
