memory_store = []

def store_memory(user_input, bot_response):
    memory_store.append({"user": user_input, "bot": bot_response})

def get_memory():
    return memory_store[-3:] if len(memory_store) > 3 else memory_store
