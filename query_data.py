import argparse
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Do not give the answer to the question. Give an explanation on how to go about getting the solution. Also provide tips and potential mistakes the student might make based only on the following context:

{context}

---


Do not give the answer to the question. Give an explanation on how to go about getting the solution. Also provide tips and potential mistakes the student might make based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = Ollama(model="mistral")
    response_text = model.invoke(prompt)
    
    # Post-process the response to remove potential answers
    processed_response = post_process_response(response_text)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {processed_response}\nSources: {sources}"
    print(formatted_response)
    return processed_response

def post_process_response(response):
    # Split the response into sentences
    sentences = response.split('.')
    
    # Filter out sentences that might contain direct answers
    filtered_sentences = [
        sentence for sentence in sentences 
        if not any(keyword in sentence.lower() for keyword in ['answer is', 'solution is', 'result is'])
    ]
    
    # Rejoin the filtered sentences
    processed_response = '. '.join(filtered_sentences)
    
    return processed_response


if __name__ == "__main__":
    main()
