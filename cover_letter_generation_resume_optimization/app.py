import streamlit as st
from data.mock import generate_mock_candidates
from ui.sidebar.upload import file_upload_section
from ui.sidebar.filters import filter_sidebar
from ui.main.candidate import display_candidate_details
from ui.main.summary_table import display_summary_table_and_chart

st.set_page_config(page_title="Генерация сопроводительного письма и оптимизация резюме", layout="wide")

file_upload_section()

candidates = generate_mock_candidates()
filtered, _ = filter_sidebar(candidates)

st.title("Генерация сопроводительного письма и оптимизация резюме")

if not filtered:
    st.warning("Нет подходящих кандидатов по заданным фильтрам.")
    st.stop()

st.write("Выберите кандидата для просмотра подробного отчета:")
selected = st.selectbox(
    "Кандидат",
    options=filtered,
    format_func=lambda candidate: f"{candidate['name']} ({candidate['matching_score']}%)",
    index=0
)

st.markdown("---")

display_candidate_details(selected)

display_summary_table_and_chart(filtered)
