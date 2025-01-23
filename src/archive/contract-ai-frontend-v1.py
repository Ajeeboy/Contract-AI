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
    page_title='decipher.ai',
    page_icon=':briefcase:',
    layout='wide'
    )

    # Red banner with text
st.markdown(
    """
    <style>
        .red-banner {
            background-color: #FF0000;
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="red-banner">This is a solid red banner!</div>', unsafe_allow_html=True)


# Navigation
st.sidebar.title('Workflow Steps')
options = ['Select Documents', 'Set Questions', 'Review', 'Alert Functionality', 'History', 'Review Outputs']
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

# Document upload and selection
if selection == 'Select Documents':
    st.title('Loading / Selecting Contracts')

    with st.form(key='doc_form'):
        uploaded_files = st.file_uploader("Upload contracts", accept_multiple_files=True, key='file_uploader')
        submit_button = st.form_submit_button(label='Load Selected Contracts')

    if submit_button:
        for uploaded_file in uploaded_files:
            # Simulate processing the document
            filename = process_document(uploaded_file)
            st.session_state['uploaded_files'].append(filename)

# Setting Questions
elif selection == 'Set Questions':
    st.title('Setting Questions')

    with st.form(key='questions_form'):
        questions_input = st.text_area('Enter questions separated by newline', height=300)
        submit_questions = st.form_submit_button('Submit Questions')

    if submit_questions:
        st.session_state['questions'] = questions_input.split('\n')

# Review
elif selection == 'Review':
    st.title('Review Inputs')
    if st.session_state['uploaded_files']:
        st.subheader('Selected Documents:')
        for filename in st.session_state['uploaded_files']:
            st.write(filename)
    else:
        st.write("No documents uploaded.")

    if st.session_state['questions']:
        st.subheader('Questions to ask:')
        for question in st.session_state['questions']:
            st.write(question)
    else:
        st.write("No questions set.")

# Alert Functionality
elif selection == 'Alert Functionality':
    st.title('Alert Functionality')
    alert_message = st.text_input("Enter the message for the alert:")
    if st.button('Send Alert'):
        send_alert(alert_message)

# History
elif selection == 'History':
    st.title('History View')
    history_data = get_history()
    for run, date in history_data:
        st.write(f"Run: {run}, Date: {date}")

# Review Outputs
elif selection == 'Review Outputs':
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