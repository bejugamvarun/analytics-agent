# Risk Analytics Agent UI

This is a CopilotKit UI for the Risk Analytics Agent, built using Google's [ADK](https://google.github.io/adk-docs/) and [CopilotKit](https://copilotkit.ai). It provides a modern Next.js application with an integrated financial liquidity risk analytics agent that can analyze MLO (Modeled Liquidity Outflow) data, perform variance analysis, detect anomalies, and generate comprehensive reports.

## Prerequisites

- Node.js 18+
- Python 3.12+
- Google Makersuite API Key (for the ADK agent) (see https://makersuite.google.com/app/apikey)
- Any of the following package managers:
  - pnpm (recommended)
  - npm
  - yarn
  - bun

> **Note:** This repository ignores lock files (package-lock.json, yarn.lock, pnpm-lock.yaml, bun.lockb) to avoid conflicts between different package managers. Each developer should generate their own lock file using their preferred package manager. After that, make sure to delete it from the .gitignore.

## Getting Started

1. Install dependencies using your preferred package manager:
```bash
# Using pnpm (recommended)
pnpm install

# Using npm
npm install

# Using yarn
yarn install

# Using bun
bun install
```

2. Install Python dependencies for the ADK agent:
```bash
# Using pnpm
pnpm install:agent

# Using npm
npm run install:agent

# Using yarn
yarn install:agent

# Using bun
bun run install:agent
```

> **Note:** This will automatically setup a `.venv` (virtual environment) in the root project directory.
>
> To activate the virtual environment manually, you can run:
> ```bash
> source ../../.venv/bin/activate  # From the risk-analytics-frontend directory
> # or
> source .venv/bin/activate  # From the root directory
> ```


3. Set up your Google API key and other required environment variables:
```bash
export GOOGLE_API_KEY="your-google-api-key-here"
# See root .env.example for other required variables
```

4. Start the servers independently:

**Terminal 1 - Start the UI:**
```bash
# Using pnpm
pnpm dev

# Using npm
npm run dev

# Using yarn
yarn dev

# Using bun
bun run dev
```

**Terminal 2 - Start the Agent Server:**
```bash
# Using pnpm
pnpm dev:agent

# Using npm
npm run dev:agent

# Using yarn
yarn dev:agent

# Using bun
bun run dev:agent
```

This will start:
- UI on port 3000
- Agent server on port 8000

## Available Scripts
The following scripts can also be run using your preferred package manager:
- `dev` - Starts the Next.js UI server in development mode
- `dev:agent` - Starts the ADK agent server
- `build` - Builds the Next.js application for production
- `start` - Starts the production server
- `lint` - Runs ESLint for code linting
- `install:agent` - Installs Python dependencies for the agent

## Documentation

The main UI component is in `src/app/page.tsx`. You can:
- Modify the theme colors and styling
- Add new frontend actions
- Customize the CopilotKit sidebar appearance

The Risk Analytics Agent is located in the root `src/risk_analytics_agent` directory and includes:
- Multi-agent orchestration system
- Sub-agents for data retrieval, variance analysis, anomaly detection, and report generation
- Snowflake database integration for liquidity data analysis

## 📚 Documentation

- [ADK Documentation](https://google.github.io/adk-docs/) - Learn more about the ADK and its features
- [CopilotKit Documentation](https://docs.copilotkit.ai) - Explore CopilotKit's capabilities
- [Next.js Documentation](https://nextjs.org/docs) - Learn about Next.js features and API


## Contributing

Feel free to submit issues and enhancement requests! This starter is designed to be easily extensible.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Agent Connection Issues
If you see "I'm having trouble connecting to my tools", make sure:
1. The Risk Analytics Agent server is running on port 8000
2. Your Google API key and other required environment variables are set correctly
3. Both servers (UI and agent) started successfully
4. The Snowflake connection is configured properly (if using database features)

### Python Dependencies
If you encounter Python import errors:
```bash
cd ../..  # Navigate to root directory
source .venv/bin/activate
uv sync
```