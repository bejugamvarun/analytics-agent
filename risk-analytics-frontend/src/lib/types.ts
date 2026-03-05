// State of the Risk Analytics agent
export type AgentState = {
  currentAnalysis?: {
    type: string;
    status: string;
    progress: number;
  };
  latestMetrics?: {
    mloTotal?: number;
    variancePercent?: number;
    anomalyCount?: number;
    lastUpdateDate?: string;
  };
  analysisResults?: AnalysisResult[];
  databaseInfo?: {
    connectedDatabase?: string;
    availableSchemas?: string[];
    lastQuery?: string;
  };
}

export type AnalysisResult = {
  id: string;
  type: "variance" | "anomaly" | "drilldown" | "quantitative";
  timestamp: string;
  summary: string;
  details?: Record<string, any>;
  metrics?: {
    label: string;
    value: number | string;
    unit?: string;
    change?: number;
  }[];
}