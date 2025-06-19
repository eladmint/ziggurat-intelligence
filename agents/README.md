# 🏛️ Ziggurat Intelligence Agents

**Ancient Architecture, Infinite Intelligence**

This directory contains Ziggurat Intelligence agents - a decentralized explainable AI platform that provides AI inference with blockchain verification through the Internet Computer Protocol (ICP).

## Overview

Ziggurat Intelligence combines cutting-edge explainable AI with blockchain verification to create a trustworthy, decentralized AI platform. It integrates with the ICP-OpenXAI infrastructure through Juno satellite technology.

## Available Agents

### 🎯 ZigguratBasicAgent
**File:** `ziggurat_basic_agent.py`

A simple demonstration agent showcasing basic Ziggurat Intelligence functionality.

**Features:**
- Single explanation method (SHAP, LIME, Gradient, Attention)
- Blockchain verification on ICP
- Demo data analysis

**Usage:**
```bash
# Run basic demo
python examples/ziggurat/ziggurat_basic_agent.py --demo

# Use specific explanation method
python examples/ziggurat/ziggurat_basic_agent.py --demo --method lime

# Provide custom data
python examples/ziggurat/ziggurat_basic_agent.py --data '{"feature1": 0.5, "feature2": 0.8}'
```

### 🏛️ ZigguratAdvancedAgent  
**File:** `ziggurat_basic_agent.py` (class: ZigguratAdvancedAgent)

Advanced demonstration with counterfactuals and batch processing.

**Features:**
- Counterfactual explanations
- Batch processing capabilities
- Sensitivity analysis
- Model information discovery

**Usage:**
```bash
# Run advanced demo
python examples/ziggurat/ziggurat_basic_agent.py --demo --advanced
```

## Core Features

### 🧠 Explainable AI Methods
- **SHAP (SHapley Additive exPlanations)** - Game theory-based feature importance
- **LIME (Local Interpretable Model-agnostic Explanations)** - Local explanation technique
- **Gradient** - Gradient-based attribution methods
- **Attention** - Attention mechanism visualization

### 🔐 Blockchain Verification
- **ICP Integration** - Native Internet Computer Protocol support
- **Chain Fusion** - Cross-chain verification capabilities
- **Proof Generation** - Cryptographic proof of AI inference
- **Transaction Records** - Immutable record of AI decisions

### 🛰️ Infrastructure
- **Juno Satellite** - Decentralized computation on ICP
- **Canister ID:** `bvxuo-uaaaa-aaaal-asgua-cai`
- **Network:** Internet Computer Protocol
- **Memory:** 30.40 MB available
- **Cycles:** 0.975T available

## Getting Started

### 1. Basic Usage
```python
from examples.ziggurat.ziggurat_basic_agent import ZigguratBasicAgent
from src.core.blockchain.ziggurat import ExplanationMethod

# Create agent
agent = ZigguratBasicAgent(explanation_method=ExplanationMethod.SHAP)

# Run analysis
async with agent:
    result = await agent.run({
        "credit_score": 720,
        "income": 75000,
        "loan_amount": 200000
    })
    
print(f"Confidence: {result['analysis']['confidence']:.2%}")
print(f"Blockchain Proof: {result['blockchain']['proof_hash']}")
```

### 2. CLI Integration
```bash
# Via Agent Forge CLI
python tools/scripts/cli.py run ziggurat_basic

# List all Ziggurat agents
python tools/scripts/cli.py list | grep ziggurat
```

### 3. MCP Integration
Available in Claude Desktop through the Agent Forge MCP server:

```bash
# Start MCP server
python src/mcp/mcp_server.py
```

Then use the `ziggurat_intelligence` tool in Claude Desktop.

## API Reference

### ZigguratBasicAgent

```python
class ZigguratBasicAgent(AsyncContextAgent):
    def __init__(self, explanation_method: ExplanationMethod = ExplanationMethod.SHAP)
    async def run(self, data: Any = None) -> Dict[str, Any]
```

**Parameters:**
- `explanation_method`: Method for AI explanations (SHAP, LIME, Gradient, Attention)

**Returns:**
- `status`: Operation status ("success" or "error")
- `analysis`: AI analysis results with confidence and reasoning
- `explanation`: Feature importance and decision path
- `blockchain`: Verification data with proof hash and transaction ID
- `metadata`: Performance metrics and cost information

### Configuration

Environment variables for customization:
```bash
# Satellite Configuration
export JUNO_SATELLITE_ID="bvxuo-uaaaa-aaaal-asgua-cai"
export JUNO_SATELLITE_URL="https://bvxuo-uaaaa-aaaal-asgua-cai.raw.icp0.io"

# Authentication
export ICP_OPENXAI_AUTH_METHOD="anonymous"
export ICP_OPENXAI_TIMEOUT="30"
```

