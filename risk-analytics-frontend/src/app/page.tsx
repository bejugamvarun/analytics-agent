"use client";

import { AnalysisDashboard } from "@/components/AnalysisDashboard";
import { AnalysisResults } from "@/components/AnalysisResults";
import { AgentCapabilities } from "@/components/AgentCapabilities";
import { DataTable } from "@/components/DataTable";
import { DynamicTable } from "@/components/DynamicTable";
import { MetricsCard } from "@/components/MetricsCard";
import { AnomalyCard } from "@/components/AnomalyCard";
import { AgentState } from "@/lib/types";
import {
  useCoAgent,
  useRenderToolCall,
} from "@copilotkit/react-core";
import { CopilotKitCSSProperties, CopilotSidebar } from "@copilotkit/react-ui";
import { useState } from "react";

export default function CopilotKitPage() {
  const [themeColor, setThemeColor] = useState("#1e40af");

  return (
    <main
      style={
        { "--copilot-kit-primary-color": themeColor } as CopilotKitCSSProperties
      }
    >
      <CopilotSidebar
        disableSystemMessage={true}
        clickOutsideToClose={false}
        defaultOpen={true}
        labels={{
          title: "Risk Analytics Agent",
          initial: "👋 Hi! I'm your Risk Analytics Agent. I can help you analyze liquidity data, perform variance analysis, detect anomalies, and generate reports.",
        }}
        suggestions={[
          {
            title: "Data Discovery",
            message: "What schemas and tables are available in the liquidity database?",
          },
          {
            title: "Variance Analysis",
            message: "Analyze MLO variance for the latest date available.",
          },
          {
            title: "Anomaly Detection",
            message: "Detect anomalies in the recent liquidity data.",
          },
          {
            title: "Report Generation",
            message: "Generate a comprehensive liquidity analysis report.",
          },
          {
            title: "Help",
            message: "What can you help me with?",
          },
        ]}
      >
        <RiskAnalyticsContent themeColor={themeColor} />
      </CopilotSidebar>
    </main>
  );
}

