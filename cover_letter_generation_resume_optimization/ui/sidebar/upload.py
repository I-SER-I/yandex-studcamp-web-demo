import streamlit as st

UPLOAD_TITLE = "Загрузка данных"
EXPANDER_TITLE = "Загрузить резюме и вакансию"

RESUME_LABEL = "Загрузить резюме (PDF/TXT)"
VACANCY_LABEL = "Загрузить вакансию (PDF/TXT)"

SUCCESS_MESSAGE = "Данные успешно загружены! (пока не обрабатываются)"
INFO_MESSAGE = "Ожидается загрузка второго файла..."

def file_upload_section():
    st.sidebar.title(UPLOAD_TITLE)
    with st.sidebar.expander(EXPANDER_TITLE):
        uploaded_resume = st.file_uploader(
            RESUME_LABEL, type=["pdf", "txt"], key="resume"
        )
        uploaded_vacancy = st.file_uploader(
            VACANCY_LABEL, type=["pdf", "txt"], key="vacancy"
        )

        if uploaded_resume and uploaded_vacancy:
            st.success(SUCCESS_MESSAGE)
        elif uploaded_resume or uploaded_vacancy:
            st.info(INFO_MESSAGE)
