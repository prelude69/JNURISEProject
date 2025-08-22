import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    import analysisBase as ab
else:
    import Analysis.analysisBase as ab

def patternAnalysis(ar:ab.analysisResult , analysisType:str):
    printData = ar.divData.copy()
    if analysisType == "priceType":
        printData['priceType'] = pd.Categorical(ar.divData['priceType'], ordered=True)
    elif analysisType == "baseHour":
        printData['baseHour'] = pd.Categorical(ar.divData['baseHour'], ordered=True)
    elif analysisType == "dayOfWeek":
        printData['dayOfWeek'] = pd.Categorical(ar.divData['dayOfWeek'], categories=ab.weekdayOrder, ordered=True)
    else:
        raise ValueError("Unknown analysis type")
    
    plt.figure(figsize=(10, 6))
    for key, group in printData.groupby(analysisType):
        plt.plot(group[analysisType].astype(str), group['userCount'], label=str(key))
    plt.title(f'{analysisType}별 이용자 수')
    plt.xlabel(analysisType)
    plt.ylabel('이용자 수')
    plt.legend()
    plt.show()