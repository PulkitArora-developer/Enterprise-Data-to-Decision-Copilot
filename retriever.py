"""
Mock data retrieval from enterprise sources
"""
import json
import csv
import os
from typing import Dict, List, Any

class DataRetriever:
    def __init__(self, data_dir: str = "sample_data"):
        self.data_dir = data_dir
        
    def retrieve_relevant_data(self, query: str) -> Dict[str, Any]:
        """Retrieve relevant data based on query keywords"""
        query_lower = query.lower()
        
        # Load all data sources
        crm_data = self._load_crm_data()
        support_data = self._load_support_data()
        erp_data = self._load_erp_data()
        
        # Filter based on query context
        relevant_data = {
            "crm": crm_data,
            "support": support_data, 
            "erp": erp_data,
            "query_context": self._extract_context(query_lower)
        }
        
        return relevant_data
    
    def _load_crm_data(self) -> List[Dict]:
        """Load CRM customer data"""
        try:
            with open(os.path.join(self.data_dir, "crm.json"), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _load_support_data(self) -> List[Dict]:
        """Load support ticket data"""
        try:
            with open(os.path.join(self.data_dir, "support.csv"), 'r') as f:
                return list(csv.DictReader(f))
        except FileNotFoundError:
            return []
    
    def _load_erp_data(self) -> List[Dict]:
        """Load ERP financial data"""
        try:
            with open(os.path.join(self.data_dir, "erp.json"), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _extract_context(self, query: str) -> Dict[str, bool]:
        """Extract context keywords from query"""
        return {
            "churn_analysis": any(word in query for word in ["churn", "risk", "retention", "leaving"]),
            "financial_focus": any(word in query for word in ["revenue", "payment", "financial", "billing"]),
            "support_focus": any(word in query for word in ["support", "tickets", "issues", "problems"]),
            "q4_focus": "q4" in query or "quarter" in query,
            "customer_focus": any(word in query for word in ["customer", "client", "account"])
        }