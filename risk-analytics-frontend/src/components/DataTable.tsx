export interface DataTableProps {
  title?: string;
  data: Record<string, any>[];
  themeColor: string;
  maxRows?: number;
}

export function DataTable({ title, data, themeColor, maxRows = 10 }: DataTableProps) {
  if (!data || data.length === 0) {
    return (
      <div
        className="rounded-lg p-8 text-center border"
        style={{
          backgroundColor: "rgba(255, 255, 255, 0.05)",
          borderColor: "rgba(255, 255, 255, 0.1)",
        }}
      >
        <p className="text-white/60">No data to display</p>
      </div>
    );
  }

  const columns = Object.keys(data[0]);
  const displayData = data.slice(0, maxRows);
  const hasMore = data.length > maxRows;

  return (
    <div
      className="rounded-lg shadow-lg border overflow-hidden"
      style={{
        backgroundColor: "rgba(255, 255, 255, 0.05)",
        borderColor: "rgba(255, 255, 255, 0.2)",
      }}
    >
      {title && (
        <div
          className="px-6 py-4 border-b"
          style={{
            backgroundColor: "rgba(255, 255, 255, 0.1)",
            borderColor: "rgba(255, 255, 255, 0.1)",
          }}
        >
          <h3 className="text-lg font-semibold text-white">{title}</h3>
          <p className="text-sm text-white/60 mt-1">
            Showing {displayData.length} of {data.length} rows
          </p>
        </div>
      )}

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr
              style={{
                backgroundColor: themeColor,
              }}
            >
              {columns.map((column) => (
                <th
                  key={column}
                  className="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider"
                >
                  {formatColumnName(column)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {displayData.map((row, rowIndex) => (
              <tr
                key={rowIndex}
                className="border-b border-white/10 hover:bg-white/5 transition-colors"
              >
                {columns.map((column) => (
                  <td
                    key={column}
                    className="px-6 py-4 whitespace-nowrap text-sm text-white/90"
                  >
                    {formatCellValue(row[column])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {hasMore && (
        <div
          className="px-6 py-3 text-center border-t"
          style={{
            backgroundColor: "rgba(255, 255, 255, 0.05)",
            borderColor: "rgba(255, 255, 255, 0.1)",
          }}
        >
          <p className="text-sm text-white/60">
            + {data.length - maxRows} more rows not displayed
          </p>
        </div>
      )}
    </div>
  );
}

function formatColumnName(name: string): string {
  return name
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatCellValue(value: any): string {
  if (value === null || value === undefined) {
    return "—";
  }
  
  if (typeof value === "number") {
    // Format large numbers with commas
    if (Math.abs(value) >= 1000) {
      return value.toLocaleString(undefined, { maximumFractionDigits: 2 });
    }
    return value.toFixed(2);
  }
  
  if (typeof value === "boolean") {
    return value ? "✓" : "✗";
  }
  
  if (value instanceof Date) {
    return value.toLocaleDateString();
  }
  
  if (typeof value === "object") {
    return JSON.stringify(value);
  }
  
  return String(value);
}
