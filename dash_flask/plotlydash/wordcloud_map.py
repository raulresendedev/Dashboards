import numpy as np
import pandas as pd
import unidecode
import matplotlib.pyplot as plt
from PIL import Image
from cfg_bd import q_wordcloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

df = q_wordcloud()

respostas = " ".join(s for s in df['RESPOSTA'])
respostas = respostas.lower()
respostas = unidecode.unidecode(respostas)
respostas = respostas.replace("muito obrigado", "muito-obrigado")
stopwords = set(STOPWORDS)

stopwords.update(["da", "meu", "em", "você", "de", "ao", "os", "e", "que", "foi", "o", "ja", "ou", "não",
                  "samuel", "das", "ou", "via", "idem", "link", "para", "pelo", "ser", "ricardo", "angela", "um", "deu", "caiu"
                  ,"sem", "virtual", "tem", "problema", "é", "nao", "chamado", "resolucao", "analista"])

wordcloud = WordCloud(stopwords=stopwords,
                      background_color="black",
                      colormap='winter',
                      width=1600, height=800).generate(respostas)

# mostrar a imagem final
fig, ax = plt.subplots(figsize=(10,6))
ax.imshow(wordcloud, interpolation='bilinear')
ax.set_axis_off()
plt.imshow(wordcloud);
wordcloud.to_file("respostas_wordcloud.png")

print(respostas)