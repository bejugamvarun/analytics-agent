"use client";

interface Anomaly {
  entity: string;
  date: string;
  metric: string;
  value: number;
  expected_value: number;
  z_score: number;
  deviation_pct: number;
  severity: "HIGH" | "MEDIUM" | "LOW";
}

interface AnomalyCardProps {
  anomalies: Anomaly[];
  title?: string;
}

export function AnomalyCard({ anomalies, title }: AnomalyCardProps) {
  if (!anomalies || anomalies.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          {title || "Anomalies"}
        </h3>
        <div className="text-center py-8 text-gray-500">
          <div className="text-4xl mb-2">✓</div>
          <p>No anomalies detected</p>
        </div>
      </div>
    );
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "HIGH":
        return "bg-red-100 text-red-800 border-red-300";
      case "MEDIUM":
        return "bg-yellow-100 text-yellow-800 border-yellow-300";
      case "LOW":
        return "bg-blue-100 text-blue-800 border-blue-300";
      default:
        return "bg-gray-100 text-gray-800 border-gray-300";
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case "HIGH":
        return "🔴";
      case "MEDIUM":
        return "🟡";
      case "LOW":
        return "🔵";
      default:
        return "⚪";
    }
  };

  const formatCurrency = (value: number) => {
    if (Math.abs(value) >= 1e9) {
      return `$${(value / 1e9).toFixed(2)}B`;
    } else if (Math.abs(value) >= 1e6) {
      return `$${(value / 1e6).toFixed(2)}M`;
    }
    return `$${value.toLocaleString()}`;
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">
          {title || "Detected Anomalies"}
        </h3>
        <span className="px-3 py-1 bg-red-100 text-red-800 text-sm font-medium rounded-full">
          {anomalies.length} Anomalies
        </span>
      </div>

      <div className="space-y-3">
        {anomalies.map((anomaly, idx) => (
          <div
            key={idx}
            className={`p-4 rounded-lg border-l-4 ${
              anomaly.severity === "HIGH"
                ? "bg-red-50 border-red-500"
                : anomaly.severity === "MEDIUM"
                ? "bg-yellow-50 border-yellow-500"
                : "bg-blue-50 border-blue-500"
            }`}
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="text-lg">{getSeverityIcon(anomaly.severity)}</span>
                <div>
                  <div className="font-semibold text-gray-900">
                    {anomaly.entity}
                  </div>
                  <div className="text-xs text-gray-600">{anomaly.date}</div>
                </div>
              </div>
              <span
                className={`px-2 py-1 text-xs font-semibold rounded border ${getSeverityColor(
                  anomaly.severity
                )}`}
              >
                {anomaly.severity}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3 mt-3 text-sm">
              <div className="bg-white p-2 rounded">
                <div className="text-xs text-gray-600">Actual Value</div>
                <div className="font-semibold text-gray-900">
                  {formatCurrency(anomaly.value)}
                </div>
              </div>
              <div className="bg-white p-2 rounded">
                <div className="text-xs text-gray-600">Expected Value</div>
                <div className="font-semibold text-gray-900">
                  {formatCurrency(anomaly.expected_value)}
                </div>
              </div>
              <div className="bg-white p-2 rounded">
                <div className="text-xs text-gray-600">Deviation</div>
                <div
                  className={`font-semibold ${
                    anomaly.deviation_pct > 0 ? "text-red-600" : "text-green-600"
                  }`}
                >
                  {anomaly.deviation_pct > 0 ? "+" : ""}
                  {anomaly.deviation_pct.toFixed(2)}%
                </div>
              </div>
              <div className="bg-white p-2 rounded">
                <div className="text-xs text-gray-600">Z-Score</div>
                <div className="font-semibold text-gray-900">
                  {anomaly.z_score.toFixed(2)}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
