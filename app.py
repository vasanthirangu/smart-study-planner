# import streamlit as st
# import datetime
# import PyPDF2
# import os
# from dotenv import load_dotenv
# from google import genai
# import time

# # ==============================
# # 🔐 Load Environment Variables
# # ==============================

# load_dotenv()
# API_KEY = os.getenv("GOOGLE_API_KEY")

# AI_AVAILABLE = False
# client = None

# if API_KEY:
#     try:
#         client = genai.Client(api_key=API_KEY)
#         AI_AVAILABLE = True
#     except Exception:
#         AI_AVAILABLE = False


# PRIMARY_MODEL = "gemini-1.5-flash"
# FALLBACK_MODEL = "gemini-1.5-flash-8b"


# # ==============================
# # 🔁 Safe Gemini Call
# # ==============================

# def generate_with_retry(prompt):
#     if not AI_AVAILABLE:
#         return None

#     for attempt in range(3):
#         try:
#             response = client.models.generate_content(
#                 model=PRIMARY_MODEL,
#                 contents=prompt
#             )
#             return response.text
#         except Exception:
#             time.sleep(2)

#     try:
#         response = client.models.generate_content(
#             model=FALLBACK_MODEL,
#             contents=prompt
#         )
#         return response.text
#     except Exception:
#         return None


# # ==============================
# # 📄 Extract Topics from PDF/Text
# # ==============================

# def extract_topics_from_text(text):
#     if not AI_AVAILABLE:
#         return text

#     prompt = f"""
#     Extract important study topics from this syllabus.
#     Return as clean bullet points only.

#     {text}
#     """

#     result = generate_with_retry(prompt)
#     return result if result else text


# # ==============================
# # 📅 Generate Study Schedule
# # ==============================

# def generate_study_schedule(subject, topics, exam_date, hours_per_day):

#     today = datetime.date.today()
#     days_left = (exam_date - today).days

#     if days_left <= 0:
#         return None

#     # Clean and split topics properly
#     topic_list = []

#     for line in topics.split("\n"):
#         parts = line.split(",")  # split long comma lines
#         for part in parts:
#             cleaned = part.strip("-• ").strip()
#             if cleaned:
#                 topic_list.append(cleaned)

#     if not topic_list:
#         return None

#     total_topics = len(topic_list)

#     # Distribute evenly using ceiling division
#     topics_per_day = (total_topics + days_left - 1) // days_left

#     schedule_data = []
#     index = 0

#     for i in range(days_left):
#         current_date = today + datetime.timedelta(days=i)

#         daily_topics = topic_list[index:index + topics_per_day]
#         index += topics_per_day

#         if not daily_topics:
#             break

#         # Add Sunday revision
#         if current_date.weekday() == 6:
#             daily_topics.append("Revision")

#         schedule_data.append({
#             "Date": current_date.strftime("%d-%m-%Y"),
#             "Subject": subject,
#             "Topics": " | ".join(daily_topics),
#             "Hours per Day": hours_per_day
#         })

#     return schedule_data


# # ==============================
# # 🌐 Streamlit UI
# # ==============================

# # st.set_page_config(page_title="Smart Study Planner", layout="wide")
# # st.title("📚 Smart Study Planner Agent")

# # subject = st.text_input("Enter Subject Name")

# # topics_input = st.text_area("Enter Topics (one per line or comma separated)")

# # uploaded_file = st.file_uploader(
# #     "Upload syllabus file (PDF or TXT)",
# #     type=["pdf", "txt"]
# # )

# # exam_date = st.date_input("Exam Date")
# # hours = st.number_input("Hours per day", 1, 12, 2)

# # extracted_topics = ""
# # ==============================
# # 🌐 Streamlit UI (Improved UI)
# # ==============================

# st.set_page_config(
#     page_title="Smart Study Planner",
#     page_icon="📚",
#     layout="wide"
# )

# st.markdown("""
#     <style>
#         .main-title {
#             font-size: 40px;
#             font-weight: bold;
#         }
#         .section-title {
#             font-size: 22px;
#             font-weight: 600;
#             margin-top: 20px;
#         }
#     </style>
# """, unsafe_allow_html=True)

# st.markdown('<p class="main-title">📚 Smart Study Planner Agent</p>', unsafe_allow_html=True)
# st.write("Generate structured AI-powered study schedules in seconds.")

# st.divider()

# # ==============================
# # 📌 Layout Columns
# # ==============================

# left, right = st.columns([2, 1])

# with left:
#     st.markdown('<p class="section-title">📝 Study Details</p>', unsafe_allow_html=True)

#     subject = st.text_input("Subject Name")

#     topics_input = st.text_area(
#         "Enter Topics (one per line or comma separated)",
#         height=150
#     )

#     uploaded_file = st.file_uploader(
#         "Upload syllabus (PDF or TXT)",
#         type=["pdf", "txt"]
#     )

# with right:
#     st.markdown('<p class="section-title">📅 Planning Settings</p>', unsafe_allow_html=True)

#     exam_date = st.date_input("Exam Date")

#     hours = st.slider("Hours per day", 1, 12, 2)

#     generate_btn = st.button("🚀 Generate Study Plan", use_container_width=True)

# st.divider()

# # ==============================
# # 📂 File Processing
# # ==============================

# # if uploaded_file is not None:
# #     try:
# #         if uploaded_file.type == "application/pdf":
# #             pdf_reader = PyPDF2.PdfReader(uploaded_file)
# #             text = ""
# #             for page in pdf_reader.pages:
# #                 extracted = page.extract_text()
# #                 if extracted:
# #                     text += extracted
# #         else:
# #             text = uploaded_file.read().decode("utf-8")

# #         extracted_topics = extract_topics_from_text(text)

# #     except Exception:
# #         st.error("File processing failed.")

# # ==============================
# # 📂 File Processing
# # ==============================

# extracted_topics = ""

# if uploaded_file is not None:
#     try:
#         if uploaded_file.type == "application/pdf":
#             pdf_reader = PyPDF2.PdfReader(uploaded_file)
#             text = ""
#             for page in pdf_reader.pages:
#                 extracted = page.extract_text()
#                 if extracted:
#                     text += extracted
#         else:
#             text = uploaded_file.read().decode("utf-8")

#         extracted_topics = extract_topics_from_text(text)

#         st.success("✅ Topics extracted successfully!")

#         with st.expander("View Extracted Topics"):
#             st.write(extracted_topics)

#     except Exception:
#         st.error("File processing failed.")
# # ==============================
# # 🚀 Generate Plan
# # ==============================

# # if st.button("Generate Study Plan"):

# #     if not subject.strip():
# #         st.error("Please enter subject name.")

# #     else:
# #         final_topics = topics_input if topics_input else extracted_topics