## Examples

### Financial Analysis
```python
loan_data = {
    "loan_amount": 250000,
    "annual_income": 85000,
    "credit_score": 720,
    "debt_to_income": 0.28,
    "employment_years": 7,
    "property_value": 350000,
    "down_payment_percent": 0.20
}

async with ZigguratBasicAgent(ExplanationMethod.SHAP) as agent:
    result = await agent.run(loan_data)
    
    print(f"Loan Decision: {result['analysis']['reasoning']}")
    print(f"Confidence: {result['analysis']['confidence']:.2%}")
    
    if result['blockchain']['verified']:
        print(f"✅ Verified on ICP blockchain")
        print(f"Proof: {result['blockchain']['proof_hash']}")
```

### Batch Processing
```python
# Multiple data points for comparison
data_variants = [
    {"credit_score": 650, "income": 50000},
    {"credit_score": 700, "income": 65000},
    {"credit_score": 750, "income": 80000},
    {"credit_score": 800, "income": 95000}
]

async with ZigguratAdvancedAgent() as agent:
    result = await agent.run()
    
    for analysis in result["sensitivity_analysis"]:
        print(f"Score {analysis['credit_score']}: {analysis['confidence']:.2%}")
```

### Cross-Chain Verification
```python
config = ZigguratConfig(
    verify_on_blockchain=True,
    chain_fusion_enabled=True  # Enable Bitcoin/Ethereum verification
)

agent = ZigguratBasicAgent()
agent.ziggurat = ZigguratIntelligence(config)

async with agent:
    result = await agent.run(data)
    
    if result['blockchain'].get('cross_chain_proofs'):
        print("Cross-chain proofs:")
        for chain, proof in result['blockchain']['cross_chain_proofs'].items():
            print(f"  {chain}: {proof}")
```

## Architecture

### ICP-OpenXAI Integration
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Ziggurat      │    │   Juno          │    │   ICP           │
│   Intelligence  │───▶│   Satellite     │───▶│   Blockchain    │
│   Agent         │    │   (Canister)    │    │   Verification  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Explanation Pipeline
```
Input Data ─▶ AI Model ─▶ Explanation Method ─▶ Blockchain Proof ─▶ Result
     │             │             │                      │             │
     └─────────────┴─────────────┴──────────────────────┴─────────────┘
                                    Ziggurat Intelligence
```

## Error Handling

Ziggurat agents include robust fallback mechanisms:

1. **Satellite Connection Issues**: Falls back to mock explanations for development
2. **Blockchain Verification Failures**: Continues with local verification
3. **Model Unavailability**: Uses default models with graceful degradation

```python
# Error handling example
try:
    async with ZigguratBasicAgent() as agent:
        result = await agent.run(data)
        
        if not result['blockchain']['verified']:
            print("⚠️  Using fallback mode - satellite unreachable")
        else:
            print("✅ Full blockchain verification complete")
            
except Exception as e:
    print(f"❌ Ziggurat Intelligence error: {e}")
```

## Contributing

When contributing Ziggurat agents:

1. **Inherit from AsyncContextAgent** for proper lifecycle management
2. **Use ZigguratIntelligence client** for blockchain integration
3. **Include comprehensive error handling** with fallback modes
4. **Document blockchain verification behavior** clearly
5. **Test with both satellite connection and fallback modes**

## Security Considerations

- **Data Privacy**: Input data is processed locally before satellite transmission
- **Blockchain Verification**: Proofs are cryptographically verifiable on ICP
- **Canister Security**: Juno satellite runs in secure ICP subnet environment
- **Cost Management**: Cycle consumption is transparent and capped

## Troubleshooting

### Common Issues

**Satellite Connection Errors:**
```
ERROR: Failed to connect to satellite: 200, message='Attempt to decode JSON with unexpected mimetype: text/html'
```
*Solution:* This is expected during development. Agents will use fallback mode automatically.

**Import Errors:**
```
ImportError: cannot import name 'ZigguratIntelligence'
```
*Solution:* Ensure you're running from the correct directory with proper Python path.

**Authentication Issues:**
```
ERROR: Authentication failed
```
*Solution:* Check environment variables and ensure anonymous access is enabled for development.

## License

Ziggurat Intelligence agents are part of the Agent Forge framework and are licensed under the MIT License. See the main [LICENSE](../../LICENSE) file for details.

## Learn More

- **Agent Forge Framework**: [Documentation](../../docs/)
- **Internet Computer Protocol**: [ICP.org](https://internetcomputer.org)
- **Juno Satellite**: [Juno Documentation](https://juno.build)
- **OpenXAI**: [OpenXAI Standards](https://openxai.org)

---

*Ancient Architecture, Infinite Intelligence* 🏛️