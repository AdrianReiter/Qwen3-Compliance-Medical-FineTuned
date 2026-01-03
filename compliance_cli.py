import sys
import re
from mlx_lm import load, generate

def main():
    # Define model paths
    ADAPTER_PATH = "./Qwen3-compliance_agent_medical-v1"
    BASE_MODEL = "Qwen/Qwen3-0.6B"

    print("Loading Compliance Model...")
    
    # 1. Try loading the fine-tuned (fused) model
    try:
        model, tokenizer = load(ADAPTER_PATH)
        print(f"Loaded fine-tuned model from {ADAPTER_PATH}")
    except Exception as e:
        print(f"Could not load local adapter: {e}")
        print(f"ℹFalling back to base model: {BASE_MODEL}")
        
        # 2. Fallback to base model
        try:
             model, tokenizer = load(BASE_MODEL)
             print(f"Loaded base model: {BASE_MODEL}")
        except Exception as e_base:
             print(f"Error: Could not load base model either: {e_base}")
             print("Please ensure internet connection is active or run training first.")
             sys.exit(1)

    print("\nCompliance Officer Ready. (Type 'quit' to exit)")
    print("---------------------------------------------------")

    while True:
        try:
            user_input = input("\nDescribe the feature/change: ")
            if not user_input: continue
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            sys.exit(0)
            
        if user_input.lower() in ['quit', 'exit']: 
            break

        # 3. FIX: Use tokenizer's chat template instead of hardcoded strings
        # This ensures correct handling of special tokens (<|im_start|>, etc.)
        messages = [
            {"role": "system", "content": "You are a Regulatory Consultant. Always analyze dependencies and risk before answering."},
            {"role": "user", "content": user_input}
        ]

        if hasattr(tokenizer, "apply_chat_template"):
            prompt = tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
            )
        else:
            # Fallback if tokenizer doesn't support chat templates (rare for modern HF models)
            prompt = f"<|im_start|>system\nYou are a Regulatory Consultant. Always analyze dependencies and risk before answering.<|im_end|>\n<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
        
        # Generate response
        # Increased max_tokens to allow for full chain-of-thought and answer
        response = generate(model, tokenizer, prompt=prompt, max_tokens=1500, verbose=False)
        
        # 4. Parse out the thinking block for the "Audit Trail"
        # Using DOTALL to capture newlines inside the tag
        think_match = re.search(r"<think>(.*?)</think>", response, re.DOTALL)
        
        if think_match:
            think_part = think_match.group(1).strip()
            # The answer is everything strictly after the closing tag
            answer_part = response.split("</think>")[-1].strip()
            
            print(f"\n⚙️  [AUDIT TRAIL / LOGIC TRACE]\n{think_part}")
            print(f"\n📋 [REGULATORY GUIDANCE]\n{answer_part}")
        else:
            # If no thinking block is found, print the whole response
            # (The model might have skipped the thought process or formatting failed)
            print(f"\n📋 [RESPONSE]\n{response.strip()}")

if __name__ == "__main__":
    main()