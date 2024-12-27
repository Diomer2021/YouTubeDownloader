
import streamlit as st
import yt_dlp

def download_video(url, format_type="video"):
    """
    Descarga un video o audio de YouTube usando yt-dlp.
    Args:
        url (str): URL del video de YouTube.
        format_type (str): "video" para video o "audio" para solo audio.
    Returns:
        str: Ruta del archivo descargado o un mensaje de error.
    """
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Carpeta de salida
    }
    
    if format_type == "audio":
        ydl_opts.update({
            'format': 'bestaudio/best',  # Solo audio
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts.update({'format': 'bestvideo+bestaudio/best'})  # Mejor calidad de video
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
            return file_path, "Descarga exitosa."
    except Exception as e:
        return None, f"Error: {str(e)}"

# Interfaz de Streamlit
st.title("Descargador de Videos de YouTube con yt-dlp")
st.write("Introduce el enlace de un video de YouTube para descargarlo.")

# Entrada de URL
url = st.text_input("URL del video de YouTube:")

# Selección de formato
format_type = st.radio(
    "Selecciona el formato:",
    ("Video", "Audio (MP3)")
)

# Botón para iniciar la descarga
if st.button("Descargar"):
    if url:
        st.write("Procesando la descarga...")
        format_option = "audio" if format_type == "Audio (MP3)" else "video"
        file_path, message = download_video(url, format_option)
        
        if file_path:
            st.success(message)
            with open(file_path, "rb") as file:
                st.download_button(
                    label="Haz clic aquí para descargar el archivo",
                    data=file,
                    file_name=file_path.split("/")[-1],
                    mime="audio/mpeg" if format_option == "audio" else "video/mp4"
                )
        else:
            st.error(message)
    else:
        st.error("Por favor, introduce una URL válida.")
    
# Pie de página
st.markdown("---")  # Línea separadora
st.markdown(
    """
    **Realizado por:** [Diomer Algendonis](https://www.linkedin.com/in/diomer-algendonis-reyes-44395067/)  
    **Contacto:** [diomer.algendonis@gmail.com](diomer.algendonis@gmail.com)  
    **Repositorio GitHub:** [Ver código fuente](https://github.com/Diomer2021/Motor_Yield)
    """
)