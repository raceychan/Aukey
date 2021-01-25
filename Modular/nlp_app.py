import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

import en_core_web_sm
import matplotlib.pyplot as plt 
from wordcloud import WordCloud
from textblob import TextBlob 
from Data_app import Data

class Nlp(Data):
    nlp = en_core_web_sm.load()

    def run_nlp():
        st.subheader('亚马逊商品评论智能分析')
        st.set_option('deprecation.showPyplotGlobalUse', False)

        #数据加载
        asins = Nlp.nlp_asins()
        chosedasin=st.selectbox('ASIN:',asins['asin'].unique())
        review = Nlp.nlp_data(chosedasin)
        #数据加载

        st.write(review)
        no=st.number_input('输入你想要看到的评论序号',min_value=1,value=1,step=1)
        ct=review.iloc[no,1]
        raw_text =st.text_area('选择序号自动引用评论，或在下框手动输入文本',f'{ct}')

        #关键词提取        
        docx = Nlp.nlp(raw_text)
        c_tokens = [ token.text for token in docx ]
        c_lemma = [token.lemma_ for token in docx]
        c_pos = [word.tag_ for word in docx]
        new_df = pd.DataFrame(zip(c_tokens,c_lemma,c_pos),columns=['Tokens','Lemma','POS'])
        adj=new_df[(new_df['POS']=='JJ')|(new_df['POS']=='NN')]['Lemma'].value_counts()
        wordcount=str(adj).replace('dtype','').replace('Lemma','').replace('int64','').replace('Name','')
        #关键词提取

        #情感分析
        blob = TextBlob(raw_text)
        sent_res=[]
        sent_res.append(blob.polarity)
        sent_res.append(blob.subjectivity)  
        #情感分析

        c1,c2,c3,c4=st.beta_columns(4)
        with c1:
            _token=st.button('开始切分')
        with c2:
            _wordcloud=st.button('生成词云')
        with c3:
            _sentiment_analysis=st.button('情感分析')
        with c4:
            _lemma=st.button('查看词频')
        if _sentiment_analysis:          
            st.success(f'该评论的偏向性为:{sent_res[0]},主观性为:{sent_res[1]}')
            if sent_res[0]>0.3:
                st.success('该客户颇为喜爱此商品！')
            elif sent_res[0]>=-0.3 and sent_res[0]<=0.3:
                st.info('该客户对此商品没有明显偏向')
            else:
                st.warning('该客户对产品很不满！')
        if _wordcloud:
            wordcloud =  WordCloud().generate(wordcount)
            plt.imshow(wordcloud,interpolation='bilinear')
            plt.axis("off")
            st.pyplot()
        if _lemma:
            st.write(pd.DataFrame(adj.rename('Count')).transpose()) 
        if _token:
            st.dataframe(new_df)

if __name__=='__main__':
    Nlp.run_nlp()