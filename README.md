# BFSI Call Center AI Assistant

This is a local AI assistant for BFSI call centers, utilizing a RAG pipeline and a Small Language Model (SLM).

## Project Structure
- `data/`: Contains the dataset and raw files.
- `models/`: Contains the FAISS vector index and metadata.
- `src/`: Source code for the application.
- `app.py`: Main Streamlit application.

## Setup Instructions

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Generate Dataset**:
    ```bash
    python src/data_gen.py
    ```

3.  **Create Vector Database**:
    ```bash
    python src/vector_db.py
    ```

4.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```

## Features
- **Dataset Match**: High-precision answers from a curated dataset.
- **RAG Retrieval**: Fallback to similar queries if exact match not found.
- **SLM Generation**: Uses a local SLM (e.g., TinyLlama) for generative responses (configured to use CPU/GPU).

## Configuration
- Modify `src/slm_interface.py` to change the model (default: `TinyLlama/TinyLlama-1.1B-Chat-v1.0`).
- Modify `src/data_gen.py` to add more samples.
