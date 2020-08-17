import pandas as pd

df = pd.read_excel("Prices/Handle_base/Moinitor_Jun_ITR_Models_Src.xlsx")

df = df[['Vendor', 'Model', 'Vendor model']].copy()

df = df.drop_duplicates(subset=['Vendor', 'Model', 'Vendor model'], keep='first')

df.to_excel("Prices/Handle_base/Moinitor_Jun_ITR_Models_Src_drop.xlsx")