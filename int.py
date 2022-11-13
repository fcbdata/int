import streamlit as st
import pandas as pd
import altair as alt

# app page config
st.set_page_config(page_icon='⚽', page_title='Comparador de Interés')
st.title('📈 Comparador de Interés')
st.info('Los datos se actualizan cada día laborable a las 17:00h CET', icon="ℹ️")

# get data and define dataframe
#@st.cache
def get_data():
    path = r'int.json'
    return pd.read_json(path)

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
nearest1 = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['antelacion'], empty='none')

# the basic line
line1 = alt.Chart(filtered_df).mark_line(interpolate='basis').encode(
    x='antelacion:Q',
    y='interes_acumulado:Q',
    color='id:N'
)

# transparent selectors across the chart – this is what tells the x-value of the cursor
selectors1 = alt.Chart(filtered_df).mark_point().encode(
    x='antelacion:Q',
    opacity=alt.value(0)
).add_selection(
    nearest1
)

# draw points on the line and highlight based on selection
points1 = line1.mark_point().encode(
    opacity=alt.condition(nearest1, alt.value(1), alt.value(0))
)

# draw text labels near the points and highlight based on selection
text1 = line1.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest1, 'interes_acumulado:Q', alt.value(' '))
)

# draw a rule at the location of the selection
rules1 = alt.Chart(filtered_df).mark_rule(color='gray').encode(
    x='antelacion:Q',
).transform_filter(
    nearest1
)

# put the five layers into a chart and bind the data
d = alt.layer(
    line1, selectors1, points1, rules1, text1
).properties(
    width=900, height=300
)

st.subheader('**Interés Acumulado por Antelación**')
st.altair_chart(d, use_container_width=False)

# INTERÉS NO-ACUMULADO
# create a selection that chooses the nearest point & selects based on x-value
nearest2 = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['antelacion'], empty='none')

# the basic line
line2 = alt.Chart(filtered_df).mark_line(interpolate='basis').encode(
    x='antelacion:Q',
    y='interes:Q',
    color='id:N'
)

# transparent selectors across the chart – this is what tells the x-value of the cursor
selectors2 = alt.Chart(filtered_df).mark_point().encode(
    x='antelacion:Q',
    opacity=alt.value(0)
).add_selection(
    nearest2
)

# draw points on the line and highlight based on selection
points2 = line2.mark_point().encode(
    opacity=alt.condition(nearest2, alt.value(1), alt.value(0))
)

# draw text labels near the points and highlight based on selection
text2 = line2.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest2, 'interes:Q', alt.value(' '))
)

# draw a rule at the location of the selection
rules2 = alt.Chart(filtered_df).mark_rule(color='gray').encode(
    x='antelacion:Q',
).transform_filter(
    nearest2
)

# put the five layers into a chart and bind the data
c = alt.layer(
    line2, selectors2, points2, rules2, text2
).properties(
    width=900, height=300
)

st.subheader('**Interés por Antelación**')
st.altair_chart(c, use_container_width=False)

# EVOLUCIÓN %CR
# create a selection that chooses the nearest point & selects based on x-value
nearest3 = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['antelacion'], empty='none')

# the basic line
line3 = alt.Chart(filtered_df).mark_line(interpolate='basis').encode(
    x='antelacion:Q',
    y='%cr:Q',
    color='id:N'
)

# transparent selectors across the chart – this is what tells the x-value of the cursor
selectors3 = alt.Chart(filtered_df).mark_point().encode(
    x='antelacion:Q',
    opacity=alt.value(0)
).add_selection(
    nearest3
)

# draw points on the line and highlight based on selection
points3 = line3.mark_point().encode(
    opacity=alt.condition(nearest3, alt.value(1), alt.value(0))
)

# draw text labels near the points and highlight based on selection
text3 = line3.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest3, '%cr:Q', alt.value(' '))
)

# draw a rule at the location of the selection
rules3 = alt.Chart(filtered_df).mark_rule(color='gray').encode(
    x='antelacion:Q',
).transform_filter(
    nearest3
)

# put the five layers into a chart and bind the data
e = alt.layer(
    line3, selectors3, points3, rules3, text3
).properties(
    width=900, height=300
)

st.subheader('**%CR por Antelación**')
st.altair_chart(e, use_container_width=False)


# TABLA
st.markdown("")
st.subheader('**Tabla de Datos**')
st.dataframe(filtered_df)

