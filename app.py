import streamlit as st
from dynamo import generate_requirements, calculate_clarity_score, generate_word_doc, extract_user_stories, classify_requirements
import os
import json
import base64
from datetime import datetime

# Session state for multiple users
if "user_id" not in st.session_state:
    st.session_state.user_id = str(hash(st.query_params.get("session", ["default"])[0]))
if "requirements" not in st.session_state:
    st.session_state.requirements = ""
if "functional" not in st.session_state:
    st.session_state.functional = []
if "non_functional" not in st.session_state:
    st.session_state.non_functional = []

# Initialize inventory for version control
inventory_file = "inventory.json"
if not os.path.exists(inventory_file):
    with open(inventory_file, "w") as f:
        json.dump({}, f)

# Function to encode image to base64 (for local images)
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Function to save document with version control
def save_versioned_document(user_id, functional, non_functional):
    # Load inventory
    with open(inventory_file, "r") as f:
        inventory = json.load(f)
    
    # Initialize user inventory if not exists
    if user_id not in inventory:
        inventory[user_id] = []
    
    # Create versioned filename
    version = len(inventory[user_id]) + 1
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"requirements/{user_id}/version_{version}_{timestamp}.docx"
    
    # Create directory if not exists
    os.makedirs(f"requirements/{user_id}", exist_ok=True)
    
    # Generate document
    generate_word_doc(functional, non_functional, filename)
    
    # Update inventory
    inventory[user_id].append({
        "version": version,
        "filename": filename,
        "timestamp": timestamp
    })
    
    # Save inventory
    with open(inventory_file, "w") as f:
        json.dump(inventory, f, indent=4)
    
    return filename

