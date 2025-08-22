import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

weekdayOrder = ['월', '화', '수', '목', '금', '토', '일']

class analysisResult:
    def __init__(self, Mean, Std, divData):
        self.Mean = Mean
        self.Std = Std
        self.divData = divData

    def printDivData(self, xcol):
        printData = self.divData
        if xcol == "dayOfWeek":
           printData['dayOfWeek'] = pd.Categorical(printData['dayOfWeek'], categories=weekdayOrder, ordered=True)
           printData = printData.sort_values('dayOfWeek')
        else:
            printData[xcol] = pd.Categorical(printData[xcol], ordered=True)
            printData = printData.sort_values(xcol)
        plt.figure(figsize=(10, 6))
        for key, group in printData.groupby(xcol):
                plt.plot(group[xcol].astype(str), group['userCount'], label=str(key))
        plt.title(f'{xcol}별 이용자 수')
        plt.xlabel(xcol)
        plt.ylabel('이용자 수')
        plt.legend()
        plt.show()