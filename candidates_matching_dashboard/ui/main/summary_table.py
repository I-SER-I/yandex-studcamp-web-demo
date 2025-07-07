import streamlit as st
import pandas as pd
import plotly.express as px

TABLE_HEADER = "📋 Обзор всех кандидатов"
CHART_HEADER = "📈 Сравнительный график matching score"
CHART_TITLE = "Matching Score по кандидатам"

def display_summary_table_and_chart(candidates):
    st.markdown("---")
    st.subheader(TABLE_HEADER)

    df = pd.DataFrame(candidates)
    df_view = df[["name", "position", "vacancy_title", "matching_score"]].rename(
        columns={
            "name": "Имя",
            "position": "Позиция",
            "vacancy_title": "Вакансия",
            "matching_score": "Score"
        }
    )
    st.dataframe(df_view, use_container_width=True)

    st.markdown("---")
    st.subheader(CHART_HEADER)

    fig = px.bar(
        df_view,
        x="Имя",
        y="Score",
        color="Вакансия",
        text="Score",
        title=CHART_TITLE
    )
    st.plotly_chart(fig, use_container_width=True)
