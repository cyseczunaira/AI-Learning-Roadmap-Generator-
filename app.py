
import streamlit as st
from groq import Groq
from pypdf import PdfReader
from docx import Document
import os


client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)


def read_file(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    elif file_name.endswith(".txt"):

        return uploaded_file.read().decode("utf-8")

    elif file_name.endswith(".docx"):

        document = Document(uploaded_file)

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    return ""


def generate_roadmap(domain, level, learning_time, study_material):

    prompt = f"""
You are an AI Learning Roadmap Generator.

The user wants to learn:

Domain:
{domain}

Skill level:
{level}

Available learning time:
{learning_time}

Study material uploaded by the user:
{study_material}

Create a personalized and practical learning roadmap.

Include:

1. Learning Goal
2. Prerequisites
3. Week-by-week Learning Plan
4. Topics to Study
5. Practical Exercises
6. Projects
7. Recommended Study Schedule
8. Final Assessment
9. Expected Skills After Completion

Important instructions:

- Adapt the roadmap to the user's skill level.
- Adapt it to the available learning time.
- Use the uploaded study material when relevant.
- Start with basic concepts before advanced concepts.
- Keep the roadmap realistic.
- Do not overload the learner.
- Explain difficult concepts in simple language.
- Organize the roadmap in a clear order.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are an expert AI learning roadmap generator."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content


st.set_page_config(
    page_title="AI Learning Roadmap Generator",
    page_icon="🎓"
)

st.title("🎓 AI Learning Roadmap Generator")

st.write(
    "Create a personalized learning roadmap using AI."
)


domain = st.text_input(
    "What do you want to learn?"
)


level = st.selectbox(
    "Select your skill level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)


learning_time = st.text_input(
    "How much time do you have to learn?",
    placeholder="Example: 2 months"
)


files = st.file_uploader(
    "Upload your study material",
    type=["pdf", "txt", "docx"],
    accept_multiple_files=True
)


if st.button("🚀 Generate Roadmap"):

    if not domain:

        st.warning("Please enter a learning domain.")

    elif not learning_time:

        st.warning("Please enter your available learning time.")

    else:

        study_material = ""

        if files:

            for file in files:

                study_material += (
                    f"\n\n--- {file.name} ---\n"
                )

                study_material += read_file(file)

        with st.spinner("AI is creating your roadmap..."):

            roadmap = generate_roadmap(
                domain,
                level,
                learning_time,
                study_material
            )

        st.success("Roadmap generated!")

        st.markdown(roadmap)
        
