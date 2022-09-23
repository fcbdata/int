import streamlit as st
import pandas as pd
import altair as alt

# app page config
st.set_page_config(page_icon='⚽', page_title='Comparador Interés Partidos')
st.title('📈 Comparador Interés Partidos')
st.markdown("""
***Data source:*** [Adobe Analytics](https://www3.an.adobe.com/x/3_j78uz)
""")
st.markdown("")

# get data and define dataframe
#@st.cache
def get_data():
    path = r'int.csv'
    return pd.read_csv(path)

df = get_data()

# app sidebar
st.sidebar.header('📖 Definición de Interés')
st.sidebar.markdown(
    """
    El **Interés** por partido es una métrica proxy que representa el nivel de demanda de entradas 
    basic para un partido en concreto. Se mide por el número de clics en el botón 
    de 'Entradas' regulares en la web oficial del FC Barcelona.
    """
)

from PIL import Image
image = Image.open('int.png')

st.sidebar.image(image, use_column_width='auto')
st.markdown("")
st.sidebar.subheader('⚠️ Consideraciones')
st.sidebar.markdown(
    """
    - El número de clics en botón de entradas basic, no entradas VIP
    - Sin importar en qué apartado de la web se encuentre el botón
    - No discrimina por usuario único, cada clic cuenta suma 1
    """
)

# app main functionalities
options = df['id'].unique().tolist()
selected_options = st.multiselect('Seleccionar partidos a comparar:',options,
                   default=("22/23 · Gamper · Pumas", "18/19 · Gamper · Boca Juniors"))

st.markdown("")

filtered_df = df[df['id'].isin(selected_options)]

# INTERÉS ACUMULADO
# create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['antelacion'], empty='none')

# the basic line
line = alt.Chart(filtered_df).mark_line(interpolate='basis').encode(
    x='antelacion:Q',
    y='int_acum:Q',
    color='id:N'
)

# transparent selectors across the chart – this is what tells the x-value of the cursor
selectors = alt.Chart(filtered_df).mark_point().encode(
    x='antelacion:Q',
    opacity=alt.value(0)
).add_selection(
    nearest
)

# draw points on the line and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# draw text labels near the points and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'int_acum:Q', alt.value(' '))
)

# draw a rule at the location of the selection
rules = alt.Chart(filtered_df).mark_rule(color='gray').encode(
    x='antelacion:Q',
).transform_filter(
    nearest
)

# put the five layers into a chart and bind the data
d = alt.layer(
    line, selectors, points, rules, text
).properties(
    width=900, height=300
)

st.subheader('**Interés · Acumulado por Antelación**')
st.altair_chart(d, use_container_width=False)

# INTERÉS NO-ACUMULADO
# create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['antelacion'], empty='none')

# the basic line
line = alt.Chart(filtered_df).mark_line(interpolate='basis').encode(
    x='antelacion:Q',
    y='interes_web:Q',
    color='id:N'
)

# transparent selectors across the chart – this is what tells the x-value of the cursor
selectors = alt.Chart(filtered_df).mark_point().encode(
    x='antelacion:Q',
    opacity=alt.value(0)
).add_selection(
    nearest
)

# draw points on the line and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# draw text labels near the points and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'interes_web:Q', alt.value(' '))
)

# draw a rule at the location of the selection
rules = alt.Chart(filtered_df).mark_rule(color='gray').encode(
    x='antelacion:Q',
).transform_filter(
    nearest
)

# put the five layers into a chart and bind the data
c = alt.layer(
    line, selectors, points, rules, text
).properties(
    width=900, height=300
)

st.subheader('**Interés · Evolución por Antelación**')
st.altair_chart(c, use_container_width=False)

# EVOLUCIÓN CR
# create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['cr'], empty='none')

# the basic line
line = alt.Chart(filtered_df).mark_line(interpolate='basis').encode(
    x='antelacion:Q',
    y='cr:Q',
    color='id:N'
)

# transparent selectors across the chart – this is what tells the x-value of the cursor
selectors = alt.Chart(filtered_df).mark_point().encode(
    x='antelacion:Q',
    opacity=alt.value(0)
).add_selection(
    nearest
)

# draw points on the line and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# draw text labels near the points and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'cr:Q', alt.value(' '))
)

# draw a rule at the location of the selection
rules = alt.Chart(filtered_df).mark_rule(color='gray').encode(
    x='antelacion:Q',
).transform_filter(
    nearest
)

# put the five layers into a chart and bind the data
e = alt.layer(
    line, selectors, points, rules, text
).properties(
    width=900, height=300
)

st.subheader('**CR · Evolución por Antelación**')
st.altair_chart(e, use_container_width=False)


# TABLA
st.markdown("")
st.subheader('**Tabla de Datos**')
st.table(filtered_df)

