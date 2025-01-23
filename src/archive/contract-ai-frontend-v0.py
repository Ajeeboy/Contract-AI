# Import handler libraries
import streamlit as st
import pandas as pd
import time
from io import BytesIO

# Initialise session state variables
if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = []

if 'questions' not in st.session_state:
    st.session_state['questions'] = []

# Initialise webapp configs
st.set_page_config(
    page_title='Contract.ai',
    page_icon=':robot_face:',
    layout='wide'
    )

# Red banner with text
st.markdown(
    """
    <style>
        .red-banner {
            display: flex;
            align-items: center;
            background-color: #BCC2B5;
            color: white;
            padding: 15px;
            font-size: 20px;
            font-weight: bold;
        }

        .logo {
            width: 40px;  /* Adjust the width of the logo as needed */
            margin-right: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="red-banner"><img src="https://ddl-conference.com/wp-content/uploads/2016/06/PA-logo.png" class="logo">PA Consulting [Client Name]</div>',
    unsafe_allow_html=True
)


# Navigation
st.sidebar.title('Process Staging')
options = ['Select Documents', 'Set Questions', 'Review and Submit', 'Review Outputs']
#History deleted for now
#Alert Functionality deleted for now
selection = st.sidebar.selectbox("Choose step:", options)

# Function to simulate processing and returning the filename
def process_document(file):
    time.sleep(1)  # Simulate some processing time
    return file.name

# Function to simulate sending an alert
def send_alert(message):
    time.sleep(1)  # Simulate some processing time
    st.success(f"Alert sent: {message}")

# Function to simulate saving and retrieving history
def save_history(run, date):
    # This is where you would save the history
    pass

def get_history():
    # This would normally retrieve history from a database or file
    return [("Run 1", "2023-01-01"), ("Run 2", "2023-02-01")]

# Function to simulate exporting data to Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data

#Function to send to AI
def to_gpt():
    pass

# Document upload and selection
if selection == 'Select Documents':
    st.title('Upload Documents')

    with st.form(key='doc_form'):
        uploaded_files = st.file_uploader("Upload Documents", accept_multiple_files=True, key='file_uploader')
        submit_button = st.form_submit_button(label='Load Selected Contracts')

    if submit_button:
        for uploaded_file in uploaded_files:
            # Simulate processing the document
            filename = process_document(uploaded_file)
            st.session_state['uploaded_files'].append(filename)

# Setting Questions
if selection == 'Set Questions':
    st.title('Setting Questions')
    
    # Questions df
    if 'questions_df' not in st.session_state:
        st.session_state.questions_df = pd.DataFrame(columns=["Question"])
    
    with st.form(key='questions_form'):
        questions_input = st.text_area('Enter questions separated by newline', height=300)
        submit_questions = st.form_submit_button('Submit Questions')
    
    # Button to clear all rows
    if st.button('Clear All'):
        st.session_state.questions_df = pd.DataFrame(columns=["Question"])

    if submit_questions:
        # Split the input into a list of questions
        questions_list = questions_input.split('\n')
        
        # Create a DataFrame with each question as a separate entry
        new_questions_df = pd.DataFrame({"Question": questions_list})
        
        # Concatenate the existing DataFrame with the new DataFrame
        st.session_state.questions_df = pd.concat([st.session_state.questions_df, new_questions_df], ignore_index=True)

        st.table(st.session_state.questions_df)

    back_button_select = st.button('Previous Step')
    
    if back_button_select:
        selection = options[0]
        st.write(selection)
        
        

if selection == 'Review and Submit':
    st.title('Review Inputs')
    if st.session_state['uploaded_files']:
        st.subheader('Selected Documents:')
        for filename in st.session_state['uploaded_files']:
            st.write(filename)
    else:
        st.write("No documents uploaded.")

    if 'questions_df' not in st.session_state:
        st.write("No questions set")
    elif not st.session_state.questions_df.empty:
        st.subheader('Questions to ask:')
        st.table(st.session_state.questions_df)
    else:
        st.write("No questions set.")

    st.title("Alert Configuration")
    with st.form("alert_form"):
        # Dropdown for selecting alert type
        alert_type = st.selectbox("Select Alert Type:", ["Email", "SMS", "Push Notification", "No Alert"])

        # Checkbox for confirmation
        confirmation = st.checkbox("I confirm that I want to set up this alert.")

        # Submit button
        submitted = st.form_submit_button("Set Up Alert")

        # Handle form submission
        if submitted and confirmation:
            st.success(f"Alert type '{alert_type}' successfully set up!")
        elif submitted:
            st.warning("Please confirm that you want to set up the alert.")

    Final_submit_button = st.button(label='Submit', on_click=to_gpt)

# # Alert Functionality
# elif selection == 'Alert Functionality':
#     st.title('Alert Functionality')
#     alert_message = st.text_input("Enter the message for the alert:")
#     if st.button('Send Alert'):
#         send_alert(alert_message)

# # History
# elif selection == 'History':
#     st.title('History View')
#     history_data = get_history()
#     for run, date in history_data:
#         st.write(f"Run: {run}, Date: {date}")

# Review Outputs
if selection == 'Review Outputs':
    st.title('Review Outputs')
    # Dummy dataframe
    df_output = pd.DataFrame({
        'Document': ['Contract 1', 'Contract 3', 'Contract 5'],
        'Question 1': ['Answer 1', 'Answer 3', 'Answer 5'],
        'Question 2': ['Answer 2', 'Answer 4', 'Answer 6'],
        # More questions and answers
    })

    st.table(df_output)

    if st.button('Export to Excel'):
        # Simulate exporting to Excel
        excel_data = to_excel(df_output)
        st.download_button(
            label="Download Excel file",
            data=excel_data,
            file_name="output.xlsx",
            mime="application/vnd.ms-excel"
        )