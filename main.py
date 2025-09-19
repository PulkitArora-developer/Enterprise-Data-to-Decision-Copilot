#!/usr/bin/env python3
"""
Enterprise Data-to-Decision Copilot CLI with Bedrock Agent
"""
import json
from bedrock_agent import run_bedrock_agent

def main():
    print("🤖 Enterprise Data-to-Decision Copilot")
    print("=" * 50)
    
    while True:
        query = input("\n💬 Enter your business query (or 'quit' to exit): ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
            
        if not query:
            continue
            
        try:
            print("\n🤖 Invoking Bedrock Agent...")
            result = run_bedrock_agent(query)
            
            print("\n📊 DECISION ANALYSIS")
            print("=" * 30)
            print(f"Decision: {result['decision']}")
            print(f"Confidence: {result['confidence']}%")
            
            print("\n🎯 Key Drivers:")
            for i, driver in enumerate(result['drivers'], 1):
                print(f"  {i}. {driver}")
                
            print("\n⚡ Recommended Actions:")
            for i, action in enumerate(result['actions'], 1):
                print(f"  {i}. {action}")
                
            print(f"\n📋 Evidence Sources: {', '.join(result['evidence'])}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()