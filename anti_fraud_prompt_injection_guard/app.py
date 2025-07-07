import streamlit as st
import pandas as pd
import random
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.colored_header import colored_header
import datetime

st.set_page_config(page_title="Anti-Fraud & Prompt-Injection Guard", layout="wide")
st.title("Anti-Fraud & Prompt-Injection Guard")

def generate_mock_data():
    categories = ["Spam", "Toxicity", "Prompt Injection"]
    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    data = []
    for i in range(1000):
        user_id = random.randint(1000, 1100)
        chat_id = random.randint(200, 210)
        course = random.choice(["ML Basics", "Prompt Engineering", "Python for DS"])
        violation = random.choices(categories + ["None"], [0.1, 0.1, 0.05, 0.75])[0]
        is_confirmed = random.random() > 0.5 if violation != "None" else False
        data.append({
            "msg_id": i,
            "user_id": user_id,
            "chat_id": chat_id,
            "course": course,
            "violation": violation,
            "confirmed": is_confirmed,
            "risk_score": round(random.uniform(0.1, 0.99), 2),
            "trust_score": round(random.uniform(0.4, 1.0), 2),
            "timestamp": start_date + datetime.timedelta(days=random.randint(0, 30))
        })
    return pd.DataFrame(data)

data = generate_mock_data()
tabs = st.tabs(["Общий обзор", "Пользователи"])

with tabs[0]:
    selected_chat = st.selectbox("Выберите чат:", sorted(data["chat_id"].unique()))
    filtered = data[data["chat_id"] == selected_chat]

    colored_header("Метрики по чату", "Обновляется в реальном времени", "blue-70")
    col1, col2, col3 = st.columns(3)
    col1.metric("Сообщений", len(filtered))
    col2.metric("Уникальных пользователей", filtered["user_id"].nunique())
    col3.metric("Проблемных сообщений", len(filtered[filtered["violation"] != "None"]))
    style_metric_cards()

    colored_header("Типы нарушений", "Распределение по категориям", "red-70")
    viols = filtered[filtered["violation"] != "None"]["violation"].value_counts().reset_index()
    viols.columns = ["Тип", "Количество"]
    st.altair_chart(alt.Chart(viols).mark_bar().encode(
        x=alt.X("Тип", sort="-y"),
        y="Количество",
        color="Тип"
    ), use_container_width=True)

    colored_header("Безопасные сообщения", "Процент не нарушающих сообщений", "green-70")
    safe_percent = 100 * len(filtered[filtered["violation"] == "None"]) / max(len(filtered), 1)
    st.progress(int(safe_percent))
    st.markdown(f"**{safe_percent:.1f}% безопасных сообщений**")

    colored_header("Пользователи с нарушениями", "% пользователей с >= 3 нарушениями", "orange-70")
    user_counts = filtered[filtered["violation"] != "None"].groupby("user_id").size()
    malicious_users = user_counts[user_counts >= 3]
    percent_flagged = 100 * len(malicious_users) / max(filtered["user_id"].nunique(), 1)
    st.metric("Флагнутые пользователи", f"{percent_flagged:.1f}%")

    colored_header("Оценка риска", "Средние метрики по диалогу", "gray-70")
    col1, col2 = st.columns(2)
    avg_risk = filtered["risk_score"].mean()
    col1.metric("Средний Risk Score", f"{avg_risk:.2f}")

    confirmed_msgs = filtered[filtered["confirmed"] & (filtered["violation"] != "None")]
    confirmed_avg = confirmed_msgs["risk_score"].mean() if not confirmed_msgs.empty else 0
    col2.metric("Risk Score (валид.)", f"{confirmed_avg:.2f}" if confirmed_avg else "—")

    trust_score = filtered["trust_score"].mean()
    st.metric("Индекс доверия", f"{trust_score:.2f}")

with tabs[1]:
    st.subheader("Пользовательская аналитика")
    top_users = data[data["violation"] != "None"].groupby("user_id").agg(
        violations=("violation", "count"),
        avg_risk=("risk_score", "mean"),
        trust_score=("trust_score", "mean")
    ).sort_values("violations", ascending=False).reset_index()
    st.dataframe(top_users, use_container_width=True)

    selected_user = st.selectbox("Выберите user_id:", top_users["user_id"])
    user_msgs = data[data["user_id"] == selected_user]
    st.markdown(f"**Сообщений:** {len(user_msgs)}")
    st.markdown(f"**Нарушений:** {len(user_msgs[user_msgs['violation'] != 'None'])}")
    st.markdown(f"**Средний Risk Score:** {user_msgs['risk_score'].mean():.2f}")
    st.markdown(f"**Средний Trust Score:** {user_msgs['trust_score'].mean():.2f}")

    st.markdown("---")
    st.markdown("**История сообщений:**")
    st.dataframe(user_msgs.sort_values("timestamp", ascending=False), use_container_width=True)
