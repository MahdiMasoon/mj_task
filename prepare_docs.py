import json

import sentence_transformers.util as util
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.documents import Document
from langchain_core.load import dumps
from langchain_ollama.llms import OllamaLLM
from sentence_transformers import SentenceTransformer
from tqdm.autonotebook import tqdm

with open('scrape_chats/chats.json') as f:
    faqs = json.load(f)

sbert_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
questions = [faq['question'] for faq in faqs]
embeddings = sbert_model.encode(questions, convert_to_tensor=True, show_progress_bar=True, normalize_embedding=False)

unique_faqs = []
seen_questions = set()


def merge_faq(base_faq, similars):
    for ans in [a for f in similars for a in f['answers']]:
        base_faq['answers'].append(ans)

    return base_faq


for i, faq in tqdm(enumerate(faqs), total=len(faqs)):

    if faq['question'] not in seen_questions:

        seen_questions.add(faq['question'])

        similar_ids = []

        for j in range(i + 1, len(faqs)):

            if util.pytorch_cos_sim(embeddings[i], embeddings[j]) > 0.85:
                similar_ids.append(j)

                seen_questions.add(faqs[j]['question'])

        if len(similar_ids) > 0:
            unique_faqs.append(merge_faq(faq.copy(), [faqs[j] for j in similar_ids]))
        else:
            unique_faqs.append(faq)

# Alternative scheme for summarizing questions using chain which was replaced due to lack of resources
# ## # Initialize the Ollama model
# instruct_model = OllamaLLM(model="llama3.1")
#
# response_schemas = [
#     ResponseSchema(name="question", description="summarized_question"),
# ]
# output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
#
# format_instructions = output_parser.get_format_instructions()
#
# # Define a prompt template
# prompt_template = PromptTemplate(
#     template="""با توجه به سؤالات مشابه زیر از یک انجمن QA، آنها را در یک سؤال متداول واحد، واضح و مختصر خلاصه کنید. در خلاصه خود به نکات زیر توجه کنید:
#  1. مرتبط بودن: مطمئن شوید که سؤال به یک نگرانی مشترک می پردازد.
#  2. وضوح: از زبان ساده استفاده کنید.
#  3. مختصر بودن: آن را مختصر و بر یک موضوع متمرکز کنید.
#  4. کاربرد عمومی: آن را برای مخاطبان گسترده مرتبط کنید.
#  5. ویژگی: اطمینان حاصل کنید که می توان به آن پاسخ قطعی داد.
#                 سوال ها: {questions}""",
#     input_variables=["questions"],
# )
#
# # Create a chain
# chain = prompt_template | model
#
# # summarize similar questions
# chain.invoke({'questions': '\n'.join(questions)})  ###


def faq_to_doc(faqs):
    docs = []

    for faq in faqs:
        docs.append(Document(page_content=faq['question'], metadata={'answers': '\n'.join(
            [f"{answer['dr_name']} {answer['dr_exp']}: {answer['answer_text']}" for answer in faq['answers']])}))

    return docs


docs = faq_to_doc(unique_faqs)

print(f"we have {len(faqs)} chats and after this process we have {len(docs)} documents")

with open("docs.json", "w") as fp:
    string_representation = dumps(docs)
    fp.write(string_representation)
