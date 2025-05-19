from llama_cpp import Llama

llm = Llama(model_path="C:\\llama_models\\mistral.gguf", n_ctx=2048)

def get_response(prompt):
    output = llm(prompt, max_tokens=512)
    return output["choices"][0]["text"].strip()
