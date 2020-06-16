import pandas as pd

df = pd.read_excel('Prices/Монитор-Цены-от-Apr-20----16--15-50.xlsx')

for i, row in df.iterrows():
    string = row['Name'].split()
    string = string[:-1]

    new_ = " ".join(string)

    df.loc[i, 'Name'] = new_

print(df.Name)

df.to_excel('Монитор-Цены-от-Apr-20----restrict.xlsx')

