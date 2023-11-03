import streamlit as st
import subprocess
import os
import pandas as pd
import spacy

"""
@author: Ayush Garg
ayush@science.org.in
"""
project_name = "project"
output_file = "output.csv"
output_file_name = os.path.join(os.getcwd(), project_name, output_file)
run_pygetpapers = False
make_section = True


# Function to run the docanalysis command
def run_command(command):
    with st.spinner("Running the command..."):
        process = subprocess.run(
            command,
            shell=True,
            text=True,
        )


# Streamlit UI layout
st.title("DocAnalysis Command Runner")

with st.form("docanalysis_form"):
    # Define the user inputs
    # project_name = st.text_input("Project")
    # output_file = st.text_input("Output File", value="./output.csv")
    # run_pygetpapers = st.checkbox("Run PyGetPapers")
    # make_section = st.checkbox("Make Section")
    query = st.text_input("Query", max_chars=200)
    hits = st.number_input("Number of Hits", min_value=1, value=10)

    # File and Folder Picker for Dictionary and Output Directory
    dictionary_file = st.file_uploader(
        "Choose a Dictionary File", type=["xml", "json", "txt"]
    )
    sections_to_search = st.multiselect(
        "Sections to Search",
        [
            "ALL",
            "ACK",
            "AFF",
            "AUT",
            "CON",
            "DIS",
            "ETH",
            "FIG",
            "INT",
            "KEY",
            "MET",
            "RES",
            "TAB",
            "TIL",
        ],
        default=["ALL"],
    )
    entities = st.multiselect(
        "Entities to Extract",
        ["GPE", "LANGUAGE", "ORG", "PERSON", "CHEMICAL", "DISEASE"],
        default=["GPE", "LANGUAGE", "ORG", "PERSON"],
    )
    spacy_model = st.selectbox("SpaCy Model", ["spacy", "scispacy"], index=0)

    # Submit button
    submit_button = st.form_submit_button(label="Run DocAnalysis")

    if submit_button:
        # Construct the command with the provided inputs
        command_elements = ["docanalysis"]
        if run_pygetpapers:
            command_elements.append("--run_pygetpapers")
        if make_section:
            command_elements.append("--make_section")
        if query:
            command_elements.extend(["-q", f'"{query}"'])
        if hits:
            command_elements.extend(["-k", str(hits)])
        command_elements.extend(["--project_name", f"{project_name}"])
        command_elements.extend(["-o", output_file])
        if dictionary_file is not None:
            # Save the uploaded file and pass it to the command
            dictionary_path = os.path.join(os.getcwd(), dictionary_file.name)
            with open(dictionary_path, "wb") as f:
                f.write(dictionary_file.getbuffer())
            command_elements.extend(["-d", f"{dictionary_path}"])
        # if make_ami_dict:
        #     command_elements.append("--make_ami_dict")
        if sections_to_search:
            command_elements.extend(["--search_section"] + sections_to_search)
        if entities:
            command_elements.extend(["--entities"] + entities)
        if spacy_model:
            command_elements.extend(["--spacy_model", spacy_model])

        # Join command elements to form the final command
        final_command = " ".join(command_elements)
        st.text("Running command:")
        st.code(final_command)

        # Run the command
        run_command(final_command)
if os.path.exists(output_file_name):
    # Display the CSV file as a downloadable link
    with open(output_file_name, "rb") as file:
        st.download_button("Download CSV", file, file_name=output_file)

    # Display the content of the CSV on the screen
    df = pd.read_csv(output_file_name)

    # Remove 'file_path' column if it exists
    df = df.drop(columns="file_path", errors="ignore")

    # Drop columns with all None values
    df = df.dropna(axis=1, how="all")

    st.dataframe(df)
