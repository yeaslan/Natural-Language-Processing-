# Notebooks

This directory hosts exploratory notebooks and demos. Suggested starting point:

1. Load synthetic or public Q&A data (StackExchange, WikiQA).
2. Run the NER → Entity Linking → Relation Extraction pipeline on sample entries.
3. Upsert entities and relations into a local Neo4j instance.
4. Visualize subgraphs or export to external tools (Gephi, Neptune, etc.).
5. Capture evaluation metrics (precision/recall, hits@k) and log them via MLflow.

Add notebooks such as `01_demo.ipynb` following the outline in the project specification.
