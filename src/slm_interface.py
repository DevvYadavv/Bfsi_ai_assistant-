from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

class SLMInterface:
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.model_name = model_name
        self.pipeline = None
        # Lazy loading to avoid memory issues during dev
        self.loaded = False

    def load_model(self):
        try:
            # Check for GPU
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Loading model on {device}...")
            
            # Using pipeline for simplicity
            self.pipeline = pipeline("text-generation", model=self.model_name, device_map="auto")
            self.loaded = True
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load model: {e}")

    def generate_response(self, query, context=None):
        if not self.loaded:
            # Simulate response if model not loaded
            return "Based on my training, I can answer general BFSI queries. (Model not loaded)"
        
        prompt = f"User Query: {query}\n"
        if context:
            prompt = f"Context: {context}\n" + prompt
        
        prompt += "Answer:"
        
        try:
            sequences = self.pipeline(
                prompt,
                max_new_tokens=100,
                do_sample=True,
                top_k=10,
                num_return_sequences=1,
                eos_token_id=self.pipeline.tokenizer.eos_token_id,
            )
            return sequences[0]['generated_text'].replace(prompt, "").strip()
        except Exception as e:
            return f"Error generating response: {e}"

slm_interface = SLMInterface()
