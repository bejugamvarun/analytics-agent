# Running the Risk Analytics Agent

## Overview

The application now uses the **ADK App class with InMemoryRunner** for better lifecycle management and follows ADK best practices.

## Architecture

```
agent.py
├── root_agent (orchestrator_agent)
└── app (App object wrapping root_agent)

app.py
├── InMemoryRunner(app=app)
├── run_simple()  - One-shot queries
├── run_cli()     - Interactive mode
└── main()        - CLI entry point

main.py
└── Application entry point
```

## Ways to Run

### 1. Interactive CLI (Recommended for Testing)

```bash
# Using main.py
python main.py

# Or using app.py directly
python src/risk_analytics_agent/app.py
```

**Features**:
- Interactive conversation mode
- Session persistence during the session
- Type `quit`, `exit`, or `q` to exit
- Emoji indicators (🔵 You, 🤖 Agent)

### 2. Single Query Mode

```bash
# Pass query as command line argument
python main.py "What schemas are available in the liquidity database?"

# Or in code
python -c "import asyncio; from risk_analytics_agent.app import run_simple; print(asyncio.run(run_simple('Hello')))"
```

### 3. ADK CLI (Official ADK Commands)

```bash
# Web UI (browser-based interface)
adk web src/risk_analytics_agent/agent.py

# Command line (interactive terminal)
adk run src/risk_analytics_agent/agent.py

# API Server (REST API)
adk api_server src/risk_analytics_agent/agent.py
```

### 4. Demo Mode

```python
# Edit app.py to use demo() instead of main()
if __name__ == "__main__":
    asyncio.run(demo())
```

Or run directly:
```bash
python -c "import asyncio; from risk_analytics_agent.app import demo; asyncio.run(demo())"
```

## Code Examples

### Simple One-Shot Query

```python
import asyncio
from risk_analytics_agent.app import run_simple

async def query_agent():
    response = await run_simple(
        "Calculate MLO variance between March 1 and March 15"
    )
    print(response)

asyncio.run(query_agent())
```

### Multiple Queries with Session

```python
import asyncio
from google.adk.runners import InMemoryRunner
from risk_analytics_agent.agent import app
from risk_analytics_agent.app import run_single_query

async def multi_query():
    runner = InMemoryRunner(app=app)
    
    queries = [
        "What schemas are available?",
        "Show me MLO data for March 1st",
        "Detect anomalies in yesterday's data",
    ]
    
    session_id = None
    for query in queries:
        print(f"\nQuery: {query}")
        response = await run_single_query(
            runner=runner,
            query=query,
            session_id=session_id,
        )
        print(f"Response: {response}\n")

asyncio.run(multi_query())
```

### Custom Runner Configuration

```python
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from risk_analytics_agent.agent import app

# Create custom runner
runner = InMemoryRunner(
    app=app,
    # session_service=custom_session_service,  # Optional
    # plugins=[...],  # Optional plugins
)

# Use runner.run() for streaming responses
async for event in runner.run(
    user_id="user123",
    new_message=content,
):
    # Process events
    pass
```

## InMemoryRunner vs Runner

| Feature | InMemoryRunner | Runner (Old) |
|---------|----------------|--------------|
| **App Support** | ✅ Yes (recommended) | ❌ Agent only |
| **Session Management** | ✅ Built-in | ⚙️ Manual setup required |
| **Lifecycle Hooks** | ✅ Via App | ❌ No |
| **Plugin Support** | ✅ Via App | ❌ No |
| **Simplicity** | ✅ Less boilerplate | ❌ More setup code |
| **run_debug()** | ✅ Yes (ADK 1.18+) | ❌ No |

## Environment Setup

```bash
# 1. Activate virtual environment
.\.venv\Scripts\Activate.ps1  # PowerShell
# Or: source .venv/bin/activate  # Linux/Mac

# 2. Install dependencies (if not done)
pip install -e .

# 3. Set environment variables
# Create .env file:
GOOGLE_API_KEY=your_key_here
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse

# 4. Run the app
python main.py
```

## Features of App-Based Approach

### 1. Centralized Configuration
```python
app = App(
    name="risk_analytics_agent",
    root_agent=root_agent,
    plugins=[logging_plugin, monitoring_plugin],
    context_cache_config=cache_config,
    resumability_config=resume_config,
)
```

### 2. Lifecycle Hooks (Future Enhancement)
```python
@app.on_startup
async def startup():
    # Initialize database connections
    # Load configurations
    # Warm up caches
    pass

@app.on_shutdown
async def shutdown():
    # Close database connections
    # Save state
    # Cleanup resources
    pass
```

### 3. Application-Level State
```python
# State with app: prefix is scoped to the entire app
app_state = context.get_state("app:connection_pool")
```

## Troubleshooting

### "run_debug() not available"
- **Cause**: ADK version < 1.18.0
- **Solution**: Upgrade ADK: `pip install --upgrade google-adk`
- **Fallback**: The code automatically falls back to `run_single_query()`

### "Module not found: google.adk"
- **Cause**: ADK not installed
- **Solution**: `pip install google-adk>=1.25.0`

### Session not persisting
- **Expected**: InMemoryRunner sessions are in-memory only
- **For persistence**: Use a custom session service (Redis, database, etc.)

### Skills not loading
- **Check**: ADK version >= 1.25.0 for Skills support
- **Test**: `python skills/test_skills.py`

## Comparison: Before vs After

### Before (Direct Runner)
```python
# More boilerplate
session_service = InMemorySessionService()
session = await session_service.create_session(...)

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

async for event in runner.run_async(
    user_id=USER_ID,
    session_id=session.id,
    new_message=content,
):
    # process event
```

### After (App + InMemoryRunner)
```python
# Much simpler
runner = InMemoryRunner(app=app)

# One-liner for simple queries
response = await runner.run_debug("Hello")

# Or streaming
async for event in runner.run(user_id=USER_ID, new_message=content):
    # process event
```

## Next Steps

1. **Try it out**: `python main.py`
2. **Test single queries**: `python main.py "What can you help with?"`
3. **Use ADK Web UI**: `adk web src/risk_analytics_agent/agent.py`
4. **Add lifecycle hooks**: Enhance the App with startup/shutdown logic
5. **Implement plugins**: Add observability, logging, or custom plugins
6. **Deploy**: The App is a deployable unit ready for production

## Resources

- [ADK Apps Documentation](https://google.github.io/adk-docs/apps/)
- [ADK Runtime Documentation](https://google.github.io/adk-docs/runtime/)
- [InMemoryRunner API](https://google.github.io/adk-docs/api-reference/)