# #         if not final_topics:
# #             st.error("Please enter topics or upload syllabus.")

# #         else:
# #             schedule = generate_study_schedule(
# #                 subject,
# #                 final_topics,
# #                 exam_date,
# #                 hours
# #             )

# #             if schedule:
# #                 st.subheader("📅 Your Study Schedule")
# #                 st.table(schedule)

# #                 days_remaining = (exam_date - datetime.date.today()).days
# #                 st.success(f"Total Days Remaining: {days_remaining}")
# #             else:
# #                 st.error("⚠️ Exam date must be in the future and topics must be valid.")

# #             if not AI_AVAILABLE:
# #                 st.info("AI prioritization disabled. Using basic scheduling mode.")
# # ==============================
# # 🚀 Generate Plan
# # ==============================

# if generate_btn:

#     if not subject.strip():
#         st.error("Please enter subject name.")
#     else:
#         final_topics = topics_input if topics_input else extracted_topics

#         if not final_topics:
#             st.error("Please enter topics or upload syllabus.")
#         else:
#             schedule = generate_study_schedule(
#                 subject,
#                 final_topics,
#                 exam_date,
#                 hours
#             )

#             if schedule:
#                 st.subheader("📅 Your Study Schedule")

#                 st.dataframe(
#                     schedule,
#                     use_container_width=True
#                 )

#                 days_remaining = (exam_date - datetime.date.today()).days
#                 st.success(f"🎯 Total Days Remaining: {days_remaining}")

#                 if not AI_AVAILABLE:
#                     st.info("AI prioritization disabled. Using basic scheduling mode.")

#             else:
#                 st.error("⚠️ Exam date must be in the future and topics must be valid.")

# import streamlit as st
# import datetime
# import PyPDF2
# import os
# from dotenv import load_dotenv
# from google import genai
# import time

# # ==============================
# # 🔐 Load Environment Variables
# # ==============================

# # load_dotenv()
# # API_KEY = os.getenv("AIzaSyBV1kcD4vSN-fNlSCJ_RUL7Ncek21i0U9M")
# API_KEY = "AIzaSyBroSbVnOhQ5VHBd70SS7YWfdfGTaXEZHM"
# # ✅ DEBUG LINE (temporary)
# st.write("API Key Loaded:", bool(API_KEY))
# AI_AVAILABLE = False
# client = None

# if API_KEY:
#     try:
#         client = genai.Client(api_key=API_KEY)
#         AI_AVAILABLE = True
#     except Exception:
#         AI_AVAILABLE = False

# PRIMARY_MODEL = "gemini-1.5-flash"
# FALLBACK_MODEL = "gemini-1.5-flash-8b"

# # ==============================
# # 🔁 Safe Gemini Call
# # ==============================

# def generate_with_retry(prompt):
#     if not AI_AVAILABLE:
#         return None

#     for attempt in range(3):
#         try:
#             response = client.models.generate_content(
#                 model=PRIMARY_MODEL,
#                 contents=prompt
#             )
#             return response.text
#         except Exception:
#             time.sleep(2)

#     try:
#         response = client.models.generate_content(
#             model=FALLBACK_MODEL,
#             contents=prompt
#         )
#         return response.text
#     except Exception:
#         return None

# # ==============================
# # 📄 Extract Topics from PDF/Text
# # ==============================

# def extract_topics_from_text(text):
#     if not AI_AVAILABLE:
#         return text

#     prompt = f"""
#     Extract important study topics from this syllabus.
#     Return clean bullet points only.
#     {text}
#     """

#     result = generate_with_retry(prompt)
#     return result if result else text

# # ==============================
# # 🚀 Generate Questions (Single API Call)
# # ==============================

# def generate_all_questions(subject, schedule_data):
#     if not AI_AVAILABLE:
#         return {}

#     formatted_days = ""
#     for i, day in enumerate(schedule_data):
#         formatted_days += f"""
#         Day {i+1}
#         Date: {day['Date']}
#         Topics: {day['Topics']}
#         """

#     prompt = f"""
#     Generate 5 important exam-focused questions for EACH day separately.

#     Subject: {subject}

#     {formatted_days}

#     Format strictly like:

#     Day 1:
#     1.
#     2.
#     3.
#     4.
#     5.

#     Day 2:
#     1.
#     2.
#     3.
#     4.
#     5.

#     Do not add explanations.
#     """

#     result = generate_with_retry(prompt)

#     if not result:
#         return {}

#     questions_dict = {}
#     current_day = None

#     for line in result.split("\n"):
#         line = line.strip()
#         if line.startswith("Day"):
#             current_day = line.replace(":", "")
#             questions_dict[current_day] = ""
#         elif current_day:
#             questions_dict[current_day] += line + "\n"

#     return questions_dict

# # ==============================
# # 📅 Generate Study Schedule
# # ==============================

# def generate_study_schedule(subject, topics, exam_date, hours_per_day):

#     today = datetime.date.today()
#     days_left = (exam_date - today).days

#     if days_left <= 0:
#         return None

#     topic_list = []

#     for line in topics.split("\n"):
#         parts = line.split(",")
#         for part in parts:
#             cleaned = part.strip("-• ").strip()
#             if cleaned:
#                 topic_list.append(cleaned)

#     if not topic_list:
#         return None

#     total_topics = len(topic_list)
#     topics_per_day = (total_topics + days_left - 1) // days_left

#     schedule_data = []
#     index = 0

#     for i in range(days_left):
#         current_date = today + datetime.timedelta(days=i)

#         daily_topics = topic_list[index:index + topics_per_day]
#         index += topics_per_day

#         if not daily_topics:
#             break

#         if current_date.weekday() == 6:
#             daily_topics.append("Revision")

#         schedule_data.append({
#             "Date": current_date.strftime("%d-%m-%Y"),
#             "Subject": subject,
#             "Topics": " | ".join(daily_topics),
#             "Hours per Day": hours_per_day
#         })

#     # 🔥 Single API call for all questions
#     questions_map = generate_all_questions(subject, schedule_data)

#     for i, day in enumerate(schedule_data):
#         day_key = f"Day {i+1}"
#         day["Important Questions"] = questions_map.get(day_key, "Not generated")

#     return schedule_data

# # ==============================
# # 🌐 Streamlit UI
# # ==============================

# st.set_page_config(page_title="Smart Study Planner", layout="wide")
# st.title("📚 Smart Study Planner Agent")

# subject = st.text_input("Enter Subject Name")

# topics_input = st.text_area("Enter Topics (one per line or comma separated)")

# uploaded_file = st.file_uploader(
#     "Upload syllabus file (PDF or TXT)",
#     type=["pdf", "txt"]
# )

