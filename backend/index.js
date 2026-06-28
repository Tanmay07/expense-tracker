const express = require('express');
const cors = require('cors');
const db = require('./database');

const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

// Get all expenses
app.get('/api/expenses', (req, res) => {
    const sql = "SELECT * FROM expenses ORDER BY date DESC";
    db.all(sql, [], (err, rows) => {
        if (err) {
            res.status(400).json({ "error": err.message });
            return;
        }
        res.json({
            "message": "success",
            "data": rows
        });
    });
});

// Add a new expense
app.post('/api/expenses', (req, res) => {
    const { title, amount, category, date } = req.body;
    if (!title || !amount || !category || !date) {
        return res.status(400).json({ "error": "All fields are required" });
    }
    
    const sql = 'INSERT INTO expenses (title, amount, category, date) VALUES (?,?,?,?)';
    const params = [title, amount, category, date];
    db.run(sql, params, function (err) {
        if (err) {
            res.status(400).json({ "error": err.message });
            return;
        }
        res.json({
            "message": "success",
            "data": {
                id: this.lastID,
                title,
                amount,
                category,
                date
            }
        });
    });
});

// Delete an expense
app.delete('/api/expenses/:id', (req, res) => {
    const sql = 'DELETE FROM expenses WHERE id = ?';
    db.run(sql, req.params.id, function (err) {
        if (err) {
            res.status(400).json({ "error": err.message });
            return;
        }
        res.json({ "message": "deleted", changes: this.changes });
    });
});

app.listen(port, () => {
    console.log(`Backend server running on http://localhost:${port}`);
});
