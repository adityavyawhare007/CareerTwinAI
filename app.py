import pandas as pd
import joblib
import sqlite3
import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_file
)

from pdf_generator import generate_report

DATABASE = "database/career.db"

app = Flask(__name__)

# Load AI Model
model = joblib.load("ml_model/career_model.pkl")
encoders = joblib.load("ml_model/label_encoders.pkl")

app.secret_key = "CareerTwinAI2026"

# ===========================================
# Career Information Database
# ===========================================

career_info = {

    "Machine Learning Engineer": {
        "description": "Designs intelligent AI systems and predictive models using Python, Machine Learning and Data Science.",
        "salary": "₹8 LPA - ₹18 LPA",
        "skills": ["Python","Machine Learning","Statistics","SQL"],
        "courses": ["Python Advanced","Machine Learning","Data Science"]
    },

    "Software Engineer": {
        "description": "Develops software applications using programming languages and algorithms.",
        "salary": "₹6 LPA - ₹15 LPA",
        "skills": ["Java","Python","Git","OOP"],
        "courses": ["Java Programming","Data Structures","Software Engineering"]
    },

    "Web Developer": {
        "description": "Builds responsive websites and web applications.",
        "salary": "₹4 LPA - ₹10 LPA",
        "skills": ["HTML","CSS","JavaScript","React"],
        "courses": ["Frontend Development","JavaScript","React"]
    },

    "Database Administrator": {
        "description": "Manages databases and improves performance.",
        "salary": "₹5 LPA - ₹12 LPA",
        "skills": ["SQL","Oracle","Database Design","Backup"],
        "courses": ["SQL","Oracle Database","Database Administration"]
    },

    "Data Analyst": {
        "description": "Analyzes business data for better decision making.",
        "salary": "₹6 LPA - ₹14 LPA",
        "skills": ["Python","Excel","Power BI","SQL"],
        "courses": ["Data Analysis","Power BI","Python"]
    },

    "Cyber Security Analyst": {
        "description": "Protects systems from cyber attacks.",
        "salary": "₹6 LPA - ₹16 LPA",
        "skills": ["Network Security","Ethical Hacking","Linux","Cyber Security"],
        "courses": ["Cyber Security","CEH Basics","Network Security"]
    },

    "Network Engineer": {
        "description": "Designs and manages computer networks.",
        "salary": "₹5 LPA - ₹11 LPA",
        "skills": ["Networking","Cisco","Routing","Switching"],
        "courses": ["CCNA","Networking","Network Security"]
    },

    "Cloud Engineer": {
        "description": "Develops cloud infrastructure.",
        "salary": "₹8 LPA - ₹20 LPA",
        "skills": ["AWS","Azure","Linux","Docker"],
        "courses": ["AWS Cloud","Azure Fundamentals","Docker"]
    },

    "QA Engineer": {
        "description": "Tests software quality.",
        "salary": "₹4 LPA - ₹9 LPA",
        "skills": ["Testing","Selenium","Automation","Bug Tracking"],
        "courses": ["Software Testing","Selenium","Automation Testing"]
    },

    "UI UX Designer": {
        "description": "Designs attractive user interfaces.",
        "salary": "₹5 LPA - ₹12 LPA",
        "skills": ["Figma","Adobe XD","UI Design","UX Research"],
        "courses": ["UI Design","Figma","UX Design"]
    }

}

career_skill_gap = {

    "Machine Learning Engineer":{

        "strengths":[
            "Python",
            "Problem Solving",
            "Artificial Intelligence"
        ],

        "missing":[
            "Statistics",
            "NumPy",
            "Pandas",
            "TensorFlow"
        ],

        "recommendation":
        "Improve your Statistics and TensorFlow knowledge before applying for Machine Learning roles."

    },

    "Software Engineer":{

        "strengths":[
            "Programming",
            "Java",
            "Problem Solving"
        ],

        "missing":[
            "Data Structures",
            "Algorithms",
            "Git",
            "System Design"
        ],

        "recommendation":
        "Practice Data Structures and Git to become a stronger Software Engineer."

    },

    "Web Developer":{

        "strengths":[
            "HTML",
            "CSS",
            "JavaScript"
        ],

        "missing":[
            "React",
            "Node.js",
            "REST API",
            "MongoDB"
        ],

        "recommendation":
        "Learn React and Node.js to become a Full Stack Web Developer."

    },

    "Data Analyst":{

        "strengths":[
            "SQL",
            "Excel",
            "Python"
        ],

        "missing":[
            "Power BI",
            "Statistics",
            "Pandas",
            "Visualization"
        ],

        "recommendation":
        "Focus on Power BI and Statistics to become an industry-ready Data Analyst."

    }

}

