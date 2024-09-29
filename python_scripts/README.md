# **CRISP: Client Relationship Insight & Sentiment Performance**

## Project Overview
**CRISP** is a comprehensive client management platform tailored for hedge funds and financial institutions. It leverages Natural Language Processing (NLP) and Machine Learning to evaluate daily interactions and portfolio data, ultimately delivering a unified **Client Relationship Insight & Sentiment Performance (CRISP)** score. The CRISP score enables portfolio managers and advisors to gain deeper insights into client sentiment, manage portfolio risks, and optimize overall satisfaction, ensuring that high-value clients remain engaged and satisfied.

### Why **CRISP**?
The **CRISP** platform is built to address the challenges hedge funds face in managing complex client relationships. Financial institutions need clear, actionable insights to proactively manage client satisfaction and engagement. By combining sentiment analysis, risk management, and satisfaction scoring, CRISP acts as a single source of truth for understanding and optimizing client relationships.

## Key Features of **CRISP**:
- **Client Sentiment Analysis**: Automatically classifies daily client interactions into positive, neutral, or negative sentiment categories, offering a granular view of client sentiment trends.
- **Risk Assessment**: Analyzes daily portfolio performance and computes a risk score, highlighting portfolios that may be at risk of underperformance.
- **Unified CRISP Score**: Integrates sentiment and risk data to generate a single score that reflects the health of the client relationship.
- **Proactive Client Engagement**: Identifies high-priority clients who may require immediate attention to prevent disengagement or churn.
- **Dashboard Visualization**: Displays all analysis results in a user-friendly dashboard (not included in this repository) for quick and intuitive access.

## Components of CRISP:
The project is divided into four main scripts, each handling a specific part of the analysis pipeline:

1. **Sentiment Analysis (`sentiment_analysis.py`)**:
   - Analyzes daily client communications (emails, phone call notes, and chat logs) using OpenAI's GPT model.
   - Outputs: Daily sentiment summaries stored in the `dailysentiments` collection.

2. **Risk Analysis (`risk_analysis.py`)**:
   - Analyzes the daily changes in client portfolios to compute a risk score and risk level.
   - Outputs: Daily risk summaries stored in the `dailyrisks` collection.

3. **Client Satisfaction Analysis (`client_satisfaction.py`)**:
   - Integrates daily risk and sentiment data to compute a comprehensive **Client Satisfaction Score**.
   - Outputs: Satisfaction levels, scores, and key reasons stored in the `clientSatisfaction` collection.

4. **Main Execution Script (`main.py`)**:
   - Runs the entire pipeline by sequentially executing the three scripts.

## Data Flow and Architecture
The application uses a modular approach, with separate MongoDB collections for storing intermediate and final results:

1. **`clientInteraction`**: Stores raw client interactions data (emails, chats, phone call notes).
2. **`dailysentiments`**: Stores daily sentiment scores and summaries for each client.
3. **`portfolios`**: Contains information about each client’s portfolio, including daily changes in value.
4. **`dailyrisks`**: Stores daily risk analysis and performance trends for each client portfolio.
5. **`clientSatisfaction`**: Final output collection storing the overall satisfaction levels, scores, and reasons.

## Setup and Execution:

### Prerequisites:
- **Python**: 3.8+
- **MongoDB Atlas** (or local MongoDB setup)
- **OpenAI API Key** for GPT models.

### Setup Guide:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repository/CRISP.git
   cd CRISP
   ```

2. **Install the Required Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MongoDB**:
   - Create a MongoDB Atlas cluster or use a local setup.
   - Update the connection URI in the `.env` file:
     ```
     MONGODB_URI="your_mongodb_connection_uri"
     ```

4. **Create a `.env` File**:
   Add a `.env` file in the root directory with the following variables:
   ```ini
   OPENAI_API_KEY=<your_openai_api_key>
   MONGODB_URI=<your_mongodb_uri>
   ```

5. **Run the Main Script**:
   Execute the `main.py` script to run the entire pipeline:
   ```bash
   python main.py
   ```

## Script Descriptions:

### 1. **`main.py`**
Runs all the scripts in the required order and handles any errors during execution.

### 2. **`sentiment_analysis.py`**
Generates daily sentiment analysis based on client interactions.

- **Input**: Data from the `clientInteraction` collection.
- **Output**: Sentiment summary stored in `dailysentiments`.

### 3. **`risk_analysis.py`**
Analyzes portfolio risk based on daily changes and performance trends.

- **Input**: Data from the `portfolios` collection.
- **Output**: Risk scores and levels stored in `dailyrisks`.

### 4. **`client_satisfaction.py`**
Integrates daily sentiment and risk data to produce the final client satisfaction score.

- **Input**: Data from `dailysentiments` and `dailyrisks`.
- **Output**: Satisfaction levels and scores stored in `clientSatisfaction`.

## Dashboard Visualization:
The platform is designed to integrate with a user-friendly dashboard that visualizes the CRISP score, sentiment trends, and risk levels for each client (not included in this repository).

## Future Enhancements:
1. **Expand Portfolio Data**: Add more assets and performance metrics.
2. **Incorporate Market Trends**: Include external market data to contextualize client performance.
3. **Real-Time Updates**: Implement real-time data pipelines for continuous monitoring.

## Troubleshooting:
1. **MongoDB Connection Issues**:
   - Verify the MongoDB URI in the `.env` file.
   
2. **OpenAI API Errors**:
   - Ensure that your OpenAI API key is correctly set in the `.env` file.

3. **Script Execution Errors**:
   - Run each script individually to identify specific issues.

---

**Project Name**: **CRISP**  
**Author**: Sai Krishna Vishnumolakala, Siddu  
**Contact**: svishnu1@umbc.edu  
**Version**: 1.0.0  

---
