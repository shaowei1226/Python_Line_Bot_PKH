from pymongo import MongoClient

# 连接到MongoDB
mongo_uri = 'mongodb+srv://shaowei:dzoiWAuaPg5bXJEn@cluster0.alqkc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(mongo_uri)

# 选择数据库和集合
db = client['poker_hands']
collection = db['hands']

# 插入单条数据
data = {
    "name": "John Doe",
    "age": 29,
    "city": "New York"
}
collection.insert_one(data)

# 插入多条数据
multiple_data = [
    {"name": "Jane Doe", "age": 25, "city": "Chicago"},
    {"name": "Alice", "age": 28, "city": "Los Angeles"}
]
collection.insert_many(multiple_data)

# 查询数据
for document in collection.find():
    print(document)