career_roadmap = {

    "Machine Learning Engineer":[

        "Python Advanced",
        "Statistics",
        "NumPy & Pandas",
        "Machine Learning",
        "TensorFlow",
        "Build 3 ML Projects",
        "Apply for Internship"

    ],

    "Software Engineer":[

        "Java Advanced",
        "Data Structures",
        "Algorithms",
        "Git & GitHub",
        "System Design",
        "Build Full Stack Project",
        "Apply for Internship"

    ],

    "Web Developer":[

        "HTML & CSS",
        "JavaScript",
        "React",
        "Node.js",
        "MongoDB",
        "Build Portfolio Website",
        "Apply for Internship"

    ],

    "Data Analyst":[

        "Excel",
        "SQL",
        "Python",
        "Power BI",
        "Statistics",
        "Dashboard Project",
        "Apply for Internship"

    ]

}

def create_database():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        mobile TEXT NOT NULL,
        education TEXT NOT NULL,
        password TEXT NOT NULL

    )
    """)

    connection.commit()
    cursor.execute("""

CREATE TABLE IF NOT EXISTS prediction_history(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    email TEXT,

    career TEXT,

    confidence REAL,

    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        connection=sqlite3.connect(DATABASE)
        cursor=connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email,password)
        )

        user=cursor.fetchone()

        connection.close()

        if user:

            session["user"] = user[1]
            session["email"] = user[2]

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid Email or Password!"
        )

    return render_template("login.html")


@app.route("/register",methods=["GET","POST"])
def register():

    if request.method=="POST":

        full_name=request.form["full_name"]
        email=request.form["email"]
        mobile=request.form["mobile"]
        education=request.form["education"]
        password=request.form["password"]
        confirm_password=request.form["confirm_password"]

        if password!=confirm_password:

            return render_template(
                "register.html",
                error="Passwords do not match!"
            )

        connection=sqlite3.connect(DATABASE)
        cursor=connection.cursor()

        try:

            cursor.execute("""
            INSERT INTO users
            (full_name,email,mobile,education,password)
            VALUES(?,?,?,?,?)
            """,
            (full_name,email,mobile,education,password))

            connection.commit()

        except sqlite3.IntegrityError:

            connection.close()

            return render_template(
                "register.html",
                error="Email already exists!"
            )

        connection.close()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(

        """
        SELECT COUNT(*)
        FROM prediction_history
        WHERE email=?
        """,

        (session["email"],)

    )

    total_predictions = cursor.fetchone()[0]

    cursor.execute(

        """
        SELECT career, confidence

        FROM prediction_history

        WHERE email=?

        ORDER BY prediction_date DESC

        LIMIT 1
        """,

        (session["email"],)

    )

    latest = cursor.fetchone()

    connection.close()

    if latest:

        latest_career = latest[0]
        latest_confidence = latest[1]

    else:

        latest_career = "No Prediction Yet"
        latest_confidence = 0

    return render_template(

        "dashboard.html",

        user=session["user"],

        total_predictions=total_predictions,

        latest_career=latest_career,

        latest_confidence=latest_confidence

    )


@app.route("/prediction")
def prediction():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("prediction.html")


