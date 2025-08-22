import pandas as pd

if __name__ == "__main__":
    import analysisBase as ab
else:
    import Analysis.analysisBase as ab

def preAnalysis(tData):
    tData.columns = ['base_date', 'day_of_week', 'base_hour', 'user_type', 'user_count']
    tData = tData.dropna()
    tData = tData.drop_duplicates()
    tData.columns = ['baseDate', 'dayOfWeek', 'baseHour', 'userType', 'userCount']
    tData['baseHour'] = tData['baseHour'].astype(str).str.extract(r'(\d{2})')
    return tData

def timeAnalysisDOW(tData):
    tData.columns = tData.columns.str.strip()
    tData['userCount'] = pd.to_numeric(tData['userCount'], errors='coerce')
    dowDataMean = tData.groupby('dayOfWeek')['userCount'].mean()
    dowDataStd = tData.groupby('dayOfWeek')['userCount'].std()
    dowDataDivData = tData.sort_values('dayOfWeek')
    return ab.analysisResult(dowDataMean, dowDataStd, dowDataDivData)

def timeAnalysisTime(tData):
    tData.columns = tData.columns.str.strip()
    tData['userCount'] = pd.to_numeric(tData['userCount'], errors='coerce')
    timeDataMean = tData.groupby('baseHour')['userCount'].mean()
    timeDataStd = tData.groupby('baseHour')['userCount'].std()
    timeDataDivData = tData.sort_values('baseHour')
    return ab.analysisResult(timeDataMean, timeDataStd, timeDataDivData)
