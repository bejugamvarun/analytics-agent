"use client";

import { useState } from "react";

interface DynamicTableProps {
  data: any[];
  title?: string;
  maxRows?: number;
}

export function DynamicTable({ data, title, maxRows = 20 }: DynamicTableProps) {
  const [currentPage, setCurrentPage] = useState(1);
  const rowsPerPage = 10;

  if (!data || data.length === 0) {
    return (
      <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
        <p className="text-gray-500 text-center">No data available</p>
      </div>
    );
  }

  const columns = Object.keys(data[0]);
  const displayData = data.slice(0, maxRows);
  const totalPages = Math.ceil(displayData.length / rowsPerPage);
  const startIdx = (currentPage - 1) * rowsPerPage;
  const endIdx = startIdx + rowsPerPage;
  const currentData = displayData.slice(startIdx, endIdx);

  const formatValue = (value: any): string => {
    if (value === null || value === undefined) return "-";
    if (typeof value === "number") {
      if (Math.abs(value) >= 1e9) {
        return `$${(value / 1e9).toFixed(2)}B`;
      } else if (Math.abs(value) >= 1e6) {
        return `$${(value / 1e6).toFixed(2)}M`;
      } else if (Number.isInteger(value)) {
        return value.toLocaleString();
      } else {
        return value.toFixed(2);
      }
    }
    if (typeof value === "boolean") return value ? "✓" : "✗";
    return String(value);
  };

  const formatColumnName = (col: string): string => {
    return col
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      {title && (
        <div className="px-4 py-3 bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          <p className="text-sm text-gray-600 mt-1">
            Showing {startIdx + 1}-{Math.min(endIdx, displayData.length)} of{" "}
            {displayData.length} rows
          </p>
        </div>
      )}

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gradient-to-r from-gray-50 to-gray-100">
            <tr>
              {columns.map((col) => (
                <th
                  key={col}
                  className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider border-b-2 border-gray-300"
                >
                  {formatColumnName(col)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {currentData.map((row, idx) => (
              <tr
                key={idx}
                className="hover:bg-blue-50 transition-colors duration-150"
              >
                {columns.map((col) => (
                  <td
                    key={col}
                    className="px-4 py-3 text-sm text-gray-900 whitespace-nowrap"
                  >
                    {formatValue(row[col])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="px-4 py-3 bg-gray-50 border-t border-gray-200 flex items-center justify-between">
          <button
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            disabled={currentPage === 1}
            className="px-3 py-1 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <span className="text-sm text-gray-700">
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
            className="px-3 py-1 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