@app.route("/predict", methods=["POST"])
def predict():

    if "user" not in session:
        return redirect(url_for("login"))

    # ============================
    # Get Form Data
    # ============================

    education = request.form["education"]
    percentage = int(request.form["percentage"])
    favorite_subject = request.form["favorite_subject"]

    programming_skill = request.form["programming_skill"]
    communication = request.form["communication"]
    problem_solving = request.form["problem_solving"]

    interest = request.form["interest"]
    work_style = request.form["work_style"]

    # ============================
    # Dynamic Skill Analysis
    # ============================

    skill_map = {
        "Beginner": 45,
        "Average": 65,
        "Good": 80,
        "Excellent": 95
    }

    programming_score = skill_map.get(programming_skill, 70)
    communication_score = skill_map.get(communication, 70)
    problem_score = skill_map.get(problem_solving, 70)

    # ============================
    # Encode Data
    # ============================

    education_encoded = encoders["Education"].transform([education])[0]
    favorite_subject_encoded = encoders["Favorite_Subject"].transform([favorite_subject])[0]
    programming_encoded = encoders["Programming_Skill"].transform([programming_skill])[0]
    communication_encoded = encoders["Communication"].transform([communication])[0]
    problem_encoded = encoders["Problem_Solving"].transform([problem_solving])[0]
    interest_encoded = encoders["Interest"].transform([interest])[0]
    work_style_encoded = encoders["Work_Style"].transform([work_style])[0]

    # ============================
    # Create DataFrame
    # ============================

    input_data = pd.DataFrame([{

        "Education": education_encoded,
        "Percentage": percentage,
        "Favorite_Subject": favorite_subject_encoded,
        "Programming_Skill": programming_encoded,
        "Communication": communication_encoded,
        "Problem_Solving": problem_encoded,
        "Interest": interest_encoded,
        "Work_Style": work_style_encoded

    }])

    # ============================
    # Predict
    # ============================

    probabilities = model.predict_proba(input_data)[0]

    top3_index = probabilities.argsort()[-3:][::-1]

    top3 = []

    for index in top3_index:

        career_name = encoders["Career"].inverse_transform([index])[0]

        score = round(probabilities[index] * 100, 2)

        top3.append({

            "career": career_name,
            "score": score

        })

    career = top3[0]["career"]
    confidence = top3[0]["score"]

    info = career_info.get(

        career,

        {

            "description": "Career information not available.",
            "salary": "N/A",
            "skills": [],
            "courses": []

        }

    )

    gap = career_skill_gap.get(

        career,

        {

            "strengths": [],
            "missing": [],
            "recommendation": "Keep improving your skills."

        }

    )

    roadmap = career_roadmap.get(career, [])

    # ============================
    # Save History
    # ============================

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(

        """
        INSERT INTO prediction_history
        (email, career, confidence)
        VALUES (?, ?, ?)
        """,

        (
            session["email"],
            career,
            confidence
        )

    )

    connection.commit()
    connection.close()

    # ============================
    # Store Report
    # ============================

    session["report"] = {

        "name": session["user"],
        "career": career,
        "confidence": confidence,
        "description": info["description"],
        "salary": info["salary"],
        "skills": info["skills"],
        "courses": info["courses"],
        "top3": top3,
        "roadmap": roadmap,

        "skill_analysis": [

            {
                "name": "Python",
                "score": programming_score
            },

            {
                "name": "Communication",
                "score": communication_score
            },

            {
                "name": "Problem Solving",
                "score": problem_score
            }

        ]

    }

    return render_template(

        "result.html",

        career=career,
        confidence=confidence,

        description=info["description"],
        salary=info["salary"],

        skills=info["skills"],
        courses=info["courses"],

        top3=top3,

        strengths=gap["strengths"],
        missing=gap["missing"],
        recommendation=gap["recommendation"],

        roadmap=roadmap

    )
    

@app.route("/download-report")
def download_report():

    if "report" not in session:

        return redirect(url_for("prediction"))

    report = session["report"]

    filename = "CareerTwinAI_Report.pdf"

    generate_report(

        filename=filename,

        name=report["name"],

        career=report["career"],

        confidence=report["confidence"],

        description=report["description"],

        salary=report["salary"],

        skills=report["skills"],

        courses=report["courses"],

        top3=report["top3"]

    )

    return send_file(

        filename,

        as_attachment=True,

        download_name="CareerTwinAI_Report.pdf"

    )

