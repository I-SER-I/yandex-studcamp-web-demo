import streamlit as st
import pandas as pd
import json
from io import BytesIO
import streamlit_echarts as echarts
from streamlit_extras.metric_cards import style_metric_cards

# ======================== MOCK FUNCTIONS ========================
def parse_resume(uploaded_file):
    return mock_resume

def parse_vacancy(uploaded_file):
    return mock_vacancy

def generate_suggestions(resume, vacancy):
    return mock_suggestions

def generate_cover_letter(resume, vacancy):
    return mock_cover_letter

def analyze_resume(resume):
    return mock_analysis

def generate_pdf(analysis, cover_letter):
    buffer = BytesIO()
    return buffer

# ======================== MOCK DATA ========================
mock_resume = {
    "name": "Георгий Круглов",
    "title": "Python Developer",
    "experience": [
        {"company": "ООО Рога и Копыта", "role": "Backend Developer", "description": "Разработка REST API на Flask, PostgreSQL, Docker."},
        {"company": "TechStar", "role": "ML Engineer", "description": "Разработка ML-пайплайнов, оптимизация моделей, пайплайны на Airflow."}
    ],
    "skills": ["Python", "Django", "FastAPI", "PostgreSQL", "Docker", "Git"],
    "education": "ИТМО, магистр, Прикладная информатика"
}

mock_vacancy = {
    "title": "Senior Python Developer",
    "company": "Ozon",
    "requirements": [
        "Опыт с Django/Flask/FastAPI",
        "Опыт с Docker, Git",
        "Знание PostgreSQL, Redis",
        "Опыт оптимизации SQL-запросов",
        "Опыт работы в Agile-командах"
    ]
}

mock_suggestions = {
    "structure": [
        {"section": "Опыт работы", "action": "Поднять выше образования"},
        {"section": "Навыки", "action": "Добавить Redis, Agile"}
    ],
    "wording": [
        {"old": "Разработка REST API на Flask", "new": "Проектирование и реализация REST API на Flask с покрытием тестами"},
        {"old": "ML-пайплайны", "new": "Построение production-ready ML пайплайнов на Airflow"}
    ]
}

mock_cover_letter = """
Уважаемые представители Ozon,

Изучив вакансию Senior Python Developer, я понял, что мои навыки и опыт идеально соответствуют вашим требованиям. За последние 5 лет я работал над созданием высоконагруженных backend-систем, используя Flask и FastAPI. Я также активно применяю Docker, PostgreSQL, участвую в Agile-разработке и покрываю код тестами.

С радостью расскажу подробнее при личной встрече.

С уважением, Георгий Круглов
"""

mock_analysis = {
    "score": 63,
    "keywords": {"score": 3, "found": [".NET"], "missing": ["Docker", "Redis", "backend", "QA"]},
    "structure": {"score": 63, "sections": {"О себе": 80, "Образование": 100, "Опыт работы": 60, "Навыки": 0, "Сертификаты": 0, "Проекты": 0, "Языки": 100}},
    "tone": {"score": 100, "comment": "Ваше резюме имеет профессиональный и позитивный тон"},
    "xyz": {"score": 17, "x": 5, "y": 0, "z": 0, "comments": ["Добавьте количественные метрики в опыт работы.", "Опишите методы и инструменты, которые вы использовали."]},
    "contacts": {"score": 100, "found": 4},
    "recommendations": [
        "Раздел образования хорошо отформатирован",
        "Контактная информация четко представлена",
        "Рекомендуется добавить описание проектов для демонстрации навыков"
    ]
}

# ======================== APP ========================
st.set_page_config(page_title="Анализ и генерация резюме", layout="wide")
st.title("📄 Анализ и генерация резюме + сопроводительное письмо")

uploaded_resume = st.file_uploader("Загрузите резюме", type=["pdf", "docx", "json"])
uploaded_vacancy = st.file_uploader("Загрузите вакансию", type=["txt", "json"])

