from llama_cpp import Llama

llm = Llama(model_path="C:\\llama_models\\mistral.gguf", n_ctx=2048)

def get_response(prompt):
    output = llm(prompt, max_tokens=512, echo=False)
    return output["choices"][0]["text"].strip()

# Test the model
if __name__ == "__main__":
    print(get_response("What is the capital of France?"))