# exam_date = st.date_input("Exam Date")
# hours = st.number_input("Hours per day", 1, 12, 2)

# extracted_topics = ""

# # ==============================
# # 📂 File Processing
# # ==============================

# if uploaded_file is not None:
#     try:
#         if uploaded_file.type == "application/pdf":
#             pdf_reader = PyPDF2.PdfReader(uploaded_file)
#             text = ""
#             for page in pdf_reader.pages:
#                 extracted = page.extract_text()
#                 if extracted:
#                     text += extracted
#         else:
#             text = uploaded_file.read().decode("utf-8")

#         extracted_topics = extract_topics_from_text(text)

#         st.success("Topics extracted successfully.")

#     except Exception:
#         st.error("File processing failed.")

# # ==============================
# # 🚀 Generate Plan
# # ==============================

# if st.button("Generate Study Plan"):

#     if not subject.strip():
#         st.error("Please enter subject name.")
#     else:
#         final_topics = topics_input if topics_input else extracted_topics

#         if not final_topics:
#             st.error("Please enter topics or upload syllabus.")
#         else:
#             schedule = generate_study_schedule(
#                 subject,
#                 final_topics,
#                 exam_date,
#                 hours
#             )

#             if schedule:
#                 st.subheader("📅 Your Study Schedule")
#                 st.dataframe(schedule, use_container_width=True)

#                 days_remaining = (exam_date - datetime.date.today()).days
#                 st.success(f"Total Days Remaining: {days_remaining}")

#                 if not AI_AVAILABLE:
#                     st.info("AI disabled. Questions not generated.")
#             else:
#                 st.error("Exam date must be in the future and topics must be valid.")

# import streamlit as st
# import datetime
# import PyPDF2
# import os
# from google import genai
# import time

# # ==============================
# # 🔐 API KEY (PASTE YOUR KEY HERE)
# # ==============================

# API_KEY = "AIzaSyDjxKt3atiiGu1iqvBbT1CdT1BiKjEVM5I"

# st.write("API Key Loaded:", bool(API_KEY))

# AI_AVAILABLE = False
# client = None

# if API_KEY:
#     try:
#         client = genai.Client(api_key=API_KEY)
#         AI_AVAILABLE = True
#     except Exception as e:
#         print("Client init error:", e)
#         AI_AVAILABLE = False

# PRIMARY_MODEL = "gemini-1.5-flash"
# FALLBACK_MODEL = "gemini-1.5-flash-8b"

# # ==============================
# # 🔁 Safe Gemini Call (FIXED)
# # ==============================

# def generate_with_retry(prompt):
#     if not AI_AVAILABLE:
#         return None

#     for attempt in range(3):
#         try:
#             response = client.models.generate_content(
#                 model=PRIMARY_MODEL,
#                 contents=prompt
#             )

#             if response and response.candidates:
#                 return response.candidates[0].content.parts[0].text

#         except Exception as e:
#             print("Primary error:", e)
#             time.sleep(2)

#     try:
#         response = client.models.generate_content(
#             model=FALLBACK_MODEL,
#             contents=prompt
#         )

#         if response and response.candidates:
#             return response.candidates[0].content.parts[0].text

#     except Exception as e:
#         print("Fallback error:", e)

#     return None

# # ==============================
# # 📄 Extract Topics
# # ==============================

# def extract_topics_from_text(text):
#     if not AI_AVAILABLE:
#         return text

#     prompt = f"""
#     Extract important study topics from this syllabus.
#     Return clean bullet points only.
#     {text}
#     """

#     result = generate_with_retry(prompt)
#     return result if result else text

# # ==============================
# # 🚀 Generate All Questions (Single API Call)
# # ==============================

# def generate_all_questions(subject, schedule_data):
#     if not AI_AVAILABLE or not schedule_data:
#         return {}

#     formatted_days = ""
#     for i, day in enumerate(schedule_data):
#         formatted_days += f"""
# Day {i+1}
# Date: {day['Date']}
# Topics: {day['Topics']}
# """

#     prompt = f"""
# Generate 5 important exam-focused questions for EACH day separately.

# Subject: {subject}

# {formatted_days}

# Format STRICTLY like:

# Day 1:
# 1.
# 2.
# 3.
# 4.
# 5.

# Day 2:
# 1.
# 2.
# 3.
# 4.
# 5.

# No explanations.
# """

#     result = generate_with_retry(prompt)

#     if not result:
#         return {}

#     questions_dict = {}

#     # Robust parsing
#     sections = result.split("Day ")

#     for section in sections:
#         section = section.strip()
#         if not section:
#             continue

#         first_line_end = section.find("\n")
#         if first_line_end == -1:
#             continue

#         day_number = section[:first_line_end].replace(":", "").strip()
#         questions_text = section[first_line_end:].strip()

#         questions_dict[f"Day {day_number}"] = questions_text

#     return questions_dict

# # ==============================
# # 📅 Generate Study Schedule
# # ==============================

# def generate_study_schedule(subject, topics, exam_date, hours_per_day):

#     today = datetime.date.today()
#     days_left = (exam_date - today).days

#     if days_left <= 0:
#         return None

#     topic_list = []

#     for line in topics.split("\n"):
#         parts = line.split(",")
#         for part in parts:
#             cleaned = part.strip("-• ").strip()
#             if cleaned:
#                 topic_list.append(cleaned)

#     if not topic_list:
#         return None

#     total_topics = len(topic_list)
#     topics_per_day = (total_topics + days_left - 1) // days_left

#     schedule_data = []
#     index = 0

#     for i in range(days_left):
#         current_date = today + datetime.timedelta(days=i)

#         daily_topics = topic_list[index:index + topics_per_day]
#         index += topics_per_day

#         if not daily_topics:
#             break

#         if current_date.weekday() == 6:
#             daily_topics.append("Revision")

#         schedule_data.append({
#             "Date": current_date.strftime("%d-%m-%Y"),
#             "Subject": subject,
#             "Topics": " | ".join(daily_topics),
#             "Hours per Day": hours_per_day
#         })

#     # 🔥 Generate all questions in ONE call
#     questions_map = generate_all_questions(subject, schedule_data)

#     for i, day in enumerate(schedule_data):
#         day_key = f"Day {i+1}"
#         day["Important Questions"] = questions_map.get(day_key, "Not generated")

#     return schedule_data

# # ==============================
# # 🌐 Streamlit UI
# # ==============================

# st.set_page_config(page_title="Smart Study Planner", layout="wide")
# st.title("📚 Smart Study Planner Agent")

# subject = st.text_input("Enter Subject Name")

# topics_input = st.text_area(
#     "Enter Topics (one per line or comma separated)"
# )

# uploaded_file = st.file_uploader(
#     "Upload syllabus file (PDF or TXT)",
#     type=["pdf", "txt"]
# )

