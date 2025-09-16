
import streamlit as st
import psycopg2, os, boto3

# ============================
# 🔎 Configuración DB (Railway)
# ============================
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:rByEQidKiDRkpkRNEsbUbhgCjbcfJJuJ@yamanote.proxy.rlwy.net:15387/railway")

def get_connection():
    try:
        conn = psycopg2.connect(DB_URL)
        return conn
    except Exception as e:
        raise RuntimeError(f"❌ Error al conectar a la DB: {e}")

# ============================
# ☁️ Configuración Backblaze B2
# ============================
B2_KEY_ID = os.getenv("B2_KEY_ID")
B2_APP_KEY = os.getenv("B2_APP_KEY")
B2_BUCKET = os.getenv("B2_BUCKET")
B2_ENDPOINT = "https://s3.us-west-002.backblazeb2.com"

s3 = boto3.client(
    "s3",
    endpoint_url=B2_ENDPOINT,
    aws_access_key_id=B2_KEY_ID,
    aws_secret_access_key=B2_APP_KEY
)

# ============================
# 🚀 Interfaz Streamlit
# ============================
st.title("🚀 Mi App con Streamlit + PostgreSQL + Backblaze B2")

# --- Guardar texto en PostgreSQL ---
st.header("Guardar texto en la base de datos")
texto = st.text_input("Escribe algo para guardar en PostgreSQL:")
if st.button("Guardar en DB"):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS datos (id SERIAL PRIMARY KEY, info TEXT);")
        cur.execute("INSERT INTO datos (info) VALUES (%s)", (texto,))
        conn.commit()
        cur.close()
        conn.close()
        st.success("Texto guardado en la base de datos ✅")
    except Exception as e:
        st.error(f"No se pudo guardar: {e}")

# --- Subir archivos a Backblaze B2 ---
st.header("Subir archivo a Backblaze B2")
archivo = st.file_uploader("Selecciona un archivo")
if archivo is not None:
    if st.button("Subir a Backblaze"):
        try:
            s3.upload_fileobj(archivo, B2_BUCKET, archivo.name)
            st.success(f"Archivo '{archivo.name}' subido correctamente 🚀")
        except Exception as e:
            st.error(f"Error al subir archivo: {e}")

