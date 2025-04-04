

# =============================
#   Install Dependencies
# =============================

# 1) Install key libraries
!pip install spacy sentence_transformers networkx

# 2) Download and link spaCy's small English model
!python -m spacy download en_core_web_sm

# =============================
#   Import Libraries
# =============================
import spacy
from sentence_transformers import SentenceTransformer
import networkx as nx
import numpy as np

# =============================
#   Load Models
# =============================
# Load spaCy English model for sentence segmentation, POS tagging
nlp = spacy.load("en_core_web_sm")

# Load a SentenceTransformer model for creating embeddings
# (this serves as our "SONAR embedding" stand-in)
model = SentenceTransformer('all-MiniLM-L6-v2')

# =============================
#   Example Paragraph
# =============================
paragraph = """
AI is transforming industries. Machines are learning human languages
because automation helps free humans from repetitive tasks, so employees
can focus on more innovative work. This development will likely create
new opportunities in tech and data science.
"""

# =============================
#   1) Sentence Segmentation
# =============================
doc = nlp(paragraph.strip())
sentences = [sent.text for sent in doc.sents if sent.text.strip()]

print("\n--- Step 1: Sentence Segmentation ---")
for i, s in enumerate(sentences, start=1):
    print(f"Sentence {i}: {s}")

# =============================
#   2) SONAR Embedding (Concept Representation)
# =============================
# We'll embed each sentence to capture overall meaning
sentence_embeddings = model.encode(sentences)

print("\n--- Step 2: SONAR Embeddings Shape ---")
print("Each sentence is turned into a vector of dimension:", sentence_embeddings.shape[1])

# =============================
#   3) Diffusion Process (Contextual / Relation Graph)
# =============================
# Create a simple graph of sentence relationships if they share common nouns
G = nx.Graph()

for i, s in enumerate(sentences):
    G.add_node(i, text=s)

# A trivial example: connect sentences if they share any noun
for i in range(len(sentences)):
    for j in range(i+1, len(sentences)):
        # Extract nouns from each sentence
        nouns_i = {token.lemma_.lower() for token in nlp(sentences[i]) if token.pos_ == "NOUN"}
        nouns_j = {token.lemma_.lower() for token in nlp(sentences[j]) if token.pos_ == "NOUN"}
        # If they share any noun, create an edge
        if nouns_i.intersection(nouns_j):
            G.add_edge(i, j)

print("\n--- Step 3: Diffusion Graph Edges (Sentence Connections) ---")
for edge in G.edges:
    print(f"Edge between sentence {edge[0]+1} and {edge[1]+1}")

# =============================
#   4) Advanced Patterning (Cause-Effect, etc.)
# =============================
# A rudimentary approach: look for 'because' or similar words as cause indicators
cause_effect_pairs = []
for i, s in enumerate(sentences):
    if "because" in s.lower():
        cause_effect_pairs.append((i, s))

print("\n--- Step 4: Cause-Effect Pattern Detection ---")
if cause_effect_pairs:
    for idx, text_cause in cause_effect_pairs:
        print(f"Sentence {idx+1} has a cause-effect indicator: '{text_cause.strip()}'")
else:
    print("No direct cause-effect indicators found in this paragraph.")

# =============================
#   5) Hidden Process (Pseudo Memory)
# =============================
# Here we simulate storing a "memory" of the paragraph under a key.
memory_store = {}
memory_key = "paragraph_context"
memory_store[memory_key] = paragraph.strip()

# In a real system, this memory could be used to provide context to future queries.
print("\n--- Step 5: Hidden Process (Memory) ---")
print("Stored paragraph in memory_store under key 'paragraph_context'.")
print("Memory content:\n", memory_store[memory_key])

# =============================
#   6) Quantization (Efficient Embedding Storage)
# =============================
# Convert float embeddings to 8-bit integers to save space (example of quantization)
quantized_embeddings = []
for vec in sentence_embeddings:
    # Scale values from -1..1 to 0..255 for demonstration (assuming typical range)
    scaled = 127.5 * (vec + 1.0)
    quantized = np.clip(scaled, 0, 255).astype(np.uint8)
    quantized_embeddings.append(quantized)

quantized_embeddings = np.array(quantized_embeddings)

print("\n--- Step 6: Quantization ---")
print(f"Original embeddings shape: {sentence_embeddings.shape}")
print(f"Quantized embeddings shape: {quantized_embeddings.shape}")

# =============================
#   7) Output Generation
# =============================
# A simple example: "LCM" output might combine
# (a) sentences, (b) embeddings, (c) cause/effect flags, (d) memory reference
print("\n--- Step 7: Final Structured LCM Output ---")
final_structured_output = {
    "segmented_sentences": sentences,
    "cause_effect_sentences": [sent for (_, sent) in cause_effect_pairs],
    "graph_edges": list(G.edges),
    "memory_reference": memory_store.get(memory_key, ""),
    "quantized_embeddings_preview": quantized_embeddings[0][:10].tolist()  # first 10 dims of first sentence
}

print(final_structured_output)
