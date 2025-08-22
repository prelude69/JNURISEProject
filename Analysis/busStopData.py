import os
import requests
import pandas as pd
from datetime import datetime, timedelta

if __name__ == "__main__":
    import analysisBase as ab
    csvFilePath = "../csvData/bus_stop_data.csv"
else:
    import Analysis.analysisBase as ab
    csvFilePath = "csvData/bus_stop_data.csv"

baseUrl = "https://open.jejudatahub.net/api/proxy/1t4tbb16b4t1t11tt11tDt1ab6114a1t/"
projectKey = "tbb53o2e0ott80b2bjpeer35e5c3tbpt"

dayMap = {
    "Monday": "월", "Tuesday": "화", "Wednesday": "수",
    "Thursday": "목", "Friday": "금", "Saturday": "토", "Sunday": "일"
}

def requestBusStopData(startDate, endDate, page=1, limit=100):
    param = f"startDate={startDate}&endDate={endDate}&moveType=승차&page={page}&limit={limit}"
    url = baseUrl + projectKey + "?" + param
    response = requests.get(url)
    try:
        return response.json()
    except Exception as e:
        print(f"[API ERROR] {e}")
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text[:300]}")
        return {"data": []}

def fetchBusStopDataByMonthLimited(startDate, endDate, maxTotalRequests=1000, maxRequestsPerMonth=50):
    allData = []
    cur = datetime.strptime(str(startDate), "%Y%m%d")
    end = datetime.strptime(str(endDate), "%Y%m%d")
    totalRequests = 0
    while cur <= end and totalRequests < maxTotalRequests:
        month_start = cur.replace(day=1)
        next_month = (month_start + timedelta(days=32)).replace(day=1)
        month_end = min(end, next_month - timedelta(days=1))
        requestsForThisMonth = min(maxRequestsPerMonth, maxTotalRequests - totalRequests)
        print(f"Fetching: {month_start.strftime('%Y-%m-%d')} ~ {month_end.strftime('%Y-%m-%d')}")
        month_data = fetchBusStopData(
            month_start.strftime("%Y%m%d"),
            month_end.strftime("%Y%m%d"),
            maxRequests=requestsForThisMonth
        )
        allData.extend(month_data)
        totalRequests += requestsForThisMonth
        cur = next_month
    return allData

def fetchBusStopData(startDate, endDate, maxRequests=500):
    allData = []
    curPage = 1
    perPage = 100
    requestMade = 0
    while requestMade < maxRequests:
        bsData = requestBusStopData(startDate, endDate, page=curPage, limit=perPage)
        data = bsData.get('data', [])
        if not data:
            break
        allData.extend(data)
        if not bsData.get('hasMore', False):
            break
        curPage += 1
        requestMade += 1
    return allData

def refineData(bsData: pd.DataFrame):
    if bsData.empty or 'baseDate' not in bsData.columns:
        print("데이터가 비어있거나 baseDate 컬럼이 없습니다.")
        print("컬럼명:", bsData.columns.tolist())
        print("데이터 예시:", bsData.head())
        return bsData
    bsData['baseDate'] = pd.to_datetime(bsData['baseDate'])
    bsData['dayOfWeek'] = bsData['baseDate'].dt.day_name().map(dayMap)
    return bsData

def preAnalysis():
    os.makedirs(os.path.dirname(csvFilePath), exist_ok=True)
    if os.path.exists(csvFilePath):
        csv = pd.read_csv(csvFilePath)
        if not csv.empty:
            return csv
    # 월별로, 하루 최대 1000회만 요청
    rawData = fetchBusStopDataByMonthLimited(20190101, 20250801, maxTotalRequests=1000, maxRequestsPerMonth=50)
    df = refineData(pd.DataFrame(rawData))
    df.to_csv(csvFilePath, index=False)
    return df

def busStopAnalysisDOW():
    bsData = preAnalysis()
    bsData.columns = bsData.columns.str.strip()
    bsData['userCount'] = pd.to_numeric(bsData['userCount'], errors='coerce')
    dow_data_mean = bsData.groupby('dayOfWeek')['userCount'].mean()
    dow_data_std = bsData.groupby('dayOfWeek')['userCount'].std()
    dow_data_divData = bsData.sort_values('dayOfWeek')
    return ab.analysisResult(dow_data_mean, dow_data_std, dow_data_divData)

def busStopAnalysisRoute():
    bsData = preAnalysis()
    bsData.columns = bsData.columns.str.strip()
    bsData['userCount'] = pd.to_numeric(bsData['userCount'], errors='coerce')
    route_data_mean = bsData.groupby('routeName')['userCount'].mean()
    route_data_std = bsData.groupby('routeName')['userCount'].std()
    route_data_divData = bsData.sort_values('routeName')
    return ab.analysisResult(route_data_mean, route_data_std, route_data_divData)