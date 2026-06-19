import pandas as pd

xls = pd.ExcelFile("../../data/raw/raw_data.xlsx")
print(xls.sheet_names)
df = pd.read_excel("../../data/raw/raw_data.xlsx", nrows=10)

print(df.head())
print(df.head())
