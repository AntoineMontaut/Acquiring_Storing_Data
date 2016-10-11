'''tests on DataFrame and pandas'''

import pandas as pd

df = pd.DataFrame([[0, 2, 3], [4, 8, 2], [6, 2, 5], [4, 7, 3]], index=['One', 'Two', 'Three', 'Four'], columns=['A', 'B', 'C'])
print(df)

df_neg = df * -1
df_neg = df_neg.shift(1)
print(df_neg)

df_diff = df + df_neg
df_diff.loc['One'] = 0.0
print(df_diff)

sums = abs(df_diff).sum()
print(sums)

print(df.index[2])

df_diff2 = abs(df - df.shift(1))
# df_diff2.loc[df.index[0]] = 0
print(df_diff2)
print(df_diff2.sum())