"use client";

import { CopilotKitCSSProperties, CopilotChat } from "@copilotkit/react-ui";
import { useState } from "react";
import { AgentProcessingPanel } from "@/components/AgentProcessingPanel";
import { MapPanel } from "@/components/MapPanel";

export default function Home() {
  const [accentColor] = useState("#3b82f6"); // Blue color

  return (
    <main
      style={{ "--copilot-kit-primary-color": accentColor } as CopilotKitCSSProperties}
      className="h-screen w-screen flex flex-col bg-white"
    >
      {/* Top Navigation Bar */}
      <div className="border-b border-gray-200 bg-white px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-red-300 flex items-center justify-center shadow-md">
            <span className="text-2xl">🚨</span>
          </div>
          <h1 className="text-2xl font-semibold text-gray-900">First Responder Agent</h1>
        </div>
        <div className="flex items-center gap-4">
          <button className="text-gray-600 hover:text-gray-900 text-sm font-medium">Help</button>
          <button className="text-gray-600 hover:text-gray-900 text-sm font-medium">About</button>
        </div>
      </div>

      {/* Main Content Area - Layout: Map (2) | Chat (2) | Status (1) */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Column - Map */}
        <div style={{ flex: "2" }} className="flex flex-col bg-gray-100 overflow-hidden border-r border-gray-200">
          <MapPanel />
        </div>

        {/* Center Column - Chat */}
        <div style={{ flex: "2" }} className="h-full border-r border-gray-200">
          <CopilotChat
            className="h-full"
            labels={{
              initial: "👋 **Welcome to First Responder Agent**\n\nI'm your AI emergency response assistant. I can help you with:\n\n🌪️ **Disaster Discovery**\n• Track active disasters and emergencies\n• Get real-time updates from FEMA and NOAA\n\n🏥 **Relief Resources**\n• Find emergency shelters\n• Locate medical facilities\n• Discover relief organizations\n\n📊 **Intelligent Insights**\n• Analyze emergency situations\n• Get AI-powered recommendations\n• Coordinate response efforts\n\nWhat would you like to know?",
              placeholder: "Ask about disasters, relief resources, or emergency response...",
            }}
          />
        </div>

        {/* Right Column - Agent Processing Panel (Half width of chat) */}
        <div style={{ flex: "1" }} className="flex flex-col overflow-hidden">
          <AgentProcessingPanel />
        </div>
      </div>
    </main>
  );
}
