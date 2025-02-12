import json
#import torch
from transformers import pipeline
from tools import search_products, estimate_shipping, check_discount, compare_prices, get_return_policy
#from huggingface_hub import login

#login(token="#")


# # Load model
# MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"  # at least 8GB VRAM (best with GPU)
# MODEL_NAME = "facebook/opt-1.3b"  #~1.3B parameters (~5-6GB RAM usage, even on CPU)

# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_NAME, 
#     torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32, 
#     device_map=None 
# )

# Load a free LLM (like Hugging Face's GPT-2 for local inference)
llm = pipeline("text-generation", model="gpt2")  # ~124M parameters (~500MB RAM usage, even on CPU)

def process_user_query(user_query, user_location ,promo_code=None):
    """Processes the user query, determines necessary tool calls, and generates a response."""
    
    tool_instructions = """
    You are a virtual shopping assistant. You can use the following tools:
    - search_products: Find products based on criteria.
    - estimate_shipping: Calculate shipping costs and time.
    - check_discount: Apply and verify promo codes.
    - compare_prices: Compare product prices across stores.
    - get_return_policy: Retrieve return policies of stores.

    Your task is to break down the query, decide the necessary tools, and call them in the correct sequence.
    """

    # Generate reasoning using LLM (simplified prompt-based ATC approach)
    reasoning_prompt = f"{tool_instructions}\nUser query: {user_query}\nWhat tools should be used?"
    tool_decision = llm(reasoning_prompt, max_new_tokens=50)[0]["generated_text"]

    # Determine tool execution sequence (simplified parsing)
    tool_calls = []
    if "search_products" in tool_decision:
        tool_calls.append("search_products")
    if "estimate_shipping" in tool_decision:
        tool_calls.append("estimate_shipping")
    if "check_discount" in tool_decision:
        tool_calls.append("check_discount")
    if "compare_prices" in tool_decision:
        tool_calls.append("compare_prices")
    if "get_return_policy" in tool_decision:
        tool_calls.append("get_return_policy")

    # Execute the necessary tools
    results = {}

    # Search products first
    matched_products = search_products(user_query)
    if matched_products:
        results["products"] = matched_products
        
        if "check_discount" in tool_calls:
            results["discount"] = check_discount(user_query, promo_code)

        if "compare_prices" in tool_calls:
            results["comparison"] = compare_prices(user_query)

        if "estimate_shipping" in tool_calls:
            results["shipping"] = estimate_shipping(user_location,user_query)

        if "get_return_policy" in tool_calls:
            results["returns"] = get_return_policy(user_query)
    else:
        results["message"] = "No matching products found for the given criteria."

    return json.dumps(results, indent=2)