# exam_date = st.date_input("Exam Date")
# hours = st.number_input("Hours per day", 1, 12, 2)

# extracted_topics = ""

# # ==============================
# # 📂 File Processing
# # ==============================

# if uploaded_file is not None:
#     try:
#         if uploaded_file.type == "application/pdf":
#             pdf_reader = PyPDF2.PdfReader(uploaded_file)
#             text = ""
#             for page in pdf_reader.pages:
#                 extracted = page.extract_text()
#                 if extracted:
#                     text += extracted
#         else:
#             text = uploaded_file.read().decode("utf-8")

#         extracted_topics = extract_topics_from_text(text)
#         st.success("Topics extracted successfully.")

#     except Exception:
#         st.error("File processing failed.")

# # ==============================
# # 🚀 Generate Plan
# # ==============================

# if st.button("Generate Study Plan"):

#     if not subject.strip():
#         st.error("Please enter subject name.")

#     else:
#         final_topics = topics_input if topics_input else extracted_topics

#         if not final_topics:
#             st.error("Please enter topics or upload syllabus.")

#         else:
#             schedule = generate_study_schedule(
#                 subject,
#                 final_topics,
#                 exam_date,
#                 hours
#             )

#             if schedule:
#                 st.subheader("📅 Your Study Schedule")
#                 st.dataframe(schedule, use_container_width=True)

#                 days_remaining = (exam_date - datetime.date.today()).days
#                 st.success(f"Total Days Remaining: {days_remaining}")

#                 if not AI_AVAILABLE:
#                     st.info("AI disabled. Questions not generated.")

#             else:
#                 st.error("Exam date must be in the future and topics must be valid.")

# import streamlit as st
# import datetime
# import PyPDF2
# from google import genai
# import time

# # ==============================
# # 🔐 API KEY (PASTE YOUR KEY HERE)
# # ==============================

# API_KEY = "AIzaSyAUpx-vIDgo2NmrvQBRnziQnuh1DylIkgY"

# st.write("API Key Loaded:", bool(API_KEY))

# AI_AVAILABLE = False
# client = None

# if API_KEY:
#     try:
#         client = genai.Client(api_key=API_KEY)
#         AI_AVAILABLE = True
#     except Exception as e:
#         st.error(f"Client init error: {e}")
#         AI_AVAILABLE = False

# PRIMARY_MODEL = "gemini-2.0-flash"

# # ==============================
# # 🔁 Safe Gemini Call (FIXED FOR v1.64.0)
# # ==============================

# def generate_with_retry(prompt):
#     if not AI_AVAILABLE:
#         return None

#     try:
#         response = client.models.generate_content(
#             model=PRIMARY_MODEL,
#             contents=prompt
#         )

#         # ✅ CORRECT for google-genai 1.64.0
#         if response and response.text:
#             return response.text.strip()

#     except Exception as e:
#         st.error(f"AI Error: {e}")

#     return None


# # ==============================
# # 📄 Extract Topics
# # ==============================

# def extract_topics_from_text(text):
#     if not AI_AVAILABLE:
#         return text

#     prompt = f"""
# Extract important study topics from this syllabus.
# Return clean bullet points only.
# {text}
# """

#     result = generate_with_retry(prompt)
#     return result if result else text


# # ==============================
# # 🚀 Generate All Questions (Single API Call)
# # ==============================

# def generate_all_questions(subject, schedule_data):
#     if not AI_AVAILABLE or not schedule_data:
#         return {}

#     formatted_days = ""
#     for i, day in enumerate(schedule_data):
#         formatted_days += f"""
# Day {i+1}
# Date: {day['Date']}
# Topics: {day['Topics']}
# """

#     prompt = f"""
# Generate 5 important exam-focused questions for EACH day separately.

# Subject: {subject}

# {formatted_days}

# Format STRICTLY like:

# Day 1:
# 1.
# 2.
# 3.
# 4.
# 5.

# Day 2:
# 1.
# 2.
# 3.
# 4.
# 5.

# No explanations.
# """

#     result = generate_with_retry(prompt)

#     if not result:
#         st.error("No response received from AI.")
#         return {}

#     questions_dict = {}

#     sections = result.split("Day ")

#     for section in sections:
#         section = section.strip()
#         if not section:
#             continue

#         parts = section.split(":", 1)
#         if len(parts) < 2:
#             continue

#         day_number = parts[0].strip()
#         questions_text = parts[1].strip()

#         questions_dict[f"Day {day_number}"] = questions_text

#     return questions_dict


# # ==============================
# # 📅 Generate Study Schedule
# # ==============================

# def generate_study_schedule(subject, topics, exam_date, hours_per_day):

#     today = datetime.date.today()
#     days_left = (exam_date - today).days

#     if days_left <= 0:
#         return None

#     topic_list = []

#     for line in topics.split("\n"):
#         parts = line.split(",")
#         for part in parts:
#             cleaned = part.strip("-• ").strip()
#             if cleaned:
#                 topic_list.append(cleaned)

#     if not topic_list:
#         return None

#     total_topics = len(topic_list)
#     topics_per_day = (total_topics + days_left - 1) // days_left

#     schedule_data = []
#     index = 0

#     for i in range(days_left):
#         current_date = today + datetime.timedelta(days=i)

#         daily_topics = topic_list[index:index + topics_per_day]
#         index += topics_per_day

#         if not daily_topics:
#             break

#         if current_date.weekday() == 6:
#             daily_topics.append("Revision")

#         schedule_data.append({
#             "Date": current_date.strftime("%d-%m-%Y"),
#             "Subject": subject,
#             "Topics": " | ".join(daily_topics),
#             "Hours per Day": hours_per_day
#         })

#     # 🔥 Generate all questions in ONE call
#     questions_map = generate_all_questions(subject, schedule_data)

#     for i, day in enumerate(schedule_data):
#         day_key = f"Day {i+1}"
#         day["Important Questions"] = questions_map.get(day_key, "Not generated")

#     return schedule_data


# # ==============================
# # 🌐 Streamlit UI
# # ==============================

# st.set_page_config(page_title="Smart Study Planner", layout="wide")
# st.title("📚 Smart Study Planner Agent")

# subject = st.text_input("Enter Subject Name")

# topics_input = st.text_area(
#     "Enter Topics (one per line or comma separated)"
# )

# uploaded_file = st.file_uploader(
#     "Upload syllabus file (PDF or TXT)",
#     type=["pdf", "txt"]
# )

# exam_date = st.date_input("Exam Date")
# hours = st.number_input("Hours per day", 1, 12, 2)

# extracted_topics = ""

# # ==============================
# # 📂 File Processing
# # ==============================

