import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- Ortam değişkenlerini yükle
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Google API key bulunamadı. .env dosyasını kontrol et.")

# --- Excel dosyasını oku
oyun_df = pd.read_excel("Tiyatro_Oyunlari_Dataset.xlsx")

# --- Sayfa başlığı ve açıklama
st.title("🎭 Tiyatro Asistanı")
st.markdown("""
👋 **Hoş geldin!** Aşağıya tiyatroyla ilgili bir soru yazarak oyun arayabilirsin.  
Örnek sorular:
- "Dram türünde iki kişilik bir oyun önerir misin?"
- "Haldun Taner'in yazdığı oyunlar neler?"
- "Ormanda geçen tiyatro oyunu var mı?"
- "1972 yılında yazılmış oyunlar var mı?"
---
""")

# --- Excel'den veri -> Document
def oyun_to_document(row):
    text = f"""Oyun Adı: {row['Oyun Adı']}
Yazar: {row['Yazar']}
Yıl: {row['Yıl']}
Mekan: {row['Mekan']}
Tür: {row['Tür']}
Özet: {row['Özet']}
Kaç Kişilik: {row['Kaç Kişilik']}
Roller Özeti: {row['Roller Özeti']}
Roller Detayı: {row['Roller Detayı']}"""
    return Document(page_content=text)

docs = [oyun_to_document(row) for _, row in oyun_df.iterrows()]
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_docs = splitter.split_documents(docs)

# --- Vektör veritabanı
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = Chroma.from_documents(
    documents=split_docs,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# --- LLM tanımı
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.3,
    max_tokens=500
)

# --- Intent sınıflandırma zinciri
intent_prompt = PromptTemplate.from_template("""
Aşağıdaki kullanıcı cümlesinin hangi intent'e ait olduğunu belirle. 
Intent kategorileri:
- Oyun Önerisi
- Yazar Sorgusu
- Mekan Sorgusu
- Yıl Sorgusu
- Karakter Sayısı
- Selamlama
- Vedalaşma
- Bilinmeyen

Cümle: {soru}
Intent:
""")
intent_chain = intent_prompt | llm | StrOutputParser()

# --- RAG prompt
system_prompt = (
    "Sen tiyatro oyunları hakkında bilgi veren bir asistansın.\n"
    "Aşağıdaki oyun özetlerini kullanarak kullanıcı sorusunu yanıtla.\n"
    "Cevabın kısa, net ve bağlama dayalı olsun. Bilinmeyen bir şey varsa 'emin değilim' de.\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

# --- Kullanıcıdan input al
query = st.text_input("🎤 Tiyatroyla ilgili bir sorun varsa buraya yaz:")

if query:
    intent = intent_chain.invoke({"soru": query})
    st.markdown(f"**🎯 Intent tespiti:** `{intent}`")

    if intent.lower() in ["oyun önerisi", "yazar sorgusu", "mekan sorgusu", "yıl sorgusu", "karakter sayısı"]:
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        response = rag_chain.invoke({"input": query})
        st.write(response["answer"])

    elif intent.lower() == "selamlama":
        st.write("Merhaba! Tiyatro dünyasına hoş geldiniz. Bir sorunuz var mı? 🎭")

    elif intent.lower() == "vedalaşma":
        st.write("Görüşmek üzere! Yeni oyunlarda buluşmak dileğiyle. 👋")

    else:
        st.write("Bu sorunun kapsamını anlayamadım. Lütfen daha açık bir şey sorabilir misiniz?")
