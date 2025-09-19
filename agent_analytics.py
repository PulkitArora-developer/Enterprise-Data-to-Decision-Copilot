"""
Agent Performance Analytics and Optimization
"""
import json
import time
from typing import Dict, Any, List
from collections import defaultdict
from aws_lambda_powertools import Logger, Metrics
from aws_lambda_powertools.metrics import MetricUnit

logger = Logger()
metrics = Metrics(namespace="BedrockAgentCore")

class AgentPerformanceTracker:
    """Track and analyze agent performance metrics"""
    
    def __init__(self):
        self.query_metrics = []
        self.tool_performance = defaultdict(list)
        self.decision_accuracy = []
        self.response_times = []
    
    def track_query(self, query: str, response: Dict[str, Any], execution_time: float, tools_used: List[str]):
        """Track individual query performance"""
        
        query_metric = {
            "query": query,
            "response_time": execution_time,
            "confidence": response.get("confidence", 0),
            "tools_used": tools_used,
            "timestamp": time.time(),
            "decision_type": self._classify_query(query)
        }
        
        self.query_metrics.append(query_metric)
        self.response_times.append(execution_time)
        
        # Track tool performance
        for tool in tools_used:
            self.tool_performance[tool].append(execution_time / len(tools_used))
        
        # Send metrics to CloudWatch
        metrics.add_metric(name="QueryResponseTime", unit=MetricUnit.Seconds, value=execution_time)
        metrics.add_metric(name="DecisionConfidence", unit=MetricUnit.Percent, value=response.get("confidence", 0))
        metrics.add_metric(name="ToolsUsed", unit=MetricUnit.Count, value=len(tools_used))
    
    def _classify_query(self, query: str) -> str:
        """Classify query type for analytics"""
        query_lower = query.lower()
        if "churn" in query_lower: return "churn_analysis"
        elif "revenue" in query_lower: return "financial_analysis"
        elif "support" in query_lower: return "support_analysis"
        return "general"
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        if not self.query_metrics:
            return {"status": "no_data"}
        
        avg_response_time = sum(self.response_times) / len(self.response_times)
        avg_confidence = sum(m["confidence"] for m in self.query_metrics) / len(self.query_metrics)
        
        # Tool efficiency analysis
        tool_efficiency = {}
        for tool, times in self.tool_performance.items():
            tool_efficiency[tool] = {
                "avg_time": sum(times) / len(times),
                "usage_count": len(times),
                "efficiency_score": 100 / (sum(times) / len(times))  # Higher is better
            }
        
        # Query type distribution
        query_types = defaultdict(int)
        for metric in self.query_metrics:
            query_types[metric["decision_type"]] += 1
        
        return {
            "total_queries": len(self.query_metrics),
            "avg_response_time": avg_response_time,
            "avg_confidence": avg_confidence,
            "tool_efficiency": tool_efficiency,
            "query_distribution": dict(query_types),
            "performance_grade": self._calculate_performance_grade(avg_response_time, avg_confidence)
        }
    
    def _calculate_performance_grade(self, avg_time: float, avg_confidence: float) -> str:
        """Calculate overall performance grade"""
        time_score = 100 if avg_time < 2.0 else max(0, 100 - (avg_time - 2.0) * 20)
        confidence_score = avg_confidence
        
        overall_score = (time_score + confidence_score) / 2
        
        if overall_score >= 90: return "A+"
        elif overall_score >= 80: return "A"
        elif overall_score >= 70: return "B"
        elif overall_score >= 60: return "C"
        else: return "D"

class AgentOptimizer:
    """Optimize agent performance based on analytics"""
    
    def __init__(self, performance_tracker: AgentPerformanceTracker):
        self.tracker = performance_tracker
    
    def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Generate optimization recommendations"""
        recommendations = []
        summary = self.tracker.get_performance_summary()
        
        if summary.get("status") == "no_data":
            return [{"type": "info", "message": "Insufficient data for optimization"}]
        
        # Response time optimization
        if summary["avg_response_time"] > 3.0:
            recommendations.append({
                "type": "performance",
                "priority": "high",
                "issue": "Slow response times",
                "recommendation": "Consider tool caching or parallel execution",
                "expected_improvement": "30-50% faster responses"
            })
        
        # Tool efficiency optimization
        inefficient_tools = [
            tool for tool, data in summary["tool_efficiency"].items()
            if data["efficiency_score"] < 50
        ]
        
        if inefficient_tools:
            recommendations.append({
                "type": "tools",
                "priority": "medium",
                "issue": f"Inefficient tools: {', '.join(inefficient_tools)}",
                "recommendation": "Optimize data retrieval or consider tool replacement",
                "expected_improvement": "20-30% better tool performance"
            })
        
        # Confidence optimization
        if summary["avg_confidence"] < 75:
            recommendations.append({
                "type": "accuracy",
                "priority": "high",
                "issue": "Low decision confidence",
                "recommendation": "Enhance training data or adjust model parameters",
                "expected_improvement": "10-15% higher confidence scores"
            })
        
        return recommendations