# Custom CSS for modern aesthetic with Discord palette and logo styling
st.markdown(f"""
    <style>
    /* Import Inter Font for a modern look */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Apply Inter Font */
    * {{
        font-family: 'Inter', sans-serif !important;
    }}

    /* Background with Discord dark theme */
    .stApp {{
        background: #23272A;  /* Discord dark background */
        color: #FFFFFF;  /* White text */
    }}

    /* Fixed Header */
    .header {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: #2C2F33;  /* Discord secondary background */
        padding: 10px 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    /* Logo Styling */
    .logo {{
        height: 40px;
        transition: transform 0.3s ease;
    }}
    .logo:hover {{
        transform: scale(1.05);
    }}

    /* Main Content */
    .main-content {{
        margin-top: 80px;
        padding: 20px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }}

    /* Card Styling */
    .card {{
        background: #2C2F33;  /* Discord secondary background */
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    .card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
    }}

    /* Requirement Cards */
    .requirement-card {{
        background: #35393F;  /* Slightly lighter secondary background */
        border-left: 5px solid #5865F2;  /* Blurple border */
        padding: 10px;
        margin: 10px 0;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        transition: background-color 0.3s ease;
    }}
    .requirement-card:hover {{
        background-color: #3E4249;
    }}
    .requirement-text {{
        flex-grow: 1;
        font-size: 16px;
        color: #FFFFFF;
        font-weight: 400;
    }}
    .clarity-badge {{
        background-color: #5865F2;  /* Blurple badge */
        color: #FFFFFF;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        margin-left: 10px;
        font-weight: 600;
    }}

    /* Buttons */
    .stButton>button {{
        background-color: #5865F2;  /* Blurple */
        color: #FFFFFF;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        transition: background-color 0.3s ease;
    }}
    .stButton>button:hover {{
        background-color: #4752C4;  /* Darker Blurple */
    }}

    /* Text Area */
    .stTextArea textarea {{
        background: #35393F !important;
        border: 2px solid #5865F2 !important;
        color: #FFFFFF !important;
        font-size: 16px !important;
        caret-color: #5865F2 !important;
        border-radius: 8px !important;
    }}
    .stTextArea textarea::placeholder {{
        color: #99AAB5 !important;  /* Muted text */
        font-weight: 400;
    }}
    .stTextArea textarea:focus {{
        border-color: #5865F2 !important;
        box-shadow: 0 0 5px rgba(88, 101, 242, 0.5) !important;
    }}

    /* Dropdown */
    .stSelectbox div[data-baseweb="select"] {{
        background: #35393F !important;
        border: 2px solid #5865F2 !important;
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 5px !important;
    }}
    .stSelectbox div[data-baseweb="select"] > div > div:last-child {{
        background-color: #5865F2 !important;
        border-radius: 0 8px 8px 0 !important;
    }}
    .stSelectbox div[role="listbox"] {{
        background: #35393F !important;
        border: 2px solid #5865F2 !important;
        border-radius: 8px !important;
    }}
    .stSelectbox div[role="option"] {{
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 400 !important;
    }}
    .stSelectbox div[role="option"]:hover {{
        background-color: #3E4249 !important;
        color: #FFFFFF !important;
    }}
    .stSelectbox div[data-baseweb="select"]:hover {{
        border-color: #4752C4 !important;
    }}
    .stSelectbox div[data-baseweb="select"]:focus-within {{
        border-color: #5865F2 !important;
        box-shadow: 0 0 5px rgba(88, 101, 242, 0.5) !important;
    }}

    /* Progress Bar */
    .stProgress > div > div {{
        border-radius: 8px !important;
    }}

    /* File Uploader */
    .stFileUploader {{
        background: #35393F !important;
        border: 2px solid #5865F2 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }}

    /* Sidebar */
    .stSidebar {{
        background: #2C2F33 !important;
        padding: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# Encode the logo to base64 (assuming it's saved as logo.png in the same directory)
try:
    logo_base64 = get_base64_image("logo.png")
except FileNotFoundError:
    st.error("Logo file 'logo.png' not found. Please place the logo in the same directory as app.py or provide a URL.")
    logo_base64 = ""

# Header with logo
st.markdown(f"""
    <div class="header">
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{logo_base64}" class="logo" alt="Team Dynamo Logo">
        </div>
        <div style="display: flex; gap: 20px;">
            <a href="#" style="color: #FFFFFF; text-decoration: none; font-weight: 600;">Home</a>
            <a href="#" style="color: #FFFFFF; text-decoration: none; font-weight: 600;">Input</a>
            <a href="#" style="color: #FFFFFF; text-decoration: none; font-weight: 600;">Export</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar for input options
with st.sidebar:
    st.header("Input Options")
    input_type = st.selectbox("Select Input Type", ["Text", "Image", "PDF", "Word", "Excel", "Web Page"])
    
    # Dialect selection
    dialect = st.selectbox("Select English Dialect", ["American", "British"])
    
    user_input = None
    if input_type == "Text":
        user_input = st.text_area("Enter Your Idea", "e.g., Build a secure payment app", height=150)
    else:
        uploaded_file = st.file_uploader(f"Upload {input_type}", type={
            "Image": ["png", "jpg", "jpeg"],
            "PDF": ["pdf"],
            "Word": ["docx"],
            "Excel": ["xlsx"],
            "Web Page": None
        }.get(input_type, None))
        if input_type == "Web Page":
            user_input = st.text_input("Enter Web Page URL", "e.g., https://example.com")
        elif uploaded_file:
            user_input = uploaded_file

# Main content
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Input and Refinement Section
st.markdown('<div class="card">', unsafe_allow_html=True)
st.header("Generate Requirements")

# Define refinement questions
refinement_questions = {
    "secure": {
        "question": "Does 'secure' mean two-factor authentication?",
        "options": ["Yes", "No"],
        "requirement": "Implement two-factor authentication for user login."
    },
    "fast": {
        "question": "Should the system prioritize low latency (under 2 seconds)?",
        "options": ["Yes", "No"],
        "requirement": "Load time must be under 2 seconds for transactions."
    },
    "fraud": {
        "question": "Should the system monitor transactions in real-time for fraud detection?",
        "options": ["Yes", "No"],
        "requirement": "System must monitor transactions in real-time."
    },
    "payment": {
        "question": "Should the payment system comply with PCI-DSS standards?",
        "options": ["Yes", "No"],
        "requirement": "Must comply with PCI-DSS for payment security."
    }
}

if st.button("Generate"):
    if user_input:
        with st.spinner("Generating requirements..."):
            # Generate requirements based on input type and dialect
            functional, non_functional, requirements = generate_requirements(user_input, input_type.lower(), dialect)
            st.session_state.functional = functional
            st.session_state.non_functional = non_functional
            st.session_state.requirements = requirements
            
            # Detect keywords in user input
            user_input_text = user_input if input_type == "Text" else requirements
            user_input_lower = user_input_text.lower()
            relevant_questions = []
            for keyword, details in refinement_questions.items():
                if keyword in user_input_lower:
                    relevant_questions.append((keyword, details))
            
            # Refinement questions
            if relevant_questions:
                st.header("Refinement Questions")
                additional_requirements = []
                for keyword, details in relevant_questions:
                    answer = st.selectbox(details["question"], details["options"], key=f"{st.session_state.user_id}_{keyword}")
                    if answer == "Yes":
                        additional_requirements.append(details["requirement"])
                
                # Append additional requirements
                if additional_requirements:
                    requirements += "\n" + "\n".join(additional_requirements)
                    st.session_state.requirements = requirements
                    # Re-classify after adding new requirements
                    functional, non_functional = classify_requirements(requirements)
                    st.session_state.functional = functional
                    st.session_state.non_functional = non_functional

st.markdown('</div>', unsafe_allow_html=True)

# Generated Requirements Section
if st.session_state.requirements:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Generated Requirements")
    
    st.subheader("Functional Requirements")
    clarity_score, clarity_comment = calculate_clarity_score(st.session_state.requirements)
    for req in st.session_state.functional:
        if req.strip():
            st.markdown(
                f"""
                <div class="requirement-card">
                    <span class="requirement-text">✔ {req}</span>
                    <span class="clarity-badge">{clarity_score}/10</span>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.subheader("Non-Functional Requirements")
    for req in st.session_state.non_functional:
        if req.strip():
            st.markdown(
                f"""
                <div class="requirement-card">
                    <span class="requirement-text">✔ {req}</span>
                    <span class="clarity-badge">{clarity_score}/10</span>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Graphical Clarity Score
    st.subheader("Overall Clarity Score")
    if clarity_score <= 3:
        bar_color = "#D32F2F"
    elif clarity_score <= 7:
        bar_color = "#FFA000"
    else:
        bar_color = "#57F287"  # Discord green for high clarity
    st.markdown(f"""
        <style>
        .stProgress > div > div {{
            background-color: {bar_color} !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    st.progress(clarity_score / 10)
    st.write(f"Score: {clarity_score}/10 - {clarity_comment}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Version Control and Export Section
if st.session_state.requirements:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Export & Version Control")
    
    # Export options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export to Word"):
            word_file = save_versioned_document(st.session_state.user_id, st.session_state.functional, st.session_state.non_functional)
            with open(word_file, "rb") as file:
                st.download_button("Download Word Document", file, file_name=os.path.basename(word_file))
    
    with col2:
        if st.button("Export User Stories to Excel"):
            excel_file = extract_user_stories(st.session_state.functional)
            with open(excel_file, "rb") as file:
                st.download_button("Download Excel for Jira", file, file_name=excel_file)
    
    # Version history
    st.subheader("Version History")
    with open(inventory_file, "r") as f:
        inventory = json.load(f)
    
    if st.session_state.user_id in inventory:
        versions = inventory[st.session_state.user_id]
        for version in versions:
            st.write(f"Version {version['version']} - {version['timestamp']}")
            with open(version["filename"], "rb") as file:
                st.download_button(
                    f"Download Version {version['version']}",
                    file,
                    file_name=os.path.basename(version["filename"])
                )
    else:
        st.write("No versions available yet.")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; padding: 20px; background: #2C2F33; border-radius: 10px; margin-top: 20px;">
        <h2 style="font-size: 24px; font-weight: 700; color: #5865F2; margin: 0;">Dynamo v1.0</h2>
        <p style="font-size: 14px; color: #99AAB5; margin: 5px 0;">AI-Powered Requirement Writing by Team Dynamo</p>
    </div>
""", unsafe_allow_html=True)