"use client";

import { useCoAgent, useCopilotChat } from "@copilotkit/react-core";
import { useEffect } from "react";

// Map agent names to user-friendly info
const AGENT_INFO: Record<string, { name: string; icon: string; description: string; color: string }> = {
  "first_responder": {
    name: "First Responder",
    icon: "🚨",
    description: "Coordinating emergency response",
    color: "blue"
  },
  "first_responder_agent": {
    name: "First Responder",
    icon: "🚨",
    description: "Coordinating emergency response",
    color: "blue"
  },
  "disaster_discovery_agent": {
    name: "Disaster Discovery",
    icon: "🌪️",
    description: "Searching for active disasters and emergencies",
    color: "orange"
  },
  "relief_finder_agent": {
    name: "Relief Finder",
    icon: "🏥",
    description: "Locating relief resources and facilities",
    color: "green"
  },
  "shelter_finder_agent": {
    name: "Shelter Finder",
    icon: "🏠",
    description: "Finding emergency shelters nearby",
    color: "purple"
  },
  "hospital_finder_agent": {
    name: "Hospital Finder",
    icon: "🏥",
    description: "Locating medical facilities",
    color: "red"
  },
  "supply_finder_agent": {
    name: "Supply Finder",
    icon: "📦",
    description: "Finding emergency supplies",
    color: "yellow"
  },
  "insights_agent": {
    name: "Insights Agent",
    icon: "📊",
    description: "Analyzing data and creating action plan",
    color: "indigo"
  },
  "fema_live_agent": {
    name: "FEMA Data",
    icon: "🚨",
    description: "Checking FEMA disaster declarations",
    color: "red"
  },
  "noaa_live_agent": {
    name: "NOAA Weather",
    icon: "🌊",
    description: "Checking weather alerts and forecasts",
    color: "blue"
  },
  "bigquery_storms_tool": {
    name: "BigQuery Storms",
    icon: "🌩️",
    description: "Querying storm data from BigQuery",
    color: "purple"
  },
  "bigquery_shelter_tool": {
    name: "BigQuery Shelters",
    icon: "🏠",
    description: "Querying shelter data from BigQuery",
    color: "purple"
  },
  "bigquery_hospital_tool": {
    name: "BigQuery Hospitals",
    icon: "🏥",
    description: "Querying hospital data from BigQuery",
    color: "purple"
  },
  "bigquery_supply_tool": {
    name: "BigQuery Supplies",
    icon: "📦",
    description: "Querying supply data from BigQuery",
    color: "purple"
  },
  "maps_search_tool": {
    name: "Google Maps Search",
    icon: "🗺️",
    description: "Searching locations on Google Maps",
    color: "green"
  },
};

interface AgentActivity {
  agent: string;
  timestamp: number;
  status: "running" | "completed";
}

// Agent state type for useCoAgent
type AgentActivityState = {
  currentAgent: string | null;
  activityHistory: AgentActivity[];
}

