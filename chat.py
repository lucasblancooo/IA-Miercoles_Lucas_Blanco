import streamlit as st
from groq import Groq



st.set_page_config(page_title="Lucas Blanco", page_icon="👍")
st.title("Soy Lucas Blanco y esta es mi primera aplicacion")

nombre = st.text_input("Cual es tu nombre?")
if st.button("Saludar!"):
    st.write(f"Hola {nombre}! Bienvenido a talento tech")

MODELOS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile', 'llama3-8b']

def configurar_pagina():
    st.title("Mi Chat Lucas Blanco")
    st.sidebar.title("Configuracion de la IA")

    elegirModelo = st.sidebar.selectbox(
        "Elegi un modelo",
        options = MODELOS,
        index = 0
    )

    return elegirModelo

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
    model=modelo,
    messages=[{"role": "user", "content": mensajeDeEntrada}],
    stream=True
)

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

#Funciones agregadas en CLASE 8
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border= True)
    with contenedorDelChat: mostrar_historial()

def generar_respuestas(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():

    clienteUsuario = crear_usuario_groq()
    modelo = configurar_pagina()
    inicializar_estado()
    area_chat()
    # Tomamos el mensaje del usuario por el input.
    mensaje = st.chat_input("Escribí tu mensaje:")
    # Verificamos que el mensaje no esté vacío antes de configurar el modelo


    #-----Dentro del -------------------------------------
    if mensaje:
        actualizar_historial("user", mensaje, "😁")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
                with st.chat_message("assistant"):
                    respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                    actualizar_historial("assistant", respuesta_completa, "🤖")
                    st.rerun()

if __name__ == "__main__":

    main()
