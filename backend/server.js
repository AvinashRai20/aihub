const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');
const path = require('path');

dotenv.config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Serve static frontend files
app.use(express.static(path.join(__dirname, '../frontend')));

// MongoDB Connection (Placeholder - needs real URI)
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/ai-all-in-one';
mongoose.connect(MONGO_URI)
    .then(() => console.log('✅ Connected to MongoDB'))
    .catch(err => console.error('❌ MongoDB Connection Error:', err));

// Routes
app.get('/api/health', (req, res) => {
    res.json({ status: 'OK', message: 'AI Hub Pro API is running' });
});

// Auth and Tool routes would be imported and used here
// const authRoutes = require('./routes/auth');
// const toolRoutes = require('./routes/tools');
// app.use('/api/auth', authRoutes);
// app.use('/api/tools', toolRoutes);

// Fallback for SPA routing if needed
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
});
