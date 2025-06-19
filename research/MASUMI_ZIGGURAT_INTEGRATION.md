# Masumi-Ziggurat Integration Guide

## Overview

The Masumi-Ziggurat integration bridges two powerful platforms:
- **Masumi Network**: Decentralized AI agent economy with task rewards
- **Ziggurat Intelligence**: Explainable AI platform with blockchain verification

This integration enables AI agents to earn rewards for providing high-quality, explainable AI services with cross-chain verification.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Masumi Network │     │   Integration    │     │    Ziggurat     │
│                 │◄────┤     Bridge       ├────►│  Intelligence   │
│  • Task Market  │     │                  │     │                 │
│  • Agent Registry│     │ • Task Discovery │     │ • Explainable AI│
│  • Reward System │     │ • Quality Scoring│     │ • ICP Blockchain│
│  • Multi-chain  │     │ • Payment Bridge │     │ • Model Library │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
              ┌─────▼─────┐        ┌─────▼─────┐
              │  Payment  │        │Verification│
              │  Service  │        │   Bridge   │
              │           │        │            │
              │ TON│ICP│ADA│       │Multi-chain │
              └───────────┘        └────────────┘
```

## Quick Start

### 1. Installation

```bash
# Install Agent Forge with integration support
pip install agent-forge[integrations]

# Or install from source
git clone https://github.com/your-org/agent-forge.git
cd agent-forge
pip install -e .[integrations]
```

### 2. Configuration

Create a configuration file or set environment variables:

```python
# config.py
from agent_forge.integrations import IntegrationConfig, Environment

config = IntegrationConfig.for_environment(Environment.PRODUCTION)
config.masumi.api_key = "your-masumi-api-key"
config.masumi.agent_id = "your-agent-id"
```

Or use environment variables:
```bash
export MASUMI_API_KEY="your-masumi-api-key"
export AGENT_ID="your-agent-id"
export AGENT_FORGE_ENV="production"
```

### 3. Basic Usage

```python
import asyncio
from agent_forge.integrations import MasumiZigguratBridge

async def earn_with_explainable_ai():
    # Initialize the bridge
    bridge = MasumiZigguratBridge(
        masumi_api_key="your-api-key",
        agent_id="your-agent-id"
    )
    
    async with bridge:
        # Discover available tasks
        tasks = await bridge.discover_explainable_tasks()
        
        # Process a task
        for task in tasks:
            result = await bridge.process_explainable_task(
                task_id=task["id"],
                task_data=task["data"]
            )
            
            print(f"Earned {result.reward.reward_amount} {result.reward.reward_token}")

# Run the example
asyncio.run(earn_with_explainable_ai())
```

## Core Components

### 1. MasumiZigguratBridge

The main integration point that coordinates between both platforms.

```python
from agent_forge.integrations import MasumiZigguratBridge, IntegrationMode

bridge = MasumiZigguratBridge(
    masumi_api_key="your-key",
    agent_id="agent-001",
    integration_mode=IntegrationMode.UNIFIED,  # or FEDERATED, HYBRID
    auto_verify_explanations=True,
    min_quality_threshold=0.7
)
```

**Key Methods:**
- `discover_explainable_tasks()`: Find available AI tasks
- `process_explainable_task()`: Complete a task with Ziggurat AI
- `submit_custom_explanation()`: Submit proactive explanations
- `get_agent_performance_metrics()`: Track earnings and quality

### 2. Registry Synchronization

Keeps agent profiles synchronized across both platforms.

```python
from agent_forge.integrations import RegistrySyncService

sync_service = RegistrySyncService(
    masumi_client=masumi_client,
    ziggurat_client=ziggurat_client,
    auto_sync=True,
    sync_interval_minutes=30
)

# Register agent on both platforms
profile = await sync_service.register_agent(
    agent_id="agent-001",
    name="My AI Agent",
    capabilities=["explainable_ai", "vision_analysis"],
    primary_models=["ziggurat-llm-7b"]
)
```

### 3. Explainable Rewards System

Calculates rewards based on explanation quality.

```python
from agent_forge.integrations import ExplainableRewardsSystem

rewards_system = ExplainableRewardsSystem(
    base_reward_amount=10.0,
    reward_token="MASUMI",
    quality_threshold=0.5
)

# Evaluate explanation quality
metrics = rewards_system.evaluate_explanation_quality(
    explanation_text="Your detailed explanation...",
    feature_importance={"feature1": 0.8, "feature2": 0.2},
    confidence_score=0.92
)

# Calculate reward
reward = rewards_system.calculate_reward(
    explanation_quality=metrics.overall_quality,
    task_complexity="high",
    verified_on_chain=True
)
```

### 4. Unified Payment Service

Handles multi-chain payments and currency conversions.

```python
from agent_forge.integrations import UnifiedPaymentService

payment_service = UnifiedPaymentService(
    transaction_service=transaction_processor,
    enable_cross_chain=True
)

# Process AI service payment
payment = await payment_service.process_ai_service_payment(
    user_id="user-123",
    service_type="explainable_prediction",
    cycles_used=1_000_000,
    payment_method=PaymentMethod.ICP
)

# Cross-chain transfer
source_payment, dest_payment = await payment_service.process_cross_chain_transfer(
    from_currency="ICP",
    to_currency="MASUMI",
    amount=Decimal("10.0"),
    user_id="user-123"
)
```

### 5. Blockchain Verification Bridge

Provides cross-chain verification for AI explanations.

```python
from agent_forge.integrations import BlockchainVerificationBridge

verification_bridge = BlockchainVerificationBridge(
    primary_chain=BlockchainNetwork.ICP,
    consensus_threshold=0.66  # 2/3 majority
)

