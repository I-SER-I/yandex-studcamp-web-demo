import streamlit as st
import pandas as pd
import random
import altair as alt
import datetime

def generate_mock_data():
    categories = ["PII", "Shocking Content", "Competitor Ads", "Off-topic"]
    data = []
    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    for i in range(1000):
        violation = random.choices(categories + ["None"], [0.1, 0.1, 0.1, 0.1, 0.6])[0]
        message = "This is a generated response."
        if violation == "PII":
            message = "My phone number is +7 900 000-00-00."
        elif violation == "Shocking Content":
            message = "This content contains graphic violence."
        elif violation == "Competitor Ads":
            message = "You should use AnotherPlatform.com instead."
        elif violation == "Off-topic":
            message = "Let me tell you about my vacation to Bali."

        entry = {
            "response_id": i,
            "chat_id": random.randint(100, 110),
            "course_id": random.choice(["Python Basics", "AI Ethics", "Data Science"]),
            "user_id": random.randint(2000, 2100),
            "risk_score": round(random.uniform(0, 1), 2),
            "safe": random.random() > 0.3,
            "action": random.choices(["pass", "mask", "block", "rewrite"], [0.5, 0.2, 0.2, 0.1])[0],
            "violation": violation,
            "timestamp": start_date + datetime.timedelta(days=random.randint(0, 30)),
            "response_text": message,
            "moderated_text": message.replace("+7 900 000-00-00", "[REDACTED]")
                .replace("graphic violence", "[CONTENT WARNING]")
                .replace("AnotherPlatform.com", "[Competitor Site]")
                .replace("vacation to Bali", "irrelevant information")
        }
        data.append(entry)
    return pd.DataFrame(data)


df = generate_mock_data()
st.set_page_config(page_title="Leakage Guard Dashboard", layout="wide")
st.title("Output-Safety & Leakage Guard Dashboard")

selected_chat = st.selectbox("Выберите chat_id:", sorted(df["chat_id"].unique()))
filtered = df[df["chat_id"] == selected_chat]

tabs = st.tabs(["Аналитика", "Модерация"])

with tabs[0]:
    colored_header(label="Обзор по чатам", description="Выберите чат и получите ключевые метрики безопасности", color_name="blue-70")
    col1, col2, col3 = st.columns(3)
    col1.metric("Проверенных ответов", len(filtered))
    col2.metric("Уникальных пользователей", filtered["user_id"].nunique())
    col3.metric("Всего нарушений", len(filtered[filtered["violation"] != "None"]))
    style_metric_cards()

    colored_header(label="Нарушения по категориям", description="Сравните частоту разных типов нарушений", color_name="red-70")
    violations = filtered[filtered["violation"] != "None"]["violation"].value_counts().reset_index()
    violations.columns = ["Тип", "Количество"]
    chart = alt.Chart(violations).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        x=alt.X("Тип", sort="-y"),
        y="Количество",
        color="Тип"
    )
    st.altair_chart(chart, use_container_width=True)

    colored_header(label="Динамика нарушений", description="Изменение количества нарушений по дням", color_name="gray-70")
    time_series = filtered[filtered["violation"] != "None"]
    time_series = time_series.groupby(time_series["timestamp"].dt.date).size().reset_index(name="Нарушения")
    time_chart = alt.Chart(time_series).mark_line(point=True).encode(
        x="timestamp:T",
        y="Нарушения",
        tooltip=["timestamp:T", "Нарушения"]
    ).properties(height=300)
    st.altair_chart(time_chart, use_container_width=True)

    colored_header(label="Безопасные ответы", description="Процент ответов без нарушений", color_name="green-70")
    safe_pct = 100 * filtered["safe"].mean()
    st.progress(int(safe_pct))
    st.markdown(f"### **{safe_pct:.1f}% безопасных ответов**")
    if safe_pct > 80:
        rain(emoji="🛡️", font_size=20, falling_speed=5, animation_length="medium")

    colored_header(label="Действия модерации", description="Как система реагировала на нарушения", color_name="violet-70")
    actions = filtered["action"].value_counts(normalize=True).reset_index()
    actions.columns = ["Действие", "Доля"]
    actions["%"] = (actions["Доля"] * 100).round(1)
    st.dataframe(actions[["Действие", "%"]], use_container_width=True)

    colored_header(label="Индексы безопасности", description="Агрегированные метрики качества", color_name="orange-70")
    col1, col2, col3 = st.columns(3)
    col1.metric("Средний Safety Score", f"{filtered['risk_score'].mean():.2f}")
    debated = filtered[filtered["risk_score"] > 0.7]
    if not debated.empty:
        debated_validated = debated.sample(frac=0.5)
        col2.metric("Score без спорных", f"{debated_validated['risk_score'].mean():.2f}")
    else:
        col2.metric("Score без спорных", "—")
    leakage_score = 1 - (len(filtered[filtered["violation"] == "PII"]) / max(len(filtered), 1))
    status = "⚠️" if leakage_score < 0.8 else "✅"
    col3.metric("Leakage Risk Index", f"{leakage_score:.2f}", delta=status)

with tabs[1]:
    colored_header(label="Режим ручной модерации", description="Просмотр оригинальных и откорректированных ответов", color_name="blue-green-70")
    violated_responses = filtered[filtered["violation"] != "None"]
    if not violated_responses.empty:
        selected_response = st.selectbox("Выберите response_id:", violated_responses["response_id"])
        entry = violated_responses[violated_responses["response_id"] == selected_response].iloc[0]

        st.markdown(f"**Курс:** {entry['course_id']}")
        st.markdown(f"**Тип нарушения:** {entry['violation']}")
        st.markdown("---")
        st.markdown("**Оригинальный ответ:**")
        st.code(entry['response_text'], language='text')
        st.markdown("**Скорректированный ответ:**")
        st.code(entry['moderated_text'], language='text')
    else:
        st.info("Нет нарушений в этом чате")

st.sidebar.header("Фильтры")
st.sidebar.multiselect("Курс:", df["course_id"].unique())
st.sidebar.multiselect("Тип нарушения:", df["violation"].unique())