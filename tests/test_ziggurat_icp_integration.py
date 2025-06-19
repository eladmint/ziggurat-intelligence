"""
Integration tests for Ziggurat ICP-OpenXAI communication.

Tests the integration between Ziggurat Intelligence and ICP/OpenXAI platforms,
including satellite communication, canister interactions, and cross-chain functionality.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import aiohttp
from typing import Dict, Any, List
import json
from datetime import datetime, timedelta

from src.core.blockchain.ziggurat import (
    ZigguratIntelligence, 
    ZigguratConfig,
    ExplanationMethod,
    BlockchainNetwork
)
from src.core.blockchain.ziggurat.icp_openxai_client import ICPOpenXAIClient


@pytest.fixture
def icp_test_config():
    """ICP test configuration."""
    return {
        "satellite_id": "bvxuo-uaaaa-aaaal-asgua-cai",
        "satellite_url": "https://bvxuo-uaaaa-aaaal-asgua-cai.raw.icp0.io",
        "subnet_id": "6pbhf-q...7hc-vae",
        "network": "testnet",
        "identity_file": None,
        "auth_method": "anonymous"
    }


@pytest.fixture
async def mock_icp_client(icp_test_config):
    """Mock ICP client for testing."""
    client = AsyncMock(spec=ICPClient)
    client.config = icp_test_config
    client.is_connected = True
    client.canister_id = icp_test_config["satellite_id"]
    return client


@pytest.fixture
async def ziggurat_client_connected(icp_test_config):
    """Create a connected Ziggurat client."""
    config = ZigguratConfig(**icp_test_config)
    client = ZigguratIntelligence(config=config)
    
    # Mock the connection
    with patch.object(client, '_create_session') as mock_create:
        mock_session = AsyncMock()
        mock_create.return_value = mock_session
        
        # Mock health check
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {"status": "healthy"}
        mock_session.get.return_value.__aenter__.return_value = mock_response
        
        await client.connect()
        client._session = mock_session
        
    yield client
    
    await client.disconnect()


@pytest.mark.integration
class TestICPSatelliteConnection:
    """Test ICP satellite connection and communication."""
    
    @pytest.mark.asyncio
    async def test_satellite_health_check(self, ziggurat_client_connected):
        """Test satellite health check endpoint."""
        client = ziggurat_client_connected
        
        # Mock health check response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "status": "healthy",
            "version": "v0.0.22",
            "canister_id": "bvxuo-uaaaa-aaaal-asgua-cai",
            "memory_usage": "30.40MB",
            "cycles": "0.975T"
        }
        client._session.get.return_value.__aenter__.return_value = mock_response
        
        health = await client.check_health()
        
        assert health["status"] == "healthy"
        assert health["version"] == "v0.0.22"
        assert "memory_usage" in health
        assert "cycles" in health
    
    @pytest.mark.asyncio
    async def test_satellite_authentication(self, ziggurat_client_connected):
        """Test satellite authentication flow."""
        client = ziggurat_client_connected
        
        # Test anonymous auth
        assert client.config.auth_method == "anonymous"
        
        # Mock auth response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "authenticated": True,
            "method": "anonymous",
            "session_id": "test-session-123"
        }
        client._session.post.return_value.__aenter__.return_value = mock_response
        
        auth_result = await client.authenticate()
        
        assert auth_result["authenticated"] is True
        assert auth_result["method"] == "anonymous"
    
    @pytest.mark.asyncio
    async def test_satellite_api_versioning(self, ziggurat_client_connected):
        """Test API version compatibility."""
        client = ziggurat_client_connected
        
        # Mock version check
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "api_version": "v1",
            "supported_versions": ["v1", "v2-beta"],
            "features": ["openxai", "chain-fusion", "explainable-ai"]
        }
        client._session.get.return_value.__aenter__.return_value = mock_response
        
        version_info = await client.get_api_version()
        
        assert version_info["api_version"] == "v1"
        assert "openxai" in version_info["features"]


@pytest.mark.integration
class TestOpenXAIPlatformIntegration:
    """Test OpenXAI platform integration."""
    
    @pytest.mark.asyncio
    async def test_openxai_model_discovery(self, ziggurat_client_connected):
        """Test discovering available OpenXAI models."""
        client = ziggurat_client_connected
        
        # Mock OpenXAI model list
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "models": [
                {
                    "id": "llama-2-70b-icp",
                    "provider": "openxai",
                    "type": "language",
                    "on_chain": True,
                    "explainable": True,
                    "cost_per_token": 0.0001
                },
                {
                    "id": "stable-diffusion-xl-icp",
                    "provider": "openxai",
                    "type": "image",
                    "on_chain": True,
                    "explainable": True,
                    "cost_per_generation": 0.01
                }
            ],
            "total": 50
        }
        client._session.get.return_value.__aenter__.return_value = mock_response
        
        models = await client.discover_openxai_models()
        
        assert len(models["models"]) == 2
        assert models["models"][0]["on_chain"] is True
        assert models["total"] == 50
    
    @pytest.mark.asyncio
    async def test_openxai_inference_request(self, ziggurat_client_connected):
        """Test making inference request to OpenXAI."""
        client = ziggurat_client_connected
        
        # Mock inference response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "inference_id": "inf-123456",
            "model_id": "llama-2-70b-icp",
            "result": {
                "text": "The capital of France is Paris.",
                "tokens": 8,
                "confidence": 0.99
            },
            "execution_time_ms": 250,
            "on_chain": True,
            "canister_id": "openxai-llama-canister"
        }
        client._session.post.return_value.__aenter__.return_value = mock_response
        
        result = await client.run_inference({
            "model_id": "llama-2-70b-icp",
            "prompt": "What is the capital of France?",
            "max_tokens": 50
        })
        
        assert result["model_id"] == "llama-2-70b-icp"
        assert result["on_chain"] is True
        assert "result" in result
        assert result["execution_time_ms"] < 1000
    
    @pytest.mark.asyncio
    async def test_openxai_batch_inference(self, ziggurat_client_connected):
        """Test batch inference capabilities."""
        client = ziggurat_client_connected
        
        # Mock batch inference response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "batch_id": "batch-789",
            "results": [
                {"inference_id": "inf-1", "status": "completed", "result": {"text": "Result 1"}},
                {"inference_id": "inf-2", "status": "completed", "result": {"text": "Result 2"}},
                {"inference_id": "inf-3", "status": "failed", "error": "Token limit exceeded"}
            ],
            "total_time_ms": 750,
            "successful": 2,
            "failed": 1
        }
        client._session.post.return_value.__aenter__.return_value = mock_response
        
        batch_result = await client.run_batch_inference([
            {"prompt": "Question 1"},
            {"prompt": "Question 2"},
            {"prompt": "Question 3 with very long input..."}
        ])
        
        assert batch_result["successful"] == 2
        assert batch_result["failed"] == 1
        assert len(batch_result["results"]) == 3


@pytest.mark.integration
class TestChainFusionIntegration:
    """Test Chain Fusion cross-chain integration."""
    
    @pytest.mark.asyncio
    async def test_cross_chain_verification(self, ziggurat_client_connected):
        """Test cross-chain verification via Chain Fusion."""
        client = ziggurat_client_connected
        
        # Mock Chain Fusion verification
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "verification_id": "verify-456",
            "chains": {
                "icp": {
                    "verified": True,
                    "block_height": 123456,
                    "transaction_hash": "0xicp123"
                },
                "bitcoin": {
                    "verified": True,
                    "block_height": 789012,
                    "transaction_hash": "btc456..."
                },
                "ethereum": {
                    "verified": False,
                    "status": "pending",
                    "estimated_blocks": 12
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        client._session.post.return_value.__aenter__.return_value = mock_response
        
        verification = await client.verify_cross_chain({
            "data_hash": "0xabcdef",
            "chains": ["icp", "bitcoin", "ethereum"]
        })
        
        assert verification["chains"]["icp"]["verified"] is True
        assert verification["chains"]["bitcoin"]["verified"] is True
        assert verification["chains"]["ethereum"]["verified"] is False
    
    @pytest.mark.asyncio
    async def test_chain_key_signing(self, ziggurat_client_connected):
        """Test Chain-Key cryptography for cross-chain transactions."""
        client = ziggurat_client_connected
        
        # Mock Chain-Key signing
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "signature": {
                "type": "ecdsa",
                "value": "0xsignature123",
                "public_key": "0xpubkey456",
                "chain": "ethereum"
            },
            "canister_id": "chain-key-canister",
            "request_id": "req-789"
        }
        client._session.post.return_value.__aenter__.return_value = mock_response
        
        signature = await client.chain_key_sign({
            "message": "Test message",
            "chain": "ethereum",
            "key_type": "ecdsa"
        })
        
        assert signature["signature"]["type"] == "ecdsa"
        assert signature["signature"]["chain"] == "ethereum"
        assert "value" in signature["signature"]


@pytest.mark.integration
class TestCanisterInteraction:
    """Test direct canister interaction."""
    
    @pytest.mark.asyncio
    async def test_canister_query(self, ziggurat_client_connected, mock_icp_client):
        """Test querying canister methods."""
        client = ziggurat_client_connected
        client._icp_client = mock_icp_client
        
        # Mock canister query response
        mock_icp_client.query_canister.return_value = {
            "method": "get_model_info",
            "result": {
                "model_id": "gpt-4-turbo",
                "parameters": 175000000000,
                "last_updated": datetime.now().isoformat()
            }
        }
        
        result = await client.query_canister_method(
            "get_model_info",
            {"model_id": "gpt-4-turbo"}
        )
        
        assert result["result"]["model_id"] == "gpt-4-turbo"
        assert "parameters" in result["result"]
    
    @pytest.mark.asyncio
    async def test_canister_update(self, ziggurat_client_connected, mock_icp_client):
        """Test updating canister state."""
        client = ziggurat_client_connected
        client._icp_client = mock_icp_client
        
        # Mock canister update response
        mock_icp_client.update_canister.return_value = {
            "method": "store_inference_result",
            "success": True,
            "transaction_id": "tx-123",
            "gas_used": 1000
        }
        
        result = await client.update_canister_state(
            "store_inference_result",
            {
                "inference_id": "inf-999",
                "result": {"text": "Stored result"},
                "timestamp": datetime.now().isoformat()
            }
        )
        
        assert result["success"] is True
        assert "transaction_id" in result


@pytest.mark.integration
class TestExplainableAIIntegration:
    """Test explainable AI integration with ICP."""
    
    @pytest.mark.asyncio
    async def test_on_chain_explanation(self, ziggurat_client_connected):
        """Test generating explanations on-chain."""
        client = ziggurat_client_connected
        
        # Mock on-chain explanation
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "explanation": {
                "method": "shap",
                "features": {
                    "temperature": 0.35,
                    "humidity": 0.28,
                    "pressure": 0.22,
                    "wind_speed": 0.15
                },
                "reasoning": "Weather prediction based on atmospheric conditions",
                "confidence": 0.87,
                "computation_canister": "shap-compute-canister",
                "gas_used": 5000
            },
            "on_chain": True,
            "verifiable": True
        }
        client._session.post.return_value.__aenter__.return_value = mock_response
        
        explanation = await client.generate_on_chain_explanation({
            "data": {
                "temperature": 22.5,
                "humidity": 65,
                "pressure": 1013,
                "wind_speed": 10
            },
            "model_id": "weather-predictor",
            "method": "shap"
        })
        
        assert explanation["on_chain"] is True
        assert explanation["explanation"]["method"] == "shap"
        assert "features" in explanation["explanation"]
    
    @pytest.mark.asyncio
    async def test_explanation_visualization(self, ziggurat_client_connected):
        """Test explanation visualization generation."""
        client = ziggurat_client_connected
        
        # Mock visualization response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "visualization": {
                "type": "feature_importance_chart",
                "format": "svg",
                "data_url": "data:image/svg+xml;base64,...",
                "interactive_url": "https://ziggurat.ai/viz/123"
            },
            "explanation_id": "exp-123",
            "generated_by": "viz-canister"
        }
        client._session.post.return_value.__aenter__.return_value = mock_response
        
        viz = await client.generate_explanation_visualization({
            "explanation_id": "exp-123",
            "type": "feature_importance_chart"
        })
        
        assert viz["visualization"]["type"] == "feature_importance_chart"
        assert "data_url" in viz["visualization"]


@pytest.mark.integration
class TestPerformanceMonitoring:
    """Test performance monitoring for ICP integration."""
    
    @pytest.mark.asyncio
    async def test_latency_tracking(self, ziggurat_client_connected):
        """Test latency tracking for ICP operations."""
        client = ziggurat_client_connected
        
        # Track multiple operations
        operations = []
        
        for i in range(5):
            start_time = datetime.now()
            
            # Mock quick response
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json.return_value = {"result": f"Operation {i}"}
            client._session.post.return_value.__aenter__.return_value = mock_response
            
            await client.run_inference({"prompt": f"Test {i}"})
            
            end_time = datetime.now()
            latency_ms = (end_time - start_time).total_seconds() * 1000
            operations.append(latency_ms)
        
        # Check performance metrics
        avg_latency = sum(operations) / len(operations)
        assert avg_latency < 1000  # Should be under 1 second
        assert all(lat < 2000 for lat in operations)  # No operation over 2 seconds
    
    @pytest.mark.asyncio
    async def test_cycle_consumption_tracking(self, ziggurat_client_connected):
        """Test tracking cycle consumption on ICP."""
        client = ziggurat_client_connected
        
        # Mock cycle consumption data
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "operations": [
                {"method": "inference", "cycles": 1000000},
                {"method": "explanation", "cycles": 2000000},
                {"method": "verification", "cycles": 500000}
            ],
            "total_cycles": 3500000,
            "remaining_cycles": "0.971T",
            "estimated_operations_left": 277428571
        }
        client._session.get.return_value.__aenter__.return_value = mock_response
        
        consumption = await client.get_cycle_consumption()
        
        assert consumption["total_cycles"] == 3500000
        assert "remaining_cycles" in consumption
        assert consumption["estimated_operations_left"] > 0


@pytest.mark.integration
class TestErrorHandlingIntegration:
    """Test error handling in ICP integration."""
    
    @pytest.mark.asyncio
    async def test_canister_error_handling(self, ziggurat_client_connected):
        """Test handling canister errors."""
        client = ziggurat_client_connected
        
        # Mock canister error
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_response.json.return_value = {
            "error": {
                "code": "CANISTER_ERROR",
                "message": "Canister trapped: out of memory",
                "canister_id": "error-canister",
                "details": {
                    "memory_used": "500MB",
                    "memory_limit": "500MB"
                }
            }
        }
        client._session.post.return_value.__aenter__.return_value = mock_response
        
        with pytest.raises(Exception) as exc_info:
            await client.run_inference({"prompt": "Test"})
        
        assert "out of memory" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_network_partition_handling(self, ziggurat_client_connected):
        """Test handling network partitions."""
        client = ziggurat_client_connected
        
        # Simulate network partition
        client._session.post.side_effect = aiohttp.ClientError("Network unreachable")
        
        # Should attempt reconnection
        with patch.object(client, 'connect', new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = False
            
            with pytest.raises(aiohttp.ClientError):
                await client.run_inference({"prompt": "Test"})
            
            # Verify reconnection was attempted
            mock_connect.assert_called()
    
    @pytest.mark.asyncio
    async def test_rate_limit_handling(self, ziggurat_client_connected):
        """Test handling rate limits."""
        client = ziggurat_client_connected
        
        # Mock rate limit response
        mock_response = AsyncMock()
        mock_response.status = 429
        mock_response.headers = {"Retry-After": "60"}
        mock_response.json.return_value = {
            "error": "Rate limit exceeded",
            "retry_after_seconds": 60,
            "limit": "100 requests per minute"
        }
        client._session.post.return_value.__aenter__.return_value = mock_response
        
        with pytest.raises(Exception) as exc_info:
            await client.run_inference({"prompt": "Test"})
        
        assert "Rate limit" in str(exc_info.value)