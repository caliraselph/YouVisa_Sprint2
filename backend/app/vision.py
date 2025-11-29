def validar_documento(nombre_archivo):
    ext = nombre_archivo.split('.')[-1].lower()
    # Simula OpenCV: si termina en jpg/png/pdf => válido
    if ext in ("pdf", "jpg", "jpeg", "png"):
        return True, "Formato reconocido"
    else:
        return False, "Formato no permitido"
