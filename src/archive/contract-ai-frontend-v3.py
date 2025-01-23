# Import handler libraries
import streamlit as st
import hydralit_components as hc
import pandas as pd
import time
from io import BytesIO


# Initialise webapp configs
st.set_page_config(
    page_title="Contract.ai",
    page_icon=":robot_face:",
    layout="wide"
    )
st.markdown(
    """
    <style>
        .banner {
            display: flex;
            align-items: center;
            background-color: #FFFFFF;
            color: white;
            padding: 15px;
            font-size: 20px;
            font-weight: bold;
            }
        .logo {
            width: 40px;
            margin-right: 10px;
            }
    </style>
    """,
    unsafe_allow_html=True
    )
st.markdown(
    "<div class='banner' style='color: black'><img src='https://upload.wikimedia.org/wikipedia/en/7/7f/PA_Consulting_Group_logo.svg' class='logo'>Contract.ai</div>",
    unsafe_allow_html=True
    )


# Define reference session states
if "current_menu" not in st.session_state:
    st.session_state["current_menu"] = "Start"
if "uploaded_files" not in st.session_state:
    st.session_state["uploaded_files"] = []
if "questions" not in st.session_state:
    st.session_state["questions"] = []


#Define categories and associated questions
categories = {
    "Autorenewals": ["Question 1 for Autorenewals", "Question 2 for Autorenewals", "Question 3 for Autorenewals"],
    "Suppliers": ["Question 1 for Suppliers", "Question 2 for Suppliers", "Question 3 for Suppliers"]
    # Add more categories and associated questions as needed
    }


# Placeholder function to retrieve file names
def process_document(file):
    time.sleep(3)  # Simulate processing time
    return file.name

# Placeholder function to export outputs to Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data

# Placeholder funtion to data pass to gpt model
def to_gpt():
    time.sleep(3) # Simulate processing time
    pass

# Session state check to load homepage
if st.session_state["current_menu"].replace(" ","") == ("Start").replace(" ",""):
    st.title("Welcome to IAG's Contract AI Solution")
    st.markdown("Contract.ai is an advanced contract AI solution developed by PA Consulting. Our platform offers streamlined contract management capabilities, empowering you to effortlessly process, analyse, and manage your contracts with ease.", unsafe_allow_html=True)

# Check for button clicks
if "clicked" not in st.session_state:
        st.session_state.clicked = False

# Define our button click function
def click_button():
        st.session_state.clicked = True
        VarClickCheck = True

st.button(label="Let's get started!", on_click=click_button)

# Function to display previously reviewed outputs table
def display_reviewed_outputs():
    st.title("Previously Reviewed Outputs")

    df_output = pd.DataFrame({
        "Document": ["Contract 1", "Contract 3", "Contract 5"],
        "Question 1": ["Answer 1", "Answer 3", "Answer 5"],
        "Question 2": ["Answer 2", "Answer 4", "Answer 6"],
        # More questions and answers dummy
    })

    st.table(df_output)

# Add this to the home page
display_reviewed_outputs()

if st.session_state.clicked == True:
    # st.title("PA CONTRACT AI SOLUTION")
    st.session_state["current_menu"] = ("Select Documents").replace(" ", "")
    
    st.markdown("")

# Function for "Select Documents" menu
def display_select_documents():
    st.title("Select Documents")

    if not st.session_state.get("uploaded_files"):
        upload_status = st.empty()  
        upload_status.text("Waiting for you to upload document")

    with st.form(key="doc_form"):
        uploaded_files = st.file_uploader("Upload Documents", accept_multiple_files=True, key="file_uploader_1")
        submit_button = st.form_submit_button(label="Upload Selected Documents")
        st.markdown("<span style='color:red'>File should be a PDF</span>", unsafe_allow_html=True)
    
    if uploaded_files:
        st.session_state["uploaded_files"] = []  
        for uploaded_file in uploaded_files:
            filename = process_document(uploaded_file)
            st.session_state["uploaded_files"].append(filename)
        
        if not st.session_state.get("uploaded_files"):
            upload_status = st.empty()  
            upload_status.text("Document has been uploaded")
        
    time.sleep(5)  

def display_questions():
    st.title("Setting Questions")
    
    # Questions df
    if "questions_df" not in st.session_state:
        st.session_state.questions_df = pd.DataFrame(columns=["Question"])

    # Checkbox to load preset questions
    load_preset_questions = st.checkbox("Load preset questions")  
   
    if load_preset_questions:  
        preset_topics = ["Autorenewals", "Suppliers"]  # Example preset topics
        selected_topics = st.multiselect("Select topics:", preset_topics)  # Display checkboxes to select topics

        for selected_topic in selected_topics:
            preset_questions = categories.get(selected_topic, [])  # Get preset questions for the selected topic
            st.subheader(f"Preset Questions for {selected_topic}:")
            for i, question in enumerate(preset_questions):
               st.checkbox(f"Question {i+1}: {question}")
            st.write("")   # Add some space
    
  
    with st.form(key="questions_form"):
        questions_input = st.text_area("Add bespoke questions\nThese must be separated by newline if submitting multiple questions at once", height=1)
        submit_questions = st.form_submit_button("Enter Questions")

    

    if submit_questions:
        # Split the input into a list of questions
        questions_list = questions_input.split("\n")
        
        # Create a DataFrame with each question as a separate entry
        new_questions_df = pd.DataFrame({"Question": questions_list})
        
        # Concatenate the existing DataFrame with the new DataFrame
        st.session_state.questions_df = pd.concat([st.session_state.questions_df, new_questions_df], ignore_index=True)

        st.table(st.session_state.questions_df)

        # Button to clear all rows
        if st.button("Clear All") and submit_questions:
            st.session_state.questions_df = pd.DataFrame(columns=["Question"])