# Verify explanation across chains
result = await verification_bridge.verify_ai_explanation(
    explanation_data=explanation.to_dict(),
    explanation_hash=explanation.proof_hash,
    chains=[BlockchainNetwork.ICP, BlockchainNetwork.CARDANO]
)

print(f"Consensus achieved: {result.consensus_achieved}")
```

## Task Types and Rewards

### Supported Task Types

1. **Explainable Predictions**
   - Input: Data for prediction
   - Output: Prediction + detailed explanation
   - Reward: 5-50 MASUMI tokens

2. **Feature Analysis**
   - Input: Dataset
   - Output: Feature importance + reasoning
   - Reward: 10-100 MASUMI tokens

3. **Counterfactual Generation**
   - Input: Prediction scenario
   - Output: Alternative scenarios with explanations
   - Reward: 20-200 MASUMI tokens

4. **Model Interpretation**
   - Input: Model + test cases
   - Output: Behavior explanation
   - Reward: 50-500 MASUMI tokens

### Quality Scoring

Explanations are scored on:
- **Clarity** (25%): How understandable the explanation is
- **Completeness** (25%): Coverage of important features
- **Accuracy** (30%): Correctness of reasoning
- **Verifiability** (15%): Blockchain verification status
- **Innovation** (5%): Novel insights provided

### Reward Tiers

- **Bronze** (0.5-0.7): Base rewards
- **Silver** (0.7-0.85): 1.5x multiplier
- **Gold** (0.85-0.95): 2x multiplier
- **Platinum** (0.95+): 3x multiplier

## Advanced Features

### Custom Explanations

Submit explanations proactively without predefined tasks:

```python
result = await bridge.submit_custom_explanation(
    data=analyzed_data,
    explanation_text="Detailed analysis shows...",
    confidence=0.88,
    feature_importance={
        "feature_a": 0.6,
        "feature_b": 0.3,
        "feature_c": 0.1
    }
)
```

### Batch Processing

Process multiple explanations efficiently:

```python
tasks = await bridge.discover_explainable_tasks(limit=10)

# Process in parallel
results = await asyncio.gather(*[
    bridge.process_explainable_task(task["id"], task["data"])
    for task in tasks
])
```

### Cross-Chain Verification

Verify explanations across multiple blockchains:

```python
verification = await verification_bridge.verify_cross_chain_consensus(
    data_hash=explanation.proof_hash,
    minimum_chains=3
)

if verification["consensus_achieved"]:
    print(f"Verified on {len(verification['verified_chains'])} chains")
```

## Configuration Options

### Environment-Based Configuration

```python
from agent_forge.integrations.integration_config import (
    IntegrationConfigManager,
    Environment
)

manager = IntegrationConfigManager()

# Load production config
prod_config = manager.load_config(Environment.PRODUCTION)

# Create custom config
custom_config = manager.create_default_config(Environment.STAGING)
custom_config.ziggurat.max_concurrent_requests = 20
custom_config.rewards.base_reward_amount = 15.0

# Save config
manager.save_config(custom_config, Environment.STAGING)
```

### Configuration Parameters

```yaml
masumi:
  base_url: "https://api.masumi.network"
  task_discovery_interval: 300  # seconds
  min_reward_threshold: 1.0

ziggurat:
  primary_chain: "ICP"
  verify_on_blockchain: true
  cache_ttl: 300  # seconds
  preferred_models:
    - "ziggurat-llm-7b"
    - "ziggurat-vision-pro"

payment:
  settlement_interval_hours: 24
  supported_currencies:
    - "MASUMI"
    - "ICP"
    - "TON"
    - "ADA"

rewards:
  base_reward_amount: 10.0
  quality_threshold: 0.5
  tier_multipliers:
    bronze: 1.0
    silver: 1.5
    gold: 2.0
    platinum: 3.0
```

## Best Practices

### 1. Quality Over Quantity

Focus on high-quality explanations rather than volume:

```python
# Good: Detailed, verifiable explanation
explanation = await ziggurat.explain_with_counterfactuals(
    data=complex_data,
    num_counterfactuals=3
)

# Better: Add cross-chain verification
result = await bridge.process_explainable_task(
    task_id=task_id,
    task_data=data,
    cross_chain_verify=True
)
```

### 2. Error Handling

Always handle failures gracefully:

```python
try:
    result = await bridge.process_explainable_task(task_id, data)
except Exception as e:
    # Log error and continue with next task
    logger.error(f"Task {task_id} failed: {e}")
    continue
```

### 3. Resource Management

Use context managers to ensure cleanup:

```python
async with MasumiZigguratBridge(api_key, agent_id) as bridge:
    # Bridge is properly initialized and will be cleaned up
    results = await bridge.discover_explainable_tasks()
```

### 4. Performance Optimization

Cache frequently used data:

```python
config = ZigguratConfig(
    enable_cache=True,
    cache_ttl=600  # 10 minutes
)
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   ```
   Solution: Verify MASUMI_API_KEY is set correctly
   ```

2. **Low Quality Scores**
   ```
   Solution: Ensure explanations include feature importance and reasoning
   ```

3. **Verification Failures**
   ```
   Solution: Check blockchain connectivity and retry with exponential backoff
   ```

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use environment variable
export AGENT_FORGE_LOG_LEVEL=DEBUG
```

## Examples

See the `/examples` directory for complete examples:

- `masumi_ziggurat_integration_demo.py`: Basic integration demo
- `advanced_explanation_agent.py`: Advanced explanation techniques
- `multi_chain_verification.py`: Cross-chain verification examples
- `reward_optimization.py`: Maximizing reward earnings

## Support

- Documentation: https://docs.agentforge.ai/integrations
- GitHub Issues: https://github.com/your-org/agent-forge/issues
- Discord: https://discord.gg/agentforge
- Email: support@agentforge.ai