# if uploaded_file is not None:
#     try:
#         if uploaded_file.type == "application/pdf":
#             pdf_reader = PyPDF2.PdfReader(uploaded_file)
#             text = ""
#             for page in pdf_reader.pages:
#                 extracted = page.extract_text()
#                 if extracted:
#                     text += extracted
#         else:
#             text = uploaded_file.read().decode("utf-8")

#         extracted_topics = extract_topics_from_text(text)
#         st.success("Topics extracted successfully.")

#     except Exception:
#         st.error("File processing failed.")

# # ==============================
# # 🚀 Generate Plan
# # ==============================

# if st.button("Generate Study Plan"):

#     if not subject.strip():
#         st.error("Please enter subject name.")

#     else:
#         final_topics = topics_input if topics_input else extracted_topics

#         if not final_topics:
#             st.error("Please enter topics or upload syllabus.")

#         else:
#             schedule = generate_study_schedule(
#                 subject,
#                 final_topics,
#                 exam_date,
#                 hours
#             )

#             if schedule:
#                 st.subheader("📅 Your Study Schedule")
#                 st.dataframe(schedule, use_container_width=True)

#                 days_remaining = (exam_date - datetime.date.today()).days
#                 st.success(f"Total Days Remaining: {days_remaining}")

#                 if not AI_AVAILABLE:
#                     st.info("AI disabled. Questions not generated.")

#             else:
#                 st.error("Exam date must be in the future and topics must be valid.")

# import streamlit as st
# import datetime
# import PyPDF2
# from google import genai
# import urllib.parse

# # ==============================
# # 🔐 API KEY
# # ==============================

# API_KEY = "AIzaSyAUpx-vIDgo2NmrvQBRnziQnuh1DylIkgY"

# PRIMARY_MODEL = "gemini-2.0-flash"

# AI_AVAILABLE = False
# client = None

# if API_KEY:
#     try:
#         client = genai.Client(api_key=API_KEY)
#         AI_AVAILABLE = True
#     except Exception as e:
#         st.error(f"AI Initialization Error: {e}")

# # ==============================
# # 🔁 Safe Gemini Call (Stable)
# # ==============================

# def generate_with_retry(prompt):
#     if not AI_AVAILABLE:
#         return None

#     try:
#         response = client.models.generate_content(
#             model=PRIMARY_MODEL,
#             contents=prompt
#         )

#         # ✅ Safe parsing for google-genai 1.64.0
#         if hasattr(response, "text") and response.text:
#             return response.text.strip()

#         if response.candidates:
#             return response.candidates[0].content.parts[0].text.strip()

#     except Exception as e:
#         st.error(f"AI Error: {e}")

#     return None


# # ==============================
# # 📄 Extract Topics
# # ==============================

# def extract_topics_from_text(text):
#     if not AI_AVAILABLE:
#         return text

#     prompt = f"""
# Extract important study topics from this syllabus.
# Return only clean bullet points.
# {text}
# """
#     result = generate_with_retry(prompt)
#     return result if result else text


# # ==============================
# # 🔗 Generate Learning Links
# # ==============================

# def generate_learning_links(topics_string):
#     topics = topics_string.split(" | ")
#     links = []

#     for topic in topics:
#         query = urllib.parse.quote_plus(topic + " tutorial")
#         link = f"https://www.google.com/search?q={query}"
#         links.append(link)

#     return " | ".join(links)


# # ==============================
# # 🧠 Generate All Questions (1 API Call)
# # ==============================

# def generate_all_questions(subject, schedule_data):

#     if not AI_AVAILABLE or not schedule_data:
#         return {}

#     formatted_days = ""

#     for i, day in enumerate(schedule_data):
#         formatted_days += f"""
# Day {i+1}
# Date: {day['Date']}
# Topics: {day['Topics']}
# """

#     prompt = f"""
# Generate 5 important exam-focused questions for EACH day separately.

# Subject: {subject}

# {formatted_days}

# Format STRICTLY like:

# Day 1:
# 1.
# 2.
# 3.
# 4.
# 5.

# Day 2:
# 1.
# 2.
# 3.
# 4.
# 5.

# No explanations.
# """

#     result = generate_with_retry(prompt)

#     if not result:
#         return {}

#     questions_dict = {}

#     sections = result.split("Day ")

#     for section in sections:
#         section = section.strip()
#         if not section:
#             continue

#         parts = section.split(":", 1)
#         if len(parts) < 2:
#             continue

#         day_number = parts[0].strip()
#         questions_text = parts[1].strip()

#         questions_dict[f"Day {day_number}"] = questions_text

#     return questions_dict


# # ==============================
# # 📅 Generate Study Schedule
# # ==============================

# def generate_study_schedule(subject, topics, exam_date, hours_per_day):

#     today = datetime.date.today()
#     days_left = (exam_date - today).days

#     if days_left <= 0:
#         return None

#     topic_list = []

#     for line in topics.split("\n"):
#         parts = line.split(",")
#         for part in parts:
#             cleaned = part.strip("-• ").strip()
#             if cleaned:
#                 topic_list.append(cleaned)

#     if not topic_list:
#         return None

#     total_topics = len(topic_list)
#     topics_per_day = (total_topics + days_left - 1) // days_left

#     schedule_data = []
#     index = 0

#     for i in range(days_left):
#         current_date = today + datetime.timedelta(days=i)
#         daily_topics = topic_list[index:index + topics_per_day]
#         index += topics_per_day

#         if not daily_topics:
#             break

#         # Sunday = revision
#         if current_date.weekday() == 6:
#             daily_topics.append("Revision")

#         topics_joined = " | ".join(daily_topics)
#         links = generate_learning_links(topics_joined)

#         schedule_data.append({
#             "Date": current_date.strftime("%d-%m-%Y"),
#             "Subject": subject,
#             "Topics": topics_joined,
#             "Learning Links": links,
#             "Hours per Day": hours_per_day
#         })

#     # 🔥 Generate all questions in ONE call
#     questions_map = generate_all_questions(subject, schedule_data)

#     for i, day in enumerate(schedule_data):
#         day_key = f"Day {i+1}"
#         day["Important Questions"] = questions_map.get(day_key, "Not Generated")

#     return schedule_data


# # ==============================
# # 🌐 STREAMLIT UI
# # ==============================

# st.set_page_config(page_title="Smart Study Planner", layout="wide")
# st.title("📚 Smart Study Planner Agent")

# subject = st.text_input("Enter Subject Name")

# topics_input = st.text_area(
#     "Enter Topics (one per line or comma separated)"
# )

# uploaded_file = st.file_uploader(
#     "Upload syllabus file (PDF or TXT)",
#     type=["pdf", "txt"]
# )

# exam_date = st.date_input("Exam Date")
# hours = st.number_input("Hours per day", 1, 12, 2)

