#!/usr/bin/env python3
"""
Masumi-Ziggurat Integration Demo

Demonstrates the complete integration between Masumi Network's agent economy
and Ziggurat Intelligence's explainable AI platform.

This example shows:
1. Agent registration on both platforms
2. Discovering and claiming explainable AI tasks
3. Processing tasks with Ziggurat Intelligence
4. Earning rewards based on explanation quality
5. Cross-chain verification of results
"""

import asyncio
import os
from datetime import datetime
from typing import Dict, Any

# Add parent directory to path for imports
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.integrations import (
    MasumiZigguratBridge,
    IntegrationMode,
    RegistrySyncService,
    ExplainableRewardsSystem,
    UnifiedPaymentService,
    BlockchainVerificationBridge
)
from src.core.integrations.integration_config import (
    get_integration_config,
    Environment
)
from src.core.blockchain.ziggurat import ExplanationMethod
from src.core.billing.services.transaction_processing_service import TransactionProcessingService


async def demonstrate_basic_integration():
    """Demonstrate basic Masumi-Ziggurat integration."""
    print("=== Masumi-Ziggurat Integration Demo ===\n")
    
    # Load configuration
    config = get_integration_config(Environment.DEVELOPMENT)
    
    # Initialize the integration bridge
    bridge = MasumiZigguratBridge(
        masumi_api_key=os.getenv("MASUMI_API_KEY", "demo-key"),
        agent_id="demo-agent-001",
        integration_mode=IntegrationMode.UNIFIED
    )
    
    async with bridge:
        print("✅ Integration bridge initialized\n")
        
        # 1. Discover available explainable AI tasks
        print("📋 Discovering explainable AI tasks...")
        tasks = await bridge.discover_explainable_tasks(min_reward=5.0)
        
        if tasks:
            print(f"Found {len(tasks)} explainable AI tasks:")
            for task in tasks[:3]:  # Show first 3
                print(f"  - Task {task['id']}: {task['description']}")
                print(f"    Reward: {task['reward_amount']} {task['reward_token']}")
                print(f"    Supported methods: {', '.join(task['supported_methods'])}")
            print()
            
            # 2. Process the first task
            first_task = tasks[0]
            print(f"🤖 Processing task: {first_task['id']}")
            
            # Simulate task data
            task_data = {
                "input_features": {
                    "feature_1": 0.75,
                    "feature_2": 0.45,
                    "feature_3": 0.92
                },
                "context": "Demo prediction task"
            }
            
            # Process with explainable AI
            result = await bridge.process_explainable_task(
                task_id=first_task['id'],
                task_data=task_data,
                explanation_method=ExplanationMethod.SHAP,
                include_counterfactuals=True,
                cross_chain_verify=True
            )
            
            print(f"\n✅ Task completed successfully!")
            print(f"  - Explanation confidence: {result.explanation.confidence:.2%}")
            print(f"  - Quality score: {result.quality_score:.2f}")
            print(f"  - Processing time: {result.execution_time_ms}ms")
            print(f"  - Cost: {result.total_cost_cycles:,} cycles")
            
            if result.reward:
                print(f"\n💰 Reward earned:")
                print(f"  - Amount: {result.reward.reward_amount} {result.reward.reward_token}")
                print(f"  - Transaction: {result.reward.transaction_hash}")
            
            if result.verification_proofs:
                print(f"\n🔗 Cross-chain verification:")
                for chain, proof in result.verification_proofs.items():
                    print(f"  - {chain}: {proof}")
                    
        else:
            print("No tasks available. Creating custom explanation...")
            
            # 3. Submit custom explanation
            custom_data = {"demo": "data", "value": 42}
            custom_result = await bridge.submit_custom_explanation(
                data=custom_data,
                explanation_text="This data shows high confidence patterns due to the value parameter exceeding threshold.",
                confidence=0.85,
                feature_importance={"value": 0.9, "demo": 0.1}
            )
            
            print(f"\n✅ Custom explanation submitted!")
            print(f"  - Quality score: {custom_result.quality_score:.2f}")
            print(f"  - Verification: {custom_result.explanation.blockchain_verified}")
        
        # 4. Get performance metrics
        metrics = await bridge.get_agent_performance_metrics()
        print(f"\n📊 Agent Performance Metrics:")
        print(f"  - Total tasks: {metrics['total_tasks_completed']}")
        print(f"  - Total earnings: {metrics['total_earnings']}")
        print(f"  - Average quality: {metrics['average_quality_score']:.2f}")
        print(f"  - Verification rate: {metrics['verification_rate']:.2%}")


