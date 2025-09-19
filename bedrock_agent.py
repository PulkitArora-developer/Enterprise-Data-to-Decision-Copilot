"""
Bedrock Agent with AgentCore Memory, Observability, and Tools
"""
import json
import boto3
from typing import Dict, Any, List
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.metrics import MetricUnit

from common import boto3_clients
from retriever import DataRetriever
from advanced_memory import AdvancedAgentMemory
from agent_analytics import AgentPerformanceTracker
import time

logger = Logger()
tracer = Tracer()
metrics = Metrics(namespace="BedrockAgentCore")

class AgentCoreMemory:
    """Simple in-memory storage for agent context"""
    def __init__(self):
        self.conversation_history = []
        self.context_data = {}
    
    def add_interaction(self, query: str, response: Dict[str, Any]):
        self.conversation_history.append({
            "query": query,
            "response": response,
            "timestamp": json.dumps({"timestamp": "now"})
        })
    
    def get_context(self) -> Dict[str, Any]:
        return {
            "history": self.conversation_history[-3:],  # Last 3 interactions
            "context": self.context_data
        }

class BedrockAgentTools:
    """Agent tools for data operations"""
    def __init__(self):
        self.retriever = DataRetriever()
    
    @tracer.capture_method
    def retrieve_customer_data(self, customer_filter: str = None) -> Dict[str, Any]:
        """Tool: Retrieve customer data from CRM"""
        data = self.retriever.retrieve_relevant_data("customer data")
        return {"tool": "customer_data", "data": data["crm"]}
    
    @tracer.capture_method
    def analyze_support_tickets(self, severity_filter: str = None) -> Dict[str, Any]:
        """Tool: Analyze support ticket patterns"""
        data = self.retriever.retrieve_relevant_data("support tickets")
        return {"tool": "support_analysis", "data": data["support"]}
    
    @tracer.capture_method
    def get_financial_metrics(self, period: str = "current") -> Dict[str, Any]:
        """Tool: Get financial and ERP data"""
        data = self.retriever.retrieve_relevant_data("financial data")
        return {"tool": "financial_metrics", "data": data["erp"]}

