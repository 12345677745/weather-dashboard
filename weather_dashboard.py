import requests
import streamlit as st
import pandas as pd

st.set_page_config(page_title="台灣氣象資料 Dashboard", page_icon="🌦️", layout="wide")
st.title("🌦️ 台灣氣象資料 Dashboard")

# ✅ 你的中央氣象署授權碼
API_KEY = "CWA-C0931842-A3DF-41E7-AF99-1007BC492006"

# ✅ 城市名稱必須與資料集一致（如台北市、新北市等）
LOCATION = st.selectbox(
    "選擇城市：",
    [
        "臺北市", "新北市", "桃園市", "臺中市",
        "臺南市", "高雄市", "基隆市", "花蓮縣", "臺東縣"
    ]
)

# ✅ 組合正確 API URL（使用繁體中文地名）
url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}&locationName={LOCATION}"

# 取得資料
res = requests.get(url)
data = res.json()

# ✅ 檢查資料是否存在
if "records" in data and data["records"]["location"]:
    location = data["records"]["location"][0]
    st.subheader(f"📍 {location['locationName']} 36小時天氣預報")

    # 整理成表格
    elements = {}
    for element in location["weatherElement"]:
        name = element["elementName"]
        times = element["time"]
        values = [t["parameter"]["parameterName"] for t in times]
        elements[name] = values

    # 顯示資料表格
    df = pd.DataFrame(elements)
    st.dataframe(df)

    # 顯示降雨機率折線圖（如果有 PoP）
    if "PoP" in elements:
        try:
            rain = [int(v) if v.isdigit() else 0 for v in elements["PoP"]]
            st.line_chart(pd.DataFrame({"降雨機率(%)": rain}))
        except:
            st.warning("無法繪製降雨機率圖表，資料格式錯誤。")

else:
    st.error("⚠️ 無法取得該城市的氣象資料，請確認授權碼或地點名稱。")
