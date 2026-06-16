import streamlit as st
import pickle
# import nltk
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
# import stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer

nltk.download('punkt_tab')


ps=PorterStemmer()

def text_trans(text):
  text =text.lower()
  text =nltk.word_tokenize(text)
  y=[]
  for i in text:
    if i.isalnum():
      y.append(i)


  text= y[:]
  y.clear()

  for i in text:
    if i not in stopwords.words('english') and i not in string.punctuation:
      y.append(i)
  text= y[:]
  y.clear()

  for i in text:
    y.append(ps.stem(i))

  return " ".join(y)

tdf=pickle.load(open('vectorizer (1).pkl','rb'))

model =pickle.load(open('model (1).pkl','rb'))

st.title("Email/SMS classifier")
input_sms = st.text_area("Enter message")
if st.button('press'):


    trans_sms = text_trans(input_sms)

    vector_input = tdf.transform([trans_sms])

    result = model.predict(vector_input)[0]

    if result == 1:
        st.error("spam")

    else:
        st.success("not spam")

