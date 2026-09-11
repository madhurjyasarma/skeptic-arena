import chromadb

# Initialize persistent local vector database
client = chromadb.PersistentClient(path="./chroma_store")
collection = client.get_or_create_collection(name="skeptic_objections")

# Seed library: Universal blind spots and objections
OBJECTIONS = [
    {
        "id": "obj_wrapper",
        "category": "Defensibility",
        "text": "This is a thin wrapper around a foundational model. The moment the underlying provider updates their API or ships a native UI feature, your entire competitive advantage disappears overnight."
    },
    {
        "id": "obj_distribution",
        "category": "Go-To-Market",
        "text": "Building the product is easy; acquiring customers profitably is the real bottleneck. Your CAC (Customer Acquisition Cost) will outpace user LTV before you hit viable scale."
    },
    {
        "id": "obj_inertia",
        "category": "Behavior Change",
        "text": "Human habit and enterprise inertia are undefeated. Your solution is 10% better, but switching requires 10x the effort. Users will stick with their clunky existing routine because familiarity beats optimization."
    },
    {
        "id": "obj_nice_to_have",
        "category": "Product-Market Fit",
        "text": "This is a vitamin, not a painkiller. During budget cuts, economic pressure, or personal belt-tightening, discretionary tools like this are the first subscription cancelled."
    },
    {
        "id": "obj_retention_leak",
        "category": "Economics",
        "text": "You have a novel novelty spike at signup, but zero recurring daily utility. Churn will hollow out your user base within 30 to 60 days of launch."
    },
    {
        "id": "obj_trust_liability",
        "category": "Risk & Trust",
        "text": "Hallucinations, data privacy leaks, or edge-case errors will destroy user trust immediately. One critical failure in high-stakes workflows ruins the brand permanently."
    }
]

# Insert documents, metadata, and IDs into ChromaDB
collection.upsert(
    ids=[item["id"] for item in OBJECTIONS],
    documents=[item["text"] for item in OBJECTIONS],
    metadatas=[{"category": item["category"]} for item in OBJECTIONS]
)

print(f"ChromaDB initialized with {collection.count()} attack vectors.")