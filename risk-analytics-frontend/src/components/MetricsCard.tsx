"use client";

interface Metric {
  label: string;
  value: number | string;
  unit?: string;
  change?: number;
  format?: "currency" | "percentage" | "number" | "ratio";
}

interface MetricsCardProps {
  metrics: Metric[];
  title?: string;
}

export function MetricsCard({ metrics, title }: MetricsCardProps) {
  const formatValue = (metric: Metric): string => {
    const { value, format, unit } = metric;

    if (typeof value === "string") return value;

    switch (format) {
      case "currency":
        if (Math.abs(value) >= 1e9) {
          return `$${(value / 1e9).toFixed(2)}B`;
        } else if (Math.abs(value) >= 1e6) {
          return `$${(value / 1e6).toFixed(2)}M`;
        }
        return `$${value.toLocaleString()}`;
      case "percentage":
        return `${value.toFixed(2)}%`;
      case "ratio":
        return value.toFixed(2);
      case "number":
      default:
        return value.toLocaleString();
    }
  };

  const getChangeStyle = (change: number | undefined) => {
    if (change === undefined) return "";
    if (change > 0) return "text-green-600";
    if (change < 0) return "text-red-600";
    return "text-gray-600";
  };

  const getChangeIcon = (change: number | undefined) => {
    if (change === undefined) return null;
    if (change > 0) return "↑";
    if (change < 0) return "↓";
    return "→";
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      {title && (
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {metrics.map((metric, idx) => (
          <div
            key={idx}
            className="p-4 bg-gradient-to-br from-gray-50 to-blue-50 rounded-lg border border-gray-200"
          >
            <div className="text-xs font-medium text-gray-600 uppercase tracking-wide mb-1">
              {metric.label}
            </div>
            <div className="flex items-baseline justify-between">
              <div className="text-2xl font-bold text-gray-900">
                {formatValue(metric)}
                {metric.unit && (
                  <span className="text-sm font-normal text-gray-500 ml-1">
                    {metric.unit}
                  </span>
                )}
              </div>
              {metric.change !== undefined && (
                <div
                  className={`text-sm font-semibold ${getChangeStyle(
                    metric.change
                  )}`}
                >
                  {getChangeIcon(metric.change)} {Math.abs(metric.change)}%
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
