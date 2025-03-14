import streamlit as st
import sqlite3
import os

# Inizializza lo stato della sessione
for key in [
    "maggiorenne", "importanza_ambiente", "val_passata", "val_pasta", "val_pane", 
    "val_parmigiano", "val_olio", "val_tonno", "val_caffe", "selected_brand",
    "selected_image", "frequenza_acquisto"
]:
    if key not in st.session_state:
        st.session_state[key] = None

if 'pagina' not in st.session_state:
    st.session_state.pagina = 1

def next_page():
    st.session_state.pagina += 1

def prev_page():
    st.session_state.pagina -= 1

# Funzione per salvare i dati nel database
def salva_risposte():
    with sqlite3.connect("risposte.db") as conn:
        cursor = conn.cursor()
        
        # Ricreazione della tabella con le colonne corrette
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS risposte (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                maggiorenne TEXT,
                importanza_ambiente INTEGER,
                passata INTEGER,
                pasta INTEGER,
                pane INTEGER,
                parmigiano INTEGER,
                olio INTEGER,
                tonno INTEGER,
                caffe INTEGER,
                brand TEXT,
                selected_image TEXT,
                frequenza_acquisto TEXT
            )
        ''')
        
        # Inserimento dei dati nel database
        cursor.execute('''
            INSERT INTO risposte (maggiorenne, importanza_ambiente, passata, pasta, pane, parmigiano,
                                  olio, tonno, caffe, brand, selected_image, frequenza_acquisto)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (st.session_state.maggiorenne,
              st.session_state.importanza_ambiente,
              st.session_state.val_passata,
              st.session_state.val_pasta,
              st.session_state.val_pane,
              st.session_state.val_parmigiano,
              st.session_state.val_olio,
              st.session_state.val_tonno,
              st.session_state.val_caffe,
              st.session_state.selected_brand,
              st.session_state.selected_image,
              st.session_state.frequenza_acquisto))
        
        conn.commit()

# Pagina 1: Maggiorenne?
if st.session_state.pagina == 1:
    st.title("🌿 Questionario sull Sostenibilità dei prodotti alimentari (1/5)")
    maggiorenne = st.radio("Sei maggiorenne?", ["Sì", "No"])

    if maggiorenne == "No":
        st.warning("Il questionario è riservato ai maggiorenni.")
    else:
        if st.button("Avanti"):
            st.session_state.maggiorenne = maggiorenne
            next_page()

# Pagina 2: Importanza ambiente
elif st.session_state.pagina == 2:
    st.title("🌿 Importanza Ambiente (2/5)")
    importanza_ambiente = st.slider("Quanto è importante che i prodotti che acquisti siano rispettosi dell'ambiente?", 1, 5)
    if st.button("Avanti"):
        st.session_state.importanza_ambiente = importanza_ambiente
        next_page()
    if st.button("Indietro"):
        prev_page()
   
# Pagina 3: Valutazioni prodotti
elif st.session_state.pagina == 3:
    st.title("🌿 Valuta i prodotti (3/5) - Quanto pensi che questi prodotti impattano sull'ambiente? 1 = per ninete impattante, 7 = estremamente impattante")
    passata = st.slider("Passata di pomodoro", 1, 7, key="passata")
    pasta = st.slider("Pasta", 1, 7, key="pasta")
    pane = st.slider("Pane in cassetta", 1, 7, key="pane")
    parmigiano = st.slider("Parmigiano", 1, 7, key="parmigiano")
    olio = st.slider("Olio d'oliva", 1, 7, key="olio")
    tonno = st.slider("Tonno", 1, 7, key="tonno")
    caffe = st.slider("Caffè", 1, 7, key="caffe")

    if st.button("Indietro"):
        prev_page()
    if st.button("Avanti"):
        st.session_state.val_passata = passata
        st.session_state.val_pasta = pasta
        st.session_state.val_pane = pane
        st.session_state.val_parmigiano = parmigiano
        st.session_state.val_olio = olio
        st.session_state.val_tonno = tonno
        st.session_state.val_caffe = caffe
        next_page()


#
elif st.session_state.pagina == 4:
    st.title("🌿 Ti chiederemo ora di esprimere la tua preferenza per le categorie di prodotto precedentemente mostrate")
    if st.button("Avanti"):
        next_page()

# Pagina 4: Scelta del Brand e immagini affiancate
elif st.session_state.pagina == 5:
    st.title("🌿 Scelta del Brand (4/5)")
    
    # Dizionario con i brand e le relative immagini
    brands = {
        "": ["", ""],  # Opzione vuota iniziale
        "Coop": ["coop_pack1.jpeg", "coop_pack2.jpeg"],
        "DeCecco": ["dececco_pack1.png", "dececco_pack2.png"],
        "Mutti": ["mutti_pack1.png", "mutti_pack2.png"],
        "Petti": ["petti_pack1.png", "petti_pack2.png"],
        "Altro": ["altro_pack1.png", "altro_pack2.png"]
    }
    
    # Dropdown per selezionare il brand con opzione iniziale vuota
    selected_brand = st.selectbox("Quale brand di passata di pomodoro acquisti più frequentemente?", list(brands.keys()))
    
    if selected_brand:  # Mostra le immagini solo se un brand è stato selezionato
        st.session_state.selected_brand = selected_brand

        # Percorso delle immagini
        img1, img2 = brands[selected_brand]

        # Visualizza le immagini affiancate
        col1, col2 = st.columns(2)
        with col1:
            if os.path.exists(img1):
                st.image(img1, caption="Immagine 1", use_container_width=True)
            else:
                st.warning(f"Immagine {img1} non trovata!")
        with col2:
            if os.path.exists(img2):
                st.image(img2, caption="Immagine 2", use_container_width=True)
            else:
                st.warning(f"Immagine {img2} non trovata!")

        # Domanda su quale immagine è preferita
        st.write("**Quale prodotto pensi sia più rispettoso dell'ambiente?**")
        selected_image = st.radio("Seleziona un'opzione:", ["Immagine 1", "Immagine 2"])
        st.session_state.selected_image = selected_image

        if st.button("Avanti"):
            next_page()

    if st.button("Indietro"):
        prev_page()

# Pagina 5: Frequenza acquisto passata di pomodoro
elif st.session_state.pagina == 6:
    st.title("🌿 Frequenza Acquisto (5/5)")
    st.session_state.frequenza_acquisto = st.selectbox("Quanto frequentemente acquisti passata di pomodoro?", 
        ["Raramente", "Una volta al mese", "Più di una volta al mese", "Una volta a settimana", "Più di una volta alla settimana"])
    if st.button("Indietro"):
        prev_page()
    if st.button("Invia risposte definitive"):
        salva_risposte()
        st.success("Grazie per il tuo tempo! Le risposte sono state registrate correttamente.")
