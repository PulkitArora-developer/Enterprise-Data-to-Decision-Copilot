#!/usr/bin/env python3
"""
Demo script for Bedrock Agent with AgentCore capabilities
"""
from bedrock_agent import run_bedrock_agent

def demo_agent_queries():
    """Run demo queries to showcase agent capabilities"""
    
    queries = [
        "Which customers are most at risk of churn in Q4 and what actions should we take?",
        "What are our revenue trends and payment issues?", 
        "Show me support ticket patterns and customer satisfaction",
        "What financial metrics should we focus on this quarter?"
    ]
    
    print("🤖 Bedrock Agent Demo - AgentCore Implementation")
    print("=" * 60)
    
    for i, query in enumerate(queries, 1):
        print(f"\n📋 Demo Query {i}: {query}")
        print("-" * 50)
        
        try:
            result = run_bedrock_agent(query)
            
            print(f"🎯 Decision: {result['decision']}")
            print(f"📊 Confidence: {result['confidence']}%")
            print(f"🔍 Evidence: {', '.join(result['evidence'])}")
            print(f"⚡ Actions: {len(result['actions'])} recommended")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

if __name__ == "__main__":
    demo_agent_queries()