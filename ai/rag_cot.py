from langchain.chains import RetrievalQA, LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import GooglePalm
from langchain.chains.question_answering import load_qa_chain
from google.api_core import retry
import time

# Define custom prompt templates
rag_prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    Context: {context}
    Question: {question}
    Please provide an initial response to the question based on the given context.
    """
)

thought_prompt_template = PromptTemplate(
    input_variables=["initial_response", "previous_context"],
    template="""
    Initial Response: {initial_response}
    Previous Context: {previous_context}
    Please develop a step-by-step reasoning process to refine the initial response.
    """
)

refine_prompt_template = PromptTemplate(
    input_variables=["thought_steps"],
    template="""
    Thought Steps: {thought_steps}
    Based on these thought steps, please provide a refined and detailed final response.
    """
)

@retry.Retry(predicate=retry.if_exception_type(Exception))
def initialize_llm():
    return GooglePalm(google_api_key=google_api_key, temperature=0.1)

def get_llm():
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return initialize_llm()
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Error initializing LLM (attempt {attempt + 1}): {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise

# Use this function to get the LLM
llm = get_llm()

# Create LLMChains for thought and refine steps
thought_chain = LLMChain(llm=llm, prompt=thought_prompt_template)
refine_chain = LLMChain(llm=llm, prompt=refine_prompt_template)

def process_query_with_chain_of_thought(user_query, previous_context, index):
    # Load the QA chain for RAG
    rag_chain = load_qa_chain(llm, chain_type="stuff", prompt=rag_prompt_template)

    # Define the RetrievalQA chain
    retrieval_chain = RetrievalQA(combine_documents_chain=rag_chain, retriever=index.vectorstore.as_retriever())

    # Generate initial response
    initial_response = retrieval_chain.run({'query': user_query, 'context': previous_context})

    # Develop reasoning steps
    thought_steps = thought_chain.run(initial_response=initial_response, previous_context=previous_context)

    # Refine response based on thought steps
    final_response = refine_chain.run(thought_steps=thought_steps)

    return final_response
