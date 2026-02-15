import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os

class RAGEngine:
    def __init__(self, model_path='all-MiniLM-L6-v2', index_path='models/bfsi_vector_db.index', metadata_path='models/bfsi_metadata.pkl'):
        # Check if files exist
        if not os.path.exists(index_path) or not os.path.exists(metadata_path):
             # Try to generate them on the fly if missing (e.g. first run)
             import sys
             print("Vector DB not found. Attempting to generate...")
             # sys.path.append('src') # simpler approach for now
             # from vector_db import create_vector_db
             # create_vector_db() 
             # For robust production code, we'd handle this better. 
             # Assuming they exist for now or will be created.
             pass

        try:
            self.model = SentenceTransformer(model_path)
            self.index = faiss.read_index(index_path)
            with open(metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
            self.ready = True
        except Exception as e:
            print(f"Error loading RAG engine: {e}")
            self.ready = False

    def retrieve(self, query, top_k=1, threshold=0.85):
        if not self.ready:
            return None, 0.0

        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), top_k)
        
        best_match_idx = indices[0][0]
        score = distances[0][0] # FAISS L2 distance. Lower is better. 
        # But wait, cosine similarity is usually preferred. 
        # For L2 on normalized vectors, distance = 2 * (1 - cosine_sim).
        # So closer to 0 is better.
        
        # We need to convert L2 distance to similarity or just use a distance threshold.
        # Let's assume embeddings are normalized -> L2 distance of 0 means identical.
        # Threshold of 0.85 similarity corresponds to distance ~ 0.55 (sqrt(2*(1-0.85)))
        
        similarity = 1 - (score / 2) # Approximation for normalized vectors
        
        if best_match_idx == -1:
             return None, 0.0

        result = self.metadata[best_match_idx]
        return result, similarity

rag_engine = RAGEngine()
