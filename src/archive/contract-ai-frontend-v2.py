import streamlit as st
import pandas as pd
import time
from io import BytesIO
import hydralit_components as hc

if 'current_menu' not in st.session_state:
    st.session_state['current_menu'] = "Login"

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


# COMMENTED OUT FOR NOW Red banner with text - 21/02/2024
# st.markdown(
#     """
#     <style>
#         .red-banner {
#             display: flex;
#             align-items: center;
#             background-color: #BCC2B5;
#             color: white;
#             padding: 15px;
#             font-size: 20px;
#             font-weight: bold;
#         }

#         .logo {
#             width: 40px;  /* Adjust the width of the logo as needed */
#             margin-right: 10px;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown(
#     '<div class="red-banner"><img src="https://ddl-conference.com/wp-content/uploads/2016/06/PA-logo.png" class="logo">PA Consulting [Client Name]</div>',
#     unsafe_allow_html=True
# )

# Function to simulate processing and returning the filename
def process_document(file):
    time.sleep(1)  # Simulate some processing time
    return file.name

# Function to simulate exporting data to Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data

#PASS TO MODEL GOES HERE DYLAN
def to_gpt():
    pass

if st.session_state['current_menu'].replace(" ","") == ("Login").replace(" ",""):
    st.title('Login')
    st.subheader("Welcome to PA's Contract AI Solution")
    st.markdown("""
                <div>
                    Please Log In
                </div>
                """, unsafe_allow_html=True)

    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    def click_button():
        st.session_state.clicked = True
        VarClickCheck = True

    st.button(label="Begin", on_click=click_button)

if st.session_state.clicked == True:
    # st.title("PA CONTRACT AI SOLUTION")
    st.session_state['current_menu'] = ("Select Documents").replace(" ", "")

# Function for "Select Documents" menu
def display_select_documents():
    st.title('Upload Documents')

    with st.form(key='doc_form'):
        uploaded_files = st.file_uploader("Upload Documents", accept_multiple_files=True, key='file_uploader')
        submit_button = st.form_submit_button(label='Upload Selected Documents')

    if submit_button:
        for uploaded_file in uploaded_files:
            # Simulate processing the document
            filename = process_document(uploaded_file)
            st.session_state['uploaded_files'].append(filename)

def display_questions():
    st.title('Setting Questions')
    
    # Questions df
    if 'questions_df' not in st.session_state:
        st.session_state.questions_df = pd.DataFrame(columns=["Question"])
    
    with st.form(key='questions_form'):
        questions_input = st.text_area('Enter questions separated by newline', height=1)
        submit_questions = st.form_submit_button('Enter Questions')


    if submit_questions:
        # Split the input into a list of questions
        questions_list = questions_input.split('\n')
        
        # Create a DataFrame with each question as a separate entry
        new_questions_df = pd.DataFrame({"Question": questions_list})
        
        # Concatenate the existing DataFrame with the new DataFrame
        st.session_state.questions_df = pd.concat([st.session_state.questions_df, new_questions_df], ignore_index=True)

        st.table(st.session_state.questions_df)

        # Button to clear all rows
        if st.button('Clear All') and submit_questions:
            st.session_state.questions_df = pd.DataFrame(columns=["Question"])

def display_submit():
    st.title('Review Inputs')
    if st.session_state['uploaded_files']:
        st.subheader('Selected Documents:')
        for filename in st.session_state['uploaded_files']:
            st.write(filename)
    else:
        st.write("No documents uploaded")

    if 'questions_df' not in st.session_state:
        st.write("No questions set")
    elif not st.session_state.questions_df.empty:
        st.subheader('Questions to ask:')
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

    Final_submit_button = st.button(label='Submit', on_click=to_gpt)

def display_outputs():
    st.title('Review Outputs')

    df_output = pd.DataFrame({
        'Document': ['Contract 1', 'Contract 3', 'Contract 5'],
        'Question 1': ['Answer 1', 'Answer 3', 'Answer 5'],
        'Question 2': ['Answer 2', 'Answer 4', 'Answer 6'],
        # More questions and answers dummy
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

if st.session_state.clicked == True:
    menu_data = [
        {'label':"Select Documents"},
        {'label':"Set Questions"},
        {'label':"Review & Submit"},
        {'label':"Review Outputs"},
    ]

    menu_id = hc.nav_bar(menu_definition=menu_data, option_menu=True)
    st.session_state['current_menu'] = menu_id

# if (st.session_state['current_menu']).replace(" ", "") == ("Login").replace(" ", ""):
#     # display_home()

if (st.session_state['current_menu']).replace(" ", "") == ("Select Documents").replace(" ", "") and st.session_state.clicked == True:
    display_select_documents()

if (st.session_state['current_menu']).replace(" ", "") == ("Set Questions").replace(" ", "") and st.session_state.clicked == True:
    display_questions()

if (st.session_state['current_menu']).replace(" ", "") == ("Review & Submit").replace(" ", "") and st.session_state.clicked == True:
    display_submit()
    
if (st.session_state['current_menu']).replace(" ", "") == ("Review Outputs").replace(" ", "") and st.session_state.clicked == True:
    display_outputs()