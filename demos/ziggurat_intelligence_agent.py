#!/usr/bin/env python3
"""
Ziggurat Intelligence Agent - Decentralized Explainable AI Platform
Ancient Architecture, Infinite Intelligence

This agent provides decentralized, explainable AI inference with blockchain verification
through the ICP-OpenXAI integration using Juno satellite infrastructure.
"""

import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime

# Add parent directory to path for imports
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.agents.base import AsyncContextAgent
from src.core.blockchain.ziggurat import (
    ZigguratIntelligence, 
    ZigguratConfig, 
    ExplanationMethod,
    BlockchainNetwork
)


class ZigguratIntelligenceAgent(AsyncContextAgent):
    """
    Ziggurat Intelligence Agent - Complete decentralized explainable AI platform.
    
    Features:
    - Multiple explanation methods (SHAP, LIME, Gradient, Attention)
    - Blockchain verification on ICP with Chain Fusion
    - Cross-chain proof generation
    - Model discovery and selection
    - Batch processing capabilities
    - Counterfactual explanations
    """
    
    name = "ziggurat_intelligence"
    description = "Decentralized explainable AI platform with blockchain verification"
    
    def __init__(
        self, 
        explanation_method: str = "shap",
        blockchain_verify: bool = True,
        enable_cache: bool = True,
        cross_chain: bool = False
    ):
        """
        Initialize Ziggurat Intelligence Agent.
        
        Args:
            explanation_method: Method for AI explanations (shap, lime, gradient, attention)
            blockchain_verify: Whether to verify on blockchain
            enable_cache: Enable result caching
            cross_chain: Enable cross-chain verification (Bitcoin, Ethereum)
        """
        super().__init__()
        
        # Parse explanation method
        self.explanation_method = ExplanationMethod(explanation_method.lower())
        self.blockchain_verify = blockchain_verify
        self.enable_cache = enable_cache
        self.cross_chain = cross_chain
        self.ziggurat = None
        
    async def initialize(self):
        """Initialize Ziggurat Intelligence platform."""
        await super().initialize()
        
        # Configure Ziggurat
        config = ZigguratConfig(
            default_method=self.explanation_method,
            verify_on_blockchain=self.blockchain_verify,
            enable_cache=self.enable_cache,
            chain_fusion_enabled=self.cross_chain
        )
        
        self.ziggurat = ZigguratIntelligence(config)
        await self.ziggurat.initialize()
        
        self.logger.info(f"🏛️ Ziggurat Intelligence initialized")
        self.logger.info(f"📊 Method: {self.explanation_method.value}")
        self.logger.info(f"🔐 Blockchain: {'Enabled' if self.blockchain_verify else 'Disabled'}")
        self.logger.info(f"⛓️ Cross-chain: {'Enabled' if self.cross_chain else 'Disabled'}")
        
    async def cleanup(self):
        """Cleanup resources."""
        if self.ziggurat:
            await self.ziggurat.cleanup()
        await super().cleanup()
        
    async def run(
        self, 
        action: str = "explain",
        data: Optional[Dict[str, Any]] = None,
        model_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run Ziggurat Intelligence operations.
        
        Args:
            action: Action to perform (explain, list_models, batch_explain, counterfactuals)
            data: Input data for analysis
            model_id: Specific model to use
            **kwargs: Additional action-specific parameters
            
        Returns:
            Dict containing results based on action
        """
        
        self.logger.info(f"🏛️ Executing Ziggurat action: {action}")
        
        # Route to appropriate action
        if action == "explain":
            return await self._explain(data, model_id, **kwargs)
        elif action == "list_models":
            return await self._list_models()
        elif action == "batch_explain":
            return await self._batch_explain(data, model_id, **kwargs)
        elif action == "counterfactuals":
            return await self._counterfactuals(data, model_id, **kwargs)
        elif action == "verify":
            return await self._verify_proof(kwargs.get("proof_hash"))
        else:
            return await self._demo_showcase()
            
    async def _explain(
        self, 
        data: Optional[Dict[str, Any]] = None,
        model_id: Optional[str] = None,
        method: Optional[str] = None
    ) -> Dict[str, Any]:
        """Perform AI explanation on data."""
        
        # Default demo data if none provided
        if data is None:
            data = {
                "loan_amount": 250000,
                "annual_income": 85000,
                "credit_score": 720,
                "debt_to_income": 0.28,
                "employment_years": 7,
                "property_value": 350000,
                "down_payment_percent": 0.20
            }
            
        # Override method if provided
        if method:
            explanation_method = ExplanationMethod(method.lower())
        else:
            explanation_method = self.explanation_method
            
        self.logger.info(f"📊 Analyzing data with {explanation_method.value} method")
        
        # Get explanation
        explanation = await self.ziggurat.explain_decision(
            data=data,
            method=explanation_method,
            model_id=model_id,
            blockchain_verify=self.blockchain_verify
        )
        
        # Format results
        result = {
            "status": "success",
            "action": "explain",
            "timestamp": datetime.utcnow().isoformat(),
            "analysis": {
                "reasoning": explanation.reasoning,
                "confidence": explanation.confidence,
                "method": explanation.method_used.value,
                "model_id": explanation.model_id
            },
            "explanation": {
                "feature_importance": explanation.feature_importance,
                "decision_path": explanation.decision_path
            },
            "performance": {
                "processing_time_ms": explanation.processing_time_ms,
                "cost_cycles": explanation.cost_cycles
            }
        }
        
        # Add blockchain data if verified
        if explanation.blockchain_verified:
            result["blockchain"] = {
                "verified": True,
                "proof_hash": explanation.proof_hash,
                "chain": explanation.verification_chain.value,
                "transaction_id": explanation.transaction_id,
                "satellite_id": "bvxuo-uaaaa-aaaal-asgua-cai"
            }
            
            # Add cross-chain proofs if available
            if explanation.cross_chain_proofs:
                result["blockchain"]["cross_chain_proofs"] = {
                    chain.value: proof 
                    for chain, proof in explanation.cross_chain_proofs.items()
                }
                
        self.logger.info(f"✅ Analysis complete - Confidence: {explanation.confidence:.2%}")
        
        return result
        
    async def _list_models(self) -> Dict[str, Any]:
        """List available AI models in Ziggurat network."""
        
        self.logger.info("🤖 Fetching available models from Ziggurat network")
        
        models = await self.ziggurat.list_available_models()
        
        return {
            "status": "success",
            "action": "list_models",
            "models": [
                {
                    "model_id": model.model_id,
                    "name": model.name,
                    "description": model.description,
                    "type": model.model_type,
                    "supports": [m.value for m in model.supports_explanation],
                    "blockchain": model.deployed_on.value,
                    "canister_id": model.canister_id,
                    "cost_per_inference": model.cost_per_inference,
                    "gpu_enabled": model.gpu_enabled
                }
                for model in models
            ],
            "total_models": len(models)
        }
        
    async def _batch_explain(
        self,
        data_list: Optional[List[Dict[str, Any]]] = None,
        model_id: Optional[str] = None,
        method: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process multiple inputs in batch."""
        
        # Default demo batch if none provided
        if data_list is None:
            base_data = {
                "feature1": 0.5,
                "feature2": 0.7,
                "feature3": 0.3
            }
            data_list = [
                {**base_data, "variation": i * 0.1}
                for i in range(5)
            ]
            
        self.logger.info(f"📊 Batch processing {len(data_list)} items")
        
        # Override method if provided
        if method:
            explanation_method = ExplanationMethod(method.lower())
        else:
            explanation_method = self.explanation_method
            
        # Batch explain
        explanations = await self.ziggurat.batch_explain(
            data_list=data_list,
            method=explanation_method,
            model_id=model_id
        )
        
        # Format results
        return {
            "status": "success",
            "action": "batch_explain",
            "batch_size": len(data_list),
            "method": explanation_method.value,
            "results": [
                {
                    "index": i,
                    "confidence": exp.confidence,
                    "reasoning": exp.reasoning,
                    "processing_time_ms": exp.processing_time_ms
                }
                for i, exp in enumerate(explanations)
            ],
            "summary": {
                "average_confidence": sum(e.confidence for e in explanations) / len(explanations),
                "total_processing_time_ms": sum(e.processing_time_ms or 0 for e in explanations),
                "total_cost_cycles": sum(e.cost_cycles or 0 for e in explanations)
            }
        }
        
    async def _counterfactuals(
        self,
        data: Optional[Dict[str, Any]] = None,
        model_id: Optional[str] = None,
        num_counterfactuals: int = 3
    ) -> Dict[str, Any]:
        """Get explanation with counterfactual examples."""
        
        # Default demo data if none provided
        if data is None:
            data = {
                "age": 28,
                "income": 55000,
                "credit_score": 680,
                "loan_amount": 200000,
                "employment_status": "full_time"
            }
            
        self.logger.info(f"🔄 Generating {num_counterfactuals} counterfactuals")
        
        # Get counterfactuals
        explanation = await self.ziggurat.explain_with_counterfactuals(
            data=data,
            num_counterfactuals=num_counterfactuals,
            model_id=model_id
        )
        
        return {
            "status": "success",
            "action": "counterfactuals",
            "original_analysis": {
                "reasoning": explanation.reasoning,
                "confidence": explanation.confidence,
                "decision": "approved" if explanation.confidence > 0.7 else "denied"
            },
            "counterfactuals": explanation.counterfactuals,
            "recommendations": [
                "Consider the suggested changes to improve approval chances",
                "Focus on features with highest impact",
                "Consult with financial advisor for personalized guidance"
            ]
        }
        
    async def _verify_proof(self, proof_hash: Optional[str]) -> Dict[str, Any]:
        """Verify a blockchain proof."""
        
        if not proof_hash:
            return {
                "status": "error",
                "message": "No proof hash provided"
            }
            
        self.logger.info(f"🔐 Verifying proof: {proof_hash}")
        
        is_valid = await self.ziggurat.verify_proof(proof_hash)
        
        return {
            "status": "success",
            "action": "verify",
            "proof_hash": proof_hash,
            "verified": is_valid,
            "blockchain": "ICP",
            "message": "Proof is valid on ICP blockchain" if is_valid else "Proof verification failed"
        }
        
    async def _demo_showcase(self) -> Dict[str, Any]:
        """Run comprehensive demo showcasing all features."""
        
        self.logger.info("🏛️ Running Ziggurat Intelligence showcase demo")
        
        # 1. List available models
        models_result = await self._list_models()
        
        # 2. Single explanation
        explain_result = await self._explain()
        
        # 3. Batch processing
        batch_result = await self._batch_explain()
        
        # 4. Counterfactuals
        counterfactual_result = await self._counterfactuals()
        
        # 5. Verify a proof
        if explain_result.get("blockchain", {}).get("proof_hash"):
            verify_result = await self._verify_proof(
                explain_result["blockchain"]["proof_hash"]
            )
        else:
            verify_result = {"status": "skipped", "message": "No proof to verify"}
            
        return {
            "status": "success",
            "action": "showcase",
            "platform": "Ziggurat Intelligence",
            "tagline": "Ancient Architecture, Infinite Intelligence",
            "features": {
                "explainable_ai": "Multiple explanation methods (SHAP, LIME, Gradient, Attention)",
                "blockchain": "ICP integration with Chain Fusion capability",
                "decentralized": "Juno satellite infrastructure on Internet Computer",
                "performance": "GPU-accelerated models available",
                "economics": "Cycle-based pricing with transparent costs"
            },
            "demo_results": {
                "models_available": models_result["total_models"],
                "explanation_confidence": explain_result["analysis"]["confidence"],
                "batch_processing": f"{batch_result['batch_size']} items in {batch_result['summary']['total_processing_time_ms']}ms",
                "counterfactuals_generated": len(counterfactual_result["counterfactuals"]),
                "blockchain_verification": verify_result.get("verified", False)
            },
            "satellite_info": {
                "id": "bvxuo-uaaaa-aaaal-asgua-cai",
                "network": "Internet Computer Protocol",
                "subnet": "6pbhf-q...7hc-vae",
                "memory": "30.40 MB",
                "cycles": "0.975T available"
            }
        }


# CLI entry point
async def main():
    """CLI interface for Ziggurat Intelligence Agent."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Ziggurat Intelligence - Decentralized Explainable AI Platform"
    )
    
    parser.add_argument(
        "action",
        choices=["explain", "list_models", "batch_explain", "counterfactuals", "verify", "demo"],
        default="demo",
        nargs="?",
        help="Action to perform"
    )
    
    parser.add_argument(
        "--data",
        type=str,
        help="JSON data for analysis (file path or JSON string)"
    )
    
    parser.add_argument(
        "--method",
        choices=["shap", "lime", "gradient", "attention"],
        default="shap",
        help="Explanation method"
    )
    
    parser.add_argument(
        "--model-id",
        type=str,
        help="Specific model ID to use"
    )
    
    parser.add_argument(
        "--no-blockchain",
        action="store_true",
        help="Disable blockchain verification"
    )
    
    parser.add_argument(
        "--cross-chain",
        action="store_true",
        help="Enable cross-chain verification"
    )
    
    parser.add_argument(
        "--proof-hash",
        type=str,
        help="Proof hash to verify (for verify action)"
    )
    
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Number of items for batch processing"
    )
    
    args = parser.parse_args()
    
    # Parse data if provided
    data = None
    if args.data:
        try:
            data = json.loads(args.data)
        except:
            try:
                with open(args.data, 'r') as f:
                    data = json.load(f)
            except:
                print(f"Error: Could not parse data from '{args.data}'")
                return
                
    # Create agent
    agent = ZigguratIntelligenceAgent(
        explanation_method=args.method,
        blockchain_verify=not args.no_blockchain,
        cross_chain=args.cross_chain
    )
    
    # Run agent
    async with agent:
        result = await agent.run(
            action=args.action,
            data=data,
            model_id=args.model_id,
            proof_hash=args.proof_hash,
            batch_size=args.batch_size
        )
        
        # Pretty print results
        print("\n" + "="*70)
        print("🏛️  ZIGGURAT INTELLIGENCE - RESULTS")
        print("="*70 + "\n")
        
        print(json.dumps(result, indent=2))
        
        print("\n" + "="*70)
        print("Ancient Architecture, Infinite Intelligence")
        print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())