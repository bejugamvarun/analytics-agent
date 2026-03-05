export interface AgentCapabilitiesProps {
  themeColor: string;
}

export function AgentCapabilities({ themeColor }: AgentCapabilitiesProps) {
  const capabilities = [
    {
      icon: "🔍",
      title: "Schema Discovery",
      description: "Explore databases, schemas, tables, and columns in Snowflake",
      examples: ["What data is available?", "Show me the tables", "List all schemas"],
    },
    {
      icon: "💾",
      title: "Data Retrieval",
      description: "Generate and execute safe SQL queries to fetch liquidity data",
      examples: ["Get MLO data for last week", "Query HQLA metrics", "Fetch recent stress scenarios"],
    },
    {
      icon: "📊",
      title: "Quantitative Analysis",
      description: "Compute statistics, percentiles, distributions, and correlations",
      examples: ["Calculate statistics", "Show distribution", "Correlation analysis"],
    },
    {
      icon: "📈",
      title: "Variance Analysis",
      description: "Track day-over-day metric changes and detect significant movements",
      examples: ["Analyze DoD variance", "Show daily changes", "Track metric trends"],
    },
    {
      icon: "🔎",
      title: "Drilldown Analysis",
      description: "Decompose changes across entity, FLB, and CUSIP hierarchies",
      examples: ["What's driving the change?", "Break down by entity", "Root-cause analysis"],
    },
    {
      icon: "⚠️",
      title: "Anomaly Detection",
      description: "Detect outliers using z-score, IQR, and rolling window methods",
      examples: ["Detect anomalies", "Find outliers", "Unusual patterns"],
    },
    {
      icon: "📄",
      title: "Report Generation",
      description: "Generate comprehensive HTML/PDF and Markdown reports with charts",
      examples: ["Generate report", "Create dashboard", "Export analysis"],
    },
  ];

  const analysisWorkflows = [
    {
      name: "Full Analysis Pipeline",
      steps: ["Schema Discovery", "Data Retrieval", "Variance Analysis", "Drilldown", "Report"],
    },
    {
      name: "Anomaly Investigation",
      steps: ["Data Retrieval", "Anomaly Detection", "Drilldown", "Report"],
    },
    {
      name: "Quick Data Exploration",
      steps: ["Schema Discovery", "Data Retrieval", "Quantitative Analysis"],
    },
    {
      name: "Variance Deep-dive",
      steps: ["Data Retrieval", "Variance Analysis", "Drilldown Analysis"],
    },
  ];

  return (
    <div className="w-full max-w-6xl mx-auto p-6 space-y-8">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-white mb-3">
          What I Can Do For You
        </h2>
        <p className="text-white/70 max-w-2xl mx-auto">
          I'm a specialized Risk Analytics Agent designed to help you analyze financial liquidity data,
          detect anomalies, and generate comprehensive reports.
        </p>
      </div>

      {/* Capabilities Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {capabilities.map((capability, idx) => (
          <div
            key={idx}
            className="rounded-lg p-5 shadow-lg border transition-all hover:scale-105"
            style={{
              backgroundColor: "rgba(255, 255, 255, 0.1)",
              borderColor: "rgba(255, 255, 255, 0.2)",
            }}
          >
            <div className="text-4xl mb-3">{capability.icon}</div>
            <h3 className="text-lg font-semibold text-white mb-2">
              {capability.title}
            </h3>
            <p className="text-sm text-white/70 mb-3">
              {capability.description}
            </p>
            <div className="space-y-1">
              {capability.examples.map((example, exIdx) => (
                <div
                  key={exIdx}
                  className="text-xs text-white/60 italic pl-3 border-l-2"
                  style={{ borderColor: themeColor }}
                >
                  "{example}"
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Common Workflows */}
      <div className="mt-12">
        <h3 className="text-2xl font-bold text-white mb-6 text-center">
          Common Analysis Workflows
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {analysisWorkflows.map((workflow, idx) => (
            <div
              key={idx}
              className="rounded-lg p-6 shadow-lg border"
              style={{
                backgroundColor: "rgba(255, 255, 255, 0.08)",
                borderColor: "rgba(255, 255, 255, 0.15)",
              }}
            >
              <h4 className="text-lg font-semibold text-white mb-4">
                {workflow.name}
              </h4>
              <div className="flex items-center gap-2 flex-wrap">
                {workflow.steps.map((step, stepIdx) => (
                  <div key={stepIdx} className="flex items-center">
                    <span
                      className="px-3 py-1 rounded-full text-xs font-medium text-white"
                      style={{ backgroundColor: themeColor }}
                    >
                      {step}
                    </span>
                    {stepIdx < workflow.steps.length - 1 && (
                      <span className="text-white/60 mx-2">→</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Financial Context */}
      <div
        className="rounded-lg p-6 shadow-lg border"
        style={{
          backgroundColor: "rgba(255, 255, 255, 0.05)",
          borderColor: "rgba(255, 255, 255, 0.1)",
        }}
      >
        <h3 className="text-lg font-semibold text-white mb-3">
          📊 Financial Context
        </h3>
        <p className="text-white/80 text-sm leading-relaxed">
          I specialize in analyzing <strong>MLO (Modeled Liquidity Outflow)</strong>, 
          <strong> HQLA</strong>, <strong>stress scenarios</strong>, <strong>cash flows</strong>, 
          <strong> concentration risk</strong>, and <strong>regulatory metrics</strong>. 
          All data is sourced from Snowflake and analyzed using industry-standard methodologies.
        </p>
      </div>

      {/* Get Started CTA */}
      <div className="text-center">
        <div
          className="inline-block rounded-lg p-8 shadow-xl"
          style={{
            backgroundColor: "rgba(255, 255, 255, 0.1)",
          }}
        >
          <h3 className="text-xl font-bold text-white mb-3">
            Ready to get started?
          </h3>
          <p className="text-white/70 mb-4">
            Try one of the suggested prompts or ask me anything about your liquidity data!
          </p>
          <div className="flex gap-3 justify-center flex-wrap">
            <span className="px-4 py-2 rounded-full text-sm bg-white/20 text-white">
              💬 Use the chat panel
            </span>
            <span className="px-4 py-2 rounded-full text-sm bg-white/20 text-white">
              🎯 Try a suggestion
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
