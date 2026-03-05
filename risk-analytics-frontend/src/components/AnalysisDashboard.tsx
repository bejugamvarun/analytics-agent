import { AgentState } from "@/lib/types";

export interface AnalysisDashboardProps {
  state: AgentState;
  themeColor: string;
}

export function AnalysisDashboard({ state, themeColor }: AnalysisDashboardProps) {
  const metrics = state.latestMetrics || {};
  const analysis = state.currentAnalysis;
  const dbInfo = state.databaseInfo;

  return (
    <div className="w-full max-w-6xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">
          Risk Analytics Dashboard
        </h1>
        <p className="text-white/70">
          Financial Liquidity Risk Monitoring & Analysis
        </p>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="MLO Total"
          value={metrics.mloTotal ? `$${(metrics.mloTotal / 1e9).toFixed(2)}B` : "—"}
          themeColor={themeColor}
        />
        <MetricCard
          title="DoD Variance"
          value={metrics.variancePercent ? `${metrics.variancePercent.toFixed(2)}%` : "—"}
          themeColor={themeColor}
          trend={metrics.variancePercent}
        />
        <MetricCard
          title="Anomalies Detected"
          value={metrics.anomalyCount?.toString() || "—"}
          themeColor={themeColor}
          alert={!!(metrics.anomalyCount && metrics.anomalyCount > 0)}
        />
        <MetricCard
          title="Last Update"
          value={metrics.lastUpdateDate || "—"}
          themeColor={themeColor}
        />
      </div>

      {/* Current Analysis Status */}
      {analysis && (
        <div
          className="rounded-lg p-6 shadow-lg border"
          style={{
            backgroundColor: "rgba(255, 255, 255, 0.1)",
            borderColor: "rgba(255, 255, 255, 0.2)",
          }}
        >
          <h2 className="text-xl font-semibold text-white mb-4">
            Current Analysis: {analysis.type}
          </h2>
          <div className="space-y-2">
            <div className="flex items-center justify-between text-white/90">
              <span>Status: {analysis.status}</span>
              <span>{analysis.progress}%</span>
            </div>
            <div className="w-full bg-white/20 rounded-full h-2">
              <div
                className="h-2 rounded-full transition-all duration-300"
                style={{
                  width: `${analysis.progress}%`,
                  backgroundColor: themeColor,
                }}
              />
            </div>
          </div>
        </div>
      )}

      {/* Database Connection Info */}
      {dbInfo && (
        <div
          className="rounded-lg p-4 shadow border"
          style={{
            backgroundColor: "rgba(255, 255, 255, 0.05)",
            borderColor: "rgba(255, 255, 255, 0.15)",
          }}
        >
          <div className="flex items-center justify-between text-white/80 text-sm">
            <div className="flex items-center gap-4">
              {dbInfo.connectedDatabase && (
                <span>📊 Database: {dbInfo.connectedDatabase}</span>
              )}
              {dbInfo.availableSchemas && dbInfo.availableSchemas.length > 0 && (
                <span>📁 Schemas: {dbInfo.availableSchemas.length}</span>
              )}
            </div>
            {dbInfo.lastQuery && (
              <span className="text-xs text-white/60">
                Last query: {new Date(dbInfo.lastQuery).toLocaleTimeString()}
              </span>
            )}
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <ActionButton icon="🔍" label="Discover Data" themeColor={themeColor} />
        <ActionButton icon="📊" label="Variance Analysis" themeColor={themeColor} />
        <ActionButton icon="⚠️" label="Detect Anomalies" themeColor={themeColor} />
        <ActionButton icon="📄" label="Generate Report" themeColor={themeColor} />
      </div>
    </div>
  );
}

interface MetricCardProps {
  title: string;
  value: string;
  themeColor: string;
  trend?: number;
  alert?: boolean;
}

function MetricCard({ title, value, themeColor, trend, alert }: MetricCardProps) {
  return (
    <div
      className="rounded-lg p-4 shadow-lg border transition-all hover:scale-105"
      style={{
        backgroundColor: "rgba(255, 255, 255, 0.1)",
        borderColor: alert ? "#ef4444" : "rgba(255, 255, 255, 0.2)",
      }}
    >
      <h3 className="text-sm font-medium text-white/70 mb-1">{title}</h3>
      <div className="flex items-baseline gap-2">
        <p className="text-2xl font-bold text-white">{value}</p>
        {trend !== undefined && trend !== 0 && (
          <span
            className={`text-sm ${trend > 0 ? "text-green-400" : "text-red-400"}`}
          >
            {trend > 0 ? "↑" : "↓"} {Math.abs(trend).toFixed(1)}%
          </span>
        )}
        {alert && <span className="text-xl">⚠️</span>}
      </div>
    </div>
  );
}

interface ActionButtonProps {
  icon: string;
  label: string;
  themeColor: string;
}

function ActionButton({ icon, label, themeColor }: ActionButtonProps) {
  return (
    <button
      className="rounded-lg p-4 text-white font-medium transition-all hover:scale-105 active:scale-95 shadow-md"
      style={{
        backgroundColor: "rgba(255, 255, 255, 0.15)",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.backgroundColor = themeColor;
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.backgroundColor = "rgba(255, 255, 255, 0.15)";
      }}
    >
      <div className="text-2xl mb-1">{icon}</div>
      <div className="text-sm">{label}</div>
    </button>
  );
}