@app.route("/history")
def history():

    if "user" not in session:

        return redirect(url_for("login"))

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(

    """
    SELECT career,
           confidence,
           prediction_date

    FROM prediction_history

    WHERE email=?

    ORDER BY prediction_date DESC
    """,

    (session["email"],)

)

    history = cursor.fetchall()

    connection.close()

    return render_template(

        "history.html",

        history=history

    )

@app.route("/roadmap")
def roadmap():

    if "user" not in session:
        return redirect(url_for("login"))

    if "report" not in session:
        return redirect(url_for("prediction"))

    return render_template(
        "roadmap.html",
        roadmap=session["report"]["roadmap"],
        career=session["report"]["career"]
    )
@app.route("/courses")
def courses():

    if "user" not in session:
        return redirect(url_for("login"))

    courses_data = [

        {
            "title":"Python Advanced",
            "description":"Master Advanced Python Programming for AI and Software Development.",
            "rating":"★★★★★",
            "link":"https://www.youtube.com/results?search_query=Python+Advanced+Course"
        },

        {
            "title":"Machine Learning",
            "description":"Learn Machine Learning using Scikit-Learn and Python.",
            "rating":"★★★★★",
            "link":"https://www.youtube.com/results?search_query=Machine+Learning+Course"
        },

        {
            "title":"Data Science",
            "description":"Complete Data Science Bootcamp with Real Projects.",
            "rating":"★★★★★",
            "link":"https://www.youtube.com/results?search_query=Data+Science+Course"
        },

        {
            "title":"SQL",
            "description":"Master SQL Database Queries from Beginner to Advanced.",
            "rating":"★★★★☆",
            "link":"https://www.youtube.com/results?search_query=SQL+Course"
        },

        {
            "title":"Git & GitHub",
            "description":"Version Control and GitHub for Professional Developers.",
            "rating":"★★★★☆",
            "link":"https://www.youtube.com/results?search_query=Git+GitHub+Course"
        }

    ]

    return render_template(

        "courses.html",

        courses=courses_data

    )

@app.route("/projects")
def projects():

    if "user" not in session:
        return redirect(url_for("login"))

    projects_data = [

        {
            "title":"House Price Prediction",
            "difficulty":"⭐⭐⭐☆☆",
            "duration":"2 Weeks",
            "description":"Build an ML model to predict house prices using Python and Scikit-Learn.",
            "link":"https://www.kaggle.com/search?q=House+Price+Prediction"
        },

        {
            "title":"Spam Email Detection",
            "difficulty":"⭐⭐⭐☆☆",
            "duration":"2 Weeks",
            "description":"Detect spam emails using Machine Learning and Natural Language Processing.",
            "link":"https://www.kaggle.com/search?q=Spam+Detection"
        },

        {
            "title":"Face Mask Detection",
            "difficulty":"⭐⭐⭐⭐☆",
            "duration":"3 Weeks",
            "description":"Detect face masks using OpenCV and Deep Learning.",
            "link":"https://www.kaggle.com/search?q=Face+Mask+Detection"
        },

        {
            "title":"Resume Screening AI",
            "difficulty":"⭐⭐⭐⭐⭐",
            "duration":"4 Weeks",
            "description":"Automatically screen resumes using Artificial Intelligence.",
            "link":"https://www.kaggle.com/search?q=Resume+Screening"
        },

        {
            "title":"Student Performance Prediction",
            "difficulty":"⭐⭐⭐☆☆",
            "duration":"2 Weeks",
            "description":"Predict student academic performance using Machine Learning.",
            "link":"https://www.kaggle.com/search?q=Student+Performance"
        }

    ]

    return render_template(
        "projects.html",
        projects=projects_data
    )

@app.route("/skill-analysis")
def skill_analysis():

    if "user" not in session:
        return redirect(url_for("login"))

    if "report" not in session:

        return redirect(url_for("prediction"))

    skills = session["report"]["skill_analysis"]

    return render_template(

        "skill_analysis.html",

        skills=skills

    )

@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(

        """
        SELECT full_name,
               email,
               mobile,
               education

        FROM users

        WHERE email=?
        """,

        (session["email"],)

    )

    user = cursor.fetchone()

    connection.close()

    return render_template(

        "profile.html",

        user=user

    )

@app.route("/settings")
def settings():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("settings.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":

    create_database()

    app.run(debug=True)