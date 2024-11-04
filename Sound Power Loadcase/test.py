import pandas as pd

#create DataFrame
df = pd.DataFrame({'team': ['A', 'A', 'A', 'B', 'B', 'C'],
                   'conference': ['East', 'East', 'East', 'West', 'West', 'East'],
                   'div': [1, 1, 2, 2, 2, 1],
                   'points': [11, 8, 10, 6, 6, 5],
                   'rebounds': [7, 7, 7, 8, 8, 9]})
print(df)
cols = ['team', 'conference', 'div']

df1 = df.groupby(cols)[['points']].sum().add_suffix('_total')
print(df1)

df2 = df.join(df1, on=cols)

print(df2)

df3 = df2.groupby(cols, as_index=False).agg({'points_total': 'max', 'rebounds': 'max'})
print(df3)