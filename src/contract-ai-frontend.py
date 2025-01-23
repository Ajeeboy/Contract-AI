# Import handler libraries
import os
import sys
import configparser
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from io import BytesIO
import io
from xlsxwriter import Workbook

# Import handler scripts
src_dir = os.getcwd() + r"\src"
if not src_dir in sys.path:
    sys.path.append(src_dir)
from components.config import config
from components.modules import indexes
from components.modules import models
from components.routes import blob_handler
from components.routes import vector_handler

# Initialise config file
configfile = configparser.ConfigParser()
configfile.read(r"src\components\config\config.ini")

# Initialise session state variables
st.session_state.setdefault("current_step", "Start")
st.session_state.setdefault("clicked", False)
st.session_state.setdefault("loaded_documents", {})
st.session_state.setdefault("uploaded_documents", {})
st.session_state.setdefault("selected_documents", [])
st.session_state.setdefault("loaded_questions", {})
st.session_state.setdefault("preset_questions", [])
st.session_state.setdefault("custom_questions", [])
st.session_state.setdefault("selected_questions", [])
st.session_state.setdefault("submitted", False)     # TODO: is this useless, no False switchback
st.session_state.setdefault("processed", False)
st.session_state.setdefault("results", pd.DataFrame())
st.session_state.setdefault("exported", False)

# Initialise webapp configs
st.set_page_config(
    page_title="Contract Compass",
    page_icon=":robot_face:",
    layout="wide"
    )

