import streamlit as st
import psycopg2, os, boto3

# Configuración DB (Railway provee DATABASE_URL automáticamente)
DB_URL = os.getenv("DATABASE_URL")

# Configuración Backblaze B2
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

st.title("🚀 Mi App con Streamlit + PostgreSQL + Backblaze B2")

# --- Guardar texto en PostgreSQL ---
st.header("Guardar texto en la base de datos")
texto = st.text_input("Escribe algo para guardar en PostgreSQL:")
if st.button("Guardar en DB"):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO datos (info) VALUES (%s)", (texto,))
    conn.commit()
    cur.close()
    conn.close()
    st.success("Texto guardado en la base de datos ✅")

# --- Subir archivos a Backblaze B2 ---
st.header("Subir archivo a Backblaze B2")
archivo = st.file_uploader("Selecciona un archivo")
if archivo is not None:
    if st.button("Subir a Backblaze"):
        s3.upload_fileobj(archivo, B2_BUCKET, archivo.name)
        st.success(f"Archivo '{archivo.name}' subido correctamente 🚀")
