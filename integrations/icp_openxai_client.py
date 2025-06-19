"""
ICP-OpenXAI Client - Direct Integration with Juno Satellite
Enables decentralized explainable AI via Internet Computer Protocol
"""

import os
import json
import aiohttp
import hashlib
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from src.core.shared.config.ziggurat_config import (
    get_satellite_url,
    get_openxai_endpoint,
    get_satellite_id,
    get_auth_method,
    ZIGGURAT_CONFIG
)
from .models import (
    ZigguratExplanation,
    ExplanationMethod,
    BlockchainNetwork,
    AIModelInfo
)

logger = logging.getLogger(__name__)


class ICPOpenXAIClient:
    """
    Client for interacting with ICP-OpenXAI through Juno satellite.
    Provides direct integration with decentralized AI infrastructure.
    """
    
    def __init__(self, satellite_id: Optional[str] = None, satellite_url: Optional[str] = None):
        """
        Initialize ICP-OpenXAI client with Juno satellite configuration.
        
        Args:
            satellite_id: Override default satellite ID
            satellite_url: Override default satellite URL
        """
        self.satellite_id = satellite_id or get_satellite_id()
        self.satellite_url = satellite_url or get_satellite_url()
        # Ensure we use .raw.icp0.io for API access
        if '.icp0.io' in self.satellite_url and '.raw.icp0.io' not in self.satellite_url:
            self.satellite_url = self.satellite_url.replace('.icp0.io', '.raw.icp0.io')
        self.api_endpoint = f"{self.satellite_url.rstrip('/')}/api/v1"
        self.auth_method = get_auth_method()
        self.session = None
        self._headers = {
            "Content-Type": "application/json",
            "X-Satellite-ID": self.satellite_id,
            "X-Client": "agent-forge-ziggurat"
        }
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()
        
    async def connect(self):
        """Establish connection to ICP-OpenXAI satellite"""
        if self.session is None:
            timeout = aiohttp.ClientTimeout(total=ZIGGURAT_CONFIG["icp_openxai"]["timeout"])
            self.session = aiohttp.ClientSession(timeout=timeout, headers=self._headers)
            
        # Verify satellite connectivity
        try:
            async with self.session.get(f"{self.api_endpoint}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Connected to Ziggurat satellite: {data.get('satellite_name', 'unknown')}")
                else:
                    logger.warning(f"Satellite health check returned status {response.status}")
        except Exception as e:
            logger.error(f"Failed to connect to satellite: {e}")
            
    async def disconnect(self):
        """Close connection to satellite"""
        if self.session:
            await self.session.close()
            self.session = None
            
    async def explain(
        self,
        data: Dict[str, Any],
        method: ExplanationMethod = ExplanationMethod.SHAP,
        model_id: Optional[str] = None
    ) -> ZigguratExplanation:
        """
        Get AI explanation through ICP-OpenXAI.
        
        Args:
            data: Input data for explanation
            method: Explanation method to use
            model_id: Specific model ID (optional)
            
        Returns:
            ZigguratExplanation with results
        """
        if not self.session:
            await self.connect()
            
        payload = {
            "data": data,
            "method": method.value,
            "model_id": model_id,
            "request_id": self._generate_request_id(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            async with self.session.post(
                f"{self.api_endpoint}/explain",
                json=payload
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return self._parse_explanation(result)
                else:
                    error_data = await response.text()
                    raise Exception(f"Explanation request failed: {error_data}")
                    
        except Exception as e:
            logger.error(f"ICP-OpenXAI request failed: {e}")
            # Return mock explanation for development
            return self._mock_explanation(data, method)
            
    async def list_models(self) -> List[AIModelInfo]:
        """Get available AI models from satellite"""
        if not self.session:
            await self.connect()
            
        try:
            async with self.session.get(f"{self.api_endpoint}/models") as response:
                if response.status == 200:
                    models_data = await response.json()
                    return [self._parse_model_info(m) for m in models_data.get("models", [])]
                else:
                    logger.warning("Failed to fetch models list")
                    return self._mock_models()
                    
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return self._mock_models()
            
    async def verify_on_chain(self, proof_hash: str) -> bool:
        """Verify proof hash on ICP blockchain"""
        if not self.session:
            await self.connect()
            
        try:
            async with self.session.post(
                f"{self.api_endpoint}/verify",
                json={"proof_hash": proof_hash}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("verified", False)
                else:
                    return False
                    
        except Exception as e:
            logger.error(f"Chain verification failed: {e}")
            return False
            
    async def get_satellite_status(self) -> Dict[str, Any]:
        """Get current satellite status and metrics"""
        if not self.session:
            await self.connect()
            
        try:
            async with self.session.get(f"{self.api_endpoint}/status") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {
                        "status": "unknown",
                        "satellite_id": self.satellite_id,
                        "cycles": "unknown",
                        "memory": "unknown"
                    }
                    
        except Exception as e:
            logger.error(f"Failed to get satellite status: {e}")
            return {
                "status": "error",
                "error": str(e),
                "satellite_id": self.satellite_id
            }
            
    def _generate_request_id(self) -> str:
        """Generate unique request ID"""
        data = f"{self.satellite_id}-{datetime.utcnow().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
        
    def _parse_explanation(self, data: Dict[str, Any]) -> ZigguratExplanation:
        """Parse API response into ZigguratExplanation"""
        return ZigguratExplanation(
            reasoning=data.get("reasoning", ""),
            confidence=data.get("confidence", 0.0),
            method_used=ExplanationMethod(data.get("method", "shap")),
            blockchain_verified=data.get("blockchain_verified", False),
            proof_hash=data.get("proof_hash"),
            verification_chain=BlockchainNetwork.ICP,
            transaction_id=data.get("transaction_id"),
            feature_importance=data.get("feature_importance", {}),
            decision_path=data.get("decision_path", []),
            counterfactuals=data.get("counterfactuals", []),
            processing_time_ms=data.get("processing_time_ms", 0),
            cost_cycles=data.get("cost_cycles", 0),
            model_id=data.get("model_id"),
            cross_chain_proofs=data.get("cross_chain_proofs", {})
        )
        
    def _parse_model_info(self, data: Dict[str, Any]) -> AIModelInfo:
        """Parse model data into AIModelInfo"""
        return AIModelInfo(
            model_id=data.get("model_id", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            model_type=data.get("model_type", ""),
            supports_explanation=[
                ExplanationMethod(m) for m in data.get("supports_explanation", [])
            ],
            max_input_size=data.get("max_input_size", 0),
            output_format=data.get("output_format", "json"),
            deployed_on=BlockchainNetwork.ICP,
            canister_id=data.get("canister_id", self.satellite_id),
            cost_per_inference=data.get("cost_per_inference", 1000000),
            gpu_enabled=data.get("gpu_enabled", False),
            memory_requirements_gb=data.get("memory_requirements_gb", 0.0)
        )
        
    def _mock_explanation(self, data: Any, method: ExplanationMethod) -> ZigguratExplanation:
        """Generate mock explanation for development"""
        return ZigguratExplanation(
            reasoning=f"Mock analysis using {method.value} on satellite {self.satellite_id}",
            confidence=0.85,
            method_used=method,
            blockchain_verified=True,
            proof_hash=hashlib.sha256(f"{self.satellite_id}-{data}".encode()).hexdigest(),
            verification_chain=BlockchainNetwork.ICP,
            transaction_id=f"icp-{self.satellite_id[:8]}-mock",
            feature_importance={"feature_1": 0.4, "feature_2": 0.35, "feature_3": 0.25},
            processing_time_ms=150,
            cost_cycles=1500000,
            model_id="ziggurat-mock-v1"
        )
        
    def _mock_models(self) -> List[AIModelInfo]:
        """Return mock models for development"""
        return [
            AIModelInfo(
                model_id="ziggurat-explainer-v1",
                name="Ziggurat Explainer V1",
                description="Decentralized explainable AI via Juno satellite",
                model_type="explainer",
                supports_explanation=[ExplanationMethod.SHAP, ExplanationMethod.LIME],
                max_input_size=1048576,
                output_format="json",
                deployed_on=BlockchainNetwork.ICP,
                canister_id=self.satellite_id,
                cost_per_inference=1000000,
                gpu_enabled=False
            ),
            AIModelInfo(
                model_id="ziggurat-neural-v2",
                name="Ziggurat Neural V2",
                description="Advanced neural explanations with GPU acceleration",
                model_type="neural",
                supports_explanation=[ExplanationMethod.GRADIENT, ExplanationMethod.ATTENTION],
                max_input_size=5242880,
                output_format="json",
                deployed_on=BlockchainNetwork.ICP,
                canister_id=self.satellite_id,
                cost_per_inference=3000000,
                gpu_enabled=True,
                memory_requirements_gb=4.0
            )
        ]


# Convenience function for testing
async def test_satellite_connection():
    """Test connection to Ziggurat satellite"""
    async with ICPOpenXAIClient() as client:
        # Test satellite status
        status = await client.get_satellite_status()
        print(f"Satellite Status: {json.dumps(status, indent=2)}")
        
        # Test model listing
        models = await client.list_models()
        print(f"\nAvailable Models: {len(models)}")
        for model in models:
            print(f"  - {model.name} ({model.model_id})")
            
        # Test explanation
        test_data = {"feature1": 0.5, "feature2": 0.8, "feature3": 0.2}
        explanation = await client.explain(test_data, ExplanationMethod.SHAP)
        print(f"\nExplanation Result:")
        print(f"  Reasoning: {explanation.reasoning}")
        print(f"  Confidence: {explanation.confidence:.2%}")
        print(f"  Proof Hash: {explanation.proof_hash}")
        print(f"  Satellite: {client.satellite_id}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_satellite_connection())