export function AgentProcessingPanel() {
  const { isLoading } = useCopilotChat();

  // Shared state with agent - updated automatically via callbacks
  const { state } = useCoAgent<AgentActivityState>({
    name: "first_responder_agent",
    initialState: {
      currentAgent: null,
      activityHistory: [],
    },
  });

  // Log state updates for debugging
  useEffect(() => {
    console.log("[AgentProcessingPanel] State updated:", {
      currentAgent: state.currentAgent,
      activityHistoryLength: state.activityHistory?.length || 0,
      activityHistory: state.activityHistory,
      isLoading,
    });
  }, [state.currentAgent, state.activityHistory, isLoading]);

  const displayCurrentAgent = state.currentAgent;
  const displayActivityHistory = state.activityHistory || [];

  const getColorClasses = (color: string, variant: "bg" | "border" | "text") => {
    const colors: Record<string, Record<string, string>> = {
      blue: { bg: "bg-blue-50", border: "border-blue-200", text: "text-blue-700" },
      orange: { bg: "bg-orange-50", border: "border-orange-200", text: "text-orange-700" },
      green: { bg: "bg-green-50", border: "border-green-200", text: "text-green-700" },
      purple: { bg: "bg-purple-50", border: "border-purple-200", text: "text-purple-700" },
      red: { bg: "bg-red-50", border: "border-red-200", text: "text-red-700" },
      yellow: { bg: "bg-yellow-50", border: "border-yellow-200", text: "text-yellow-700" },
      indigo: { bg: "bg-indigo-50", border: "border-indigo-200", text: "text-indigo-700" },
    };
    return colors[color]?.[variant] || colors.blue[variant];
  };

  const activeAgentInfo = displayCurrentAgent ? AGENT_INFO[displayCurrentAgent] : null;
  // Show all activities in reverse chronological order (most recent first)
  const recentActivities = [...displayActivityHistory].reverse();

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200 bg-white">
        <h2 className="text-lg font-semibold text-gray-900">Agent Activity</h2>
        <p className="text-sm text-gray-500 mt-1">Real-time processing status</p>
      </div>

      {/* Current Activity - Prominent Status Box */}
      <div className="px-6 py-4 space-y-4">
        {isLoading || displayCurrentAgent ? (
          <div className="space-y-3">
            {/* Status Header */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-semibold text-gray-900">ACTIVE</span>
              </div>
              <span className="text-xs text-gray-500">Processing now</span>
            </div>

            {/* Active Agent Card */}
            {activeAgentInfo ? (
              <div className={`p-5 rounded-xl border-2 shadow-lg ${getColorClasses(activeAgentInfo.color, "bg")} ${getColorClasses(activeAgentInfo.color, "border")}`}>
                <div className="flex items-start gap-4">
                  <div className="text-4xl animate-pulse">{activeAgentInfo.icon}</div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-2">
                      <h3 className={`text-lg font-bold ${getColorClasses(activeAgentInfo.color, "text")}`}>
                        {activeAgentInfo.name}
                      </h3>
                      <div className="flex gap-1">
                        <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                        <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                        <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                      </div>
                    </div>
                    <p className="text-sm font-medium text-gray-700">{activeAgentInfo.description}</p>
                  </div>
                </div>
              </div>
            ) : isLoading ? (
              <div className="p-5 rounded-xl border-2 bg-blue-50 border-blue-200 shadow-lg">
                <div className="flex flex-col gap-3">
                  <div className="flex items-center gap-4">
                    <div className="flex gap-1.5">
                      <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                      <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                      <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                    </div>
                    <span className="text-base font-semibold text-gray-800">Agents Working...</span>
                  </div>
                  <div className="text-xs text-gray-600 pl-8">
                    Coordinating disaster discovery, relief resources, and analysis
                  </div>
                </div>
              </div>
            ) : null}
          </div>
        ) : (
          <div className="p-5 rounded-xl bg-gray-100 border-2 border-gray-200">
            <div className="flex items-center gap-3 text-gray-500">
              <div className="w-3 h-3 bg-gray-400 rounded-full"></div>
              <div>
                <div className="text-sm font-semibold text-gray-700">Idle</div>
                <div className="text-xs text-gray-500">Waiting for request</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Activity History */}
      {recentActivities.length > 0 ? (
        <div className="px-6 py-4 flex-1 overflow-y-auto">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Recent Activity</h3>
          <div className="space-y-2">
            {recentActivities.map((activity) => {
              const info = AGENT_INFO[activity.agent];
              if (!info) return null;

              const isCompleted = activity.status === "completed";
              const timeSince = Math.floor((Date.now() - activity.timestamp) / 1000);
              const timeText = timeSince < 60 ? `${timeSince}s ago` : `${Math.floor(timeSince / 60)}m ago`;

              return (
                <div
                  key={`${activity.agent}-${activity.timestamp}`}
                  className={`p-3 rounded-lg border ${
                    isCompleted
                      ? "bg-white border-gray-200"
                      : `${getColorClasses(info.color, "bg")} ${getColorClasses(info.color, "border")}`
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{info.icon}</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium text-gray-900 truncate">
                          {info.name}
                        </span>
                        {isCompleted && (
                          <span className="text-green-600 text-xs">✓</span>
                        )}
                      </div>
                      <span className="text-xs text-gray-500">{timeText}</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : isLoading ? (
        <div className="px-6 py-4 flex-1 flex items-center justify-center">
          <div className="text-center text-sm text-gray-500">
            <div className="mb-2">⏳</div>
            <p>Activity history will appear here as agents complete their tasks</p>
          </div>
        </div>
      ) : null}

      {/* Info Footer */}
      <div className="px-6 py-4 border-t border-gray-200 bg-white">
        <div className="flex items-start gap-2 text-xs text-gray-500">
          <span>💡</span>
          <p>
            The agent system coordinates multiple specialized agents to provide comprehensive emergency response information.
          </p>
        </div>
      </div>
    </div>
  );
}

