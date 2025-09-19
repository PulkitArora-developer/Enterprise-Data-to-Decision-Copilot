#!/usr/bin/env python3
"""
Streamlit UI for BedrockAgentCore Enterprise Decision Copilot
"""
import streamlit as st
import json
import time
import plotly.graph_objects as go
import plotly.express as px
from bedrock_agent import BedrockAgentCore
from multi_agent_orchestrator import MultiAgentOrchestrator
from agent_analytics import AgentOptimizer


# Page config
st.set_page_config(
    page_title="BedrockAgentCore Enterprise Copilot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = BedrockAgentCore()
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = MultiAgentOrchestrator()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'last_result' not in st.session_state:
    st.session_state.last_result = {}


def main():
    st.title("🤖 BedrockAgentCore Enterprise Decision Copilot")
    st.markdown("*Advanced Multi-Agent System*")
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Agent Controls")
        
        # Agent mode selection
        agent_mode = st.selectbox(
            "Agent Mode",
            ["Standard Agent", "Multi-Agent Orchestration"],
            help="Choose between single agent or multi-agent coordination"
        )
        
        # Performance metrics
        st.header("📊 Performance Metrics")
        performance = st.session_state.agent.performance_tracker.get_performance_summary()
        
        if performance.get("status") != "no_data":
            st.metric("Total Queries", performance['total_queries'])
            st.metric("Avg Response Time", f"{performance['avg_response_time']:.2f}s")
            st.metric("Avg Confidence", f"{performance['avg_confidence']:.1f}%")
            st.metric("Performance Grade", performance['performance_grade'])
        else:
            st.info("No performance data yet")
        
        # Clear history
        if st.button("🗑️ Clear History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Main chat interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Chat Interface")
        
        # Query input
        query = st.text_input(
            "Enter your business query:",
            placeholder="e.g., Analyze customer churn risk for Q4",
            key="query_input"
        )
        
        col_send, col_example = st.columns([1, 1])
        
        with col_send:
            send_button = st.button("🚀 Send Query", type="primary")

        # Process query
        if send_button and query:
            with st.spinner("🤖 Agent processing..."):
                try:
                    start_time = time.time()
                    
                    # Choose agent mode
                    if agent_mode == "Multi-Agent Orchestration":
                        result = st.session_state.orchestrator.orchestrate(query)
                        agent_type = "Multi-Agent"
                    else:
                        result = st.session_state.agent.invoke_agent(query)
                        agent_type = "Standard"
                    
                    execution_time = time.time() - start_time

                    st.session_state.last_result = result

                    # Add to chat history
                    st.session_state.chat_history.append({
                        "query": query,
                        "result": result,
                        "agent_type": agent_type,
                        "timestamp": time.strftime("%H:%M:%S")
                    })
                    
                    st.success(f"✅ Analysis complete in {execution_time:.2f}s")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        # Chat history
        st.header("📝 Analysis History")
        
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"🕐 {chat['timestamp']} - {chat['agent_type']} Agent", expanded=(i==0)):
                st.markdown(f"**Query:** {chat['query']}")
                
                result = chat['result']

                # Analysis
                if 'raw_analysis' in result:
                    st.markdown(f"**Analysis:** {result['raw_analysis']}")

    with col2:
        st.header("⚡ Specialised Analysis")
        if st.session_state.last_result and 'specialized_analysis' in st.session_state.last_result:
            st.subheader("📊 Specialized Analysis")
            try:
                parsed = st.session_state.last_result['specialized_analysis']

                if "financial" in parsed:
                    fin = parsed["financial"]
                    st.metric("Revenue Impact", f"${fin['revenue_impact']:,}")
                    st.metric("ROI", f"{fin['roi']:.2f}")
                    st.metric("Payback Period", f"{fin['payback_period']} months")
                    st.table(fin["cost_analysis"])
                    st.write("**Financial Risks:**")
                    for i in fin["financial_risks"]:
                        st.markdown(f"- {i}")

                    st.write("**Recommendations:**")
                    for r in fin["recommendations"]:
                        st.markdown(f"- {r}")

                if "risk" in parsed:
                    risk = parsed["risk"]
                    st.metric("Risk Level", risk["risk_level"])
                    st.metric("Probability", f"{risk['probability']:.2f}")
                    st.metric("Impact Score", risk["impact_score"])
                    st.write("**Risk Factors:**", risk["risk_factors"])
                    st.write("**Mitigation Strategies:**")
                    for m in risk["mitigation_strategies"]:
                        st.markdown(f"- {m}")

            except Exception:
                st.markdown(st.session_state.last_result['specialized_analysis'])


if __name__ == "__main__":
    main()