resume_data = parse_resume(uploaded_resume) if uploaded_resume else mock_resume
vacancy_data = parse_vacancy(uploaded_vacancy) if uploaded_vacancy else mock_vacancy
analysis = analyze_resume(resume_data)
suggestions = generate_suggestions(resume_data, vacancy_data)
cover_letter = generate_cover_letter(resume_data, vacancy_data)

pdf_buffer = generate_pdf(analysis, cover_letter)

st.markdown("---")
tab_labels = [
    ("📊 Обзор", analysis['score']),
    ("🧱 Структура", analysis['structure']['score']),
    ("🧠 Ключевые слова", analysis['keywords']['score']),
    ("🎯 Тон", analysis['tone']['score']),
    ("🔍 XYZ Анализ", analysis['xyz']['score']),
    ("✉️ Письмо", 100)
]

tabs = st.tabs([
    f"{label} ({'🟢' if score >= 70 else '🟡' if score >= 40 else '🔴'})" for label, score in tab_labels
])

with tabs[0]:
    if analysis['score'] < 40:
        st.error("❗ Резюме имеет низкую общую оценку. Обратите внимание на ключевые разделы ниже.")
    elif analysis['score'] < 70:
        st.warning("⚠️ Есть потенциал для улучшения. Проверьте структуру и ключевые слова.")
    else:
        st.success("✅ Резюме выглядит хорошо! Тем не менее, всегда есть что улучшить.")
    st.subheader("Общий результат")
    
    chart_scores = [
        analysis['keywords']['score'],
        analysis['structure']['score'],
        analysis['tone']['score'],
        analysis['xyz']['score'],
        analysis['contacts']['score']
    ]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Ключевые слова", f"{analysis['keywords']['score']}/100", help="Совпадение ключевых слов из вакансии", delta=None, delta_color="normal")
    col2.metric("Структура", f"{analysis['structure']['score']}/100", help="Полнота и порядок секций резюме", delta=None, delta_color="normal")
    col3.metric("Тон", f"{analysis['tone']['score']}/100", help="Профессиональный стиль изложения", delta=None, delta_color="normal")

    col4, col5 = st.columns(2)
    col4.metric("XYZ Анализ", f"{analysis['xyz']['score']}/100", help="Достижения, Метрики, Методы", delta=None, delta_color="normal")
    col5.metric("Контакты", f"{analysis['contacts']['score']}/100", help="Полнота контактных данных", delta=None, delta_color="normal")

    
    st.markdown("### 📝 Рекомендации")
    for rec in analysis['recommendations']:
        st.markdown(f"- {rec}")

with tabs[1]:
    st.subheader("Структура резюме")
    st.markdown("#### Детализация по секциям")
    import streamlit_echarts as echarts
    struct_data = [
        {"value": v, "name": k} for k, v in analysis['structure']['sections'].items()
    ]
    echarts.st_echarts({
        "tooltip": {"trigger": "item"},
        "legend": {"top": "bottom"},
        "series": [{
            "name": "Структура",
            "type": "pie",
            "radius": ["40%", "70%"],
            "itemStyle": {"borderRadius": 8, "borderColor": "#fff", "borderWidth": 2},
            "label": {"show": False},
            "emphasis": {"label": {"show": True, "fontSize": 14, "fontWeight": "bold"}},
            "labelLine": {"show": False},
            "data": struct_data
        }]
    }, height="300px")
    st.subheader("Метрики по секциям")
    cols = st.columns(3)
    for i, (section, score) in enumerate(analysis['structure']['sections'].items()):
        cols[i % 3].metric(section, f"{score}/100", help="Степень проработки и наличия секции")

    st.subheader("📋 Прогресс по секциям")
    for section, score in analysis['structure']['sections'].items():
        st.progress(score, text=f"{section}: {score}/100")

