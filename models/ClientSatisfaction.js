const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const ClientSatisfactionSchema = new Schema({
  client_id: { type: String, required: true },  // Client ID, reference to client
  client_name: { type: String, required: true }, // Client Name
  numerical_satisfaction_level: { type: Number, required: true }, // Satisfaction Level in Numbers
  overall_satisfaction_score: { type: Number, required: true }, // Satisfaction Score
  reasons_for_satisfaction: { type: [String], required: true }, // Reasons for Satisfaction (Array of strings)
  satisfaction_level: { 
    type: String, 
    enum: ['Very Satisfied', 'Satisfied Client', 'Neutral', 'Dissatisfied', 'Very Dissatisfied'], 
    required: true 
  } // Satisfaction level description
});

// Create the model
const ClientSatisfaction = mongoose.model('ClientSatisfaction', ClientSatisfactionSchema);

module.exports = ClientSatisfaction;
