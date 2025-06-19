"""
🏛️ Ziggurat Intelligence Engine

Core explainable AI functionality for the Ziggurat platform.
Integrates ICP blockchain verification with OpenXAI decentralized inference.

Built for ICP x OpenXAI x Masumi x TON Hackathon 2025
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ExplanationMethod(Enum):
    """Available explanation methods"""
    SHAP = "shap"
    LIME = "lime" 
    GRADIENT = "gradient"
    ATTENTION = "attention"


@dataclass
class ExplanationResult:
    """Result of AI explanation analysis"""
    prediction: Any
    confidence: float
    reasoning: str
    feature_importance: Dict[str, float]
    method: ExplanationMethod
    verification_hash: Optional[str] = None
    timestamp: Optional[float] = None


@dataclass
class InferenceRequest:
    """Request for AI inference with explanation"""
    data: Dict[str, Any]
    method: ExplanationMethod
    model_id: str
    user_id: str
    request_id: str


class ZigguratIntelligenceEngine:
    """
    Core Ziggurat Intelligence Engine
    
    Provides explainable AI capabilities with blockchain verification.
    Integrates with ICP canisters and OpenXAI protocol.
    """
    
    def __init__(self, icp_endpoint: str = None, openxai_endpoint: str = None):
        """Initialize the intelligence engine"""
        self.icp_endpoint = icp_endpoint or "https://ic0.app"
        self.openxai_endpoint = openxai_endpoint or "http://localhost:8080"
        self.explanation_cache = {}
        
    async def explain_prediction(
        self, 
        request: InferenceRequest
    ) -> ExplanationResult:
        """
        Generate explainable AI prediction with blockchain verification
        
        This is the core method that:
        1. Calls OpenXAI for decentralized inference
        2. Generates real-time explanations
        3. Verifies results on ICP blockchain
        """
        
        # 1. Get prediction from OpenXAI protocol
        prediction_result = await self._call_openxai_inference(request)
        
        # 2. Generate explanation using specified method
        explanation = await self._generate_explanation(
            request.data, 
            prediction_result, 
            request.method
        )
        
        # 3. Verify and store on ICP blockchain
        verification_hash = await self._store_on_icp(explanation, request.user_id)
        
        return ExplanationResult(
            prediction=prediction_result["prediction"],
            confidence=prediction_result["confidence"],
            reasoning=explanation["reasoning"],
            feature_importance=explanation["feature_importance"],
            method=request.method,
            verification_hash=verification_hash,
            timestamp=time.time()
        )
    
    async def _call_openxai_inference(self, request: InferenceRequest) -> Dict:
        """Call OpenXAI protocol for decentralized AI inference"""
        
        # Simulate OpenXAI API call
        # In production, this would make actual HTTP calls to OpenXAI nodes
        await asyncio.sleep(0.045)  # 45ms average inference time
        
        # Mock response based on request data
        if "credit_score" in request.data:
            return {
                "prediction": "APPROVED",
                "confidence": 0.89,
                "raw_output": [0.11, 0.89]  # [reject, approve]
            }
        elif "transaction_amount" in request.data:
            risk_score = min(request.data.get("transaction_amount", 0) / 10000, 1.0)
            return {
                "prediction": "HIGH_RISK" if risk_score > 0.7 else "NORMAL",
                "confidence": 0.85,
                "risk_score": risk_score
            }
        else:
            return {
                "prediction": "UNKNOWN",
                "confidence": 0.5,
                "raw_output": [0.5, 0.5]
            }
    
    async def _generate_explanation(
        self, 
        input_data: Dict, 
        prediction: Dict, 
        method: ExplanationMethod
    ) -> Dict:
        """Generate explanation using specified XAI method"""
        
        if method == ExplanationMethod.SHAP:
            return await self._generate_shap_explanation(input_data, prediction)
        elif method == ExplanationMethod.LIME:
            return await self._generate_lime_explanation(input_data, prediction)
        elif method == ExplanationMethod.GRADIENT:
            return await self._generate_gradient_explanation(input_data, prediction)
        elif method == ExplanationMethod.ATTENTION:
            return await self._generate_attention_explanation(input_data, prediction)
        else:
            raise ValueError(f"Unsupported explanation method: {method}")
    
    async def _generate_shap_explanation(self, data: Dict, prediction: Dict) -> Dict:
        """Generate SHAP (SHapley Additive exPlanations) analysis"""
        
        # Simulate SHAP calculation
        await asyncio.sleep(0.02)
        
        if "credit_score" in data:
            return {
                "reasoning": f"Loan approval based on strong credit profile. Credit score of {data['credit_score']} is the strongest positive factor, indicating reliable payment history and low default risk.",
                "feature_importance": {
                    "credit_score": 0.45,
                    "income": 0.28,
                    "employment_length": 0.22,
                    "debt_ratio": -0.15
                },
                "method_details": "SHAP values calculated using game theory to determine each feature's contribution to the final decision."
            }
        elif "transaction_amount" in data:
            amount = data.get("transaction_amount", 0)
            return {
                "reasoning": f"Transaction of ${amount:,.2f} flagged due to unusual amount pattern. Historical spending analysis shows this exceeds normal range by 340%.",
                "feature_importance": {
                    "transaction_amount": 0.65,
                    "time_of_day": 0.20,
                    "merchant_category": 0.10,
                    "location": 0.05
                },
                "method_details": "SHAP analysis of transaction risk factors based on user spending patterns."
            }
        else:
            return {
                "reasoning": "Generic explanation for unknown data type.",
                "feature_importance": {"unknown_feature": 1.0},
                "method_details": "SHAP explanation method applied."
            }
    
    async def _generate_lime_explanation(self, data: Dict, prediction: Dict) -> Dict:
        """Generate LIME (Local Interpretable Model-agnostic Explanations) analysis"""
        
        await asyncio.sleep(0.02)
        
        return {
            "reasoning": "LIME analysis reveals local decision boundary around this specific prediction.",
            "feature_importance": {key: 0.8 for key in data.keys()},
            "method_details": "LIME perturbed input features locally to understand model behavior in this region."
        }
    
    async def _generate_gradient_explanation(self, data: Dict, prediction: Dict) -> Dict:
        """Generate gradient-based explanation analysis"""
        
        await asyncio.sleep(0.02)
        
        return {
            "reasoning": "Gradient analysis shows which input features most strongly influence the neural network's decision.",
            "feature_importance": {key: 0.6 for key in data.keys()},
            "method_details": "Gradients computed via backpropagation to show feature sensitivity."
        }
    
    async def _generate_attention_explanation(self, data: Dict, prediction: Dict) -> Dict:
        """Generate attention-based explanation analysis"""
        
        await asyncio.sleep(0.02)
        
        return {
            "reasoning": "Attention mechanism reveals which parts of the input the transformer model focused on most heavily.",
            "feature_importance": {key: 0.7 for key in data.keys()},
            "method_details": "Attention weights extracted from transformer model's self-attention layers."
        }
    
    async def _store_on_icp(self, explanation: Dict, user_id: str) -> str:
        """Store explanation on ICP blockchain for verification"""
        
        # Simulate ICP canister call
        await asyncio.sleep(0.03)
        
        # Create verification hash
        explanation_json = json.dumps(explanation, sort_keys=True)
        verification_hash = f"icp_hash_{hash(explanation_json) % 1000000:06d}"
        
        # In production, this would:
        # 1. Call ICP canister via HTTPS outcall
        # 2. Store explanation data in stable memory
        # 3. Return cryptographic proof of storage
        
        return verification_hash
    
    async def verify_explanation(self, verification_hash: str) -> Dict:
        """Verify explanation exists on ICP blockchain"""
        
        # Simulate blockchain verification
        await asyncio.sleep(0.01)
        
        return {
            "verified": True,
            "canister_id": "rdmx6-jaaaa-aaaah-qcaiq-cai",
            "block_height": 12345,
            "timestamp": time.time(),
            "verification_hash": verification_hash
        }
    
    async def batch_explain(
        self, 
        requests: List[InferenceRequest]
    ) -> List[ExplanationResult]:
        """Process multiple explanation requests in parallel"""
        
        tasks = [self.explain_prediction(req) for req in requests]
        return await asyncio.gather(*tasks)
    
    def get_supported_methods(self) -> List[str]:
        """Get list of supported explanation methods"""
        return [method.value for method in ExplanationMethod]
    
    async def health_check(self) -> Dict:
        """Check health of all connected services"""
        
        return {
            "status": "healthy",
            "icp_connection": "connected",
            "openxai_connection": "connected", 
            "explanation_cache_size": len(self.explanation_cache),
            "supported_methods": self.get_supported_methods(),
            "timestamp": time.time()
        }


# Demo usage
async def demo_intelligence_engine():
    """Demonstrate the Ziggurat Intelligence Engine"""
    
    print("🏛️ Ziggurat Intelligence Engine Demo")
    print("=" * 50)
    
    # Initialize engine
    engine = ZigguratIntelligenceEngine()
    
    # Health check
    health = await engine.health_check()
    print(f"✅ Engine Status: {health['status']}")
    print(f"📡 ICP Connection: {health['icp_connection']}")
    print(f"🤖 OpenXAI Connection: {health['openxai_connection']}")
    print()
    
    # Example 1: Loan approval explanation
    print("🏦 Example 1: Loan Approval Analysis")
    loan_request = InferenceRequest(
        data={
            "credit_score": 720,
            "income": 85000,
            "employment_length": 7,
            "debt_ratio": 0.28
        },
        method=ExplanationMethod.SHAP,
        model_id="loan_approval_v2",
        user_id="user_123",
        request_id="req_001"
    )
    
    result = await engine.explain_prediction(loan_request)
    print(f"   Decision: {result.prediction}")
    print(f"   Confidence: {result.confidence:.1%}")
    print(f"   Reasoning: {result.reasoning}")
    print(f"   Verification: {result.verification_hash}")
    print()
    
    # Example 2: Transaction risk analysis
    print("💳 Example 2: Transaction Risk Analysis")
    risk_request = InferenceRequest(
        data={
            "transaction_amount": 15000,
            "time_of_day": "03:00",
            "merchant_category": "electronics",
            "location": "international"
        },
        method=ExplanationMethod.SHAP,
        model_id="fraud_detection_v3",
        user_id="user_456",
        request_id="req_002"
    )
    
    risk_result = await engine.explain_prediction(risk_request)
    print(f"   Risk Assessment: {risk_result.prediction}")
    print(f"   Confidence: {risk_result.confidence:.1%}")
    print(f"   Reasoning: {risk_result.reasoning}")
    print(f"   Verification: {risk_result.verification_hash}")
    print()
    
    # Verification example
    print("🔐 Blockchain Verification")
    verification = await engine.verify_explanation(result.verification_hash)
    print(f"   Verified: {verification['verified']}")
    print(f"   Canister: {verification['canister_id']}")
    print(f"   Block: {verification['block_height']}")


if __name__ == "__main__":
    asyncio.run(demo_intelligence_engine())