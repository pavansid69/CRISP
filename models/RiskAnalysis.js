const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const RiskAnalysisSchema = new Schema({
  client_id: { type: String, required: true },
  date: { type: Date, required: true },
  risk_analysis: {
    risk_score: { type: Number, required: true },
    risk_level: { type: String, required: true },
    daily_volatility: [
      {
        date: { type: Date, required: true },
        daily_change_percent: { type: Number, required: true }
      }
    ],
    trend_analysis: { type: String, required: true },
    suggested_actions: [{ type: String, required: true }]
  }
});

module.exports = mongoose.model('RiskAnalysis', RiskAnalysisSchema);
