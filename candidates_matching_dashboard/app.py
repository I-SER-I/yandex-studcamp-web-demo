import streamlit as st
from candidates_matching_dashboard.data.mock import generate_mock_candidates
from candidates_matching_dashboard.ui.sidebar.upload import file_upload_section
from candidates_matching_dashboard.ui.sidebar.filters import filter_sidebar
from candidates_matching_dashboard.ui.main.candidate import display_candidate_details
from candidates_matching_dashboard.ui.main.summary_table import display_summary_table_and_chart

st.set_page_config(page_title="Оценка релевантности кандидатов", layout="wide")

file_upload_section()

candidates = generate_mock_candidates()
filtered, _ = filter_sidebar(candidates)

st.title("Анализ релевантности кандидатов")

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
