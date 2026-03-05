# Rendering UI in Main Area vs Chat Window

## Overview

The application now renders dynamic content (tables, metrics, anomalies) in the **main UI area (left side)** instead of inside the chat window. This provides:

- ✅ **Full-width content display** in the main application area
- ✅ **Clean chat window** with just confirmation messages
- ✅ **Better user experience** - data doesn't clutter the conversation
- ✅ **Fixed-width chat preserved** - CopilotKit sidebar remains at optimal width

## How It Works

### 1. Backend: Tools Store Data in State

Each mock tool now stores its results in a special `ui_display` key in the agent state:

```python
# In mock_tools.py
tool_context.state["ui_display"] = {
    "type": "table",  # or "metrics", "anomalies"
    "title": "Mock Liquidity Data",
    "data": result_data,
    "timestamp": datetime.now().isoformat(),
}
```

**Supported types:**
- `"table"` - Displays data in DynamicTable component
- `"metrics"` - Shows metrics in grid cards
- `"anomalies"` - Renders anomaly cards with severity indicators

### 2. Frontend: State Rendering in Main UI

The frontend uses `useCoAgent` to access agent state and renders `ui_display` in the main content area:

```tsx
// In page.tsx
const { state } = useCoAgent({ name: "risk_analytics_agent" });
const uiDisplay = (state as any)?.ui_display;

// Render in main UI based on type
{uiDisplay?.type === "table" && <DynamicTable data={uiDisplay.data} />}
{uiDisplay?.type === "anomalies" && <AnomalyCard anomalies={uiDisplay.data} />}
{uiDisplay?.type === "metrics" && <MetricsCard metrics={...} />}
```

### 3. Chat: Minimal Confirmation Messages

Tool renderers in the chat (`useRenderToolCall`) now just show small confirmation badges:

```tsx
useRenderToolCall({
  name: "generate_mock_liquidity_data",
  render: () => (
    <div className="my-2 px-3 py-2 bg-blue-500/20 rounded">
      ✓ Liquidity data generated - Check main UI
    </div>
  ),
});
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Browser Window                          │
├──────────────────────────────────┬──────────────────────────┤
│                                  │                          │
│   MAIN UI AREA (LEFT)           │  CHAT SIDEBAR (RIGHT)    │
│   ├── Agent State Rendering      │  ├── Conversation       │
│   │   ├── Tables (DynamicTable) │  │   └── Messages       │
│   │   ├── Metrics Cards          │  ├── Tool Confirmations │
│   │   └── Anomaly Cards          │  │   └── "✓ Check UI" │
│   │                               │  └── Input Box         │
│   └── Dashboard/Capabilities     │                          │
│       (when no ui_display)        │   (Fixed Width)         │
│                                  │                          │
│   (Flexible Width)                │                          │
└──────────────────────────────────┴──────────────────────────┘
         ↑                                  ↑
         │                                  │
    State Sync                          Tool Calls
         │                                  │
    ┌────┴──────────────────────────────────┴────┐
    │      CopilotKit Runtime (WebSocket)         │
    └─────────────────┬──────────────────────────┘
                      │
                      ↓
              ┌──────────────┐
              │  FastAPI     │
              │  ADK Agent   │
              │  Mock Tools  │
              └──────────────┘
```

## User Flow Example

1. **User asks:** "Show me some liquidity data"
2. **Agent calls:** `generate_mock_liquidity_data()` tool
3. **Tool stores:** `ui_display` in agent state with type "table"
4. **Chat shows:** Small confirmation badge "✓ Liquidity data generated"
5. **Main UI renders:** Full-width table with 50 rows of data
6. **State persists:** Until next tool call updates `ui_display`

## Benefits

### Before (Tool Rendering in Chat)
- ❌ Tables cramped in narrow chat window
- ❌ Scrolling through long data disrupts conversation
- ❌ Hard to read wide tables
- ❌ Chat window bloated with data

### After (State Rendering in Main UI)
- ✅ Full-width tables with plenty of space
- ✅ Clean chat keeps focus on conversation
- ✅ Easy to read and analyze data
- ✅ Professional dashboard-like experience

## Customization

### Adding New Display Types

1. **Backend:** Add new type in tool
```python
tool_context.state["ui_display"] = {
    "type": "chart",  # New type
    "title": "Trend Analysis",
    "data": chart_data,
}
```

2. **Frontend:** Add renderer in page.tsx
```tsx
{uiDisplay?.type === "chart" && (
  <MyChartComponent data={uiDisplay.data} />
)}
```

### Styling

Main UI containers use:
- `bg-white/10 backdrop-blur-sm` - Translucent background
- `border border-white/20` - Subtle border
- `rounded-lg p-6` - Rounded corners and padding

Customize the theme color via the color picker in the UI (top-left controls icon).

## Testing

Try these prompts:
- "Generate some mock liquidity data" → See table in main UI
- "Run a variance analysis" → See variance table in main UI
- "Detect anomalies" → See anomaly cards in main UI
- "Show me current metrics" → See metrics grid in main UI
- "What tables are available?" → See schema list in main UI

All results appear in the main content area while chat stays clean!