# extracted_topics = ""

# # ==============================
# # 📂 File Processing
# # ==============================

# if uploaded_file is not None:
#     try:
#         if uploaded_file.type == "application/pdf":
#             pdf_reader = PyPDF2.PdfReader(uploaded_file)
#             text = ""
#             for page in pdf_reader.pages:
#                 extracted = page.extract_text()
#                 if extracted:
#                     text += extracted
#         else:
#             text = uploaded_file.read().decode("utf-8")

#         extracted_topics = extract_topics_from_text(text)
#         st.success("Topics extracted successfully.")

#     except Exception:
#         st.error("File processing failed.")


# # ==============================
# # 🚀 Generate Plan
# # ==============================

# if st.button("Generate Study Plan"):

#     if not subject.strip():
#         st.error("Please enter subject name.")

#     else:
#         final_topics = topics_input if topics_input else extracted_topics

#         if not final_topics:
#             st.error("Please enter topics or upload syllabus.")

#         else:
#             schedule = generate_study_schedule(
#                 subject,
#                 final_topics,
#                 exam_date,
#                 hours
#             )

#             if schedule:
#                 st.subheader("📅 Your Study Schedule")
#                 st.dataframe(schedule, use_container_width=True)

#                 days_remaining = (exam_date - datetime.date.today()).days
#                 st.success(f"Total Days Remaining: {days_remaining}")

#                 if not AI_AVAILABLE:
#                     st.info("AI disabled. Questions not generated.")

#             else:
#                 st.error("Exam date must be in the future and topics must be valid.")

# import streamlit as st
# import datetime
# import PyPDF2
# from google import genai
# import urllib.parse
# from docx import Document
# # ==============================
# # 🔐 API KEY
# # ==============================

# API_KEY = "AIzaSyAUpx-vIDgo2NmrvQBRnziQnuh1DylIkgY"

# PRIMARY_MODEL = "gemini-1.5-flash"

# AI_AVAILABLE = False
# client = None

# if API_KEY:
#     try:
#         client = genai.Client(api_key=API_KEY)
#         AI_AVAILABLE = True
#     except Exception as e:
#         st.error(f"AI Initialization Error: {e}")

# # ==============================
# # 🔁 Safe Gemini Call
# # ==============================

# def generate_with_retry(prompt):
#     if not AI_AVAILABLE:
#         return None

#     try:
#         response = client.models.generate_content(
#             model=PRIMARY_MODEL,
#             contents=prompt
#         )

#         if hasattr(response, "text") and response.text:
#             return response.text.strip()

#         if response.candidates:
#             return response.candidates[0].content.parts[0].text.strip()

#     except Exception as e:
#         st.error(f"AI Error: {e}")

#     return None


# # ==============================
# # 📄 Extract Topics
# # ==============================

# def extract_topics_from_text(text):
#     if not AI_AVAILABLE:
#         return text

#     prompt = f"""
# Extract important study topics from this syllabus.
# Return only clean bullet points.
# {text}
# """
#     result = generate_with_retry(prompt)
#     return result if result else text


# # ==============================
# # 🔗 Generate Learning Links
# # ==============================

# def generate_learning_links(topics_string):
#     topics = topics_string.split(" | ")
#     links = []

#     for topic in topics:
#         query = urllib.parse.quote_plus(topic + " tutorial")
#         link = f"https://www.google.com/search?q={query}"
#         links.append(link)

#     return " | ".join(links)


# # ==============================
# # 📅 Generate Study Schedule
# # ==============================

# def generate_study_schedule(subject, topics, exam_date, hours_per_day):

#     today = datetime.date.today()
#     days_left = (exam_date - today).days

#     if days_left <= 0:
#         return None

#     topic_list = []

#     for line in topics.split("\n"):
#         parts = line.split(",")
#         for part in parts:
#             cleaned = part.strip("-• ").strip()
#             if cleaned:
#                 topic_list.append(cleaned)

#     if not topic_list:
#         return None

#     total_topics = len(topic_list)
#     topics_per_day = (total_topics + days_left - 1) // days_left

#     schedule_data = []
#     index = 0

#     for i in range(days_left):
#         current_date = today + datetime.timedelta(days=i)
#         daily_topics = topic_list[index:index + topics_per_day]
#         index += topics_per_day

#         if not daily_topics:
#             break

#         # Sunday = revision
#         if current_date.weekday() == 6:
#             daily_topics.append("Revision")

#         topics_joined = " | ".join(daily_topics)
#         links = generate_learning_links(topics_joined)

#         schedule_data.append({
#             "Date": current_date.strftime("%d-%m-%Y"),
#             "Subject": subject,
#             "Topics": topics_joined,
#             "Learning Links": links,
#             "Hours per Day": hours_per_day
#         })

#     return schedule_data


# # ==============================
# # 🌐 STREAMLIT UI
# # ==============================

# st.set_page_config(page_title="Smart Study Planner", layout="wide")
# st.title("📚 Smart Study Planner Agent")

# subject = st.text_input("Enter Subject Name")

# topics_input = st.text_area(
#     "Enter Topics (one per line or comma separated)"
# )

# # uploaded_file = st.file_uploader(
# #     "Upload syllabus file (PDF or TXT)",
# #     type=["pdf", "txt"]
# # )
# uploaded_file = st.file_uploader(
#     "Upload syllabus file (PDF, TXT, or DOCX)",
#     type=["pdf", "txt", "docx"]
# )

# exam_date = st.date_input("Exam Date")
# hours = st.number_input("Hours per day", 1, 12, 2)

# extracted_topics = ""

# # ==============================
# # 📂 File Processing
# # ==============================

# # if uploaded_file is not None:
# #     try:
# #         if uploaded_file.type == "application/pdf":
# #             pdf_reader = PyPDF2.PdfReader(uploaded_file)
# #             text = ""
# #             for page in pdf_reader.pages:
# #                 extracted = page.extract_text()
# #                 if extracted:
# #                     text += extracted
# #         else:
# #             text = uploaded_file.read().decode("utf-8")

# #         extracted_topics = extract_topics_from_text(text)
# #         st.success("Topics extracted successfully.")

# #     except Exception:
# #         st.error("File processing failed.")
# # ==============================
# # 📂 File Processing
# # ==============================

# if uploaded_file is not None:
#     try:
#         text = ""

#         # PDF
#         if uploaded_file.type == "application/pdf":
#             pdf_reader = PyPDF2.PdfReader(uploaded_file)
#             for page in pdf_reader.pages:
#                 extracted = page.extract_text()
#                 if extracted:
#                     text += extracted

#         # TXT
#         elif uploaded_file.type == "text/plain":
#             text = uploaded_file.read().decode("utf-8")

