import pandas as pd

df = pd.read_excel("Prices/Handle_base/Monitors all models (1).xlsx")

print(len(df))
df.drop_duplicates(subset=['Vendor model'], keep='first', inplace=True)
print(len(df))

df.to_excel("Prices/Handle_base/Monitors all models drop_duplicates.xlsx")

