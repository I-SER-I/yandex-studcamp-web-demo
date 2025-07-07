from io import BytesIO


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


mock_resume = {
    "name": "Райан Гослин",
    "title": "Python Developer",
    "experience": [
        {"company": "ООО Рога и Копыта", "role": "Backend Developer",
         "description": "Разработка REST API на Flask, PostgreSQL, Docker."},
        {"company": "TechStar", "role": "ML Engineer",
         "description": "Разработка ML-пайплайнов, оптимизация моделей, пайплайны на Airflow."}
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
        {"old": "Разработка REST API на Flask",
         "new": "Проектирование и реализация REST API на Flask с покрытием тестами"},
        {"old": "ML-пайплайны", "new": "Построение production-ready ML пайплайнов на Airflow"}
    ]
}

mock_cover_letter = """
Уважаемые представители Ozon,

Изучив вакансию Senior Python Developer, я понял, что мои навыки и опыт идеально соответствуют вашим требованиям. За последние 5 лет я работал над созданием высоконагруженных backend-систем, используя Flask и FastAPI. Я также активно применяю Docker, PostgreSQL, участвую в Agile-разработке и покрываю код тестами.

С радостью расскажу подробнее при личной встрече.

С уважением, Райан Гослин
"""

mock_analysis = {
    "score": 63,
    "keywords": {"score": 3, "found": [".NET"], "missing": ["Docker", "Redis", "backend", "QA"]},
    "structure": {"score": 63,
                  "sections": {"О себе": 80, "Образование": 100, "Опыт работы": 60, "Навыки": 0, "Сертификаты": 0,
                               "Проекты": 0, "Языки": 100}},
    "tone": {"score": 100, "comment": "Ваше резюме имеет профессиональный и позитивный тон"},
    "xyz": {"score": 17, "x": 5, "y": 0, "z": 0, "comments": ["Добавьте количественные метрики в опыт работы.",
                                                              "Опишите методы и инструменты, которые вы использовали."]},
    "contacts": {"score": 100, "found": 4},
    "recommendations": [
        "Раздел образования хорошо отформатирован",
        "Контактная информация четко представлена",
        "Рекомендуется добавить описание проектов для демонстрации навыков"
    ]
}