#         # DOCX
#         elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#             doc = Document(uploaded_file)
#             for paragraph in doc.paragraphs:
#                 text += paragraph.text + "\n"

#         # Extract topics using AI (if enabled)
#         extracted_topics = extract_topics_from_text(text)

#         st.success("Topics extracted successfully.")

#     except Exception as e:
#         st.error(f"File processing failed: {e}")

# # ==============================
# # 🚀 Generate Plan
# # ==============================

# if st.button("Generate Study Plan"):

#     if not subject.strip():
#         st.error("Please enter subject name.")

#     else:
#         final_topics = topics_input if topics_input else extracted_topics

#         if not final_topics:
#             st.error("Please enter topics or upload syllabus.")

#         else:
#             schedule = generate_study_schedule(
#                 subject,
#                 final_topics,
#                 exam_date,
#                 hours
#             )

#             if schedule:
#                 st.subheader("📅 Your Study Schedule")
#                 st.dataframe(schedule, use_container_width=True)

#                 days_remaining = (exam_date - datetime.date.today()).days
#                 st.success(f"Total Days Remaining: {days_remaining}")

#             else:
#                 st.error("Exam date must be in the future and topics must be valid.")

# import streamlit as st
# import datetime
# import PyPDF2
# from google import genai
# import urllib.parse
# from docx import Document
# import pandas as pd

# # ==============================
# # 🔐 API KEY
# # ==============================

# API_KEY = "AIzaSyAUpx-vIDgo2NmrvQBRnziQnuh1DylIkgY"
# PRIMARY_MODEL = "gemini-1.5-flash"

# AI_AVAILABLE = False
# client = None

# if API_KEY:
#     try:
#         client = genai.Client(api_key=API_KEY)
#         AI_AVAILABLE = True
#     except Exception as e:
#         st.error(f"AI Initialization Error: {e}")

# # ==============================
# # 🔁 Safe Gemini Call
# # ==============================

# def generate_with_retry(prompt):
#     if not AI_AVAILABLE:
#         return None
#     try:
#         response = client.models.generate_content(
#             model=PRIMARY_MODEL,
#             contents=prompt
#         )
#         if hasattr(response, "text") and response.text:
#             return response.text.strip()
#         if response.candidates:
#             return response.candidates[0].content.parts[0].text.strip()
#     except Exception as e:
#         st.error(f"AI Error: {e}")
#     return None

# # ==============================
# # 📄 Extract Topics
# # ==============================

# def extract_topics_from_text(text):
#     if not AI_AVAILABLE:
#         return text
#     prompt = f"""
# Extract important study topics from this syllabus.
# Return only clean bullet points.
# {text}
# """
#     result = generate_with_retry(prompt)
#     return result if result else text

# # ==============================
# # 🔗 Generate Learning Links
# # ==============================

# def generate_learning_links(topics_string):
#     topics = topics_string.split("\n")
#     links = []

#     for topic in topics:
#         topic = topic.strip()
#         if topic:
#             query = urllib.parse.quote_plus(topic + " tutorial")
#             link = f"https://www.google.com/search?q={query}"
#             links.append(link)

#     return "\n".join(links)

# # ==============================
# # 📅 Generate Study Schedule
# # ==============================

# def generate_study_schedule(subject, topics, exam_date, hours_per_day):

#     today = datetime.date.today()
#     days_left = (exam_date - today).days

#     if days_left <= 0:
#         return None

#     topic_list = []

#     for line in topics.split("\n"):
#         parts = line.split(",")
#         for part in parts:
#             cleaned = part.strip("-• ").strip()
#             if cleaned:
#                 topic_list.append(cleaned)

#     if not topic_list:
#         return None

#     total_topics = len(topic_list)
#     topics_per_day = (total_topics + days_left - 1) // days_left

#     schedule_data = []
#     index = 0

#     for i in range(days_left):
#         current_date = today + datetime.timedelta(days=i)
#         daily_topics = topic_list[index:index + topics_per_day]
#         index += topics_per_day

#         if not daily_topics:
#             break

#         if current_date.weekday() == 6:
#             daily_topics.append("Revision")

#         # 🔥 MULTI-LINE FORMAT (NO HORIZONTAL SCROLL)
#         topics_joined = "\n".join(daily_topics)
#         links = generate_learning_links(topics_joined)

#         schedule_data.append({
#             "Date": current_date.strftime("%d-%m-%Y"),
#             "Subject": subject,
#             "Topics": topics_joined,
#             "Learning Links": links,
#             "Hours per Day": hours_per_day
#         })

#     return schedule_data

# # ==============================
# # 🌐 STREAMLIT UI
# # ==============================

# st.set_page_config(page_title="Smart Study Planner", layout="wide")
# st.title("📚 Smart Study Planner Agent")

# # 🔥 Word wrap styling
# st.markdown("""
# <style>
# div[data-testid="stDataFrame"] div {
#     white-space: pre-wrap !important;
#     word-wrap: break-word !important;
# }
# </style>
# """, unsafe_allow_html=True)

# subject = st.text_input("Enter Subject Name")

# topics_input = st.text_area(
#     "Enter Topics (one per line or comma separated)"
# )

# uploaded_file = st.file_uploader(
#     "Upload syllabus file (PDF, TXT, or DOCX)",
#     type=["pdf", "txt", "docx"]
# )

# exam_date = st.date_input("Exam Date")
# hours = st.number_input("Hours per day", 1, 12, 2)

# extracted_topics = ""

# # ==============================
# # 📂 File Processing
# # ==============================

# if uploaded_file is not None:
#     try:
#         text = ""

#         if uploaded_file.type == "application/pdf":
#             pdf_reader = PyPDF2.PdfReader(uploaded_file)
#             for page in pdf_reader.pages:
#                 extracted = page.extract_text()
#                 if extracted:
#                     text += extracted

#         elif uploaded_file.type == "text/plain":
#             text = uploaded_file.read().decode("utf-8")

#         elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#             doc = Document(uploaded_file)
#             for paragraph in doc.paragraphs:
#                 text += paragraph.text + "\n"

#         extracted_topics = extract_topics_from_text(text)
#         st.success("Topics extracted successfully.")

#     except Exception as e:
#         st.error(f"File processing failed: {e}")

# # ==============================
# # 🚀 Generate Plan
# # ==============================

# if st.button("Generate Study Plan"):

#     if not subject.strip():
#         st.error("Please enter subject name.")

#     else:
#         final_topics = topics_input if topics_input else extracted_topics

#         if not final_topics:
#             st.error("Please enter topics or upload syllabus.")

#         else:
#             schedule = generate_study_schedule(
#                 subject,
#                 final_topics,
#                 exam_date,
#                 hours
#             )

