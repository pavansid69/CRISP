const mongoose = require('mongoose');

const clientSchema = new mongoose.Schema({
    client_id: { type: String, required: true },
    name: { type: String, required: true },
    age: { type: Number, required: true },
    risk_tolerance: { type: String, required: true },
    investment_goal: { type: String, required: true },
    email: { type: String, required: true },
    phone: { type: String, required: true },
    account_status: { type: String, required: true }
});

const Client = mongoose.model('Client', clientSchema);

module.exports = Client;
