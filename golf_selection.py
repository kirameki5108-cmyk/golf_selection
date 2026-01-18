import streamlit as st
import numpy as np
from scipy.stats import t

st.title("ゴルフ部 大会メンバー選考")

st.write("選手のスコアとコースレートを入力してください（カンマ区切り）")

name = st.text_input("選手名")

scores_input = st.text_input("スコア（例: 72,70,71）")
rates_input = st.text_input("コースレート（例: 71.5,71.5,72.0）")
sloperates_input = st.text_input("スロープレート（例: 66,112,143) ")

if st.button("評価する"):
    try:
        scores = np.array([float(x) for x in scores_input.split(",")])
        rates = np.array([float(x) for x in rates_input.split(",")])
        sloperates = np.array([float(x) for x in sloperates_input.split(",")])

        n = len(scores)
        if n < 2:
            st.error("2ラウンド以上必要です")
        else:
            y = (scores - rates) * 113 / sloperates
            mean = y.mean()
            std_u = y.std(ddof=1)
            std = max(std_u, 0.5)
            scale = std * np.sqrt(1 + 1 / n)
            prob = t.cdf((0 - mean) / scale, df=n - 1)

            st.success("評価結果")
            st.write(f"・提出ラウンド数：{n}")
            st.write(f"・平均（スコア − レート）：{mean:.2f}")
            st.write(f"・安定度（標準偏差）：{std_u:.2f}")
            st.write(f"・レート以上で回る確率：{prob:.3f}")
    except Exception as e:
        st.error(str(e))
