"use client";

import { CopilotKitCSSProperties, CopilotChat } from "@copilotkit/react-ui";
import { useState } from "react";
import { AgentActivityIndicator } from "@/components/AgentActivityIndicator";

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
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 flex items-center justify-center">
            <span className="text-white font-bold text-lg">🚨</span>
          </div>
          <h1 className="text-2xl font-semibold text-gray-900">First Responder Agent</h1>
        </div>
        <div className="flex items-center gap-4">
          <button className="text-gray-600 hover:text-gray-900 text-sm font-medium">Help</button>
          <button className="text-gray-600 hover:text-gray-900 text-sm font-medium">About</button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-white justify-center">
        <div className="w-full max-w-2xl h-full mx-auto flex flex-col overflow-hidden">
          {/* Agent Activity Indicator - rendered at top level */}
          <AgentActivityIndicator />

          <CopilotChat
            instructions="You are the First Responder Agent, an AI assistant specialized in emergency response coordination. You help users with disaster discovery, finding relief resources, and providing intelligent insights for emergency situations. Be helpful, clear, and provide actionable information."
            labels={{
              initial: "👋 Welcome to First Responder Agent\n\nI'm your AI emergency response assistant. I can help you with:\n\n🌪️ **Disaster Discovery**\n• Track active disasters and emergencies\n• Get real-time updates from FEMA and NOAA\n\n🏥 **Relief Resources**\n• Find emergency shelters\n• Locate medical facilities\n• Discover relief organizations\n\n📊 **Intelligent Insights**\n• Analyze emergency situations\n• Get AI-powered recommendations\n• Coordinate response efforts\n\nWhat would you like to know?",
              placeholder: "Ask about disasters, relief resources, or emergency response...",
            }}
          />
        </div>
      </div>
    </main>
  );
}