#             if schedule:
#                 st.subheader("📅 Your Study Schedule")

#                 df = pd.DataFrame(schedule)

#                 st.data_editor(
#                     df,
#                     use_container_width=True,
#                     height=600,
#                     column_config={
#                         "Topics": st.column_config.TextColumn(width="large"),
#                         "Learning Links": st.column_config.TextColumn(width="large"),
#                     }
#                 )

#                 days_remaining = (exam_date - datetime.date.today()).days
#                 st.success(f"Total Days Remaining: {days_remaining}")

#             else:
#                 st.error("Exam date must be in the future and topics must be valid.")

import streamlit as st
import datetime
import PyPDF2
from google import genai
import urllib.parse
from docx import Document
import pandas as pd

# ==============================
# 🔐 API KEY
# ==============================

API_KEY = "AIzaSyAUpx-vIDgo2NmrvQBRnziQnuh1DylIkgY"
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
    if not AI_AVAILABLE:
        return None
    try:
        response = client.models.generate_content(
            model=PRIMARY_MODEL,
            contents=prompt
        )
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        if response.candidates:
            return response.candidates[0].content.parts[0].text.strip()
    except Exception as e:
        st.error(f"AI Error: {e}")
    return None

# ==============================
# 📄 Extract Topics
# ==============================

def extract_topics_from_text(text):
    if not AI_AVAILABLE:
        return text

    prompt = f"""
Extract important study topics from this syllabus.
Return only clean bullet points (one topic per line).
{text}
"""
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
        if topic:
            query = urllib.parse.quote_plus(topic + " tutorial")
            link = f"https://www.google.com/search?q={query}"
            links.append(link)

    return "\n".join(links)

# ==============================
# 📅 Generate Study Schedule
# ==============================

def generate_study_schedule(subject, topics, exam_date, hours_per_day):

    today = datetime.date.today()
    days_left = (exam_date - today).days

    if days_left <= 0:
        return None

    topic_list = []

    for line in topics.split("\n"):
        parts = line.split(",")
        for part in parts:
            cleaned = part.strip("-• ").strip()
            if cleaned:
                topic_list.append(cleaned)

    if not topic_list:
        return None

    total_topics = len(topic_list)
    topics_per_day = (total_topics + days_left - 1) // days_left

    schedule_data = []
    index = 0

    for i in range(days_left):
        current_date = today + datetime.timedelta(days=i)
        daily_topics = topic_list[index:index + topics_per_day]
        index += topics_per_day

        if not daily_topics:
            break

        if current_date.weekday() == 6:
            daily_topics.append("Revision")

        topics_joined = "\n".join(daily_topics)
        links = generate_learning_links(topics_joined)

        schedule_data.append({
            "Date": current_date.strftime("%d-%m-%Y"),
            "Subject": subject,
            "Topics": topics_joined,
            "Learning Links": links,
            "Hours per Day": hours_per_day
        })

    return schedule_data


# ==============================
# 🔄 RESCHEDULE FUNCTION
# ==============================

def reschedule_from_missed_day(schedule_df, missed_date, exam_date):

    today = datetime.datetime.strptime(missed_date, "%d-%m-%Y").date()

    pending_topics = []
    subject = schedule_df.iloc[0]["Subject"]
    hours = schedule_df.iloc[0]["Hours per Day"]

    for i in range(len(schedule_df)):
        row_date = datetime.datetime.strptime(schedule_df.iloc[i]["Date"], "%d-%m-%Y").date()
        if row_date >= today:
            topics = schedule_df.iloc[i]["Topics"].split("\n")
            pending_topics.extend(topics)

    if not pending_topics:
        return None

    combined_topics = "\n".join(pending_topics)

    return generate_study_schedule(subject, combined_topics, exam_date, hours)


# ==============================
# 🌐 STREAMLIT UI
# ==============================

st.set_page_config(page_title="Smart Study Planner", layout="wide")
st.title("📚 Smart Study Planner Agent")

# Word wrap styling (no horizontal scroll)
st.markdown("""
<style>
div[data-testid="stDataFrame"] div {
    white-space: pre-wrap !important;
    word-wrap: break-word !important;
}
</style>
""", unsafe_allow_html=True)

subject = st.text_input("Enter Subject Name")

topics_input = st.text_area(
    "Enter Topics (one per line or comma separated)"
)

uploaded_file = st.file_uploader(
    "Upload syllabus file (PDF, TXT, or DOCX)",
    type=["pdf", "txt", "docx"]
)

exam_date = st.date_input("Exam Date")
hours = st.number_input("Hours per day", 1, 12, 2)

extracted_topics = ""

# ==============================
# 📂 File Processing
# ==============================

if uploaded_file is not None:
    try:
        text = ""

        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted

        elif uploaded_file.type == "text/plain":
            text = uploaded_file.read().decode("utf-8")

        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded_file)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"

        extracted_topics = extract_topics_from_text(text)
        st.success("Topics extracted successfully.")

    except Exception as e:
        st.error(f"File processing failed: {e}")

# ==============================
# 🚀 Generate Plan
# ==============================

if st.button("Generate Study Plan"):

    final_topics = topics_input if topics_input else extracted_topics

    if not subject.strip():
        st.error("Please enter subject name.")

    elif not final_topics:
        st.error("Please enter topics or upload syllabus.")

    else:
        schedule = generate_study_schedule(
            subject,
            final_topics,
            exam_date,
            hours
        )

        if schedule:
            df = pd.DataFrame(schedule)
            st.session_state["schedule_df"] = df

        else:
            st.error("Exam date must be in the future and topics must be valid.")


# ==============================
# 📅 Show Schedule
# ==============================

if "schedule_df" in st.session_state:

    st.subheader("📅 Your Study Schedule")

    df = st.session_state["schedule_df"]

    st.data_editor(
        df,
        use_container_width=True,
        height=700,
        column_config={
            "Topics": st.column_config.TextColumn(width="large"),
            "Learning Links": st.column_config.TextColumn(width="large"),
        }
    )

    days_remaining = (exam_date - datetime.date.today()).days
    st.success(f"Total Days Remaining: {days_remaining}")

    # ==============================
    # 🔄 RESCHEDULE UI
    # ==============================

    st.subheader("🔄 Missed a Day? Reschedule")

    missed_day = st.selectbox(
        "Select missed date",
        df["Date"].tolist()
    )

    if st.button("Reschedule Plan"):

        new_schedule = reschedule_from_missed_day(
            df,
            missed_day,
            exam_date
        )

        if new_schedule:
            new_df = pd.DataFrame(new_schedule)
            st.session_state["schedule_df"] = new_df
            st.success("Schedule updated successfully!")
            st.rerun()
        else:
            st.error("Unable to reschedule.")