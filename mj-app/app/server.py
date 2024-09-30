import json

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langchain.docstore.document import Document
from langchain.prompts import ChatPromptTemplate
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_community.llms import Ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

with open("../unique_faqs.json", "r") as fp:
    faqs = json.load(fp)


def convert_to_document(faqs):
    docs = []

    for faq in faqs:
        docs.append(Document(
            page_content='\n\n'.join([faq['question']] + [answer['answer_text'] for answer in faq['answers']])))

    return docs


docs = convert_to_document(faqs)

model_kwargs = {'device': 'cpu', 'trust_remote_code': True}

encode_kwargs = {}

hf = HuggingFaceEmbeddings(
    model_name='paraphrase-multilingual-mpnet-base-v2',
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

separators = [
    "\n\n",
    ".",
    " "
]

# This text splitter is used to create the child documents
child_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
    separators=separators
)

# The vectorstore to use to index the child chunks
vectorstore = Chroma(
    collection_name="full_documents", embedding_function=hf
)

# The storage layer for the parent documents
store = InMemoryStore()
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
)

retriever.add_documents(docs, ids=None)

prompt = ChatPromptTemplate.from_template(
    "شما یک چت بات پزشکی هستید که برای پاسخ به سوالات پزشکی کاربران طراحی شده است. مجموعه‌ای از پرسش‌ها و پاسخ‌های مرتبط از یک مجموعه داده قابل اعتماد به شما ارائه می‌شود که توسط پزشک متخصص پاسخ داده می‌شود. وظیفه شما این است که تنها بر اساس این داده های ارائه شده پاسخ هایی ایجاد کنید. از هیچ دانش یا اطلاعات خارجی فراتر از مجموعه داده داده شده استفاده نکنید. نکات مهم: فقط از سوالات و پاسخ های ارائه شده برای ایجاد پاسخ استفاده کنید. اطمینان حاصل کنید که پاسخ ها دقیق و مرتبط با درخواست کاربر هستند. لحن حرفه ای و همدلانه خود را حفظ کنید.{context}")

llm = Ollama(model="llama3.1")

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
add_routes(app,
           retriever | prompt | llm,
           path='/doctor_yab')

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
