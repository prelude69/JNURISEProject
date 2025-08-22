import pandas as pd
import Analysis.timeData as tda
import Analysis.busStopData as bsda
import Analysis.patternAnalyze as pa

timeData = pd.read_csv('csvData/time_data.csv', skiprows=1)

paTimeData = tda.preAnalysis(timeData)
dowTData = tda.timeAnalysisDOW(paTimeData)
timeTData = tda.timeAnalysisTime(paTimeData)
dowBusData = bsda.busStopAnalysisDOW()
timeBusData = bsda.busStopAnalysisRoute()

#testSample1
"""
print("요일별 분석 평균:")
print(dowTData.Mean)
print("요일별 분석 표준편차:")
print(dowTData.Std)
print("요일별 분석 데이터:")
print(dowTData.divData)
print("데이터 출력:")
dowTData.printDivData("dayOfWeek")

print("시간대별 분석 평균:")
print(timeTData.Mean)
print("시간대별 분석 표준편차:")
print(timeTData.Std)
print("시간대별 분석 데이터:")
print(timeTData.divData)
timeTData.printDivData("baseHour")
"""
#testSample2
"""
print("요일별 분석 평균:")
print(dowBusData.Mean)
print("요일별 분석 표준편차:")
print(dowBusData.Std)
print("요일별 분석 데이터:")
print(dowBusData.divData)
print("데이터 출력:")
dowBusData.printDivData("dayOfWeek")

print("노선별 분석 평균:")
print(timeBusData.Mean)
print("노선별 분석 표준편차:")
print(timeBusData.Std)
print("노선별 분석 데이터:")
print(timeBusData.divData)
timeBusData.printDivData("routeName")
"""
#testSample3

pa.patternAnalysis(dowBusData, "dayOfWeek")
pa.patternAnalysis(timeBusData, "priceType")
pa.patternAnalysis(dowTData, "dayOfWeek")
pa.patternAnalysis(timeTData, "baseHour")