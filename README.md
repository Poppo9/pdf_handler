# 📄 PDF Handler

**PDF Handler** is a simple and intuitive web application built with **Streamlit** that allows users to **split** and **merge PDF files** directly in the browser. It provides visual previews of documents to help you select the right pages with ease.

---

## 🚀 Features

### 🔍 Preview PDF

* Displays thumbnails of PDF pages.
* Automatically shows previews before and after splitting or merging.

### ✂️ Split PDF

* Upload a PDF file and extract:

  * A range of pages.
  * Specific individual pages.
* Download the new PDF instantly after splitting.

### 🔗 Merge PDFs

* Upload multiple PDF files.
* Combine them into a single document.
* Download the merged file directly.

---

## 🛠️ Tech Stack

* **Streamlit** – Web interface
* **PyMuPDF (fitz)** – PDF page preview rendering
* **PyPDF2** – Splitting and merging PDF files
* **Base64 & BytesIO** – File handling and in-memory processing

---

## 🖥️ How to Run Locally

1. **Clone the repository**

   ```bash
   git clone https://github.com/Poppo9/pdf_handler.git
   cd pdf_handler
   ```

2. **Create a virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

---

## 📌 Notes

* The app runs entirely in the browser—no files are saved to the server.
* Preview rendering is limited to the first few pages for performance.

---

## 👤 Author

**Created by:** Poppo9
**Built with ❤️ using Streamlit and Python**
