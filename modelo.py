import streamlit as st

# Título de la aplicación
st.title("Generador de Modelos Parametrizados para Braquiterapia en Cáncer de Cérvix")

# Descripción de la aplicación
st.markdown("""
Esta herramienta permite crear un modelo parametrizado para planificar tratamientos de braquiterapia en cáncer de cuello uterino. 
Incluye la personalización de dimensiones del tumor, guías de inserción y agujas, generando un código Python compatible con FreeCAD.
""")

# Parámetros del tumor
st.markdown("### Configuración del Tumor")
tumor_width = st.number_input("Ancho del tumor (mm):", min_value=10.0, max_value=200.0, value=50.0, step=1.0)
tumor_height = st.number_input("Altura del tumor (mm):", min_value=10.0, max_value=200.0, value=50.0, step=1.0)
tumor_depth = st.number_input("Profundidad del tumor (mm):", min_value=10.0, max_value=200.0, value=50.0, step=1.0)

# Configuración de las guías
st.markdown("### Configuración de Guías de Inserción y Agujas")
num_guias = st.slider("Número de guías de inserción:", min_value=1, max_value=10, value=3)
guias = []

for i in range(num_guias):
    st.markdown(f"**Guía {i + 1}:**")
    outer_diameter = st.number_input(f"Diámetro exterior (mm) de la guía {i + 1}:", min_value=2.0, max_value=20.0, value=6.0, step=0.1, key=f"outer_{i}")
    inner_diameter = st.number_input(f"Diámetro interior (mm) de la guía {i + 1}:", min_value=1.0, max_value=outer_diameter, value=3.0, step=0.1, key=f"inner_{i}")
    guide_length = st.number_input(f"Largo (mm) de la guía {i + 1}:", min_value=10.0, max_value=200.0, value=50.0, step=1.0, key=f"length_{i}")
    x_pos = st.number_input(f"Coordenada X (mm) de la guía {i + 1}:", value=0.0, step=1.0, key=f"x_{i}")
    y_pos = st.number_input(f"Coordenada Y (mm) de la guía {i + 1}:", value=0.0, step=1.0, key=f"y_{i}")
    z_pos = st.number_input(f"Coordenada Z (mm) de la guía {i + 1}:", value=0.0, step=1.0, key=f"z_{i}")
    agujas_diameter = st.number_input(f"Diámetro de la aguja dentro de la guía {i + 1} (mm):", min_value=0.5, max_value=inner_diameter, value=1.0, step=0.1, key=f"needle_d_{i}")
    guias.append((outer_diameter, inner_diameter, guide_length, x_pos, y_pos, z_pos, agujas_diameter))

# Generar código Python para FreeCAD
if st.button("Generar Código Python"):
    code_lines = [
        "import FreeCAD, Part",
        "doc = FreeCAD.newDocument('Braquiterapia')",
        f"tumor = Part.makeBox({tumor_width}, {tumor_depth}, {tumor_height})",
        "tumor.translate(FreeCAD.Vector(0, 0, 0))",
        "doc.addObject('Part::Feature', 'Tumor').Shape = tumor"
    ]

    for i, (outer_d, inner_d, length, x, y, z, needle_d) in enumerate(guias, start=1):
        code_lines.extend([
            f"guia_exterior_{i} = Part.makeCylinder({outer_d / 2}, {length})",
            f"guia_interior_{i} = Part.makeCylinder({inner_d / 2}, {length})",
            f"guia_{i} = guia_exterior_{i}.cut(guia_interior_{i})",
            f"aguja_{i} = Part.makeCylinder({needle_d / 2}, {length})",
            f"aguja_{i}.translate(FreeCAD.Vector({x}, {y}, {z}))",
            f"guia_{i}.translate(FreeCAD.Vector({x}, {y}, {z}))",
            f"doc.addObject('Part::Feature', 'Guia_{i}').Shape = guia_{i}",
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

