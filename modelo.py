import streamlit as st

# Título de la aplicación
st.title("Generador de Modelos 3D para Cáncer de Cérvix")

# Ingreso de parámetros del tumor
st.header("Parámetros del Tumor")
diameter = st.number_input("Diámetro del tumor (mm)", min_value=1.0, step=0.1)
height = st.number_input("Altura del tumor (mm)", min_value=1.0, step=0.1)
location_x = st.number_input("Posición X (mm)", step=0.1)
location_y = st.number_input("Posición Y (mm)", step=0.1)
location_z = st.number_input("Posición Z (mm)", step=0.1)

# Botón para generar código
if st.button("Generar Código para FreeCAD"):
    freecad_code = f"""
import FreeCAD, Part
doc = FreeCAD.newDocument()
# Crear un cilindro representando el tumor
tumor = Part.makeCylinder({diameter / 2}, {height})
tumor.translate(FreeCAD.Vector({location_x}, {location_y}, {location_z}))
Part.show(tumor)
doc.recompute()
"""
    st.code(freecad_code, language="python")
    st.success("Código generado exitosamente. Copie y péguelo en FreeCAD para crear el modelo.")

# Información adicional
st.info("Este código es compatible con FreeCAD y puede ser utilizado para crear modelos personalizados basados en los parámetros ingresados.")
