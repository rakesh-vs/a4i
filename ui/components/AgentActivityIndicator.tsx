"use client";

import { useCopilotChat } from "@copilotkit/react-core";
import { useState, useEffect } from "react";

// Map agent names to user-friendly messages
const AGENT_MESSAGES: Record<string, string> = {
  "first_responder": "Coordinating emergency response...",
  "disaster_discovery_agent": "🌪️ Discovering disasters around you...",
  "relief_finder_agent": "🏥 Finding relief resources...",
  "shelter_finder_agent": "🏠 Finding shelters around you...",
  "hospital_finder_agent": "🏥 Finding hospitals around you...",
  "supply_finder_agent": "📦 Finding supplies around you...",
  "insights_agent": "📊 Analyzing data and creating action plan...",
  "fema_live_agent": "🚨 Checking FEMA disaster data...",
  "noaa_live_agent": "🌊 Checking NOAA weather alerts...",
};

export function AgentActivityIndicator() {
  const [currentAgent, setCurrentAgent] = useState<string | null>(null);
  const { visibleMessages, isLoading } = useCopilotChat();

  // Track messages to detect agent activity
  useEffect(() => {
    console.log("[AgentActivityIndicator] Messages updated:", visibleMessages?.length, "isLoading:", isLoading);

    if (!visibleMessages || visibleMessages.length === 0) return;

    // Log all messages to see what we're getting
    visibleMessages.forEach((msg: any, idx: number) => {
      console.log(`[AgentActivityIndicator] Message ${idx}:`, {
        role: msg.role,
        type: msg.type,
        agentName: msg.agentName,
        nodeName: msg.nodeName,
        running: msg.running,
      });
    });

    const lastMessage = visibleMessages[visibleMessages.length - 1] as any;

    // Check for AgentStateMessage
    if (lastMessage.type === "AgentStateMessage") {
      const nodeName = lastMessage.nodeName;
      const running = lastMessage.running;

      console.log("[AgentActivityIndicator] AgentStateMessage detected:", { nodeName, running });

      if (running && nodeName) {
        setCurrentAgent(nodeName);
      } else if (!running) {
        setTimeout(() => {
          setCurrentAgent(null);
        }, 500);
      }
    }
  }, [visibleMessages, isLoading]);

  console.log("[AgentActivityIndicator] Current agent:", currentAgent, "isLoading:", isLoading);

  // Show loading indicator when isLoading is true
  if (isLoading && !currentAgent) {
    return (
      <div className="w-full px-4 py-2">
        <div className="flex items-center gap-3 px-4 py-3 rounded-lg bg-blue-50 border border-blue-200">
          <div className="flex gap-1">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
          </div>

          <div className="flex flex-col min-w-0 flex-1">
            <span className="text-sm font-semibold text-gray-900">
              Processing your request...
            </span>
          </div>
        </div>
      </div>
    );
  }

  if (!currentAgent) return null;

  const message = AGENT_MESSAGES[currentAgent] || `Running ${formatAgentName(currentAgent)}...`;

  return (
    <div className="w-full px-4 py-2">
      <div className="flex items-center gap-3 px-4 py-3 rounded-lg bg-blue-50 border border-blue-200">
        <div className="flex gap-1">
          <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
          <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
          <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
        </div>

        <div className="flex flex-col min-w-0 flex-1">
          <span className="text-sm font-semibold text-gray-900">
            {message}
          </span>
        </div>
      </div>
    </div>
  );
}

function formatAgentName(name: string): string {
  return name
    .replace(/_agent$/g, "")
    .replace(/_/g, " ")
    .replace(/-/g, " ")
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

