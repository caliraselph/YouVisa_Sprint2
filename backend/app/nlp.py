def classificar_documento(nombre_archivo):
    if "passaporte" in nombre_archivo.lower():
        return "Passaporte"
    elif "formulario" in nombre_archivo.lower():
        return "Formulário"
    return "Outro"
