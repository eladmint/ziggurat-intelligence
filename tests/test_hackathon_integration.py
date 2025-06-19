"""
🧪 Ziggurat Intelligence - Hackathon Integration Tests

Validates the ICP-OpenXAI integration and Masumi agent functionality
built during the ICP x OpenXAI x Masumi x TON Hackathon 2025.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.intelligence_engine import (
    ZigguratIntelligenceEngine,
    ExplanationMethod,
    InferenceRequest,
    ExplanationResult
)


class TestHackathonIntegration:
    """Test suite for hackathon-built integrations"""
    
    @pytest.fixture
    async def engine(self):
        """Create intelligence engine for testing"""
        return ZigguratIntelligenceEngine(
            icp_endpoint="http://localhost:8000",
            openxai_endpoint="http://localhost:8080"
        )
    
    @pytest.mark.asyncio
    async def test_icp_openxai_integration(self, engine):
        """Test ICP-OpenXAI integration works end-to-end"""
        
        # Create test request
        request = InferenceRequest(
            data={"credit_score": 720, "income": 85000},
            method=ExplanationMethod.SHAP,
            model_id="test_model",
            user_id="test_user",
            request_id="test_001"
        )
        
        # Get explanation
        result = await engine.explain_prediction(request)
        
        # Verify all components worked
        assert result.prediction is not None
        assert result.confidence > 0
        assert result.reasoning is not None
        assert result.verification_hash is not None
        assert result.verification_hash.startswith("icp_hash_")
        print(f"✅ ICP-OpenXAI Integration: {result.verification_hash}")
    
    @pytest.mark.asyncio
    async def test_all_explanation_methods(self, engine):
        """Test all XAI methods implemented during hackathon"""
        
        test_data = {"feature1": 0.5, "feature2": 0.8}
        methods = [
            ExplanationMethod.SHAP,
            ExplanationMethod.LIME,
            ExplanationMethod.GRADIENT,
            ExplanationMethod.ATTENTION
        ]
        
        for method in methods:
            request = InferenceRequest(
                data=test_data,
                method=method,
                model_id="test_model",
                user_id="test_user",
                request_id=f"test_{method.value}"
            )
            
            result = await engine.explain_prediction(request)
            
            assert result.method == method
            assert len(result.feature_importance) > 0
            assert result.verification_hash is not None
            print(f"✅ {method.value.upper()} method working")
    
    @pytest.mark.asyncio
    async def test_masumi_agent_scenario(self, engine):
        """Test Masumi agent integration with explainable AI"""
        
        # Simulate Treasury Monitor Agent scenario
        treasury_data = {
            "transaction_amount": 50000,
            "wallet_balance": 1000000,
            "transaction_frequency": "unusual",
            "time_of_day": "03:00"
        }
        
        request = InferenceRequest(
            data=treasury_data,
            method=ExplanationMethod.SHAP,
            model_id="treasury_monitor_v1",
            user_id="masumi_agent_001",
            request_id="treasury_001"
        )
        
        result = await engine.explain_prediction(request)
        
        # Verify Masumi agent gets explainable results
        assert result.confidence > 0
        assert "transaction_amount" in result.feature_importance
        assert result.reasoning is not None
        print(f"✅ Masumi Treasury Agent: {result.prediction} ({result.confidence:.1%})")
        print(f"   Reasoning: {result.reasoning[:100]}...")
    
    @pytest.mark.asyncio
    async def test_multi_chain_payment_simulation(self, engine):
        """Test multi-chain payment integration (TON + ICP)"""
        
        # Simulate premium user with TON payment
        ton_user_request = InferenceRequest(
            data={"subscription_tier": "basic_premium", "payment_method": "TON"},
            method=ExplanationMethod.LIME,
            model_id="premium_features",
            user_id="ton_user_001",
            request_id="premium_001"
        )
        
        # Simulate enterprise user with ICP payment
        icp_user_request = InferenceRequest(
            data={"subscription_tier": "intelligence_premium", "payment_method": "ICP"},
            method=ExplanationMethod.SHAP,
            model_id="enterprise_features",
            user_id="icp_user_001", 
            request_id="enterprise_001"
        )
        
        # Process both payment types
        ton_result = await engine.explain_prediction(ton_user_request)
        icp_result = await engine.explain_prediction(icp_user_request)
        
        # Verify both work
        assert ton_result.verification_hash is not None
        assert icp_result.verification_hash is not None
        print(f"✅ TON Payment User: {ton_result.verification_hash}")
        print(f"✅ ICP Payment User: {icp_result.verification_hash}")
    
    @pytest.mark.asyncio
    async def test_blockchain_verification(self, engine):
        """Test blockchain verification of explanations"""
        
        # Generate explanation
        request = InferenceRequest(
            data={"test": "verification"},
            method=ExplanationMethod.SHAP,
            model_id="verification_test",
            user_id="test_user",
            request_id="verify_001"
        )
        
        result = await engine.explain_prediction(request)
        verification_hash = result.verification_hash
        
        # Verify it exists on blockchain
        verification = await engine.verify_explanation(verification_hash)
        
        assert verification["verified"] is True
        assert verification["canister_id"] is not None
        assert verification["block_height"] > 0
        print(f"✅ Blockchain Verification: Block {verification['block_height']}")
    
    @pytest.mark.asyncio
    async def test_performance_requirements(self, engine):
        """Test performance meets hackathon requirements"""
        
        import time
        
        # Test single explanation performance
        start_time = time.time()
        
        request = InferenceRequest(
            data={"performance_test": True},
            method=ExplanationMethod.SHAP,
            model_id="performance_test",
            user_id="perf_user",
            request_id="perf_001"
        )
        
        result = await engine.explain_prediction(request)
        
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Should be under 100ms for hackathon demo
        assert latency < 100
        assert result.verification_hash is not None
        print(f"✅ Performance: {latency:.1f}ms (target: <100ms)")
    
    @pytest.mark.asyncio
    async def test_batch_processing(self, engine):
        """Test batch processing for multiple agents"""
        
        # Create multiple requests simulating different Masumi agents
        requests = [
            InferenceRequest(
                data={"agent_type": "treasury_monitor", "data": f"batch_{i}"},
                method=ExplanationMethod.SHAP,
                model_id="batch_test",
                user_id=f"agent_{i}",
                request_id=f"batch_{i}"
            )
            for i in range(5)
        ]
        
        # Process all in parallel
        start_time = time.time()
        results = await engine.batch_explain(requests)
        end_time = time.time()
        
        # Verify all succeeded
        assert len(results) == 5
        for result in results:
            assert result.verification_hash is not None
        
        total_time = (end_time - start_time) * 1000
        print(f"✅ Batch Processing: 5 explanations in {total_time:.1f}ms")
    
    @pytest.mark.asyncio
    async def test_engine_health_check(self, engine):
        """Test system health monitoring"""
        
        health = await engine.health_check()
        
        assert health["status"] == "healthy"
        assert health["icp_connection"] == "connected"
        assert health["openxai_connection"] == "connected"
        assert len(health["supported_methods"]) == 4
        print(f"✅ Health Check: {health['status']}")
        print(f"   Methods: {', '.join(health['supported_methods'])}")


@pytest.mark.asyncio
async def test_hackathon_integration_suite():
    """Run full hackathon integration test suite"""
    
    print("\n🏛️ ZIGGURAT INTELLIGENCE - HACKATHON INTEGRATION TESTS")
    print("=" * 60)
    
    # Initialize test engine
    engine = ZigguratIntelligenceEngine()
    test_suite = TestHackathonIntegration()
    
    # Run all tests
    await test_suite.test_icp_openxai_integration(engine)
    await test_suite.test_all_explanation_methods(engine)
    await test_suite.test_masumi_agent_scenario(engine)
    await test_suite.test_multi_chain_payment_simulation(engine)
    await test_suite.test_blockchain_verification(engine)
    await test_suite.test_performance_requirements(engine)
    await test_suite.test_batch_processing(engine)
    await test_suite.test_engine_health_check(engine)
    
    print("\n🎉 ALL HACKATHON INTEGRATION TESTS PASSED!")
    print("✅ ICP-OpenXAI integration working")
    print("✅ All XAI methods implemented")
    print("✅ Masumi agents functional")
    print("✅ Multi-chain payments integrated")
    print("✅ Blockchain verification active")
    print("✅ Performance requirements met")
    print("✅ System health monitoring operational")


if __name__ == "__main__":
    asyncio.run(test_hackathon_integration_suite())