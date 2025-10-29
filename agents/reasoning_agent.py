def reason_with_llm(user_message, retrieved_data, past_context):
    response = f"Based on your question: '{user_message}', {retrieved_data}"
    return f"Hey, I'm Genzo 😊 — your GenAI buddy! {response}"
