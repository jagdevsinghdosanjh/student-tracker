from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["spt_db"]
scores = db.scores

def deduplicate_scores():
    print("🔍 Scanning for duplicate score entries...\n")

    pipeline = [
        {
            "$group": {
                "_id": {
                    "student_id": "$student_id",
                    "subject": "$subject",
                    "exam_date": "$exam_date"
                },
                "ids": {"$addToSet": "$_id"},
                "count": {"$sum": 1}
            }
        },
        {
            "$match": {
                "count": {"$gt": 1}
            }
        }
    ]

    duplicates = list(scores.aggregate(pipeline))
    print(f"🧾 Found {len(duplicates)} duplicate groups.\n")

    total_deleted = 0
    for group in duplicates:
        ids = group["ids"]
        ids.sort()  # Keep the first (lowest _id) and delete the rest
        to_delete = ids[1:]
        result = scores.delete_many({"_id": {"$in": to_delete}})
        total_deleted += result.deleted_count
        print(f"🗑️ Removed {result.deleted_count} duplicates for: {group['_id']}")

    print(f"\n✅ Deduplication complete. Total records deleted: {total_deleted}")

if __name__ == "__main__":
    deduplicate_scores()
