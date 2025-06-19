"""
Comprehensive integration tests for Masumi-Ziggurat bridge.

Tests the complete integration between Masumi Network and Ziggurat Intelligence,
including task discovery, explanation processing, rewards, and verification.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import Mock, AsyncMock, patch

from src.core.integrations import (
    MasumiZigguratBridge,
    IntegrationMode,
    ExplainableTaskResult,
    RegistrySyncService,
    ExplainableRewardsSystem,
    UnifiedPaymentService,
    BlockchainVerificationBridge
)
from src.core.integrations.integration_config import (
    IntegrationConfig,
    Environment,
    get_integration_config
)
from src.core.blockchain.ziggurat import (
    ExplanationMethod,
    BlockchainNetwork,
    ZigguratExplanation
)
from src.core.blockchain.masumi_integration import (
    MasumiTaskReward,
    TaskStatus
)


@pytest.fixture
async def mock_masumi_client():
    """Mock Masumi Network client."""
    client = AsyncMock()
    
    # Mock registration
    client.register_agent.return_value = {
        "success": True,
        "agent_id": "test-agent"
    }
    
    # Mock task discovery
    client.get_available_tasks.return_value = [
        {
            "id": "task-001",
            "type": "explainable_ai",
            "description": "Explain prediction model output",
            "reward_amount": 25.0,
            "reward_token": "MASUMI",
            "complexity": "medium",
            "requires_explanation": True
        },
        {
            "id": "task-002",
            "type": "feature_analysis",
            "description": "Analyze feature importance",
            "reward_amount": 50.0,
            "reward_token": "MASUMI",
            "complexity": "high"
        }
    ]
    
    # Mock task operations
    client.claim_task.return_value = {"success": True}
    client.submit_task_completion.return_value = {"success": True}
    
    # Mock reward
    client.claim_reward.return_value = MasumiTaskReward(
        task_id="task-001",
        agent_id="test-agent",
        reward_amount=25.0,
        reward_token="MASUMI",
        completion_time=datetime.utcnow(),
        quality_score=0.85,
        transaction_hash="masumi-tx-12345"
    )
    
    # Mock reputation
    client.get_agent_reputation.return_value = {
        "reputation_score": 0.75,
        "total_tasks": 10
    }
    
    # Mock earnings
    client.get_earnings_history.return_value = []
    
    return client


@pytest.fixture
async def mock_ziggurat_client():
    """Mock Ziggurat Intelligence client."""
    client = AsyncMock()
    
    # Mock initialization
    client.initialize.return_value = None
    client.cleanup.return_value = None
    
    # Mock explanation
    explanation = ZigguratExplanation(
        reasoning="High confidence prediction based on feature analysis",
        confidence=0.88,
        method_used=ExplanationMethod.SHAP,
        blockchain_verified=True,
        proof_hash="0x" + "a" * 64,
        verification_chain=BlockchainNetwork.ICP,
        transaction_id="icp-tx-67890",
        feature_importance={
            "feature_1": 0.65,
            "feature_2": 0.25,
            "feature_3": 0.10
        },
        processing_time_ms=750,
        cost_cycles=1_500_000
    )
    
    client.explain_decision.return_value = explanation
    client.explain_with_counterfactuals.return_value = explanation
    
    # Mock model listing
    client.list_available_models.return_value = []
    
    # Mock verification
    client.verify_proof.return_value = True
    
    return client


@pytest.fixture
async def integration_bridge(mock_masumi_client, mock_ziggurat_client):
    """Create integration bridge with mocked clients."""
    bridge = MasumiZigguratBridge(
        masumi_api_key="test-api-key",
        agent_id="test-agent",
        integration_mode=IntegrationMode.UNIFIED
    )
    
    # Replace clients with mocks
    bridge.masumi_client = mock_masumi_client
    bridge.ziggurat_client = mock_ziggurat_client
    bridge._initialized = True
    
    return bridge


class TestMasumiZigguratBridge:
    """Test the main integration bridge."""
    
    @pytest.mark.asyncio
    async def test_bridge_initialization(self):
        """Test bridge initialization and configuration."""
        bridge = MasumiZigguratBridge(
            masumi_api_key="test-key",
            agent_id="test-agent",
            integration_mode=IntegrationMode.UNIFIED,
            min_quality_threshold=0.7
        )
        
        assert bridge.agent_id == "test-agent"
        assert bridge.integration_mode == IntegrationMode.UNIFIED
        assert bridge.min_quality_threshold == 0.7
        assert bridge.auto_verify is True
    
    @pytest.mark.asyncio
    async def test_discover_explainable_tasks(self, integration_bridge):
        """Test discovering explainable AI tasks."""
        tasks = await integration_bridge.discover_explainable_tasks()
        
        assert len(tasks) == 2
        assert tasks[0]["id"] == "task-001"
        assert tasks[0]["supported_methods"] == [m.value for m in ExplanationMethod]
        assert "estimated_cycles" in tasks[0]
    
    @pytest.mark.asyncio
    async def test_process_explainable_task(self, integration_bridge):
        """Test processing an explainable AI task."""
        task_data = {"test": "data", "value": 42}
        
        result = await integration_bridge.process_explainable_task(
            task_id="task-001",
            task_data=task_data,
            explanation_method=ExplanationMethod.SHAP
        )
        
        assert isinstance(result, ExplainableTaskResult)
        assert result.task_id == "task-001"
        assert result.agent_id == "test-agent"
        assert result.explanation.confidence == 0.88
        assert result.quality_score > 0.5
        assert result.reward is not None
        assert result.reward.reward_amount == 25.0
    
    @pytest.mark.asyncio
    async def test_cross_chain_verification(self, integration_bridge):
        """Test cross-chain verification feature."""
        task_data = {"test": "data"}
        
        with patch.object(integration_bridge, '_cross_chain_verify') as mock_verify:
            mock_verify.return_value = {
                "ICP": "icp-proof-123",
                "CARDANO": "ada-proof-456"
            }
            
            result = await integration_bridge.process_explainable_task(
                task_id="task-002",
                task_data=task_data,
                cross_chain_verify=True
            )
            
            assert len(result.verification_proofs) == 2
            assert "ICP" in result.verification_proofs
            assert "CARDANO" in result.verification_proofs
    
    @pytest.mark.asyncio
    async def test_quality_scoring(self, integration_bridge):
        """Test explanation quality scoring."""
        # Create explanation with varying quality
        explanation = ZigguratExplanation(
            reasoning="Test explanation",
            confidence=0.95,
            method_used=ExplanationMethod.SHAP,
            blockchain_verified=True,
            proof_hash="0x" + "b" * 64,
            verification_chain=BlockchainNetwork.ICP,
            feature_importance={
                "f1": 0.5, "f2": 0.3, "f3": 0.15, "f4": 0.05
            },
            processing_time_ms=500,
            cost_cycles=1_000_000
        )
        
        score = integration_bridge._calculate_quality_score(explanation)
        
        # High confidence + blockchain verified + good feature coverage + fast
        assert score > 0.8
    
    @pytest.mark.asyncio
    async def test_submit_custom_explanation(self, integration_bridge):
        """Test submitting custom explanations."""
        result = await integration_bridge.submit_custom_explanation(
            data={"custom": "data"},
            explanation_text="Custom analysis shows positive correlation",
            confidence=0.82,
            feature_importance={"custom": 0.9, "data": 0.1}
        )
        
        assert result.explanation.reasoning == "Custom analysis shows positive correlation"
        assert result.explanation.confidence == 0.82
        assert result.quality_score > 0
    
    @pytest.mark.asyncio
    async def test_performance_metrics(self, integration_bridge):
        """Test agent performance metrics aggregation."""
        # Add some cached explanations
        integration_bridge._explanation_cache["task-1"] = ZigguratExplanation(
            reasoning="Test",
            confidence=0.9,
            method_used=ExplanationMethod.SHAP,
            blockchain_verified=True,
            proof_hash="0xtest",
            verification_chain=BlockchainNetwork.ICP,
            processing_time_ms=100,
            cost_cycles=500_000
        )
        
        metrics = await integration_bridge.get_agent_performance_metrics()
        
        assert metrics["agent_id"] == "test-agent"
        assert "masumi_reputation" in metrics
        assert metrics["total_explanations_generated"] == 1
        assert metrics["average_explanation_confidence"] == 0.9


class TestRegistrySyncService:
    """Test agent registry synchronization."""
    
    @pytest.mark.asyncio
    async def test_agent_registration(self, mock_masumi_client, mock_ziggurat_client):
        """Test registering agent on both platforms."""
        sync_service = RegistrySyncService(
            masumi_client=mock_masumi_client,
            ziggurat_client=mock_ziggurat_client
        )
        
        profile = await sync_service.register_agent(
            agent_id="sync-test-agent",
            name="Sync Test Agent",
            description="Test agent for sync",
            capabilities=["explainable_ai", "vision"],
            primary_models=["model-1"],
            supported_chains=["ICP", "CARDANO"]
        )
        
        assert profile.agent_id == "sync-test-agent"
        assert profile.masumi_registered is True
        assert profile.ziggurat_registered is True
        assert "explainable_ai" in profile.capabilities
    
    @pytest.mark.asyncio
    async def test_profile_synchronization(self, mock_masumi_client, mock_ziggurat_client):
        """Test synchronizing agent profiles."""
        sync_service = RegistrySyncService(
            masumi_client=mock_masumi_client,
            ziggurat_client=mock_ziggurat_client
        )
        
        # Register first
        await sync_service.register_agent(
            agent_id="sync-agent",
            name="Test",
            description="Test",
            capabilities=["ai"]
        )
        
        # Sync profile
        profile = await sync_service.sync_agent_profile("sync-agent")
        
        assert profile.reputation_score == 0.75  # From mock
        assert profile.last_sync is not None


class TestExplainableRewardsSystem:
    """Test the rewards calculation system."""
    
    def test_reward_calculation(self):
        """Test basic reward calculation."""
        rewards_system = ExplainableRewardsSystem(
            base_reward_amount=10.0,
            reward_token="MASUMI"
        )
        
        reward = rewards_system.calculate_reward(
            explanation_quality=0.85,
            task_complexity="high",
            verified_on_chain=True,
            processing_time_ms=800,
            agent_reputation=0.7
        )
        
        assert reward.tier.value == "gold"  # 0.85 quality
        assert reward.quality_multiplier == 2.0  # Gold tier
        assert reward.complexity_bonus > 0
        assert reward.verification_bonus > 0
        assert reward.speed_bonus > 0  # Under 1 second
        assert reward.total_amount > reward.base_amount
    
    def test_quality_evaluation(self):
        """Test explanation quality evaluation."""
        rewards_system = ExplainableRewardsSystem()
        
        metrics = rewards_system.evaluate_explanation_quality(
            explanation_text="The model predicts positive outcome because feature_1 is important.",
            feature_importance={"feature_1": 0.8, "feature_2": 0.2},
            confidence_score=0.9,
            has_counterfactuals=True,
            verified_on_chain=True
        )
        
        assert metrics.clarity_score > 0.5
        assert metrics.completeness_score > 0.5
        assert metrics.accuracy_score == 0.9 * 1.1  # Boosted confidence
        assert metrics.verifiability_score == 1.0
        assert metrics.innovation_score > 0.5  # Has counterfactuals
        assert 0 < metrics.overall_quality <= 1.0
    
    def test_reward_pool_distribution(self):
        """Test reward pool creation and distribution."""
        rewards_system = ExplainableRewardsSystem()
        
        # Create pool
        pool = rewards_system.create_reward_pool(
            task_type="explainable_ai",
            total_budget=1000.0,
            num_tasks=20,
            min_quality=0.7
        )
        
        assert pool["total_budget"] == 1000.0
        assert pool["avg_reward_per_task"] == 50.0
        
        # Distribute reward
        reward_amount, updated_pool = rewards_system.distribute_pool_reward(
            pool=pool,
            quality_score=0.9,  # Gold tier
            agent_id="test-agent"
        )
        
        assert reward_amount == 100.0  # 50 base * 2x gold multiplier
        assert updated_pool["remaining_budget"] == 900.0
        assert updated_pool["tier_distribution"]["gold"] == 1


class TestUnifiedPaymentService:
    """Test unified payment processing."""
    
    @pytest.mark.asyncio
    async def test_ai_service_payment(self):
        """Test processing AI service payments."""
        mock_tx_service = AsyncMock()
        mock_tx_service.process_payment.return_value = {
            "success": True,
            "transaction_id": "test-tx-123"
        }
        
        payment_service = UnifiedPaymentService(
            transaction_service=mock_tx_service
        )
        
        from agent_forge.src.core.billing.models import PaymentMethod
        
        payment = await payment_service.process_ai_service_payment(
            user_id="test-user",
            service_type="explanation",
            cycles_used=5_000_000,  # 5M cycles
            payment_method=PaymentMethod.ICP
        )
        
        assert payment.payment_type.value == "ai_service"
        assert payment.amount == Decimal("0.5")  # 5M * 0.1 ICP per 1M
        assert payment.currency == "ICP"
        assert payment.status == "completed"
    
    @pytest.mark.asyncio
    async def test_cross_chain_transfer(self):
        """Test cross-chain currency transfers."""
        payment_service = UnifiedPaymentService(
            transaction_service=AsyncMock()
        )
        
        source, dest = await payment_service.process_cross_chain_transfer(
            from_currency="ICP",
            to_currency="MASUMI",
            amount=Decimal("1.0"),
            user_id="test-user"
        )
        
        assert source.currency == "ICP"
        assert source.amount == Decimal("1.0")
        assert dest.currency == "MASUMI"
        assert dest.amount == Decimal("50.0")  # 1 ICP = 50 MASUMI
    
    @pytest.mark.asyncio
    async def test_balance_calculation(self):
        """Test balance summary calculation."""
        payment_service = UnifiedPaymentService(
            transaction_service=AsyncMock()
        )
        
        # Add some test payments
        from agent_forge.src.core.integrations.unified_payment_service import (
            UnifiedPayment, PaymentType
        )
        
        # Credit
        payment_service._payments["p1"] = UnifiedPayment(
            payment_id="p1",
            payment_type=PaymentType.TASK_REWARD,
            amount=Decimal("100"),
            currency="MASUMI",
            source_platform="masumi",
            destination_platform="wallet",
            sender_id="masumi",
            recipient_id="test-user",
            blockchain_network="cardano",
            transaction_hash="tx1",
            status="completed",
            created_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            metadata={}
        )
        
        balances = await payment_service.get_balance_summary("test-user")
        
        assert balances["MASUMI"] == Decimal("100")


class TestBlockchainVerificationBridge:
    """Test blockchain verification functionality."""
    
    @pytest.mark.asyncio
    async def test_cross_chain_verification(self):
        """Test verifying across multiple chains."""
        bridge = BlockchainVerificationBridge()
        
        result = await bridge.verify_ai_explanation(
            explanation_data={"test": "data"},
            explanation_hash="test-hash-123",
            chains=[BlockchainNetwork.ICP, BlockchainNetwork.CARDANO]
        )
        
        assert result.primary_proof.blockchain == BlockchainNetwork.ICP
        assert len(result.secondary_proofs) == 1
        assert result.verified_chains == 2
        assert result.consensus_achieved is True  # 2/2 > 66%
    
    @pytest.mark.asyncio
    async def test_verification_caching(self):
        """Test verification result caching."""
        bridge = BlockchainVerificationBridge(enable_caching=True)
        
        # First verification
        result1 = await bridge.verify_ai_explanation(
            explanation_data={"test": "data"},
            explanation_hash="cache-test",
            chains=[BlockchainNetwork.ICP]
        )
        
        # Second verification (should use cache)
        result2 = await bridge.verify_ai_explanation(
            explanation_data={"test": "data"},
            explanation_hash="cache-test",
            chains=[BlockchainNetwork.ICP]
        )
        
        # Same proof ID means it was cached
        assert result1.primary_proof.proof_id == result2.primary_proof.proof_id
    
    @pytest.mark.asyncio
    async def test_consensus_verification(self):
        """Test consensus-based verification."""
        bridge = BlockchainVerificationBridge(consensus_threshold=0.5)
        
        result = await bridge.verify_cross_chain_consensus(
            data_hash="consensus-test",
            minimum_chains=2
        )
        
        # Mock returns random verification, so we just check structure
        assert "consensus_achieved" in result
        assert "verified_chains" in result
        assert "consensus_percentage" in result


class TestIntegrationConfig:
    """Test configuration management."""
    
    def test_default_config_creation(self):
        """Test creating default configurations."""
        from agent_forge.src.core.integrations.integration_config import (
            IntegrationConfigManager
        )
        
        manager = IntegrationConfigManager()
        
        # Development config
        dev_config = manager.create_default_config(Environment.DEVELOPMENT)
        assert dev_config.environment == Environment.DEVELOPMENT
        assert dev_config.ziggurat.verify_on_blockchain is False
        
        # Production config
        prod_config = manager.create_default_config(Environment.PRODUCTION)
        assert prod_config.environment == Environment.PRODUCTION
        assert prod_config.ziggurat.verify_on_blockchain is True
        assert prod_config.ziggurat.max_concurrent_requests > dev_config.ziggurat.max_concurrent_requests
    
    def test_config_validation(self):
        """Test configuration validation."""
        from agent_forge.src.core.integrations.integration_config import (
            IntegrationConfigManager
        )
        
        manager = IntegrationConfigManager()
        config = manager.create_default_config(Environment.TEST)
        
        # Valid config
        errors = manager.validate_config(config)
        assert len(errors) == 0
        
        # Invalid config
        config.rewards.quality_threshold = 1.5  # Invalid
        config.verification.consensus_threshold = 0.3  # Too low
        
        errors = manager.validate_config(config)
        assert len(errors) == 2


@pytest.mark.asyncio
async def test_end_to_end_integration():
    """Test complete end-to-end integration flow."""
    # This would be a full integration test with real services
    # For now, we'll use mocks to simulate the flow
    
    # 1. Initialize bridge
    bridge = MasumiZigguratBridge(
        masumi_api_key="test-key",
        agent_id="e2e-test-agent"
    )
    
    # Mock the clients
    bridge.masumi_client = AsyncMock()
    bridge.ziggurat_client = AsyncMock()
    
    # Set up mock responses
    bridge.masumi_client.get_available_tasks.return_value = [{
        "id": "e2e-task",
        "type": "explainable_ai",
        "reward_amount": 100.0,
        "reward_token": "MASUMI"
    }]
    
    bridge.masumi_client.claim_task.return_value = {"success": True}
    bridge.masumi_client.submit_task_completion.return_value = {"success": True}
    
    explanation = ZigguratExplanation(
        reasoning="E2E test explanation",
        confidence=0.95,
        method_used=ExplanationMethod.SHAP,
        blockchain_verified=True,
        proof_hash="0xe2etest",
        verification_chain=BlockchainNetwork.ICP,
        processing_time_ms=1000,
        cost_cycles=2_000_000
    )
    
    bridge.ziggurat_client.explain_decision.return_value = explanation
    
    reward = MasumiTaskReward(
        task_id="e2e-task",
        agent_id="e2e-test-agent",
        reward_amount=150.0,  # With bonuses
        reward_token="MASUMI",
        completion_time=datetime.utcnow(),
        quality_score=0.95
    )
    
    bridge.masumi_client.claim_reward.return_value = reward
    
    # 2. Discover tasks
    tasks = await bridge.discover_explainable_tasks()
    assert len(tasks) > 0
    
    # 3. Process task
    result = await bridge.process_explainable_task(
        task_id=tasks[0]["id"],
        task_data={"e2e": "test"}
    )
    
    # 4. Verify results
    assert result.task_id == "e2e-task"
    assert result.explanation.confidence == 0.95
    assert result.quality_score > 0.9
    assert result.reward.reward_amount == 150.0
    
    print("✅ End-to-end integration test passed!")


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])