import streamlit as st

# Título de la aplicación
st.title("Generador de Modelos Parametrizados para Braquiterapia en Cáncer de Cérvix")

# Descripción de la aplicación
st.markdown("""
Esta herramienta permite crear un modelo parametrizado para planificar tratamientos de braquiterapia en cáncer de cuello uterino. 
Incluye la configuración de una guía de inserción hueca y las agujas ubicadas en su interior.
""")

# Parámetros del tumor
st.markdown("### Configuración del Tumor")
tumor_width = st.number_input("Ancho del tumor (mm):", min_value=10.0, max_value=200.0, value=50.0, step=1.0)
tumor_height = st.number_input("Altura del tumor (mm):", min_value=10.0, max_value=200.0, value=50.0, step=1.0)
tumor_depth = st.number_input("Profundidad del tumor (mm):", min_value=10.0, max_value=200.0, value=50.0, step=1.0)

# Configuración de la guía
st.markdown("### Configuración de la Guía de Inserción")
guide_outer_diameter = st.number_input("Diámetro exterior de la guía (mm):", min_value=5.0, max_value=30.0, value=10.0, step=0.1)
guide_inner_diameter = st.number_input("Diámetro interior de la guía (mm):", min_value=1.0, max_value=guide_outer_diameter, value=5.0, step=0.1)
guide_length = st.number_input("Largo de la guía (mm):", min_value=10.0, max_value=200.0, value=50.0, step=1.0)

# Configuración de las agujas
st.markdown("### Configuración de las Agujas")
num_agujas = st.slider("Número de agujas dentro de la guía:", min_value=1, max_value=10, value=3)
agujas = []

for i in range(num_agujas):
    st.markdown(f"**Aguja {i + 1}:**")
    needle_diameter = st.number_input(f"Diámetro de la aguja {i + 1} (mm):", min_value=0.5, max_value=guide_inner_diameter, value=1.0, step=0.1, key=f"needle_d_{i}")
    x_pos = st.number_input(f"Coordenada X (mm) de la aguja {i + 1}:", value=0.0, step=0.1, key=f"x_{i}")
    y_pos = st.number_input(f"Coordenada Y (mm) de la aguja {i + 1}:", value=0.0, step=0.1, key=f"y_{i}")
    z_pos = st.number_input(f"Coordenada Z (mm) de la aguja {i + 1}:", value=0.0, step=0.1, key=f"z_{i}")
    agujas.append((needle_diameter, x_pos, y_pos, z_pos))

# Generar código Python para FreeCAD
if st.button("Generar Código Python"):
    code_lines = [
        "import FreeCAD, Part",
        "doc = FreeCAD.newDocument('Braquiterapia')",
        f"tumor = Part.makeBox({tumor_width}, {tumor_depth}, {tumor_height})",
        "tumor.translate(FreeCAD.Vector(0, 0, 0))",
        "doc.addObject('Part::Feature', 'Tumor').Shape = tumor",
        f"guia_exterior = Part.makeCylinder({guide_outer_diameter / 2}, {guide_length})",
        f"guia_interior = Part.makeCylinder({guide_inner_diameter / 2}, {guide_length})",
        "guia = guia_exterior.cut(guia_interior)",
        "doc.addObject('Part::Feature', 'Guia').Shape = guia"
    ]

    for i, (needle_d, x, y, z) in enumerate(agujas, start=1):
        code_lines.extend([
            f"aguja_{i} = Part.makeCylinder({needle_d / 2}, {guide_length})",
            f"aguja_{i}.translate(FreeCAD.Vector({x}, {y}, {z}))",
            f"doc.addObject('Part::Feature', 'Aguja_{i}').Shape = aguja_{i}"
        ])

    code_lines.append("FreeCAD.Gui.ActiveDocument.ActiveView.setAxisCross(True)")

    # Mostrar el código generado
    st.markdown("### Código Generado para FreeCAD:")
    st.code("\n".join(code_lines), language="python")

    # Opción para descargar el código como archivo
    st.download_button(
        label="Descargar Código Python",
        data="\n".join(code_lines),
        file_name="braquiterapia_freecad.py",
        mime="text/x-python"
    )


