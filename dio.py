import pandas as pd

df = pd.read_excel('Prices/Монитор----Jun-20--final.xlsx', index_col=0)

for i, row in df.iterrows():
    string = row['Modification_name'].split()
    string = string[:-1]

    new_ = " ".join(string)

    df.loc[i, 'Modification_name'] = new_

print(df.Name)

df.to_excel('Prices/Монитор----Jun-20-restrict-final.xlsx')

