import pandas as pd
import plotly.express as px

file_path = 'D:/K22416C/416hk10/dataset-416.xlsx'

xls = pd.ExcelFile(file_path)

print(xls.sheet_names)

df = pd.read_excel(xls, sheet_name='Sheet1')

df.columns = df.columns.str.strip()


df_cleaned = df.dropna(subset=["Mã HP"])
df_cleaned = df_cleaned.dropna(subset=["Học Kỳ"])  # Loại bỏ hàng có NaN trong cột Học Kỳ
df_cleaned["Học Kỳ"] = df_cleaned["Học Kỳ"].apply(pd.to_numeric, errors='coerce')  # Chuyển đổi thành số, lỗi sẽ thành NaN
df_cleaned = df_cleaned.dropna(subset=["Học Kỳ"])  # Tiếp tục loại bỏ các giá trị không hợp lệ
df_cleaned["Học Kỳ"] = df_cleaned["Học Kỳ"].astype(int).astype(str)  # Chuyển sang dạng chuỗi để vẽ biểu đồ


fig = px.sunburst(df_cleaned,
                  path=["Học Kỳ", "Loại môn học", "Tên học phần"],
                  title="Phân bổ học phần theo học kỳ, loại môn học và tên học phần")

fig.show()

# Xuất biểu đồ ra file HTML
fig.write_html('416_10k.html')