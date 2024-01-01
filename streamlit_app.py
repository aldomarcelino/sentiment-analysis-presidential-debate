import streamlit as st
import pandas as pd
# import plost
from PIL import Image
import matplotlib.pyplot as plt
from transformers import pipeline
from googletrans import Translator



st.set_page_config(layout='wide')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

anies_result = pd.read_csv('anies_result.csv')


sent_pipeline = pipeline("sentiment-analysis")

st.markdown("<h1 style='text-align: center;'>Analisis Sentimen Debat Capres 2024</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Analisis dilakuan terhadap 3 calon Presiden Indonesia pada tahun 2024, dilakuan analisis sentimen pada komentar masyarakat terhadap ketiga kandidat setelah debat capres pertama silam yang diambil dari platform sosial media X(Twitter) dari tanggal 12 Desember 2023 - 13 Desember 2023</p>", unsafe_allow_html=True)

image_path = 'pictures-1.jpeg'
st.image(image_path, caption='Selasa, 12 Desember 2023')

# All Function

def translate_to_english(text, source_lang='id'):
    translator = Translator()
    translation = translator.translate(text, src=source_lang, dest='en')
    return translation.text

def check_output(output, result):
    if(output == 'POSITIVE'):
        text = 'Positif Tweet Terhadap Calon Nomor ' + str(result) if result else 'Positif Tweet'
        st.success(text)
    elif(output == 'NEGATIVE'):
        text = 'Negatif Tweet Terhadap Calon Nomor ' + str(result) if result else 'Negatif Tweet'
        st.error(text)
    else:
        text = 'Netral Tweet Terhadap Calon Nomor ' + str(result) if result else 'Netral Tweet'
        st.warning(text)

def check_side(sentence):
    candidate = {
        'anies_side': ['anies', 'baswedan', 'pks', 'muhaimin', 'imin', 'amin', 'nomor 1', 'cak', 'anis', 'nomor satu'],
        'prabowo_side': ['prabowo', 'subianto', 'gibran', 'rakabumi', 'gerindra', 'nomor 2', 'nomor dua'],
        'ganjar_side': ['ganjar', 'pranowo', 'mahduf', 'mahfud md', 'pdi', 'pdi perjuangan', 'nomor 3', 'mega', 'mega chan', 'nomor tiga'],
    }

    number = 0
    res = 0

    for key in candidate:
        number += 1
        is_include = any(keyword in sentence.lower() for keyword in candidate[key])
        if is_include:
            res = number
            break

    return res


col1, col2, col3 = st.columns([2,6,2])
result = 0

with col1:
    st.write(' ')

with col2:
    the_text = st.text_input("Input Komentar Baru: ")
    submit = st.button('Analysis')
    
    if the_text:
        result = check_side(the_text)
        translated_text = translate_to_english(the_text)
        if translated_text:
            temp = sent_pipeline(translated_text)
            if temp:
                check_output(temp[0]['label'], result)
                score_formatted = '{:.2f}'.format(temp[0]['score'] * 100)
                st.write('Score:', score_formatted, '%')

with col3:
    st.write(' ')



wrap1, wrap2, wrap3 = st.columns([2,6,2])

with wrap1:
    st.write(' ')

with wrap2:
    if(result):
        the_image = ""
        if(result == 1):
            the_image = "pks.png"
        elif(result == 2):
            the_image = "gerindra.png"
        elif(result == 3):
            the_image = "pdi.png"

        st.image(the_image,width=220)

with wrap3:
    st.write(' ')



st.markdown('### Summary')
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div style='background: rgb(247, 251, 251); box-shadow: 0px 5px 10px 0px #D3D3D3; border-radius: 20px; padding: 16px 20px;'><h3 style='margin: 0px; text-align: center;'>Anies Baswedan</h3><h5 style='margin: 0px;'>42K Mention</h5><p style='margin: 0px;'><strong>Narasi Positif:</strong></p><p style='margin: 0px;margin-bottom: 8px;'>Sosok yang aktif bicara soal gagasan, presentasi tanpa teks, bacapres paling sederhana.</p><p style='margin: 0px;'><strong>Narasi Negatif:</strong></p><p style='margin: 0px;'>Diangap mutar-mutar dan bertele-tele</p></div>", unsafe_allow_html=True)
with col2:
   st.markdown("<div style='background: rgb(247, 251, 251); box-shadow: 0px 5px 10px 0px #D3D3D3; border-radius: 20px; padding: 16px 20px;'><h3 style='margin: 0px; text-align: center;'>Prabowo Subianto</h3><h5 style='margin: 0px;'>45K Mention</h5><p style='margin: 0px;'><strong>Narasi Positif:</strong></p><p style='margin: 0px;margin-bottom: 8px;'>Terlihat jujur saat menjawab pertanyaan pertanyaan kandidat lain</p><p style='margin: 0px;'><strong>Narasi Negatif:</strong></p><p style='margin: 0px;'>Emosional, dan panik saat menjawab pertanyaan</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div style='background: rgb(247, 251, 251); box-shadow: 0px 5px 10px 0px #D3D3D3; border-radius: 20px; padding: 16px 20px;'><h3 style='margin: 0px; text-align: center;'>Ganjar Pranowo</h3><h5 style='margin: 0px;'>38K Mention</h5><p style='margin: 0px;'><strong>Narasi Positif:</strong></p><p style='margin: 0px;margin-bottom: 8px;'>Sosok paling solutif dan tegas dalam menjawab petanyaan-pertanyaan yang di lemparkan</p><p style='margin: 0px;'><strong>Narasi Negatif:</strong></p><p style='margin: 0px;'>Dicap blunder, sikap politik tidak jelas</p></div>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: left;margin-top: 12px'>Context of a discussion</h3>", unsafe_allow_html=True)

# Row A
a1, a2, a3 = st.columns(3)
with a1:
    a1.image(Image.open('anies_abstrack.png'))
with a2:
   a2.image(Image.open('prabowo_abstrack.png'))
with a3:
   a3.image(Image.open('ganjar_abstrack.png'))

# anies_result = pd.DataFrame({
#     'quantity': [382, 35, 84],
#     'status': ['Positif', 'Netral', 'Negatif']
# })

# b1, b2, b3 = st.columns(3)
# with b1:
#     st.markdown('### Bar chart')
#     plost.donut_chart(
#         data=anies_result,
#         theta='quantity',
#         color='status',)
# with b2:
#     plost.donut_chart(
#         data=stocks,
#         theta='q2',
#         color='company')
   
st.markdown("<h3 style='text-align: left;margin-top: 12px'>Analysis</h3>", unsafe_allow_html=True)

b1, b2, b3 = st.columns(3)
with b1:
    b1.image(Image.open('anies_grafic.png'))
with b2:
   b2.image(Image.open('prabowo_grafic.png'))
with b3:
   b3.image(Image.open('ganjar_grafic.png'))