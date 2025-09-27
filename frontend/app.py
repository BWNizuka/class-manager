import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from dotenv import dotenv_values
from pymongo import MongoClient

from ..backend.services.class_manager import ClassManager
from backend.data.models import Student, Teacher, Course

# -----------------------------
# Load biến môi trường từ .env
# -----------------------------
config = dotenv_values(".env")
MONGO_URI = config.get("MONGO_URI")
DB_NAME = config.get("DB_NAME", "classmanager")

# Debug hiển thị trong sidebar
st.sidebar.caption(f"🔌 Using DB: {DB_NAME}")

# -----------------------------
# Kết nối MongoDB
# -----------------------------
@st.cache_resource
def get_db():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=8000)
        client.admin.command("ping")  # test kết nối
        return client[DB_NAME]
    except Exception as e:
        st.error(f"❌ MongoDB connection failed: {e}")
        return None

db = get_db()

if db is not None:
    students_col = db["students"]
    teachers_col = db["teachers"]
    courses_col = db["courses"]
    manager = ClassManager(students_col, teachers_col, courses_col)
else:
    students_col = teachers_col = courses_col = None
    manager = None

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Class Manager", layout="wide")
st.title("📚 Class Manager — OOP + MongoDB + Streamlit")

if db is None:
    st.warning("❌ Không kết nối được tới MongoDB. Kiểm tra file .env và chuỗi MONGO_URI.")
    st.stop()

menu = st.sidebar.selectbox("Menu", [
    "Dashboard", "Students", "Teachers", "Courses", "Assign Teacher", "Enroll Student"
])

# Dashboard
if menu == "Dashboard":
    st.subheader("📊 Dashboard")
    st.metric("Students", len(manager.read_students()))
    st.metric("Teachers", len(manager.read_teachers()))
    st.metric("Courses", len(manager.read_courses()))

# Students
elif menu == "Students":
    st.subheader("👩‍🎓 Students CRUD")
    with st.form("create_student"):
        sid = st.text_input("ID")
        name = st.text_input("Name")
        email = st.text_input("Email")
        grade = st.number_input("Grade level", 1, 20, 10)
        if st.form_submit_button("Add"):
            ok, msg = manager.create_student(Student(sid, name, email, int(grade)))
            if ok:
                st.success(msg)
            else:
                st.error(msg)
    st.dataframe(pd.DataFrame(manager.read_students()))

# Teachers
elif menu == "Teachers":
    st.subheader("👨‍🏫 Teachers CRUD")
    with st.form("create_teacher"):
        tid = st.text_input("ID")
        name = st.text_input("Name")
        email = st.text_input("Email")
        spec = st.text_input("Specialization")
        if st.form_submit_button("Add"):
            ok, msg = manager.create_teacher(Teacher(tid, name, email, spec))
            if ok:
                st.success(msg)
            else:
                st.error(msg)
    st.dataframe(pd.DataFrame(manager.read_teachers()))

# Courses
elif menu == "Courses":
    st.subheader("📘 Courses CRUD")
    with st.form("create_course"):
        code = st.text_input("Course Code")
        title = st.text_input("Title")
        schedule = st.text_input("Schedule")
        if st.form_submit_button("Add"):
            ok, msg = manager.create_course(Course(code, title, schedule))
            if ok:
                st.success(msg)
            else:
                st.error(msg)
    st.dataframe(pd.DataFrame(manager.read_courses()))

# Assign Teacher
elif menu == "Assign Teacher":
    st.subheader("👨‍🏫➡️📘 Assign Teacher to Course")
    teachers = manager.read_teachers()
    courses = manager.read_courses()
    if teachers and courses:
        tid = st.selectbox("Teacher", [t["teacher_id"] for t in teachers])
        cid = st.selectbox("Course", [c["course_code"] for c in courses])
        if st.button("Assign"):
            ok, msg = manager.assign_teacher(tid, cid)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
    else:
        st.info("Cần có teacher và course trước.")

# Enroll Student
elif menu == "Enroll Student":
    st.subheader("👩‍🎓➡️📘 Enroll Student in Course")
    students = manager.read_students()
    courses = manager.read_courses()
    if students and courses:
        sid = st.selectbox("Student", [s["student_id"] for s in students])
        cid = st.selectbox("Course", [c["course_code"] for c in courses])
        if st.button("Enroll"):
            ok, msg = manager.enroll_student(sid, cid)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
    else:
        st.info("Cần có student và course trước.")
