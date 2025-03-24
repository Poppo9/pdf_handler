import streamlit as st
import tempfile
import os
from PyPDF2 import PdfReader, PdfWriter
import base64
from io import BytesIO
import fitz  # PyMuPDF

st.set_page_config(page_title="PDF Manager", layout="wide")

# Funzione per visualizzare l'anteprima del PDF
def visualizza_anteprima(file, pagine=None):
    try:
        # Leggi il PDF
        pdf_documento = fitz.open(stream=file.read(), filetype="pdf")
        file.seek(0)  # Reimposta il puntatore del file
        
        if pagine is None:
            # Se pagine non è specificato, visualizza tutte le pagine
            pagine = range(len(pdf_documento))
        elif isinstance(pagine, int):
            # Se è specificata una singola pagina
            pagine = [pagine]
        
        immagini = []
        for num_pagina in pagine:
            if 0 <= num_pagina < len(pdf_documento):
                pagina = pdf_documento.load_page(num_pagina)
                pix = pagina.get_pixmap(matrix=fitz.Matrix(0.5, 0.5))
                img_data = pix.tobytes("png")
                
                # Codifica l'immagine in base64 per visualizzarla in HTML
                img_b64 = base64.b64encode(img_data).decode()
                img_html = f'<img src="data:image/png;base64,{img_b64}" style="margin: 5px; border: 1px solid #ddd; border-radius: 5px;">'
                immagini.append(img_html)
        
        # Visualizza le immagini in una griglia
        colonne = 3
        righe = (len(immagini) + colonne - 1) // colonne
        
        for i in range(righe):
            cols = st.columns(colonne)
            for j in range(colonne):
                idx = i * colonne + j
                if idx < len(immagini):
                    with cols[j]:
                        st.markdown(immagini[idx], unsafe_allow_html=True)
                        st.caption(f"Pagina {pagine[idx] + 1}")
                        
        return len(pdf_documento)
    except Exception as e:
        st.error(f"Errore durante la visualizzazione dell'anteprima: {e}")
        return 0

# Funzione per dividere il PDF
def dividi_pdf(file_pdf, pagine_da_estrarre):
    try:
        # Leggi il PDF originale
        pdf = PdfReader(file_pdf)
        pdf_writer = PdfWriter()
        
        # Aggiungi le pagine selezionate
        for num_pagina in pagine_da_estrarre:
            if 0 <= num_pagina < len(pdf.pages):
                pdf_writer.add_page(pdf.pages[num_pagina])
        
        # Crea il nuovo PDF in memoria
        output_stream = BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        
        return output_stream
    except Exception as e:
        st.error(f"Errore durante la divisione del PDF: {e}")
        return None

# Funzione per unire i PDF
def unisci_pdf(files_pdf):
    try:
        pdf_writer = PdfWriter()
        
        # Aggiungi tutte le pagine di ogni PDF
        for file in files_pdf:
            pdf = PdfReader(file)
            for pagina in pdf.pages:
                pdf_writer.add_page(pagina)
        
        # Crea il nuovo PDF in memoria
        output_stream = BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        
        return output_stream
    except Exception as e:
        st.error(f"Errore durante l'unione dei PDF: {e}")
        return None

# Interfaccia utente
st.title("📄 Gestore PDF")
st.markdown("### Strumento semplice per dividere e unire file PDF")

tab1, tab2 = st.tabs(["📂 Dividi PDF", "🔗 Unisci PDF"])