# Initialise banner
st.markdown(
    """
    <style>
        .banner {
            display: flex;
            align-items: center;
            background-color: #0e1117;
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
    "<div class='banner' style='color: white'><img src='https://cdn-ukwest.onetrust.com/logos/f79a60b0-1d16-4114-aa58-3f05dec13dd2/513cb4cf-2cd9-4bb7-9c4c-589c3d6cd931/c2cddcca-8c2a-4e6b-819e-7f48776bf3a1/PA_Logo_2022_800px.png' class='logo'>Contract Compass</div>",
    unsafe_allow_html=True
    )


# Define function to display navigation bar
def display_navigation_bar():
    st.sidebar.title("Navigation")
    steps_without_review_outputs = [step for step in config.webapp_steps if step != "Review Outputs"]
    selected_step = st.sidebar.radio("Go to...", steps_without_review_outputs, index=steps_without_review_outputs.index(st.session_state.current_step))
    if selected_step != st.session_state.current_step:
        st.session_state.current_step = selected_step
        st.rerun()     # TODO: experiment with the placement of these throughout script
    col1, col2 = st.sidebar.columns(2)
    if not st.session_state.current_step == "Start":
        back_button = col1.button("Back")
        if back_button and st.session_state.current_step == "Select Documents":
            st.session_state.current_step = "Start"
            st.rerun()
        elif back_button and st.session_state.current_step == "Set Questions":
            st.session_state.current_step = "Select Documents"
            st.rerun()
        elif back_button and st.session_state.current_step == "Review & Submit":
            st.session_state.current_step = "Set Questions"
            st.rerun()
    if not st.session_state.current_step == "Review & Submit":
        next_button = col2.button("Next")
        if next_button and st.session_state.current_step == "Start":
            st.session_state.current_step = "Select Documents"
            st.rerun()
        elif next_button and st.session_state.current_step == "Select Documents":
            st.session_state.current_step = "Set Questions"
            st.rerun()
        elif next_button and st.session_state.current_step == "Set Questions":
            st.session_state.current_step = "Review & Submit"
            st.rerun()
    if st.sidebar.button("#DEV# Rebuild Index #DEV#"):
        indexes.index_delete()
        indexes.index_create()
        st.rerun()
    if st.sidebar.button("#DEV# Wipe Blobs #DEV#"):
        blob_handler.wipe_blobs(config.adls_connection_string, config.adls_container_input, config.adls_folder_files_input)
        st.rerun()


# Define function to display start
def display_start():
    st.title("Welcome to our Contract Compass solution")
    st.text("")
    st.markdown("<p style='font-size: 18px;'>Contract Compass is an advanced generative AI contract review tool developed by PA Consulting</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px;'>Our tool offers you the ability to ask any question of your contracts, empowering you to process, analyse, and manage your business documents with ease</p>", unsafe_allow_html=True)
    st.markdown("<hr style='height: 1px; border: none; color: #FFFFFF; background-color: #FFFFFF;'/>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    if col1.button("Get Started"):
        st.session_state.current_step = "Select Documents"
        st.session_state.clicked = True
        st.sidebar.title("Navigation")
        st.rerun()
    if col2.button("Review Outputs"):
        st.session_state.current_step = "Review Outputs"
        st.rerun()
    if col3.button("Review Summary"):
        st.session_state.current_step = "Review Summary"
        st.rerun()

# Define function to load documents
def document_loader():
    blob_data = blob_handler.download_blobs(config.adls_connection_string, config.adls_container_input, config.adls_folder_files_input)
    st.session_state.loaded_documents = blob_data

# Define function to display select documents
def display_select_documents():
    st.text("")
    st.title("Select Documents")
    st.markdown("<hr style='height: 1px; border: none; color: #FFFFFF; background-color: #FFFFFF;'/>", unsafe_allow_html=True)
    if not len(st.session_state.loaded_documents) > 0:
        document_loader()
    with st.form(key="doc_form"):
        uploaded_files = st.file_uploader("Upload New Documents", accept_multiple_files=True, key="file_uploader")
        submit_button = st.form_submit_button(label="Upload")
        upload_status = st.empty()
        if submit_button and uploaded_files:
            st.session_state.uploaded_documents = {}
            for uploaded_file in uploaded_files:
                uploaded_file_bytes = BytesIO(uploaded_file.read())
                uploaded_file_name = uploaded_file.name
                st.session_state.uploaded_documents[uploaded_file_name] = uploaded_file_bytes
                upload_status.markdown(f"<span style='color:#white'>Uploading file: {uploaded_file_name}</span>", unsafe_allow_html=True)
                blob_handler.upload_blobs(config.adls_connection_string, config.adls_container_input, config.adls_folder_files_input, uploaded_file_name, uploaded_file_bytes)
                upload_status.markdown(f"<span style='color:#white'>Uploaded file: {uploaded_file_name}</span>", unsafe_allow_html=True)
            vector_output = vector_handler.upload_vectors(st.session_state.uploaded_documents)        # TODO: see vector_handler for items
            if not vector_output == True:
                upload_status_text_list = []
                for file_name, date_time in vector_output.items():
                    upload_status_text = f"{file_name} previously uploaded on {f'{date_time[:10]} at {date_time[11:16]}'}"
                    upload_status_text_list.append(upload_status_text)
                upload_status_texts = "\n".join(upload_status_text_list)
                upload_status.markdown(f"<span style='color:#white'>{upload_status_texts}</span>", unsafe_allow_html=True)      # TODO: this doesn't work for multiple uploads
            st.session_state.uploaded_documents = [file.name for file in uploaded_files]        # TODO: stop wiping on reload
    for file in st.session_state.uploaded_documents:
        if file in st.session_state.loaded_documents:
            st.session_state.loaded_documents.pop(file)
    st.session_state.selected_documents = st.multiselect("Select Existing Documents", st.session_state.loaded_documents.keys())
    for file in st.session_state.uploaded_documents:
        if not file in st.session_state.selected_documents:
            st.session_state.selected_documents.append(file)
    if st.session_state.selected_documents:
        st.markdown("<hr style='height: 1px; border: none; color: #FFFFFF; background-color: #FFFFFF;'/>", unsafe_allow_html=True)
        st.subheader("Chosen Documents")
        for document in sorted(st.session_state.selected_documents):
            st.write(document)


# Define function to load questions
def question_loader():
    blob_data = blob_handler.download_blobs(config.adls_connection_string, config.adls_container_input, config.adls_folder_questions_input)
    for question_file_name, question_file_bytes in blob_data.items():
        question_file_bytes.seek(0)
        questions_list = [line.decode("utf-8").strip() for line in question_file_bytes.readlines()]
        st.session_state.loaded_questions[question_file_name.split(".")[0]] = questions_list

# Define function to display set questions
def display_set_questions():
    st.text("")
    st.title("Set Questions")
    st.markdown("<hr style='height: 1px; border: none; color: #FFFFFF; background-color: #FFFFFF;'/>", unsafe_allow_html=True)
    if not len(st.session_state.loaded_questions) > 0:
        question_loader()
    preset_topics = sorted(list(st.session_state.loaded_questions.keys()))
    selected_topics = st.multiselect("Preset Questions", preset_topics)
    if selected_topics:
        preset_question_list = []
        cols = st.columns(len(selected_topics))
        for index, selected_topic in enumerate(selected_topics):
            preset_batch = st.session_state.loaded_questions.get(selected_topic, [])
            with cols[index]:
                for question in preset_batch:
                    question_confirmation = st.checkbox(f"{question}")
                    if question_confirmation:
                        preset_question_list.append(question)
        st.session_state.preset_questions = preset_question_list
    with st.form(key="questions_form"):
        questions_input = st.text_area("Custom Questions (seperated on new lines)", height=1)
        submit_questions = st.form_submit_button("Submit")
    if submit_questions:
        questions_list = questions_input.split("\n")
        st.session_state.custom_questions = questions_list
    st.session_state.selected_questions = list(set(st.session_state.custom_questions + st.session_state.preset_questions))
    if len(st.session_state.selected_questions) > 0:
        st.markdown("<hr style='height: 1px; border: none; color: #FFFFFF; background-color: #FFFFFF;'/>", unsafe_allow_html=True)
        st.subheader("Chosen Questions")
        for question in sorted(st.session_state.selected_questions):
            st.write(question)


# Deifine function to display review & submit
def display_review_and_submit():
    st.text("")
    st.title("Review Inputs")
    st.markdown("<hr style='height: 1px; border: none; color: #FFFFFF; background-color: #FFFFFF;'/>", unsafe_allow_html=True)
    col1a, col2a = st.columns(2)
    with col1a:
        if st.session_state.selected_documents:
            st.subheader("Chosen Documents")
            for file in st.session_state.selected_documents:
                st.write(file)
        else:
            st.subheader("No Documents Selected")
    with col2a:
        if st.session_state.selected_questions:
            st.subheader("Chosen Questions")
            for question in st.session_state.selected_questions:
                st.write(question)
        else:
            st.subheader("No Questions Set")
    st.text("")
    st.markdown("<hr style='height: 1px; border: none; color: #FFFFFF; background-color: #FFFFFF;'/>", unsafe_allow_html=True)
    st.text("")
    with st.form("Processing Completion Email Alert"):
        st.subheader("Processing Completion Email Alert")
        submitted = st.form_submit_button("Set Up Alert")       # TODO: actually set up email alert
        if submitted:
            st.success(f"Email alert successfully set up!")
    st.markdown("<hr style='height: 1px; border: none; color: #FFFFFF; background-color: #FFFFFF;'/>", unsafe_allow_html=True)
    st.text("")
    col1b, col2b = st.columns(2)
    if col1b.button("Submit Documents & Questions"):
        if len(st.session_state.selected_documents) > 0 and len(st.session_state.selected_questions) > 0:
            st.session_state.submitted = True
            st.session_state.processed = False
            st.session_state.current_step = "Review Outputs"
            st.rerun()
        else:
            col2b.write("Please complete your submission before proceeding...")


# Define function to generate query results
def generate_results():
    results = []
    for question in sorted(st.session_state.selected_questions):
        for document in sorted(st.session_state.selected_documents):
            filtered_chunks = vector_handler.filter_chunks(document)
            answer = models.stuff_chain.invoke({"context": filtered_chunks, "question": question})
            results.append({"document": document, "question": question, "answer": answer})
    st.session_state.results = pd.DataFrame(results)
    st.session_state.results = st.session_state.results.pivot(index="document", columns="question", values="answer")
    st.session_state.processed = True

# Define function to display review outputs
def display_review_outputs():
    st.text("")
    st.title("Your Results")
    st.markdown("<hr style='height: 1px; border: none; color: #FFFFFF; background-color: #FFFFFF;'/>", unsafe_allow_html=True)
    st.text("")
    col1, col2, col3 = st.columns(3)
    if col3.button("Home"):
        st.session_state.current_step = "Start"
        st.rerun()
    if st.session_state.submitted == True:
        if st.session_state.processed == False:
            col1.subheader("Generating Results...")
            generate_results()
            st.rerun()
        if st.session_state.processed == True:
            if col1.button("Export to Excel"):
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    st.session_state.results.to_excel(writer, sheet_name="data", index=False)       # TODO: fix writing in of document name column
                buffer.seek(0)
                st.session_state.exported = True
                st.success("Outputs exported successfully")
            st.markdown("<hr style='height: 1px; border: none; color: #FFFFFF; background-color: #FFFFFF;'/>", unsafe_allow_html=True)
            st.table(st.session_state.results)
    else:
        col1.subheader("Awaiting Submission...")
    if st.session_state.exported == True:
        col2.download_button(
            label="Download Excel",
            data=buffer,
            file_name="contractai-output.xlsx",
            mime="application/vnd.ms-excel"
            )
        st.session_state.exported = False

green_red_cmap = LinearSegmentedColormap.from_list('green_red', ['red', 'yellow', 'green'])

def heatmap(input_df, input_y, input_x, input_value):
    # Aggregate the values to handle duplicate entries
    aggregated_data = input_df.groupby([input_y, input_x])[input_value].mean().reset_index()
    # Pivot the dataframe for heatmap
    heatmap_data = aggregated_data.pivot(index=input_y, columns=input_x, values=input_value)
    # Adjust figure size based on data dimensions
    num_y = len(heatmap_data.index)
    num_x = len(heatmap_data.columns)
    fig_width = min(max(num_x, 8), 16)  # Ensure a minimum width and cap at a maximum width
    fig_height = min(max(num_y, 10), 20)  # Ensure a minimum height and cap at a maximum height
    # Create a figure and set the background to be transparent
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor='none')
    # Create the heatmap
    heatmap = sns.heatmap(heatmap_data, cmap=green_red_cmap, annot=True, fmt=".0f", linewidths=.5, ax=ax,
                          cbar_kws={'label': input_value}, annot_kws={"color": "white"})    
    # Set labels and title properties
    ax.set_ylabel(input_y, fontsize=18, fontweight='bold', color='white')
    ax.set_xlabel(input_x, fontsize=18, fontweight='bold', color='white')
    ax.set_title('', fontsize=18, fontweight='bold', color='white')
    # Set the tick labels to white
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')    
    # Rotate the x-axis labels for better readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=20, color='white')
    plt.setp(ax.get_yticklabels(), rotation=0, fontsize=20, color='white')    
    # Set the background of the heatmap to be transparent
    ax.set_facecolor('none')
    fig.patch.set_alpha(0.0)    
    # Customise the colorbar
    cbar = heatmap.collections[0].colorbar
    cbar.ax.yaxis.set_tick_params(color='white')
    cbar.outline.set_edgecolor('white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), fontsize=20, color='white')
    cbar.set_label(input_value, fontsize=18, color='white')
    plt.tight_layout()    
    # Display the heatmap
    st.pyplot(fig)


def radar_chart(dimensions, scores):
    # Number of variables
    num_vars = len(dimensions)
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    # Make the plot close to a circle
    scores += scores[:1]
    angles += angles[:1]
    # Plot
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True), facecolor='none')
    ax.patch.set_alpha(0)  # Set background to transparent
    ax.fill(angles, scores, color='red', alpha=0.25, zorder=2)
    ax.plot(angles, scores, color='red', linewidth=2, zorder=3)
    # Customize text and axes color
    #ax.tick_params(colors='white')
    #ax.xaxis.label.set_color('white')
    #ax.yaxis.label.set_color('white')
    ax.yaxis.grid(True, color='white', zorder=1)
    ax.title.set_color('white')
    plt.setp(ax.get_xticklabels(), color="white", fontsize=8, weight='bold',bbox=dict(facecolor='red', alpha=0.5), zorder=5)
    plt.setp(ax.get_yticklabels(), color="white")
    ax.spines['polar'].set_color('grey')
    ax.spines['polar'].set_linewidth(0.1)
    # Labels
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions, ha='center', va='center', zorder=4)
    ax.yaxis.grid(True, color='grey')
    # Add values to the axis
    ax.set_ylim(0, 100)  # Adjust the range according to your data
    for i, angle in enumerate(angles[:-1]):
        ax.text(angle, scores[i] + 5, f"{scores[i]:.0f}", color='white', fontsize=8, fontweight='bold', ha='center', va='baseline', zorder=6) # Adjust va parameter to move the text closer to the line
    return fig

def dashboard_output():
    categories = ["Cyber", "Information", "ESG", "Reputation", "Compliance", "Operational", "Financial", "Strategic"]
    business_areas = ["Supplies", "Procurement", "Information Technology", "Occupational Health", "Informatics", "Facilities", "Security", "Finance", "Payroll", "Financial Services", "CEO Office", "Workforce"]
    data = pd.DataFrame({
        "Category": np.repeat(categories, len(business_areas)),
        "Business Area": np.tile(business_areas, len(categories)),
        "Value": np.random.rand(len(categories) * len(business_areas)) * 100
    })

    st.text("")
    st.title("Your Summary")
    st.markdown("<hr style='height: 1px; border: none; color: #FFFFFF; background-color: #FFFFFF;'/>", unsafe_allow_html=True)
    st.text("")

    col1, col2 = st.columns(2)
    with col1:
        # Calculate average scores for each business area
        average_scores = []
        for category in categories:
            avg_score = data[data["Category"] == category]["Value"].mean()
            average_scores.append(avg_score)
        st.pyplot(radar_chart(categories, average_scores))

    with col2:
        heatmap(data, "Category", "Business Area", "Value")

# Main function
def main():
    if st.session_state.current_step == "Start":
        display_start()
    elif st.session_state.current_step == "Select Documents":
        display_select_documents()
    elif st.session_state.current_step == "Set Questions":
        display_set_questions()
    elif st.session_state.current_step == "Review & Submit":
        display_review_and_submit()
    elif st.session_state.current_step == "Review Outputs":
        display_review_outputs()
    elif st.session_state.current_step == "Review Summary":
        dashboard_output()        
    if st.session_state.current_step != "Start" and st.session_state.current_step != "Review Outputs" and st.session_state.current_step != "Review Summary":
        display_navigation_bar()

# Runtime process
if __name__ == "__main__":
    main()