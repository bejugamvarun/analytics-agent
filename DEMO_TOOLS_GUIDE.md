# Using Demo/Mock Tools

Since you don't have Snowflake configured, the agent now includes mock data generation tools that you can use to demonstrate the full functionality of the Risk Analytics Agent.

## UI Rendering Approach

**Important:** Tool results are now rendered in the **main UI area (left side)**, not inside the chat window. This provides:
- Full-width tables and visualizations
- Clean chat experience with just confirmation messages  
- Professional dashboard-like interface

See [UI_RENDERING_GUIDE.md](UI_RENDERING_GUIDE.md) for technical details.

## Available Mock Tools

### 1. `generate_mock_liquidity_data`
Generates random liquidity data (MLO metrics) for demonstration purposes.

**Example prompts:**
- "Generate some mock liquidity data"
- "Show me 50 rows of MLO data"
- "Create sample liquidity metrics for ENTITY_001"

**Returns:** A table with columns like date, entity, metric_type, value, variance_pct, currency, scenario **displayed in the main UI area**

### 2. `generate_variance_analysis`
Generates day-over-day variance analysis with percentage changes.

**Example prompts:**
- "Run a variance analysis"
- "Show me variance for ENTITY_002"
- "Analyze day-over-day changes"

**Returns:** A table showing current vs previous values with variance percentages **displayed in the main UI area**

### 3. `detect_mock_anomalies`
Generates mock anomaly detection results with severity levels.

**Example prompts:**
- "Detect anomalies in the data"
- "Find outliers with z-score > 3"
- "Show me any unusual patterns"

**Returns:** Anomaly cards showing HIGH/MEDIUM severity issues with deviation percentages **displayed in the main UI area**

### 4. `generate_mock_metrics`
Generates key liquidity risk metrics for the dashboard.

**Example prompts:**
- "Show me current metrics"
- "What are the latest liquidity ratios?"
- "Display key performance indicators"

**Returns:** Metric cards for MLO Total, HQLA Ratio, LCR, NSFR, etc. **displayed in the main UI area**

### 5. `list_mock_schemas`
Lists available database schemas and tables (mock data).

**Example prompts:**
- "What tables are available?"
- "List the schemas"
- "Show me the database structure"

**Returns:** A table with database, schema, and table names **displayed in the main UI area**

## How to Use

1. Start the frontend server:
   ```bash
   cd risk-analytics-frontend
   npm run dev
   ```

2. Start the agent server:
   ```bash
   # From the root directory
   python -m risk_analytics_agent.server
   ```

3. Open http://localhost:3000 in your browser

4. Try asking the agent things like:
   - "Generate some sample liquidity data and show me the top entities"
   - "Run a variance analysis and highlight any significant changes"
   - "Detect anomalies in the mock data"
   - "Show me the current metrics"
   - "What database schemas are available?"

## Dynamic UI Components

Tool results are rendered in the **main application area (left side)**, not inside the chat sidebar. The chat shows small confirmation messages like "✓ Data generated - Check main UI" while the actual visualization appears prominently in the main area.

### Component Types

The agent automatically renders different UI components based on the tool called:

- **DynamicTable**: For tabular data with sorting and pagination
- **MetricsCard**: For displaying key metrics in a grid layout
- **AnomalyCard**: For highlighting detected anomalies with severity indicators
- **DataTable**: (Original) For SQL query results

All components feature:
- Automatic number formatting (currency, percentages, ratios)
- Color-coded severity/status indicators
- Responsive layouts
- Pagination for large datasets

## Switching to Real Snowflake Data

When you're ready to connect to real Snowflake:

1. Configure `src/risk_analytics_agent/config/snowflake.yaml` with your credentials
2. Set the appropriate environment variables
3. The agent will automatically use the real sub-agents instead of mock tools
4. All the same UI components will work with real data
