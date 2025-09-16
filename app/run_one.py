import pandas as pd
from app.agents.solution import draft_reply

df = pd.read_csv("app/data/tickets_seed.csv")
row = df.iloc[0]  # change index to test other tickets
res = draft_reply(row["subject"], row["body"])
print("\n=== INPUT ===")
print(f"Subject: {row['subject']}\nBody: {row['body']}")
print("\n=== REPLY ===")
print(res["reply"])
print("\nCitations:", res.get("cited_ids", []))
