import { AnalysisResult } from "@/lib/types";

export interface AnalysisResultsProps {
  results: AnalysisResult[];
  themeColor: string;
}

export function AnalysisResults({ results, themeColor }: AnalysisResultsProps) {
  if (!results || results.length === 0) {
    return (
      <div className="w-full max-w-4xl mx-auto p-8 text-center">
        <div
          className="rounded-lg p-12 border"
          style={{
            backgroundColor: "rgba(255, 255, 255, 0.05)",
            borderColor: "rgba(255, 255, 255, 0.1)",
          }}
        >
          <div className="text-6xl mb-4">📊</div>
          <h3 className="text-xl font-semibold text-white/80 mb-2">
            No Analysis Results Yet
          </h3>
          <p className="text-white/60">
            Ask the agent to perform variance analysis, anomaly detection, or generate reports
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full max-w-4xl mx-auto p-6 space-y-4">
      <h2 className="text-2xl font-bold text-white mb-4">Analysis Results</h2>
      {results.map((result) => (
        <ResultCard key={result.id} result={result} themeColor={themeColor} />
      ))}
    </div>
  );
}

interface ResultCardProps {
  result: AnalysisResult;
  themeColor: string;
}

function ResultCard({ result, themeColor }: ResultCardProps) {
  const typeIcons = {
    variance: "📈",
    anomaly: "⚠️",
    drilldown: "🔍",
    quantitative: "📊",
  };

  const typeColors = {
    variance: "#3b82f6",
    anomaly: "#ef4444",
    drilldown: "#8b5cf6",
    quantitative: "#10b981",
  };

  return (
    <div
      className="rounded-lg p-6 shadow-lg border transition-all hover:shadow-xl"
      style={{
        backgroundColor: "rgba(255, 255, 255, 0.1)",
        borderColor: "rgba(255, 255, 255, 0.2)",
      }}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-3xl">{typeIcons[result.type]}</span>
          <div>
            <h3 className="text-lg font-semibold text-white capitalize">
              {result.type} Analysis
            </h3>
            <p className="text-sm text-white/60">
              {new Date(result.timestamp).toLocaleString()}
            </p>
          </div>
        </div>
        <span
          className="px-3 py-1 rounded-full text-xs font-medium text-white"
          style={{ backgroundColor: typeColors[result.type] }}
        >
          {result.type}
        </span>
      </div>

      <p className="text-white/90 mb-4">{result.summary}</p>

      {result.metrics && result.metrics.length > 0 && (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-4">
          {result.metrics.map((metric, idx) => (
            <div
              key={idx}
              className="rounded p-3"
              style={{
                backgroundColor: "rgba(255, 255, 255, 0.05)",
              }}
            >
              <p className="text-xs text-white/60 mb-1">{metric.label}</p>
              <div className="flex items-baseline gap-1">
                <p className="text-lg font-semibold text-white">
                  {metric.value}
                </p>
                {metric.unit && (
                  <span className="text-xs text-white/60">{metric.unit}</span>
                )}
                {metric.change !== undefined && metric.change !== 0 && (
                  <span
                    className={`text-xs ml-auto ${
                      metric.change > 0 ? "text-green-400" : "text-red-400"
                    }`}
                  >
                    {metric.change > 0 ? "↑" : "↓"} {Math.abs(metric.change).toFixed(1)}%
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {result.details && Object.keys(result.details).length > 0 && (
        <details className="mt-4">
          <summary
            className="cursor-pointer text-sm font-medium text-white/80 hover:text-white"
            style={{ color: themeColor }}
          >
            View detailed results
          </summary>
          <div
            className="mt-3 p-4 rounded text-xs font-mono text-white/70 overflow-auto max-h-64"
            style={{
              backgroundColor: "rgba(0, 0, 0, 0.3)",
            }}
          >
            <pre>{JSON.stringify(result.details, null, 2)}</pre>
          </div>
        </details>
      )}
    </div>
  );
}
