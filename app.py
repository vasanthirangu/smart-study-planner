import streamlit as st
import datetime
import PyPDF2
from google import genai
import urllib.parse
from docx import Document
import pandas as pd

# ==============================
# 🔐 API KEY & CONFIG
# ==============================
API_KEY = "AIzaSyCzM8cHRhS0oO2TP8BE9NMzhil5FpKW5ZU"
PRIMARY_MODEL = "gemini-1.5-flash"

AI_AVAILABLE = False
client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
        AI_AVAILABLE = True
    except Exception as e:
        st.error(f"AI Initialization Error: {e}")

# ==============================
# 🔁 Safe Gemini Call
# ==============================
def generate_with_retry(prompt):
    if not AI_AVAILABLE: return None
    try:
        response = client.models.generate_content(model=PRIMARY_MODEL, contents=prompt)
        return response.text.strip() if hasattr(response, "text") else None
    except Exception as e:
        st.error(f"AI Error: {e}")
    return None

# ==============================
# 📄 Extract Topics
# ==============================
def extract_topics_from_text(text):
    if not AI_AVAILABLE: return text
    prompt = f"Extract important study topics from this syllabus. Return only clean bullet points.\n{text}"
    result = generate_with_retry(prompt)
    return result if result else text

# ==============================
# 🔗 Generate Learning Links
# ==============================
def generate_learning_links(topics_string):
    topics = topics_string.split("\n")
    links = []
    for topic in topics:
        topic = topic.strip()
        if topic and "Revision" not in topic:
            query = urllib.parse.quote_plus(topic + " tutorial")
            links.append(f"https://www.google.com/search?q={query}")
    return "\n".join(links)

# ==============================
# 📅 Generate Study Schedule
# ==============================
def generate_study_schedule(subject, topics, exam_date, hours_per_day):
    today = datetime.date.today()
    total_days = (exam_date - today).days
    if total_days <= 0: return None

    topic_list = [t.strip("-• ").strip() for t in topics.replace(",", "\n").split("\n") if t.strip()]
    if not topic_list: return None

    topics_per_day = (len(topic_list) + total_days - 1) // total_days
    schedule_data = []
    index = 0

    for i in range(total_days):
        current_date = today + datetime.timedelta(days=i)
        daily_topics = topic_list[index:index + topics_per_day]
        index += topics_per_day
        if not daily_topics: break
        
        if current_date.weekday() == 6: daily_topics.append("Revision ✨")
        
        topics_str = "\n".join(daily_topics)
        schedule_data.append({
            "Date": current_date.strftime("%d-%m-%Y"),
            "Subject": subject,
            "Topics": topics_str,
            "Resources": generate_learning_links(topics_str),
            "Hrs": hours_per_day
        })
    return schedule_data

# ==============================
# 🔄 RESCHEDULE FUNCTION
# ==============================
def reschedule_from_missed_day(schedule_df, missed_date):
    df = schedule_df.copy()
    df["Date_obj"] = pd.to_datetime(df["Date"], format="%d-%m-%Y").dt.date
    missed_idx = df[df["Date"] == missed_date].index[0]
    missed_topics = df.loc[missed_idx, "Topics"].split("\n")
    future_df = df.loc[missed_idx + 1:]

    if future_df.empty: return None

    topics_per_day = (len(missed_topics) + len(future_df) - 1) // len(future_df)
    for i in range(len(future_df)):
        extra = missed_topics[i*topics_per_day : (i+1)*topics_per_day]
        if extra:
            new_topics = df.loc[future_df.index[i], "Topics"] + "\n" + "\n".join(extra)
            df.at[future_df.index[i], "Topics"] = new_topics
            df.at[future_df.index[i], "Resources"] = generate_learning_links(new_topics)

    return df.drop(index=missed_idx).drop(columns=["Date_obj"]).reset_index(drop=True)

# ==============================
# 🌐 STREAMLIT UI
# ==============================
st.set_page_config(page_title="Smart Study Planner", layout="wide")
st.title("📚 Smart Study Planner Agent")

st.markdown("""
<style>
    table { width: 100%; }
    td { white-space: pre-line !important; vertical-align: top !important; word-break: break-word !important; }
    .stDownloadButton { text-align: right; }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    subject = st.text_input("Subject Name")
    topics_input = st.text_area("Topics (one per line)", height=150)
    uploaded_file = st.file_uploader("Upload Syllabus", type=["pdf", "txt", "docx"])

with col2:
    exam_date = st.date_input("Exam Date", min_value=datetime.date.today() + datetime.timedelta(days=1))
    hours = st.number_input("Study Hours", 1, 12, 4)
    generate_btn = st.button("🚀 Generate Study Plan", use_container_width=True)

# Process File
if uploaded_file and "extracted" not in st.session_state:
    text = ""
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "".join([p.extract_text() for p in reader.pages if p.extract_text()])
    elif uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")
    else:
        doc = Document(uploaded_file)
        text = "\n".join([p.text for p in doc.paragraphs])
    
    st.session_state["extracted"] = extract_topics_from_text(text)
    st.success("Syllabus scanned!")

if generate_btn:
    final_topics = topics_input if topics_input.strip() else st.session_state.get("extracted", "")
    if subject and final_topics:
        sched = generate_study_schedule(subject, final_topics, exam_date, hours)
        if sched: st.session_state["schedule_df"] = pd.DataFrame(sched)

# ==============================
# 📅 Display & Download
# ==============================
if "schedule_df" in st.session_state:
    df = st.session_state["schedule_df"]
    
    st.divider()
    d_col1, d_col2 = st.columns([4, 1])
    with d_col1:
        st.subheader("📅 Your Plan")
    with d_col2:
        # DOWNLOAD BUTTON
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{subject}_study_plan.csv",
            mime="text/csv",
        )
    
    st.table(df)

    # Reschedule Logic
    st.divider()
    st.subheader("🔄 Missed a Day?")
    missed_day = st.selectbox("Select Date", df["Date"].tolist())
    if st.button("Reschedule"):
        new_df = reschedule_from_missed_day(df, missed_day)
        if new_df is not None:
            st.session_state["schedule_df"] = new_df
            st.rerun()
