import streamlit as st

def display_candidate_details(candidate):
    first, second = st.columns(2)

    with first:
        st.subheader("Совпавшие навыки")
        st.success(", ".join(candidate["matched_skills"]) or "Нет")

        st.subheader("Недостающие навыки")
        st.warning(", ".join(candidate["missing_skills"]) or "Нет")

    with second:
        st.subheader("Пробелы в опыте")
        st.error("\n".join(candidate["experience_gaps"]) or "Нет")

        st.subheader("Вопросы для интервью")
        st.info("\n".join(candidate["recommendations"]) or "Нет")

    st.markdown("---")

    with st.expander("JSON-отчет кандидата"):
        st.json(candidate)

    with st.expander("Сохранить PDF (заглушка)"):
        st.button("Скачать PDF-отчет")