def display_submit():
    st.title("Review Inputs")
    if st.session_state["uploaded_files"]:
        st.subheader("Selected Documents:")
        for filename in st.session_state["uploaded_files"]:
            st.write(filename)
    #        if st.form_submit_button("Submit", on_click=to_gpt):
     #            st.write("Submitted")  
    else:
        st.write("No documents uploaded")

    if "questions_df" not in st.session_state:
        st.write("No questions set")
    elif not st.session_state.questions_df.empty:
        st.subheader("Questions to ask:")
        st.table(st.session_state.questions_df)
    else:
        st.write("No questions set")

    st.title("Alert Configuration (Optional)")
    # with st.form("SMS"):
    #     # Dropdown for selecting alert type
    #     st.subheader("SMS")

    #     Potential_PhoneNumber = st.text_input("Please insert your phone number")

    #     # Checkbox for confirmation
    #     confirmation = st.checkbox("I confirm that I want to set up this method of alert.")

    #     # Submit button
    #     submitted = st.form_submit_button("Set Up Alert")

    #     # Handle form submission
    #     if submitted and confirmation:
    #         st.success(f"SMS Alert successfully set up!")
    #         PhoneNumberStorage(Potential_PhoneNumber)
    #     else:
    #         st.info(f"Please confirm")
    
    with st.form("Email"):
        st.subheader("Email")

        # Potential_Email = st.text_input("Please insert your email address")

        # Checkbox for confirmation
        confirmation = st.checkbox("I confirm that I want to set up an email alert")

        # Submit button
        submitted = st.form_submit_button("Set Up Alert")

        # Handle form submission
        if submitted and confirmation:
            st.success(f"Email Alert successfully set up!")
            Alert_Email = True     
        else:
            st.info(f"Please confirm")

    Final_submit_button = st.button(label="Submit", on_click=to_gpt)



def display_outputs():
    st.title("Review Outputs")
    if not st.session_state["uploaded_files"] or st.session_state["questions_df"].empty:  
        st.write("Please upload documents and set questions first.")
    else:
        # Display "Generating results" message while waiting
        with st.spinner("Generating results..."):
            # Generate results with a delay
            df_output = generate_results()

            # Remove "Generating results" message once the table is generated
            st.empty()

            # Display the table
            st.table(df_output)

# Function to simulate generating results with a delay
def generate_results():
    time.sleep(5)  # Simulating a delay of 5 seconds

    df_output = pd.DataFrame({
        "Document": st.session_state["uploaded_files"],  
        "Question 1": ["Answer 1"] * len(st.session_state["uploaded_files"]),  
        "Question 2": ["Answer 2"] * len(st.session_state["uploaded_files"]),  
        # More questions and answers dummy
    })

    return df_output
if (st.session_state["current_menu"]).replace(" ", "") == ("Review Outputs").replace(" ", ""):
    # Display "Generating results" message while waiting
    st.write("Generating results...")

    # Generate results with a delay
    df_output = generate_results()

    # Remove "Generating results" message once the table is generated
    st.empty()

    # Display the table
    st.table(df_output)

# Function to simulate generating results with a delay
def generate_results():
    with st.spinner("Generating results..."):
        time.sleep(5)  # Simulating a delay of 5 seconds

    df_output = pd.DataFrame({
        "Document": ["Contract 1", "Contract 3", "Contract 5"],
        "Question 1": ["Answer 1", "Answer 3", "Answer 5"],
        "Question 2": ["Answer 2", "Answer 4", "Answer 6"],
        # More questions and answers dummy
    })

    st.table(df_output)

    if st.button("Export to Excel"):
        # Simulate exporting to Excel
        excel_data = to_excel(df_output)
        st.download_button(
            label="Download Excel file",
            data=excel_data,
            file_name="output.xlsx",
            mime="application/vnd.ms-excel"
        )

if st.session_state.clicked == True:
    menu_data = [
        {"label":"Select Documents"},
        {"label":"Set Questions"},
        {"label":"Review & Submit"},
        {"label":"Review Outputs"},
    ]

    menu_id = hc.nav_bar(menu_definition=menu_data, option_menu=True)
    st.session_state["current_menu"] = menu_id
    

# if (st.session_state["current_menu"]).replace(" ", "") == ("Start").replace(" ", ""):
#     # display_home()

if (st.session_state["current_menu"]).replace(" ", "") == ("Select Documents").replace(" ", "") and st.session_state.clicked == True:
    display_select_documents()

if (st.session_state["current_menu"]).replace(" ", "") == ("Set Questions").replace(" ", "") and st.session_state.clicked == True:
    display_questions()

if (st.session_state["current_menu"]).replace(" ", "") == ("Review & Submit").replace(" ", "") and st.session_state.clicked == True:
    display_submit()
    
if (st.session_state["current_menu"]).replace(" ", "") == ("Review Outputs").replace(" ", "") and st.session_state.clicked == True:
    display_outputs()