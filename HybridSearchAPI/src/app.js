const express = require('express');
const { Pool } = require('pg');
const app = express();
const pool = new Pool();

app.get('/search', async (req, res) => {
    const { query, vector } = req.query;

    try {
        // Keyword-based search
        const keywordResults = await pool.query(`
          SELECT mi.*, mc.content
          FROM magazine_information mi
          JOIN magazine_content mc ON mi.id = mc.magazine_id
          WHERE mi.title ILIKE $1 OR mi.author ILIKE $1 OR mc.content ILIKE $1
        `, [`%${query}%`]);

        // Vector-based search
        const vectorResults = await pool.query(`
          SELECT mi.*, mc.content
          FROM magazine_information mi
          JOIN magazine_content mc ON mi.id = mc.magazine_id
          ORDER BY mc.vector_representation <-> $1::vector
          LIMIT 10
        `, [vector]);

        // Combine the results
        const combinedResults = [...keywordResults.rows, ...vectorResults.rows];

        res.json(combinedResults);
    } catch (err) {
        console.error(err);
        res.status(500).send('Server Error');
    }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
