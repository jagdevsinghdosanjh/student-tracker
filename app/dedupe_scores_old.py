from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["spt_db"]  # Replace with your actual database name

result = db.scores.aggregate([
  {
    "$group": {
      "_id": {
        "student_id": "$student_id",
        "subject": "$subject",
        "exam_date": "$exam_date"
      },
      "ids": { "$addToSet": "$_id" },
      "count": { "$sum": 1 }
    }
  },
  { "$match": { "count": { "$gt": 1 } } }
])

for doc in result:
    print(doc)
