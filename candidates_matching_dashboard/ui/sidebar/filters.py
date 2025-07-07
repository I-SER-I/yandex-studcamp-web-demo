import streamlit as st

SIDEBAR_HEADER = "🔍 Фильтры"
VACANCY_LABEL = "Вакансия"
SCORE_LABEL = "Минимальный matching score"

def filter_sidebar(candidates):
    st.sidebar.header(SIDEBAR_HEADER)

    vacancies = sorted(set(candidate["vacancy_title"] for candidate in candidates))
    selected_vacancy = st.sidebar.selectbox(VACANCY_LABEL, options=["Все"] + vacancies)
    min_score = st.sidebar.slider(SCORE_LABEL, 0, 100, 60)

    filtered = [
        candidate for candidate in candidates
        if candidate["matching_score"] >= min_score and
           (selected_vacancy == "Все" or candidate["vacancy_title"] == selected_vacancy)
    ]

    return filtered, None
