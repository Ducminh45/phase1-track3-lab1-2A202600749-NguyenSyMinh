import json
import random

with open("data/hotpot_dev_distractor_v1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# The hotpotQA format is typically a list of dicts.
# Each dict has: _id, level, question, answer, context
# context is a list of [title, list of sentences]

examples = []
for item in data:
    context_chunks = []
    for ctx in item.get("context", []):
        title = ctx[0]
        text = "".join(ctx[1])
        context_chunks.append({"title": title, "text": text})
    
    examples.append({
        "qid": item["_id"],
        "difficulty": item["level"],
        "question": item["question"],
        "gold_answer": item["answer"],
        "context": context_chunks
    })

# Get random 100
random.seed(42)
sampled = random.sample(examples, min(100, len(examples)))

with open("data/hotpot_test.json", "w", encoding="utf-8") as f:
    json.dump(sampled, f, ensure_ascii=False, indent=2)

print(f"Saved {len(sampled)} examples to data/hotpot_test.json")
