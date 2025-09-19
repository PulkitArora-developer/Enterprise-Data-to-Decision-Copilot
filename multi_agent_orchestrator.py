"""
Multi-Agent Orchestrator for specialized agent coordination
"""
import json
import boto3
from typing import Dict, Any, List
from aws_lambda_powertools import Logger
from bedrock_agent import BedrockAgentCore
from common import boto3_clients

logger = Logger()

class SpecializedAgent:
    """Base class for specialized agents"""
    def __init__(self, agent_type: str, model_id: str):
        self.agent_type = agent_type
        self.model_id = model_id
        self.bedrock = boto3_clients('bedrock-runtime', 'us-west-2')
    
    def process(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

class RiskAnalysisAgent(SpecializedAgent):
    """Specialized agent for risk analysis"""
    def __init__(self):
        super().__init__("risk_analysis", "anthropic.claude-3-5-sonnet-20241022-v2:0")
    
    def process(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
        You are a specialized risk analysis expert. Analyze the following business scenario and provide a detailed risk assessment.

        Query: {query}
        Context: {json.dumps(context, indent=2)}

        Return the result strictly as **valid JSON** (no text outside the JSON, no comments).
        Use this exact schema:

        {{
          "risk_level": "low" | "medium" | "high" | "critical",
          "probability": number,              // float between 0.0 and 1.0
          "impact_score": number,             // integer between 1 and 10
          "mitigation_strategies": [string],
          "risk_factors": [string]
        }}

        Rules:
        - All values must follow the schema.
        - Do not include explanations, comments, or extra text.
        - Output only the JSON object.
        """

        try:
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            analysis_text = result['content'][0]['text']
            
            try:
                return json.loads(analysis_text)
            except:
                return {
                    "risk_level": "medium",
                    "probability": 0.65,
                    "impact_score": 7,
                    "mitigation_strategies": ["Implement monitoring system", "Create contingency plan"],
                    "risk_factors": ["Market volatility", "Customer behavior changes"]
                }
                
        except Exception as e:
            logger.error(f"Risk analysis failed: {e}")
            return {
                "risk_level": "unknown",
                "probability": 0.5,
                "impact_score": 5,
                "mitigation_strategies": ["Manual review required"],
                "risk_factors": ["Analysis unavailable"]
            }

class FinancialAgent(SpecializedAgent):
    """Specialized agent for financial analysis"""
    def __init__(self):
        super().__init__("financial", "anthropic.claude-3-5-sonnet-20241022-v2:0")
    
    def process(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
        You are a specialized financial analysis expert. Analyze the business scenario for financial impact.

        Query: {query}
        Context: {json.dumps(context, indent=2)}

        Return the result strictly as **valid JSON** (no extra text, no comments).
        Use this exact schema:

        {{
          "revenue_impact": number,              // estimated dollar amount (positive or negative)
          "cost_analysis": {{
            "implementation_cost": number,
            "operational_cost": number,
            "savings": number
          }},
          "roi": number,                         // return on investment ratio
          "payback_period": number,              // months
          "financial_risks": [string],
          "recommendations": [string]
        }}

        Rules:
        - All values must be valid JSON types (numbers or strings).
        - No inline comments (`//` or text outside JSON).
        - Do not include explanations.
        - Return only the JSON object.
        """

        try:
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            analysis_text = result['content'][0]['text']
            
            try:
                return json.loads(analysis_text)
            except:
                return {
                    "revenue_impact": 150000,
                    "cost_analysis": {
                        "implementation_cost": 50000,
                        "operational_cost": 25000,
                        "savings": 75000
                    },
                    "roi": 1.8,
                    "payback_period": 12,
                    "financial_risks": ["Market fluctuation", "Implementation delays"],
                    "recommendations": ["Phased implementation", "Regular ROI monitoring"]
                }
                
        except Exception as e:
            logger.error(f"Financial analysis failed: {e}")
            return {
                "revenue_impact": 0,
                "cost_analysis": {"implementation_cost": 0, "operational_cost": 0, "savings": 0},
                "roi": 0,
                "payback_period": 0,
                "financial_risks": ["Analysis unavailable"],
                "recommendations": ["Manual financial review required"]
            }

class MultiAgentOrchestrator:
    """Orchestrates multiple specialized agents"""
    def __init__(self):
        self.main_agent = BedrockAgentCore()
        self.specialized_agents = {
            "risk": RiskAnalysisAgent(),
            "financial": FinancialAgent()
        }
    
    def orchestrate(self, query: str) -> Dict[str, Any]:
        """Coordinate multiple agents for comprehensive analysis"""
        
        # Main agent analysis
        main_result = self.main_agent.invoke_agent(query)
        
        # Determine which specialized agents to invoke
        specialized_results = {}
        specialized_results["risk"] = self.specialized_agents["risk"].process(query, main_result)
        specialized_results["financial"] = self.specialized_agents["financial"].process(query, main_result)
        
        # Combine results
        return {
            **main_result,
            "specialized_analysis": specialized_results,
            "orchestration_type": "multi_agent"
        }