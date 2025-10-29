def retrieve_info(query: str):
    # Placeholder for Qdrant-based retrieval
    if "framework" in query.lower():
        return "LangChain and LlamaIndex are top frameworks for building GenAI apps."
    elif "model" in query.lower():
        return "Popular models include GPT-4, Gemini, and Mistral."
    else:
        return "GenAI enables machines to generate creative content and assist humans."
