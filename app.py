import base64
import tempfile
from pathlib import Path

import streamlit as st

def main():
    selected_box = st.sidebar.selectbox(
        'Choose one of the following',
        ("PDF表変換", 'FaceMesh', 'Image Processing', 'Graph', 'Map')
    )
    if selected_box == 'PDF閲覧':
        pdf_show()
    if selected_box == 'PDF表変換':
        pdf_convert()

def pdf_show():
    st.title("PDF閲覧ツール")
    uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            st.markdown("## Original PDF file")
            fp = Path(tmp_file.name)
            fp.write_bytes(uploaded_file.getvalue())
            st.write(write_pdf(tmp_file.name))

def write_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

def pdf_convert():
    pass

if __name__ == '__main__':
    main()