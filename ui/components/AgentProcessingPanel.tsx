"use client";

import { useCopilotChat } from "@copilotkit/react-core";
import { useState, useEffect } from "react";

// Map agent names to user-friendly info
const AGENT_INFO: Record<string, { name: string; icon: string; description: string; color: string }> = {
  "first_responder": {
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
};

interface AgentActivity {
  agent: string;
  timestamp: number;
  status: "running" | "completed";
}

export function AgentProcessingPanel() {
  const [currentAgent, setCurrentAgent] = useState<string | null>(null);
  const [activityHistory, setActivityHistory] = useState<AgentActivity[]>([]);
  const { visibleMessages, isLoading } = useCopilotChat();

  // Track agent activity
  useEffect(() => {
    if (!visibleMessages || visibleMessages.length === 0) return;

    const lastMessage = visibleMessages[visibleMessages.length - 1] as any;

    if (lastMessage.type === "AgentStateMessage") {
      const nodeName = lastMessage.nodeName;
      const running = lastMessage.running;

      if (running && nodeName) {
        setCurrentAgent(nodeName);
        setActivityHistory(prev => [
          ...prev.filter(a => a.agent !== nodeName),
          { agent: nodeName, timestamp: Date.now(), status: "running" }
        ]);
      } else if (!running && nodeName) {
        setActivityHistory(prev =>
          prev.map(a =>
            a.agent === nodeName ? { ...a, status: "completed" as const } : a
          )
        );
        setTimeout(() => {
          setCurrentAgent(null);
        }, 500);
      }
    }
  }, [visibleMessages]);

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

  const activeAgentInfo = currentAgent ? AGENT_INFO[currentAgent] : null;
  const recentActivities = activityHistory.slice(-5).reverse();

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200 bg-white">
        <h2 className="text-lg font-semibold text-gray-900">Agent Activity</h2>
        <p className="text-sm text-gray-500 mt-1">Real-time processing status</p>
      </div>

      {/* Current Activity */}
      <div className="px-6 py-4 space-y-4">
        {isLoading || currentAgent ? (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm font-medium text-gray-700">Currently Processing</span>
            </div>
            
            {activeAgentInfo && (
              <div className={`p-4 rounded-lg border-2 ${getColorClasses(activeAgentInfo.color, "bg")} ${getColorClasses(activeAgentInfo.color, "border")}`}>
                <div className="flex items-start gap-3">
                  <div className="text-3xl">{activeAgentInfo.icon}</div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className={`font-semibold ${getColorClasses(activeAgentInfo.color, "text")}`}>
                        {activeAgentInfo.name}
                      </h3>
                      <div className="flex gap-1">
                        <div className="w-1.5 h-1.5 bg-current rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                        <div className="w-1.5 h-1.5 bg-current rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                        <div className="w-1.5 h-1.5 bg-current rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                      </div>
                    </div>
                    <p className="text-sm text-gray-600">{activeAgentInfo.description}</p>
                  </div>
                </div>
              </div>
            )}

            {!activeAgentInfo && (
              <div className="p-4 rounded-lg border-2 bg-blue-50 border-blue-200">
                <div className="flex items-center gap-3">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                  </div>
                  <span className="text-sm font-medium text-gray-700">Processing your request...</span>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="p-4 rounded-lg bg-gray-100 border border-gray-200">
            <div className="flex items-center gap-2 text-gray-500">
              <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
              <span className="text-sm">Idle - Waiting for request</span>
            </div>
          </div>
        )}
      </div>

      {/* Activity History */}
      {recentActivities.length > 0 && (
        <div className="px-6 py-4 flex-1 overflow-y-auto">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Recent Activity</h3>
          <div className="space-y-2">
            {recentActivities.map((activity, idx) => {
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
      )}

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

