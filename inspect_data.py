import pandas as pd

for name in ['table_1.csv', 'table_2.csv', 'Parts.csv']:
    df = pd.read_csv(name, sep=';')
    print('\nFILE', name)
    print('shape =', df.shape)
    print('columns =', list(df.columns))
    print(df.head(3).to_string(index=False))
    if 'Type' in df.columns:
        print('Type counts:\n', df['Type'].value_counts(dropna=False).to_string())
    print('-' * 80)

# check overlaps and classifications between tables

t1 = pd.read_csv('table_1.csv', sep=';')
t2 = pd.read_csv('table_2.csv', sep=';')
print('t1 unique ids', len(t1['ID'].unique()))
print('t2 unique ids', len(t2['ID'].unique()))
print('common ids', len(set(t1['ID']) & set(t2['ID'])))
print('type match status (t1/t2 same IDs):')
if 'Type' in t1.columns and 'Type' in t2.columns:
    common = set(t1['ID']) & set(t2['ID'])
    for idx in list(common)[:10]:
        a = t1.loc[t1['ID'] == idx, 'Type'].iloc[0]
        b = t2.loc[t2['ID'] == idx, 'Type'].iloc[0]
        print(idx, a, b, 'MATCH' if a == b else 'DIFF')
else:
    missing = []
    if 'Type' not in t1.columns:
        missing.append('table_1:Type')
    if 'Type' not in t2.columns:
        missing.append('table_2:Type')
    print('Skipping type comparison — missing columns:', ', '.join(missing))
