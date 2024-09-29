const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const sentimentSummarySchema = new Schema({
  email_id: { type: String },
  sentiment: { type: String, enum: ['Positive', 'Neutral', 'Negative'], required: true },
  numeric_label: { type: Number, required: true }
});

const sentimentDetailSchema = new Schema({
  emails: [sentimentSummarySchema],
  phone_calls: [sentimentSummarySchema],
  chats: [sentimentSummarySchema],
  overall_daily_sentiment: { type: String, enum: ['Positive', 'Neutral', 'Negative'], required: true },
  overall_sentiment_numeric_label: { type: Number, required: true }
});

const dailySentimentSchema = new Schema({
  client_id: { type: String, required: true }, // Reference to the client
  date: { type: Date, required: true },
  sentiment_summary: { type: sentimentDetailSchema, required: true },
  reason_for_sentiment: { type: String, required: true }
});

const DailySentiment = mongoose.model('DailySentiment', dailySentimentSchema);

module.exports = DailySentiment;
