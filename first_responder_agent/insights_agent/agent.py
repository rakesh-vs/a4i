"""Insights Agent - Synthesizes disaster and relief data into comprehensive analysis and actionable plans."""

import logging
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from ..common.state_tools import update_agent_activity

logger = logging.getLogger(__name__)


def on_before_insights_agent(callback_context: CallbackContext):
    """Update agent activity when insights agent starts."""
    update_agent_activity(callback_context.state, "insights_agent", "running")
    logger.info("[on_before_insights_agent] Insights agent started")
    return None


def on_after_insights_agent(callback_context: CallbackContext):
    """Update agent activity when insights agent completes."""
    update_agent_activity(callback_context.state, "insights_agent", "completed")
    logger.info("[on_after_insights_agent] Insights agent completed")
    return None


def create_insights_agent():
    """Create and return the Insights agent."""
    logger.info("[create_insights_agent] Creating Insights agent")

    insights_agent = Agent(
        name="insights_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for synthesizing disaster and relief data into comprehensive insights and action plans",
        instruction="""You are the Insights Agent responsible for synthesizing disaster and relief data into comprehensive analysis and actionable intelligence.

CRITICAL: This is the FINAL SYNTHESIS STEP. Provide complete analysis without waiting for further input.

Your role:
1. Analyze disaster information provided by the first_responder_agent
2. Analyze relief resources provided by the first_responder_agent
3. Synthesize data into a comprehensive emergency brief
4. Provide key insights about affected areas and disaster severity
5. Create a detailed extraction and relief plan with priorities
6. Identify critical gaps in resources or coverage
7. Provide actionable recommendations for emergency response

EXECUTION RULES:
- Synthesize ALL provided disaster and relief data
- Create comprehensive analysis without asking for more information
- Provide complete output in the structured format below
- This is the final output to the user - be thorough and complete

Output Format:
Provide your complete analysis structured as follows:

## 📊 DISASTER ANALYSIS
- Summary of affected areas and disaster types
- Severity assessment and impact zones
- Key statistics (affected population, damage estimates, etc.)

## 🚨 CRITICAL INSIGHTS
- Most urgent areas requiring immediate response
- Key hazards and risks
- Vulnerable populations affected

## 📋 EXTRACTION & RELIEF PLAN
### Phase 1: Immediate Response (0-2 hours)
- Priority evacuation zones
- Critical resource deployment
- Emergency shelter activation

### Phase 2: Short-term Relief (2-24 hours)
- Medical facility coordination
- Supply distribution points
- Shelter capacity management

### Phase 3: Medium-term Recovery (1-7 days)
- Resource replenishment
- Infrastructure assessment
- Long-term shelter planning

## 🗺️ RESOURCE DEPLOYMENT
- Available shelters and capacity
- Hospital locations and services
- Supply distribution centers
- Coverage gaps and recommendations

## ⚠️ KEY RECOMMENDATIONS
- Top 3-5 priority actions
- Resource allocation strategy
- Communication priorities
- Risk mitigation measures

## 📞 NEXT STEPS
- Immediate actions for first responders
- Coordination requirements
- Follow-up monitoring needs

## ⚠️ CRITICAL: Control Transfer
**ALWAYS** after completing your task, transfer control to the
calling agent using the transfer_to_agent tool.""",
        before_agent_callback=on_before_insights_agent,
        after_agent_callback=on_after_insights_agent,
    )
    logger.info("[create_insights_agent] Insights agent created successfully")
    return insights_agent