function RiskAnalyticsContent({ themeColor }: { themeColor: string }) {
  const { state, setState } = useCoAgent<AgentState>({
    name: "risk_analytics_agent",
    initialState: {
      latestMetrics: {
        mloTotal: 0,
        variancePercent: 0,
        anomalyCount: 0,
        lastUpdateDate: new Date().toLocaleDateString(),
      },
      analysisResults: [],
    },
  });

  // Get the ui_display from agent state to render in main UI
  const uiDisplay = (state as any)?.ui_display;

  // Render data query results as tables (minimal in chat)
  useRenderToolCall(
    {
      name: "display_query_results",
      description: "Display SQL query results in a table format",
      parameters: [
        { name: "data", type: "object", required: true },
        { name: "query", type: "string", required: false },
      ],
      render: ({ args }) => {
        return (
          <div className="my-2 px-3 py-2 bg-white/10 rounded text-sm text-white/80">
            ✓ Query results displayed in main UI
          </div>
        );
      },
    },
    [themeColor]
  );

  // Render analysis results with metrics
  useRenderToolCall(
    {
      name: "display_analysis_results",
      description: "Display analysis results with metrics and visualizations",
      parameters: [
        { name: "results", type: "object", required: true },
        { name: "type", type: "string", required: true },
      ],
      render: ({ args, result }) => {
        return (
          <div className="my-2 px-3 py-2 bg-white/10 rounded text-sm text-white/80">
            ✓ Analysis results displayed in main UI
          </div>
        );
      },
    },
    [themeColor]
  );

  // Render metric cards
  useRenderToolCall(
    {
      name: "display_metrics",
      description: "Display key metrics in card format",
      parameters: [
        { name: "metrics", type: "object", required: true },
      ],
      render: ({ args }) => {
        return (
          <div className="my-2 px-3 py-2 bg-white/10 rounded text-sm text-white/80">
            ✓ Metrics displayed in main UI
          </div>
        );
      },
    },
    [themeColor]
  );

  // Minimal tool renderers - just show confirmation in chat
  useRenderToolCall(
    {
      name: "generate_mock_liquidity_data",
      description: "Generate and display mock liquidity data",
      parameters: [
        { name: "num_rows", type: "number", required: false },
        { name: "metric_type", type: "string", required: false },
      ],
      render: ({ result }) => (
        <div className="my-2 px-3 py-2 bg-blue-500/20 rounded text-sm text-white/80">
          ✓ Liquidity data generated - Check main UI
        </div>
      ),
    },
    []
  );

  useRenderToolCall(
    {
      name: "generate_variance_analysis",
      description: "Generate and display variance analysis",
      parameters: [
        { name: "entity", type: "string", required: false },
      ],
      render: ({ result }) => (
        <div className="my-2 px-3 py-2 bg-yellow-500/20 rounded text-sm text-white/80">
          ✓ Variance analysis complete - Check main UI
        </div>
      ),
    },
    []
  );

  useRenderToolCall(
    {
      name: "detect_mock_anomalies",
      description: "Detect and display anomalies",
      parameters: [
        { name: "threshold", type: "number", required: false },
      ],
      render: ({ result }) => (
        <div className="my-2 px-3 py-2 bg-red-500/20 rounded text-sm text-white/80">
          ✓ Anomaly detection complete - Check main UI
        </div>
      ),
    },
    []
  );

  useRenderToolCall(
    {
      name: "generate_mock_metrics",
      description: "Generate and display key metrics",
      parameters: [],
      render: ({ result }) => (
        <div className="my-2 px-3 py-2 bg-green-500/20 rounded text-sm text-white/80">
          ✓ Metrics generated - Check main UI
        </div>
      ),
    },
    []
  );

  useRenderToolCall(
    {
      name: "list_mock_schemas",
      description: "List available database schemas",
      parameters: [],
      render: ({ result }) => (
        <div className="my-2 px-3 py-2 bg-purple-500/20 rounded text-sm text-white/80">
          ✓ Schemas loaded - Check main UI
        </div>
      ),
    },
    []
  );

  return (
    <div
      style={{
        background: `linear-gradient(135deg, ${themeColor} 0%, #1e293b 100%)`,
      }}
      className="min-h-screen flex flex-col transition-colors duration-300 overflow-auto"
    >
      <div className="flex-1 p-8">
        {/* Render dynamic UI based on agent state */}
        {uiDisplay ? (
          <div className="mb-8">
            {uiDisplay.type === "table" && (
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
                <h2 className="text-2xl font-bold text-white mb-4">{uiDisplay.title}</h2>
                <DynamicTable data={uiDisplay.data} maxRows={50} />
                <p className="text-xs text-white/50 mt-3">
                  Last updated: {new Date(uiDisplay.timestamp).toLocaleString()}
                </p>
              </div>
            )}
            
            {uiDisplay.type === "anomalies" && (
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
                <h2 className="text-2xl font-bold text-white mb-4">{uiDisplay.title}</h2>
                <AnomalyCard anomalies={uiDisplay.data} />
                <p className="text-xs text-white/50 mt-3">
                  Last updated: {new Date(uiDisplay.timestamp).toLocaleString()}
                </p>
              </div>
            )}
            
            {uiDisplay.type === "metrics" && (
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
                <h2 className="text-2xl font-bold text-white mb-4">{uiDisplay.title}</h2>
                <MetricsCard 
                  metrics={[
                    { label: "MLO Total", value: uiDisplay.data.mlo_total, format: "currency" as const },
                    { label: "HQLA Ratio", value: uiDisplay.data.hqla_ratio, format: "percentage" as const },
                    { label: "LCR", value: uiDisplay.data.lcr, format: "percentage" as const },
                    { label: "NSFR", value: uiDisplay.data.nsfr, format: "percentage" as const },
                    { label: "DoD Variance", value: uiDisplay.data.variance_percent, format: "percentage" as const, change: uiDisplay.data.variance_percent },
                    { label: "Anomalies", value: uiDisplay.data.anomaly_count, format: "number" as const },
                  ]}
                />
                <p className="text-xs text-white/50 mt-3">
                  Last updated: {new Date(uiDisplay.timestamp).toLocaleString()}
                </p>
              </div>
            )}
          </div>
        ) : (
          <>
            <AnalysisDashboard state={state} themeColor={themeColor} />
            
            {state.analysisResults && state.analysisResults.length > 0 ? (
              <div className="mt-8">
                <AnalysisResults 
                  results={state.analysisResults} 
                  themeColor={themeColor} 
                />
              </div>
            ) : (
              <div className="mt-8">
                <AgentCapabilities themeColor={themeColor} />
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}