# Tab per dividere PDF
with tab1:
    st.header("Dividi PDF")
    uploaded_file = st.file_uploader("Carica un file PDF da dividere", type=["pdf"], key="split_uploader")
    
    if uploaded_file is not None:
        st.success("File caricato con successo!")
        
        # Visualizza l'anteprima
        st.subheader("Anteprima del documento")
        num_pagine = visualizza_anteprima(uploaded_file)
        uploaded_file.seek(0)  # Reimposta il puntatore del file
        
        # Selezione delle pagine
        st.subheader("Seleziona le pagine da estrarre")
        
        # Opzioni per la selezione delle pagine
        opzione_selezione = st.radio(
            "Come vuoi selezionare le pagine?",
            ["Intervallo di pagine", "Pagine specifiche"]
        )
        
        pagine_selezionate = []
        
        if opzione_selezione == "Intervallo di pagine":
            intervallo = st.slider(
                "Seleziona l'intervallo di pagine",
                1, max(1, num_pagine), (1, min(5, num_pagine))
            )
            pagine_selezionate = list(range(intervallo[0]-1, intervallo[1]))
        else:
            # Crea checkbox per ogni pagina
            num_colonne = 5
            colonne = st.columns(num_colonne)
            
            for i in range(num_pagine):
                with colonne[i % num_colonne]:
                    if st.checkbox(f"Pagina {i+1}", key=f"pagina_{i}"):
                        pagine_selezionate.append(i)
        
        # Visualizza il numero di pagine selezionate
        st.write(f"Hai selezionato {len(pagine_selezionate)} pagine.")
        
        # Pulsante per dividere
        if st.button("Dividi PDF", key="split_button"):
            if len(pagine_selezionate) > 0:
                with st.spinner("Divisione in corso..."):
                    pdf_diviso = dividi_pdf(uploaded_file, pagine_selezionate)
                    
                    if pdf_diviso:
                        # Crea un link per scaricare il PDF diviso
                        st.success("PDF diviso con successo!")
                        st.download_button(
                            label="📥 Scarica PDF diviso",
                            data=pdf_diviso,
                            file_name="pdf_diviso.pdf",
                            mime="application/pdf",
                            key="download_split"
                        )
                        
                        # Visualizza l'anteprima del PDF diviso
                        st.subheader("Anteprima del PDF diviso")
                        pdf_diviso.seek(0)
                        visualizza_anteprima(pdf_diviso)
            else:
                st.warning("Seleziona almeno una pagina prima di dividere il PDF.")

# Tab per unire PDF
with tab2:
    st.header("Unisci PDF")
    uploaded_files = st.file_uploader("Carica i file PDF da unire", type=["pdf"], accept_multiple_files=True, key="merge_uploader")
    
    if uploaded_files:
        st.success(f"Caricati {len(uploaded_files)} file PDF!")
        
        # Mostra l'anteprima di ciascun PDF
        for i, file in enumerate(uploaded_files):
            with st.expander(f"Anteprima del file {i+1}: {file.name}"):
                visualizza_anteprima(file, [0])  # Mostra solo la prima pagina
                file.seek(0)  # Reimposta il puntatore del file
        
        # Pulsante per unire
        if st.button("Unisci PDF", key="merge_button"):
            with st.spinner("Unione in corso..."):
                pdf_unito = unisci_pdf(uploaded_files)
                
                if pdf_unito:
                    # Crea un link per scaricare il PDF unito
                    st.success("PDF uniti con successo!")
                    st.download_button(
                        label="📥 Scarica PDF unito",
                        data=pdf_unito,
                        file_name="pdf_unito.pdf",
                        mime="application/pdf",
                        key="download_merge"
                    )
                    
                    # Visualizza l'anteprima del PDF unito
                    st.subheader("Anteprima del PDF unito")
                    pdf_unito.seek(0)
                    visualizza_anteprima(pdf_unito, range(min(5, len(uploaded_files))))  # Mostra le prime 5 pagine

# Sidebar con informazioni
with st.sidebar:
    st.title("📋 Informazioni")
    st.info("""
    **PDF Manager**
    
    Questa semplice applicazione ti permette di:
    - **Dividere** un PDF estraendo pagine specifiche
    - **Unire** più file PDF in un unico documento
    
    Ogni operazione include un'anteprima per aiutarti a visualizzare il contenuto.
    """)
    
    st.markdown("---")
    st.caption("Creato con Streamlit e PyPDF2")
