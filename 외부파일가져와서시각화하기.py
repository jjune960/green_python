# %%

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

path = r"C:\Users\Administrator\Desktop\python_0227\python_vscode_study\src\csv\노인요양시설.csv"
df = pd.read_csv(path, encoding='cp949')
# %%
df_t = df.set_index('년월').T
df_t.plot(kind='bar',figsize=(12,6))

plt.title('월별 요양시설 현황')
plt.xlabel('년월')
plt.ylabel('개수')

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# %%
