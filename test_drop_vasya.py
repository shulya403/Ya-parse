import pandas as pd

df = pd.read_excel("Prices/Handle_base/AllGid/Копия Monitors New Project (2).xlsx")

print(len(df))
df.drop_duplicates(subset=['Vendor model'], keep='first', inplace=True)
print(len(df))

df.to_excel("Prices/Handle_base/Monitors drop_duplicates Jun-20.xlsx")