class BedrockAgentCore:
    """Main Bedrock Agent with AgentCore capabilities"""
    
    def __init__(self):
        # Use default credentials and region from environment
        self.bedrock_agent = boto3_clients('bedrock-agent-runtime', 'us-west-2')
        self.bedrock_runtime = boto3_clients('bedrock-runtime', 'us-west-2')
        self.memory = AdvancedAgentMemory()  # Enhanced memory
        self.tools = BedrockAgentTools()
        self.performance_tracker = AgentPerformanceTracker()  # Performance analytics
        self.agent_id = "enterprise-decision-agent"
        
    @tracer.capture_method
    @metrics.log_metrics
    def invoke_agent(self, query: str) -> Dict[str, Any]:
        """Enhanced agent invocation with advanced memory and analytics"""
        
        start_time = time.time()
        
        # Log query
        logger.info("Agent invocation started", extra={"query": query})
        metrics.add_metric(name="AgentInvocations", unit=MetricUnit.Count, value=1)
        
        try:
            # Get enhanced memory context with semantic search
            context = self.memory.get_enhanced_context(query)
            
            # Let agent determine required tools
            required_tools = self._analyze_query_for_tools(query)
            
            # Execute tools
            tool_results = {}
            for tool_name in required_tools:
                tool_results[tool_name] = self._execute_tool(tool_name)
            
            # Invoke Bedrock with enhanced context and tool results
            response = self._invoke_bedrock_with_context(query, context, tool_results)
            
            # Store in enhanced memory
            self.memory.add_interaction(query, response)
            
            # Track performance
            execution_time = time.time() - start_time
            self.performance_tracker.track_query(query, response, execution_time, required_tools)
            
            # Add performance metadata to response
            response["performance"] = {
                "execution_time": execution_time,
                "tools_used": required_tools,
                "memory_context_size": len(context.get("similar_memories", []))
            }
            
            # Log success
            logger.info("Agent invocation completed", extra={
                "response_confidence": response.get("confidence", 0),
                "execution_time": execution_time
            })
            metrics.add_metric(name="SuccessfulInvocations", unit=MetricUnit.Count, value=1)
            
            return response
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error("Agent invocation failed", extra={"error": str(e), "execution_time": execution_time})
            metrics.add_metric(name="FailedInvocations", unit=MetricUnit.Count, value=1)
            raise
    
    def _analyze_query_for_tools(self, query: str) -> List[str]:
        """Let agent decide which tools to use"""
        tool_selection_prompt = f"""
Available tools:
- customer_data: Customer information, churn rates, satisfaction scores
- support_analysis: Support tickets, issues, resolution times
- financial_metrics: Revenue, payments, financial performance

Query: {query}

Which tools are needed? Respond with only tool names separated by commas, or "none" if no tools needed.
"""
        
        try:
            response = self.bedrock_runtime.invoke_model(
                modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 100,
                    "messages": [{"role": "user", "content": tool_selection_prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            tools_text = result['content'][0]['text'].strip().lower()
            
            if "none" in tools_text:
                return []
            
            available_tools = ["customer_data", "support_analysis", "financial_metrics"]
            selected_tools = [tool for tool in available_tools if tool in tools_text]
            
            return selected_tools or ["customer_data"]
            
        except Exception:
            return ["customer_data"]  # Fallback
    
    @tracer.capture_method
    def _execute_tool(self, tool_name: str) -> Dict[str, Any]:
        """Execute specific agent tool"""
        tool_map = {
            "customer_data": self.tools.retrieve_customer_data,
            "support_analysis": self.tools.analyze_support_tickets,
            "financial_metrics": self.tools.get_financial_metrics
        }
        
        if tool_name in tool_map:
            return tool_map[tool_name]()
        return {}
    
    @tracer.capture_method
    def _invoke_bedrock_with_context(self, query: str, context: Dict[str, Any], tool_results: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke Bedrock model with full context"""
        
        prompt = f"""
You are an enterprise decision agent analyzing business data. Based on the query and data provided, give a comprehensive business analysis.

Query: {query}

Data Available:
{json.dumps(tool_results, indent=2)}

Context: {json.dumps(context, indent=2)}

Provide a detailed business analysis addressing:
1. What the data reveals about the current situation
2. Key risk factors and opportunities identified
3. Specific actionable recommendations
4. Expected outcomes and success metrics

Be specific and data-driven in your analysis. Focus on practical business insights.

        """
        
        try:
            response = self.bedrock_runtime.invoke_model(
                modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1500,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            analysis_text = result['content'][0]['text']
            
            logger.info("Bedrock response received", extra={"response_length": len(analysis_text)})
            
            # Try to parse as JSON first
            try:
                parsed_json = json.loads(analysis_text)
                return parsed_json
            except json.JSONDecodeError:
                # If not JSON, create structured response from text
                return self._parse_text_to_structured(query, analysis_text, tool_results)
                
        except Exception as e:
            logger.error("Bedrock invocation failed", extra={"error": str(e), "model_id": "anthropic.claude-3-5-sonnet-20241022-v2:0"})
            return self._create_fallback_response(query, tool_results)
    
    def _parse_text_to_structured(self, query: str, analysis: str, tool_results: Dict[str, Any]) -> Dict[str, Any]:
        """Parse text response into structured format"""
        return {
            "raw_analysis": analysis
        }
    
    def _create_fallback_response(self, query: str, tool_results: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback response when Bedrock is unavailable"""
        return {
            "raw_analysis": "Something went wrong while invoking bedrock. Check logs for more details."
        }

# Entry point function
def run_bedrock_agent(query: str) -> Dict[str, Any]:
    """Main entry point for Bedrock Agent"""
    agent = BedrockAgentCore()
    return agent.invoke_agent(query)