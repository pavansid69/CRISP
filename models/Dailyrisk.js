const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const DailyVolatilitySchema = new Schema({
  date: { type: Date, required: true },  // The date of the daily volatility
  daily_change_percent: { type: Number, required: true }  // Percentage change for that day
});

const RiskAnalysisSchema = new Schema({
  risk_score: { type: Number, required: true },  // The risk score for the analysis
  risk_level: { type: String, required: true },  // The risk level (e.g., High Risk, Low Risk)
  daily_volatility: [DailyVolatilitySchema],  // Array of daily volatility objects
  trend_analysis: { type: String, required: true },  // Analysis of the portfolio's trend
  suggested_actions: [{ type: String }]  // Array of suggested actions
});

const DailyriskSchema = new Schema({
  client_id: { type: String, required: true },  // The client ID
  date: { type: Date, required: true },  // The date of the risk analysis
  risk_analysis: { type: RiskAnalysisSchema, required: true }  // Embedded risk analysis object
});

module.exports = mongoose.model('Dailyrisk', DailyriskSchema);
