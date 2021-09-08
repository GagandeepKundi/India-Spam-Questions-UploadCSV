import streamlit as st 

# EDA Pkgs
import pandas as pd 
import numpy as np
import time
import base64

#Image
from PIL import Image
image=Image.open('/Users/brl.314/Downloads/Brainly_logo.png')
st.image(image,use_column_width=True)

# Upload model
import joblib

model = joblib.load(open("/Users/brl.314/Downloads/india_spam_aug_4.pkl","rb"))

@st.cache(suppress_st_warning=True)


#Prediction function

def pred(x):

	results = model.predict([x])
	
	return results

#Confidence Function

def conf(x):
    
    confidence = model.decision_function([x])
    
    return confidence

import streamlit.components as stc

# Utils
import base64 
import time
timestr = time.strftime("%Y%m%d-%H%M%S")


def csv_downloader(data):
    csvfile = data.to_csv()
    b64 = base64.b64encode(csvfile.encode()).decode()
    new_filename = "new_text_file_{}_.csv".format(timestr)
    st.markdown("#### Download File ###")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!!</a>'
    st.markdown(href,unsafe_allow_html=True)

# Class
class FileDownloader(object):
    """docstring for FileDownloader
    >>> download = FileDownloader(data,filename,file_ext).download()

    """
    def __init__(self, data,filename='myfile',file_ext='txt'):
        super(FileDownloader, self).__init__()
        self.data = data
        self.filename = filename
        self.file_ext = file_ext

    def download(self):
        b64 = base64.b64encode(self.data.encode()).decode()
        new_filename = "{}_{}_.{}".format(self.filename,timestr,self.file_ext)
        st.markdown("#### Download File ###")
        href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}">Click Here</a>'
        st.markdown(href,unsafe_allow_html=True)


def main():
    with st.form(key='India Question Spam Classifier'):
        st.title('India Spam Classifier')
        uploaded_file = st.file_uploader("Upload a CSV/XLSX file",type=['csv','xlsx'])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head(10))
        st.form_submit_button(label='Submit')

    if st.checkbox("Check total number of questions"):
        st.write("Total questions:", str(df.shape[0]))


        with st.form(key='Make Predictions'):
            st.title('Make Predictions')
            st.form_submit_button(label='Make Predictions')

            df['Prediction'] = df['content'].apply(lambda x: pred(x))

            df['Confidence Score'] = df['content'].apply(lambda x: conf(x))

            df['Confidence Score'] = df['Confidence Score'].apply(lambda x: abs(x))

            df['Decision'] = df['Confidence Score'].apply(lambda x: 'Confident' if x > 0.5 else 'Not Sure')   

            st.success('Predictions Complete')

            st.dataframe(df.head(10))

            download = FileDownloader(df.to_csv(),file_ext='csv').download()

if __name__ == '__main__':
	main()