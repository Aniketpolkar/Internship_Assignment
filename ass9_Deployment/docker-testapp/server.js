const express = require("express");
const app = express();
const path = require("path");
const { MongoClient } = require("mongodb");

const PORT = 5050;

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static("public"));

// ✅ Correct MongoDB URL
const MONGO_URL =
  "mongodb://admin:qwerty@localhost:27017/apnacollege-db?authSource=admin";

const client = new MongoClient(MONGO_URL);

let db;

// ✅ Connect ONCE when server starts
async function connectDB() {
  await client.connect();
  console.log("Connected successfully to MongoDB");
  db = client.db("apnacollege-db");
}

connectDB().catch(console.error);

// GET all users
app.get("/getUsers", async (req, res) => {
  try {
    const data = await db.collection("users").find({}).toArray();
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST new user
app.post("/addUser", async (req, res) => {
  try {
    const userObj = req.body;
    console.log(userObj);

    const result = await db.collection("users").insertOne(userObj);
    res.json({ message: "User added", id: result.insertedId });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
