# %% 공통 데이터 로드 및 전처리
import matplotlib.pyplot as plt
import pandas as pd
import os

# 1. 윈도우 환경 전용 '맑은 고딕' 적용
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2. 상대경로 설정을 위한 동적 경로 확보
# 현재 이 .py (또는 .ipynb) 파일이 위치한 경로를 절대경로로 가져옵니다.
base_path = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()

# 3. os.path.join을 사용하여 운영체제에 맞는 경로 조립 (상대경로 방식)
# 현재 위치에서 'src', 'csv' 폴더 안에 있는 파일에 접근
path = os.path.join(base_path, "src", "csv", "노인요양시설.csv")

# 만약 코드가 이미 src 폴더 안에 있다면 아래처럼 수정하세요:
# path = os.path.join(base_path, "csv", "노인요양시설.csv")

# 4. 데이터 로드
df = pd.read_csv(path, encoding='cp949')

# 전처리
df_t = df.set_index('년월').T
df_t.columns = ['신고수', '새시설수']

print(f"로드 성공: {path}")

# %% 1. Scatter Plot (단일 이벤트 강조형)
plt.figure(figsize=(14, 5))

# 0인 베이스라인을 연하게 깔아줌
plt.axhline(0, color='black', linewidth=0.5, alpha=0.3)
plt.plot(df_t.index, df_t['신고수'], color='#d3d3d3', linestyle='--', marker='o', alpha=0.5)

# 1인 지점만 붉은색 마커로 크게 강조
target_idx = df_t[df_t['신고수'] > 0].index[0]
plt.scatter(target_idx, 1, color='red', s=300, zorder=5, label='유일한 신규 개설')

# 화살표 주석 추가
plt.annotate('송파구의 침묵을 깬\n단 1건의 신고 (2019-03)', 
             xy=(target_idx, 1), xytext=(target_idx, 1.4),
             arrowprops=dict(facecolor='red', shrink=0.05, width=2, headwidth=10),
             ha='center', fontsize=12, color='red', fontweight='bold')

plt.title('송파구 노인요양시설 신규 개설 (Scatter Plot)', fontsize=15, pad=15)
plt.ylim(-0.2, 1.8)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle=':', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()

# %% 2. Horizontal Timeline (이벤트 연대기)
plt.figure(figsize=(14, 3))

# 가로로 긴 타임라인 축 그리기
plt.hlines(0, 0, len(df_t)-1, color='gray', linewidth=2)

# 각 월별로 눈금(tick)과 이벤트 핑(ping) 찍기
for i, month in enumerate(df_t.index):
    plt.plot(i, 0, marker='|', color='black', markersize=15)
    
    # 1이 발생한 지점
    if df_t['신고수'].iloc[i] > 0:
        plt.plot(i, 0, marker='o', color='royalblue', markersize=20, zorder=5)
        plt.annotate(f'최초 공급 발생\n{month}', 
                     xy=(i, 0), xytext=(i, 0.5),
                     arrowprops=dict(facecolor='royalblue', arrowstyle='wedge,tail_width=0.7'), 
                     ha='center', color='royalblue', fontweight='bold', fontsize=11)

plt.title('송파구 신규 인프라 확장 타임라인', fontsize=15, pad=30)
plt.axis('off') # y축 박스 완전 제거
plt.tight_layout()
plt.show()

# %% 3. Cumulative Step Chart (누적 인프라 추이)
plt.figure(figsize=(14, 5))

# 누적합 계산 후 계단식(Step)으로 그리기
cumulative_sum = df_t['신고수'].cumsum()
plt.step(df_t.index, cumulative_sum, where='post', color='seagreen', linewidth=3)
plt.fill_between(df_t.index, cumulative_sum, step='post', color='seagreen', alpha=0.2)

# 강조 텍스트
target_idx = df_t[df_t['신고수'] > 0].index[0]
plt.text(target_idx, 0.5, ' 1개 시설 확보 및 유지 →', fontsize=12, color='darkgreen', fontweight='bold')

plt.title('송파구 노인요양시설 누적 인프라 변화', fontsize=15, pad=15)
plt.yticks([0, 1]) # y축을 0과 1만 보이게 통제
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# %% 4. Binary Color Bar Chart (이진 색상 막대)
plt.figure(figsize=(14, 5))

# 0인 곳은 옅은 회색, 1인 곳은 강렬한 파란색으로 리스트 생성
colors = ['royalblue' if x > 0 else '#e0e0e0' for x in df_t['신고수']]

bars = plt.bar(df_t.index, df_t['신고수'], color=colors, edgecolor='gray', linewidth=0.5)

# 1인 막대 위에만 텍스트 추가
for i, val in enumerate(df_t['신고수']):
    if val > 0:
        plt.text(i, val + 0.05, f'단 1건\n({df_t.index[i]})', 
                 ha='center', color='royalblue', fontweight='bold')

plt.title('송파구 노인요양시설 월별 신고 건수 (데이터 희소성 매핑)', fontsize=15, pad=15)
plt.yticks([0, 1])
plt.xticks(rotation=45)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.tight_layout()
plt.show()

# %% 5. Focused Zoom View (특정 구간 집중 확대)
# 1이 발생한 2019-03 전후 3개월씩만 슬라이싱
zoom_df = df_t.loc['2018-12':'2019-06']

plt.figure(figsize=(10, 5))

# 확대된 구간의 바 차트 그리기
colors_zoom = ['crimson' if x > 0 else '#d3d3d3' for x in zoom_df['신고수']]
plt.bar(zoom_df.index, zoom_df['신고수'], color=colors_zoom, width=0.6)

plt.title('송파구 데이터 집중 분석 구간 (2018.12 ~ 2019.06)', fontsize=15, pad=15)
plt.ylabel('신고 건수')
plt.yticks([0, 1])

# X축 레이블을 수평으로 두고 가독성 향상
plt.xticks(rotation=0, fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
# %%