async def demonstrate_advanced_features():
    """Demonstrate advanced integration features."""
    print("\n=== Advanced Integration Features ===\n")
    
    # Initialize all integration components
    config = get_integration_config(Environment.DEVELOPMENT)
    
    # 1. Registry Synchronization
    print("🔄 Demonstrating Registry Synchronization...")
    
    bridge = MasumiZigguratBridge(
        masumi_api_key=os.getenv("MASUMI_API_KEY", "demo-key"),
        agent_id="advanced-agent-002"
    )
    
    async with bridge:
        sync_service = RegistrySyncService(
            masumi_client=bridge.masumi_client,
            ziggurat_client=bridge.ziggurat_client,
            auto_sync=True
        )
        
        # Register agent
        profile = await sync_service.register_agent(
            agent_id="advanced-agent-002",
            name="Advanced Demo Agent",
            description="Demonstrates advanced Masumi-Ziggurat integration",
            capabilities=[
                "explainable_ai",
                "multi_chain_verification",
                "counterfactual_analysis"
            ],
            primary_models=["ziggurat-llm-7b", "ziggurat-vision-pro"],
            supported_chains=["ICP", "CARDANO", "TON"]
        )
        
        print(f"✅ Agent registered: {profile.name}")
        print(f"  - Capabilities: {len(profile.capabilities)}")
        print(f"  - Supported chains: {', '.join(profile.supported_chains)}")
        
        # 2. Rewards System
        print("\n💎 Demonstrating Rewards System...")
        
        rewards_system = ExplainableRewardsSystem(
            base_reward_amount=10.0,
            reward_token="MASUMI"
        )
        
        # Evaluate explanation quality
        explanation_metrics = rewards_system.evaluate_explanation_quality(
            explanation_text="The model predicts a positive outcome with 92% confidence due to feature_1 having the highest importance (0.75). This aligns with historical patterns where feature_1 > 0.7 correlates strongly with positive results.",
            feature_importance={"feature_1": 0.75, "feature_2": 0.15, "feature_3": 0.10},
            confidence_score=0.92,
            has_counterfactuals=True,
            verified_on_chain=True
        )
        
        print(f"✅ Explanation Quality Evaluated:")
        print(f"  - Clarity: {explanation_metrics.clarity_score:.2f}")
        print(f"  - Completeness: {explanation_metrics.completeness_score:.2f}")
        print(f"  - Accuracy: {explanation_metrics.accuracy_score:.2f}")
        print(f"  - Overall: {explanation_metrics.overall_quality:.2f}")
        
        # Calculate reward
        reward = rewards_system.calculate_reward(
            explanation_quality=explanation_metrics.overall_quality,
            task_complexity="high",
            explanation_method=ExplanationMethod.SHAP,
            verified_on_chain=True,
            processing_time_ms=850,
            agent_reputation=0.75
        )
        
        print(f"\n💰 Reward Calculation:")
        print(f"  - Base amount: {reward.base_amount}")
        print(f"  - Quality multiplier: {reward.quality_multiplier}x")
        print(f"  - Bonuses: {reward.complexity_bonus + reward.verification_bonus + reward.speed_bonus:.2f}")
        print(f"  - Total: {reward.total_amount} {reward.reward_token}")
        print(f"  - Tier: {reward.tier.value.upper()}")
        
        # 3. Blockchain Verification
        print("\n🔗 Demonstrating Blockchain Verification...")
        
        verification_bridge = BlockchainVerificationBridge(
            consensus_threshold=0.66
        )
        
        # Verify across multiple chains
        verification_result = await verification_bridge.verify_ai_explanation(
            explanation_data={
                "reasoning": "Test explanation",
                "confidence": 0.92,
                "timestamp": datetime.utcnow().isoformat()
            },
            explanation_hash="test-hash-" + datetime.utcnow().strftime("%Y%m%d%H%M%S"),
            chains=[
                BlockchainNetwork.ICP,
                BlockchainNetwork.CARDANO,
                BlockchainNetwork.TON
            ]
        )
        
        print(f"✅ Cross-Chain Verification Complete:")
        print(f"  - Primary chain: {verification_result.primary_proof.blockchain.value}")
        print(f"  - Verified chains: {verification_result.verified_chains}/{verification_result.total_chains}")
        print(f"  - Consensus achieved: {'Yes' if verification_result.consensus_achieved else 'No'}")
        print(f"  - Consensus percentage: {(verification_result.verified_chains / verification_result.total_chains) * 100:.0f}%")


async def demonstrate_payment_flow():
    """Demonstrate unified payment system."""
    print("\n=== Payment System Demo ===\n")
    
    # Mock transaction service for demo
    class MockTransactionService(TransactionProcessingService):
        async def process_payment(self, **kwargs):
            return {
                "success": True,
                "transaction_id": f"demo-tx-{datetime.utcnow().timestamp()}"
            }
    
    payment_service = UnifiedPaymentService(
        transaction_service=MockTransactionService(None)  # type: ignore
    )
    
    # 1. Process AI service payment
    print("💳 Processing AI Service Payment...")
    
    ai_payment = await payment_service.process_ai_service_payment(
        user_id="demo-user",
        service_type="explainable_prediction",
        cycles_used=2_500_000,  # 2.5M cycles
        payment_method="ICP",  # type: ignore
        explanation_id="exp-123"
    )
    
    print(f"✅ AI Service Payment Processed:")
    print(f"  - Amount: {ai_payment.amount} {ai_payment.currency}")
    print(f"  - Status: {ai_payment.status}")
    print(f"  - Transaction: {ai_payment.transaction_hash}")
    
    # 2. Estimate service costs
    print("\n💰 Service Cost Estimation:")
    
    cost_estimate = await payment_service.estimate_service_cost(
        service_type="complex_analysis",
        estimated_cycles=10_000_000,  # 10M cycles
        preferred_currency="ICP"
    )
    
    print("Estimated costs for 10M cycles:")
    for currency, estimate in cost_estimate["cost_estimates"].items():
        print(f"  - {currency}: {estimate['amount']} (~${estimate['usd_equivalent']} USD)")
    
    # 3. Check balance summary
    print("\n📊 Balance Summary:")
    
    balances = await payment_service.get_balance_summary("demo-user")
    for currency, balance in balances.items():
        if balance != 0:
            print(f"  - {currency}: {balance}")


async def main():
    """Run all demonstrations."""
    try:
        # Basic integration
        await demonstrate_basic_integration()
        
        # Advanced features
        await demonstrate_advanced_features()
        
        # Payment flow
        await demonstrate_payment_flow()
        
        print("\n✅ All demonstrations completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())