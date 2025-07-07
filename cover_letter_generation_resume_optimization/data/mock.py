import random

def generate_mock_candidates():
    skills_mock = [
        "Python", "Django", "Flask", "SQL", "Git", "PostgreSQL", "Docker", "Kubernetes",
        "CI/CD", "React", "TypeScript", "HTML", "Sklearn", "Pandas", "TestRail",
        "Selenium", "Postman", "Agile", "Scrum", "Jira", "BPMN", "Confluence",
        "PyTorch", "MLflow", "Terraform", "AWS"
    ]

    experience_gaps_mock = [
        "Нет опыта с микросервисами",
        "Нет опыта работы в команде",
        "Не участвовал в крупных проектах",
        "Нет опыта с облачными провайдерами",
        "Нет коммерческого опыта"
    ]

    recommendations_mock = [
        "Спросить о проекте с REST API",
        "Уточнить опыт CI/CD",
        "Спросить про работу над pet-проектами",
        "Уточнить опыт автоматизации тестирования",
        "Спросить о взаимодействии с бизнесом",
        "Проверить знание алгоритмов",
        "Уточнить знание SQL и аналитики"
    ]

    candidates_mock = [
        ("Иван Иванов", "Backend-разработчик", 82, ["Python", "Django", "PostgreSQL"], 101, "Senior Python Developer"),
        ("Мария Смирнова", "Backend-разработчик", 65, ["Flask", "SQL", "Git"], 101, "Senior Python Developer"),
        ("Алексей Ким", "DevOps-инженер", 77, ["Docker", "Kubernetes", "CI/CD"], 102, "DevOps Engineer"),
        ("Ольга Кузнецова", "Frontend-разработчик", 88, ["React", "TypeScript", "HTML"], 103, "Frontend Developer"),
        ("Дмитрий Орлов", "Data Scientist", 71, ["Python", "Pandas", "Sklearn"], 104, "Data Scientist"),
        ("Наталья Фомина", "QA Engineer", 79, ["TestRail", "Selenium", "Postman"], 105, "QA Engineer"),
        ("Виктор Седов", "Project Manager", 68, ["Agile", "Scrum", "Jira"], 106, "IT Project Manager"),
        ("Елена Громова", "Business Analyst", 74, ["SQL", "BPMN", "Confluence"], 107, "Business Analyst"),
        ("Руслан Беляев", "ML Engineer", 91, ["PyTorch", "MLflow", "Docker"], 104, "Data Scientist"),
        ("Ксения Литвинова", "DevOps-инженер", 86, ["Terraform", "AWS", "CI/CD"], 102, "DevOps Engineer")
    ]

    candidates = []
    for i, (name, position, score, skills, v_id, v_title) in enumerate(candidates_mock):
        missing_pool = list(set(skills_mock) - set(skills))
        missing_k = min(len(missing_pool), random.randint(1, 3))
        matched_k = min(len(skills), random.randint(2, min(4, len(skills))))
        candidates.append({
            "id": i,
            "name": name,
            "position": position,
            "matching_score": score,
            "matched_skills": random.sample(skills, k=matched_k),
            "missing_skills": random.sample(missing_pool, k=missing_k),
            "experience_gaps": random.sample(experience_gaps_mock, k=random.randint(0, 2)),
            "recommendations": random.sample(recommendations_mock, k=random.randint(1, 3)),
            "vacancy_id": v_id,
            "vacancy_title": v_title
        })
    return candidates
