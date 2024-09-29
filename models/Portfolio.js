const mongoose = require('mongoose');

// Define the schema for stocks within the portfolio
const stockSchema = new mongoose.Schema({
    stock_symbol: { type: String, required: true },
    current_value: { type: Number, required: true },
    purchase_value: { type: Number, required: true },
    quantity: { type: Number, required: true }
});

// Define the schema for daily changes in portfolio value
const dailyChangeSchema = new mongoose.Schema({
    date: { type: Date, required: true },
    portfolio_value: { type: Number, required: true },
    profit_loss: { type: Number, required: true }
});

// Define the Portfolio schema
const portfolioSchema = new mongoose.Schema({
    client_id: { type: String, required: true },
    portfolio_id: { type: String, required: true },
    total_portfolio_value: { type: Number, required: true },
    total_purchase_value: { type: Number, required: true },
    profit_loss: { type: Number, required: true },
    p_l_percent: { type: Number, required: true },
    stocks: [stockSchema],  // Array of stock objects
    daily_changes: [dailyChangeSchema]  // Array of daily changes
});

// Create a Mongoose model for Portfolio
const Portfolio = mongoose.model('Portfolio', portfolioSchema);

module.exports = Portfolio;
