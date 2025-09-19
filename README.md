# Amazon Bedrock Agent Core

Enterprise-grade AI agent system built on Amazon Bedrock with advanced memory, analytics, and multi-source data integration.

## Features

- **Advanced Memory System**: Semantic search and context-aware conversation history
- **Multi-Source Data Integration**: CRM, ERP, and Support ticket analysis
- **Performance Analytics**: Real-time tracking and optimization
- **Streamlit Dashboard**: Interactive web interface
- **AWS Integration**: Bedrock, Lambda Powertools, and CloudWatch

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │────│  Bedrock Agent   │────│   Data Sources  │
│   Dashboard     │    │      Core        │    │  (CRM/ERP/etc)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                       ┌──────────────────┐
                       │  Advanced Memory │
                       │   & Analytics    │
                       └──────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- AWS CLI configured

### Installation

```bash
git clone <repository-url>
cd AmazonBedrockAC
pip install -r requirements.txt
```

### Configuration

1. Set AWS credentials:
```bash
aws configure
```

2. Update `config.py` with your settings:
```python
AWS_REGION = "us-west-2"
BEDROCK_MODEL_ID = "anthropic.claude-3-5-sonnet-20241022-v2:0"
```

### Run Application

```bash
streamlit run streamlit_app.py
```

## Core Components

### BedrockAgentCore
Main agent orchestrator with enhanced capabilities:
- Query analysis and tool selection
- Context-aware response generation
- Performance tracking

### AdvancedAgentMemory
Semantic memory system:
- Vector-based similarity search
- Conversation history management
- Context retrieval optimization

### DataRetriever
Multi-source data integration:
- CRM customer data
- ERP financial metrics
- Support ticket analysis

### AgentPerformanceTracker
Analytics and monitoring:
- Query performance metrics
- Tool usage statistics
- Response quality tracking

## API Reference

### BedrockAgentCore.invoke_agent(query)

**Parameters:**
- `query` (str): User query or business question

**Returns:**
- `Dict[str, Any]`: Structured response with analysis and metadata

**Example:**
```python
agent = BedrockAgentCore()
response = agent.invoke_agent("Analyze customer churn risk")
```

### AdvancedAgentMemory.get_enhanced_context(query)

**Parameters:**
- `query` (str): Current query for context retrieval

**Returns:**
- `Dict[str, Any]`: Relevant conversation history and context

## Configuration

### Environment Variables

```bash
AWS_REGION=us-west-2
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
```

### Data Sources Configuration

Update `retriever.py` to connect your data sources:

```python
# CRM Configuration
CRM_ENDPOINT = "your-crm-api-endpoint"
CRM_API_KEY = "your-api-key"

# ERP Configuration  
ERP_CONNECTION_STRING = "your-erp-connection"
```

## Usage Examples

### Basic Query
```python
from bedrock_agent import BedrockAgentCore

agent = BedrockAgentCore()
response = agent.invoke_agent("What are our top customer satisfaction issues?")
print(response["analysis"])
```

### Streamlit Dashboard
```python
import streamlit as st
from bedrock_agent import BedrockAgentCore

st.title("Enterprise AI Agent")
query = st.text_input("Enter your business question:")

if query:
    agent = BedrockAgentCore()
    response = agent.invoke_agent(query)
    st.write(response["analysis"])
```

## Performance Optimization

### Memory Management
- Automatic context pruning after 100 interactions
- Vector similarity threshold: 0.7
- Maximum context window: 3 recent interactions

### Caching Strategy
- Tool results cached for 5 minutes
- Memory embeddings cached for 1 hour
- Performance metrics aggregated hourly

## Monitoring & Observability

### CloudWatch Metrics
- `AgentInvocations`: Total agent calls
- `SuccessfulInvocations`: Successful responses
- `FailedInvocations`: Error count
- `AverageResponseTime`: Performance tracking

### Logging
- Structured JSON logging via Lambda Powertools
- Query and response tracking
- Error details and stack traces

## Troubleshooting

### Common Issues

**Bedrock Access Denied**
```bash
# Ensure proper IAM permissions
aws iam attach-user-policy --user-name your-user --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
```

**Memory Performance Issues**
```python
# Reduce memory context size
memory.max_context_size = 50  # Default: 100
```

**Data Source Connection Errors**
```python
# Check retriever configuration
retriever = DataRetriever()
retriever.test_connections()
```

## Development

### Project Structure
```
AmazonBedrockAC/
├── app.py                 # Streamlit application
├── bedrock_agent.py       # Main agent core
├── advanced_memory.py     # Memory system
├── agent_analytics.py     # Performance tracking
├── retriever.py          # Data integration
├── common.py             # Shared utilities
├── config.py             # Configuration
└── requirements.txt      # Dependencies
```


