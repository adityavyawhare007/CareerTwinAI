import random
import pandas as pd

random.seed(42)

communication_levels = ["Excellent", "Good", "Average"]
work_styles = ["Remote", "Office", "Hybrid"]

career_rules = {

    "Machine Learning Engineer": {
        "subject": ["Python"],
        "interest": "Artificial Intelligence",
        "percentage": (88, 98),
        "programming": ["Excellent"],
        "problem": ["Excellent"]
    },

    "Software Engineer": {
        "subject": ["Java"],
        "interest": "Software Development",
        "percentage": (75, 95),
        "programming": ["Excellent", "Good"],
        "problem": ["Excellent", "Good"]
    },

    "Web Developer": {
        "subject": ["HTML CSS JS"],
        "interest": "Web Development",
        "percentage": (70, 92),
        "programming": ["Excellent", "Good"],
        "problem": ["Excellent", "Good"]
    },

    "Database Administrator": {
        "subject": ["SQL"],
        "interest": "Database",
        "percentage": (72, 94),
        "programming": ["Excellent", "Good"],
        "problem": ["Excellent", "Good"]
    },

    "Data Analyst": {
        "subject": ["Python", "SQL"],
        "interest": "Data Science",
        "percentage": (76, 95),
        "programming": ["Excellent", "Good"],
        "problem": ["Excellent", "Good"]
    },

    "Cyber Security Analyst": {
        "subject": ["Cyber Security"],
        "interest": "Security",
        "percentage": (74, 95),
        "programming": ["Excellent", "Good"],
        "problem": ["Excellent", "Good"]
    },

    "Network Engineer": {
        "subject": ["Networking"],
        "interest": "Networking",
        "percentage": (72, 94),
        "programming": ["Excellent", "Good"],
        "problem": ["Excellent", "Good"]
    },

    "Cloud Engineer": {
        "subject": ["Cloud Computing"],
        "interest": "Cloud",
        "percentage": (75, 96),
        "programming": ["Excellent", "Good"],
        "problem": ["Excellent", "Good"]
    },

    "QA Engineer": {
        "subject": ["Testing"],
        "interest": "Software Testing",
        "percentage": (70, 92),
        "programming": ["Excellent", "Good"],
        "problem": ["Excellent", "Good"]
    },

    "UI UX Designer": {
        "subject": ["UI UX"],
        "interest": "Design",
        "percentage": (70, 92),
        "programming": ["Good"],
        "problem": ["Good", "Average"]
    }

}

rows = []

for career, rule in career_rules.items():

    for _ in range(50):

        percentage = random.randint(*rule["percentage"])

        if percentage >= 90:
            communication = random.choice(["Excellent", "Good"])
        elif percentage >= 80:
            communication = random.choice(["Good", "Excellent"])
        else:
            communication = random.choice(["Average", "Good"])

        rows.append({

            "Education": "Diploma CSE",

            "Percentage": percentage,

            "Favorite_Subject": random.choice(rule["subject"]),

            "Programming_Skill": random.choice(rule["programming"]),

            "Communication": communication,

            "Problem_Solving": random.choice(rule["problem"]),

            "Interest": rule["interest"],

            "Work_Style": random.choice(work_styles),

            "Career": career

        })

df = pd.DataFrame(rows)

df = df.sample(frac=1).reset_index(drop=True)

df.to_csv("dataset/career_dataset.csv", index=False)

print(f"✅ Dataset Generated Successfully!")
print(f"Total Rows : {len(df)}")