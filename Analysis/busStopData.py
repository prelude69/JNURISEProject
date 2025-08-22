import requests
import pandas as pd

if __name__ == "__main__":
    import analysisBase as ab
else:
    import Analysis.analysisBase as ab

baseUrl = "https://open.jejudatahub.net/api/proxy/1t4tbb16b4t1t11tt11tDt1ab6114a1t/"
projectKey = "_50obttp5tp3_8tcbo3o5b5t_o_3j553"
    
dayMap = {
    "Monday": "월",
    "Tuesday": "화",
    "Wednesday": "수",
    "Thursday": "목",
    "Friday": "금",
    "Saturday": "토",
    "Sunday": "일"
}

def requestBusStopData(startDate, endDate, page=1, limit=100):
    param = f"startDate={startDate}&endDate={endDate}&page={page}&limit={limit}"
    url = baseUrl + projectKey + "?" + param
    response = requests.get(url)
    try:
        return response.json()
    except Exception as e:
        print(f"[API ERROR] {e}")
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text[:300]}")
        return {"data": []}

def fetchBusStopData(startDate, endDate, maxRequests = 500):
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
        return bsData  # 또는 적절히 예외 처리
    bsData['baseDate'] = pd.to_datetime(bsData['baseDate'])
    bsData['dayOfWeek'] = bsData['baseDate'].dt.day_name().map(dayMap)
    return bsData

def preAnalysis():
    rawData = fetchBusStopData(20250101, 20250801)
    return refineData(pd.DataFrame(rawData))

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