import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import pickle

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_vector_db():
    if not os.path.exists("data/bfsi_dataset.json"):
        print("Dataset not found. Run src/data_gen.py first.")
        return

    with open("data/bfsi_dataset.json", "r") as f:
        data = json.load(f)
    
    # Extract text for embedding (using inputs as queries might match better with user queries)
    # We can also combine instruction + input
    texts = [item['input'] for item in data]
    
    embeddings = model.encode(texts)
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    # Save the index
    faiss.write_index(index, "models/bfsi_vector_db.index")
    
    # Save the metadata (to retrieve the output)
    with open("models/bfsi_metadata.pkl", "wb") as f:
        pickle.dump(data, f)
        
    print(f"Vector DB created with {len(data)} entries.")

if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    create_vector_db()
