import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("GooglePlay.csv")
# pd.set_option("display.max_rows", None)

myDataFrame = pd.DataFrame(data)
printable = myDataFrame.describe(
    include="all",
)
print(printable)
column_names = ["Installs", "Rating", "Size", "Price", "Reviews"]
myDataFrame["Installs"] = myDataFrame["Installs"].str.replace("+", "")
myDataFrame["Installs"] = myDataFrame["Installs"].str.replace(",", "")
myDataFrame["Installs"] = myDataFrame["Installs"].str.replace("Free", "0")
myDataFrame["Installs"] = myDataFrame["Installs"].astype(int)

myDataFrame["Rating"] = myDataFrame["Rating"].astype(float)
myDataFrame["Reviews"] = myDataFrame["Reviews"].apply(
    lambda x: str(int(float(x[:-1])) * 1000000) if "M" in x else x
)
myDataFrame["Reviews"] = myDataFrame["Reviews"].astype(int)

myDataFrame["Price"] = myDataFrame["Price"].str.replace("$", "")
myDataFrame["Price"] = myDataFrame["Price"].str.replace("Everyone", "0")
myDataFrame["Price"] = myDataFrame["Price"].astype(float)

myDataFrame["Size"] = myDataFrame["Size"].str.replace("Varies with device", "0")
myDataFrame["Size"] = myDataFrame["Size"].str.replace("+", "")
myDataFrame["Size"] = myDataFrame["Size"].str.replace(",", "")

myDataFrame["Size"] = myDataFrame["Size"].apply(
    lambda x: str(float(x[:-1]) * 1000) if "k" in x else x
)
myDataFrame["Size"] = myDataFrame["Size"].apply(
    lambda x: str(float(x[:-1]) * 1000000) if "M" in x else x
)
myDataFrame["Size"] = myDataFrame["Size"].astype(float)

for column_name in column_names:
    print(column_name)
    installs_min = myDataFrame[column_name].min()
    installs_max = myDataFrame[column_name].max()
    installs_mean = myDataFrame[column_name].mean()
    installs_median = myDataFrame[column_name].median()
    installs_mode = myDataFrame[column_name].mode()

    Q1 = myDataFrame[column_name].quantile(0.25)
    Q3 = myDataFrame[column_name].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers1 = myDataFrame[(myDataFrame[column_name] < lower_bound)]
    outliers2 = myDataFrame[(myDataFrame[column_name] > upper_bound)]
    print("lower outliers", outliers1[column_name].shape[0])
    print("upper outliers", outliers2[column_name].shape[0])
    # Remove the outliers
    # myDataFrame = myDataFrame[
    #     (myDataFrame[column_name] >= lower_bound)
    #     & (myDataFrame[column_name] <= upper_bound)
    # ]

    print(outliers1[column_name])
    print(outliers2[column_name])
    print("Min: ", installs_min)
    print("Max: ", installs_max)
    print("Mean: ", installs_mean)
    print("Median: ", installs_median)
    print("Mode: ", installs_mode)

    plt.figure(figsize=(12, 6))
    sns.boxplot(y=myDataFrame[column_name])
    plt.title(f"Boxplot of {column_name}")
    plt.show()