with tabs[2]:
    st.subheader("Анализ ключевых слов")
    col1, col2 = st.columns(2)
    col1.metric("Найдено", str(len(analysis['keywords']['found'])), help="Ключевые слова, совпадающие с вакансией")
    col2.metric("Отсутствует", str(len(analysis['keywords']['missing'])), help="Не найденные, но ожидаемые слова")
    echarts.st_echarts({
        "tooltip": {"trigger": "item"},
        "legend": {"top": "bottom"},
        "series": [
            {
                "name": "Ключевые слова",
                "type": "pie",
                "radius": ["40%", "70%"],
                "itemStyle": {"borderRadius": 8, "borderColor": "#fff", "borderWidth": 2},
                "label": {"show": False},
                "emphasis": {"label": {"show": True, "fontSize": 14, "fontWeight": "bold"}},
                "labelLine": {"show": False},
                "data": [
                    {"value": len(analysis['keywords']['found']), "name": "Найденные"},
                    {"value": len(analysis['keywords']['missing']), "name": "Отсутствующие"}
                ]
            }
        ]
    }, height="300px")

    col1, col2 = st.columns(2)
with col1:
    st.markdown("**Найденные ключевые слова:**")
    for word in analysis['keywords']['found']:
        st.success(f"✅ {word}")

with col2:
    st.markdown("**Отсутствующие ключевые слова:**")
    for word in analysis['keywords']['missing']:
        st.error(f"❌ {word}")

with tabs[3]:
    st.subheader("Анализ тона")
    tone_value = analysis['tone']['score']
    echarts.st_echarts({
        "series": [
            {
                "type": "gauge",
                "startAngle": 180,
                "endAngle": 0,
                "min": 0,
                "max": 100,
                "progress": {"show": True, "width": 18},
                "axisLine": {"lineStyle": {"width": 18}},
                "axisTick": {"show": False},
                "splitLine": {"show": False},
                "axisLabel": {"distance": 25, "fontSize": 14},
                "pointer": {"show": True},
                "detail": {"valueAnimation": True, "formatter": "{value}%", "fontSize": 20},
                "data": [{"value": tone_value, "name": "Тон"}]
            }
        ]
    }, height="300px")
    st.info(analysis['tone']['comment'])

with tabs[4]:
    st.subheader("XYZ Анализ")
    col1, col2, col3 = st.columns(3)
    col1.metric("X: Достижения", f"{analysis['xyz']['x']}/10", help="Конкретные достижения, выраженные действиями")
    col2.metric("Y: Измерения", f"{analysis['xyz']['y']}/10", help="Числовые или фактологические подтверждения")
    col3.metric("Z: Методы", f"{analysis['xyz']['z']}/10", help="Инструменты, технологии, способы выполнения задач")
    xyz_data = [
        {"value": analysis['xyz']['x'], "name": "X (Достижения)"},
        {"value": analysis['xyz']['y'], "name": "Y (Измерение)"},
        {"value": analysis['xyz']['z'], "name": "Z (Методы)"}
    ]
    echarts.st_echarts({
        "tooltip": {"trigger": "item"},
        "legend": {"top": "bottom"},
        "series": [
            {
                "type": "pie",
                "radius": ["40%", "70%"],
                "itemStyle": {"borderRadius": 10, "borderColor": "#fff", "borderWidth": 2},
                "label": {"show": False},
                "emphasis": {"label": {"show": True, "fontSize": 14, "fontWeight": "bold"}},
                "labelLine": {"show": False},
                "data": xyz_data
            }
        ]
    }, height="300px")
    st.markdown("### Рекомендации:")
    for comment in analysis['xyz']['comments']:
        st.warning(comment)

with tabs[5]:
    st.subheader("Сопроводительное письмо")
    st.text_area("Черновик письма", value=cover_letter, height=200)
    st.download_button("📥 Скачать отчет (PDF)", data=pdf_buffer, file_name="report.pdf")
