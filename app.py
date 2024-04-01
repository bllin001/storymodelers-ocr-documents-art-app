import streamlit as st
import subprocess
import os

#=======================================================================================================================#

def clear_submit():
    st.session_state["submit"] = False

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.set_page_config(page_title='OCR App', page_icon=':pencil:', layout='wide', initial_sidebar_state='auto')

#=======================================================================================================================#

#--------------------------Sidebar--------------------------#

with st.sidebar:
    # Add a title
    st.title('Load document')

    # Add a file uploader
    uploaded_file = st.file_uploader(
            "Upload file", type=["pdf"], 
            help="Only PDF files are supported", 
            on_change=clear_submit)

    # Add a button
    if uploaded_file:
        st.markdown('---')
        st.title('Extract text from PDF')
        extract_text = st.button('Extract', help='Extract text from the document')
    
#=======================================================================================================================#

#--------------------------Main Page--------------------------#

if uploaded_file:
    # create files folder
    if not os.path.exists('files'):
        os.makedirs('files')
        
    # Create a temporary folder
    input_path = f'./files/{uploaded_file.name}'
    # Create output file
    output_file = f'{uploaded_file.name}'.replace('.pdf', '.mmd')
    output_path = f'./files/'

    # mmd path
    mmd_path = f'./files/{output_file}'

    with open(input_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    # Load the model
    @st.cache_resource(show_spinner=False)
    def load_model(input_path, output_path):
        subprocess.run(['nougat', input_path, '-o', output_path])

    
    if extract_text:
        with st.spinner('Extracting text...'):
            load_model(input_path, output_path)

        with open(mmd_path, 'r') as f:
            mmd = f.read()
            # move mmd to the session state
            st.session_state["mmd"] = mmd

    try:
        st.write(st.session_state["mmd"])
        
        with st.sidebar:
            st.success('Text extracted successfully!')
            st.markdown('---')
            st.title('Download file')
            download_output = st.download_button(label='Download', 
                                                data=st.session_state["mmd"], 
                                                file_name=output_file.replace('.mmd', '.md'),
                                                mime='text/markdown')
    
    except:
        pass


                
