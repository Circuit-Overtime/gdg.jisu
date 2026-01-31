import csv
import pandas as pd
from blackListEmails import cancelledList
def getData():
    df = pd.read_csv("swags.csv")
    return df 




def FilterData(size):
    df = getData()
    count = 0
    filtered_df = list(df['Size'])
    for i in filtered_df:
        if size in i:
            count += 1
    return count


if __name__ == "__main__":
    sizes = FilterData("T-shirt Unisex - 3XL")
    print(sizes)
    