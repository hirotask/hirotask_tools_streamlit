import base64
import tempfile
from pathlib import Path
import streamlit as st
import tabula

def main():
    selected_box = st.sidebar.selectbox(
        'Choose one of the following',
        ("PDF閲覧", 'PDF表変換')
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
    st.title("PDF表変換ツール")
    st.header("PDFにある表をCSVファイルに変換します")
    uploaded_file = st.file_uploader("Choose your .odf file", type="pdf")

    if uploaded_file is not None:
        file_name = uploaded_file.name
        dfs = tabula.read_pdf(uploaded_file, stream=True, pages='all')
        csv_files = []
        for idx, df in enumerate(dfs):
            csv_file_name = file_name[:-4] + str(idx) + ".csv"
            csv_file = df.to_csv().encode('utf-8')
            csv_files.append((csv_file_name, csv_file))
            st.table(df)

        for csv_file_name, csv in csv_files:
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=csv_file_name,
                mime='text/csv',
            )


if __name__ == '__main__':
    main()