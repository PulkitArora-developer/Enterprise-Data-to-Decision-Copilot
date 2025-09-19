"""
Advanced AgentCore Memory with Vector Storage and Semantic Search
"""
import json
import numpy as np
from typing import Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from aws_lambda_powertools import Logger

logger = Logger()

class VectorMemory:
    """Vector-based memory for semantic similarity search"""
    def __init__(self, max_memories: int = 100):
        self.memories = []
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.vectors = None
        self.max_memories = max_memories
    
    def add_memory(self, query: str, response: Dict[str, Any], context: Dict[str, Any]):
        """Add memory with vector encoding"""
        memory = {
            "query": query,
            "response": response,
            "context": context,
            "timestamp": "now",
            "memory_id": len(self.memories)
        }
        
        self.memories.append(memory)
        
        # Rebuild vectors when adding memories
        if len(self.memories) > 1:
            self._rebuild_vectors()
        
        # Maintain memory limit
        if len(self.memories) > self.max_memories:
            self.memories = self.memories[-self.max_memories:]
            self._rebuild_vectors()
    
    def _rebuild_vectors(self):
        """Rebuild vector representations"""
        texts = [f"{m['query']} {json.dumps(m['response'])}" for m in self.memories]
        self.vectors = self.vectorizer.fit_transform(texts)
    
    def find_similar_memories(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Find semantically similar memories"""
        if not self.memories or self.vectors is None:
            return []
        
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.vectors)[0]
        
        # Get top-k similar memories
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        similar_memories = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Similarity threshold
                memory = self.memories[idx].copy()
                memory["similarity_score"] = float(similarities[idx])
                similar_memories.append(memory)
        
        return similar_memories

class AdvancedAgentMemory:
    """Enhanced AgentCore Memory with multiple storage types"""
    def __init__(self):
        self.conversation_history = []
        self.vector_memory = VectorMemory()
        self.context_data = {}
        self.decision_patterns = {}
    
    def add_interaction(self, query: str, response: Dict[str, Any]):
        """Add interaction to multiple memory stores"""
        # Traditional conversation history
        interaction = {
            "query": query,
            "response": response,
            "timestamp": "now"
        }
        self.conversation_history.append(interaction)
        
        # Vector memory for semantic search
        self.vector_memory.add_memory(query, response, self.context_data)
        
        # Extract and store decision patterns
        if "decision" in response:
            decision_type = self._classify_decision(query)
            if decision_type not in self.decision_patterns:
                self.decision_patterns[decision_type] = []
            self.decision_patterns[decision_type].append({
                "query": query,
                "decision": response["decision"],
                "confidence": response.get("confidence", 0)
            })
    
    def _classify_decision(self, query: str) -> str:
        """Classify decision type for pattern storage"""
        query_lower = query.lower()
        if "churn" in query_lower or "retention" in query_lower:
            return "customer_retention"
        elif "revenue" in query_lower or "financial" in query_lower:
            return "financial_decision"
        elif "support" in query_lower or "ticket" in query_lower:
            return "support_optimization"
        return "general_business"
    
    def get_enhanced_context(self, current_query: str) -> Dict[str, Any]:
        """Get enhanced context with semantic similarity"""
        context = {
            "recent_history": self.conversation_history[-3:],
            "similar_memories": self.vector_memory.find_similar_memories(current_query),
            "decision_patterns": self.decision_patterns,
            "context_data": self.context_data
        }
        
        logger.info("Enhanced context retrieved", extra={
            "similar_memories_count": len(context["similar_memories"]),
            "decision_patterns_count": len(self.decision_patterns)
        })
        
        return context