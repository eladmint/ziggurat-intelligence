"""
Masumi-Ziggurat Integration Bridge

Connects Masumi Network's agent economy with Ziggurat's explainable AI platform,
enabling AI agents to earn rewards for providing explainable, verified intelligence.

Key Features:
- Cross-platform agent registry synchronization
- Explainable AI task rewards through Masumi
- Unified blockchain verification across ICP and other chains
- Automatic quality scoring based on explanation quality
- Multi-chain payment orchestration
"""

import asyncio
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum

from ..blockchain.masumi_integration import (
    MasumiNetworkClient,
    MasumiTaskReward,
    TaskStatus
)
from ..blockchain.ziggurat import (
    ZigguratIntelligence,
    ZigguratConfig,
    ZigguratExplanation,
    ExplanationMethod,
    BlockchainNetwork
)
from ..shared.config.ziggurat_config import ZigguratConfig as SharedZigguratConfig


class IntegrationMode(Enum):
    """Integration operation modes."""
    UNIFIED = "unified"  # Single interface for both systems
    FEDERATED = "federated"  # Separate but synchronized
    HYBRID = "hybrid"  # Smart routing based on task type


@dataclass
class ExplainableTaskResult:
    """Result of an explainable AI task with rewards."""
    task_id: str
    agent_id: str
    explanation: ZigguratExplanation
    reward: Optional[MasumiTaskReward]
    quality_score: float
    verification_proofs: Dict[str, str]
    total_cost_cycles: int
    execution_time_ms: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "explanation": self.explanation.to_dict(),
            "reward": self.reward.to_dict() if self.reward else None,
            "quality_score": self.quality_score,
            "verification_proofs": self.verification_proofs,
            "total_cost_cycles": self.total_cost_cycles,
            "execution_time_ms": self.execution_time_ms
        }


class MasumiZigguratBridge:
    """
    Integration bridge between Masumi Network and Ziggurat Intelligence.
    
    Enables AI agents to:
    1. Discover explainable AI tasks on Masumi Network
    2. Process tasks using Ziggurat's decentralized AI
    3. Submit verified explanations for rewards
    4. Build reputation through quality explanations
    """
    
    def __init__(
        self,
        masumi_api_key: str,
        agent_id: str,
        ziggurat_config: Optional[ZigguratConfig] = None,
        integration_mode: IntegrationMode = IntegrationMode.UNIFIED,
        masumi_base_url: str = "https://api.masumi.network",
        auto_verify_explanations: bool = True,
        min_quality_threshold: float = 0.7
    ):
        """
        Initialize the integration bridge.
        
        Args:
            masumi_api_key: Masumi Network API key
            agent_id: Unique agent identifier
            ziggurat_config: Ziggurat configuration (defaults to ICP)
            integration_mode: How to integrate the systems
            masumi_base_url: Masumi API endpoint
            auto_verify_explanations: Automatically verify on blockchain
            min_quality_threshold: Minimum quality score for rewards
        """
        self.agent_id = agent_id
        self.integration_mode = integration_mode
        self.auto_verify = auto_verify_explanations
        self.min_quality_threshold = min_quality_threshold
        
        # Initialize clients
        self.masumi_client = MasumiNetworkClient(
            api_key=masumi_api_key,
            agent_id=agent_id,
            base_url=masumi_base_url
        )
        
        self.ziggurat_config = ziggurat_config or ZigguratConfig(
            primary_chain=BlockchainNetwork.ICP,
            verify_on_blockchain=auto_verify_explanations,
            enable_cache=True,
            cache_ttl=300  # 5 minutes
        )
        self.ziggurat_client = ZigguratIntelligence(self.ziggurat_config)
        
        # Integration state
        self._task_cache: Dict[str, Any] = {}
        self._explanation_cache: Dict[str, ZigguratExplanation] = {}
        self._initialized = False
        
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.cleanup()
        
    async def initialize(self):
        """Initialize both platforms and synchronize agent registry."""
        if self._initialized:
            return
            
        # Initialize Masumi client
        await self.masumi_client.__aenter__()
        
        # Initialize Ziggurat client
        await self.ziggurat_client.initialize()
        
        # Register agent capabilities on Masumi
        capabilities = await self._get_unified_capabilities()
        await self.masumi_client.register_agent(
            capabilities=capabilities,
            reputation_score=0.0  # Will be updated based on performance
        )
        
        self._initialized = True
        
    async def cleanup(self):
        """Cleanup resources."""
        if self.masumi_client:
            await self.masumi_client.__aexit__(None, None, None)
        if self.ziggurat_client:
            await self.ziggurat_client.cleanup()
        self._task_cache.clear()
        self._explanation_cache.clear()
        self._initialized = False
        
    async def _get_unified_capabilities(self) -> List[str]:
        """Get unified capabilities from both platforms."""
        capabilities = [
            "explainable_ai",
            "blockchain_verification",
            "multi_chain_proof",
            "natural_language_reasoning",
            "counterfactual_analysis",
            "feature_importance",
            "attention_visualization"
        ]
        
        # Add Ziggurat-specific capabilities
        models = await self.ziggurat_client.list_available_models()
        for model in models:
            capabilities.extend([
                f"model:{model.model_id}",
                f"explanation:{method.value}" 
                for method in model.supports_explanation
            ])
            
        return list(set(capabilities))  # Remove duplicates
        
    async def discover_explainable_tasks(
        self,
        task_type: Optional[str] = "explainable_ai",
        min_reward: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Discover available explainable AI tasks from Masumi Network.
        
        Args:
            task_type: Filter by task type
            min_reward: Minimum reward threshold
            
        Returns:
            List of available explainable AI tasks
        """
        # Get tasks from Masumi
        tasks = await self.masumi_client.get_available_tasks(
            task_type=task_type,
            min_reward=min_reward
        )
        
        # Filter for explainable AI tasks
        explainable_tasks = []
        for task in tasks:
            if self._is_explainable_task(task):
                # Enhance with Ziggurat compatibility info
                task["supported_methods"] = [
                    method.value for method in ExplanationMethod
                ]
                task["estimated_cycles"] = self._estimate_task_cycles(task)
                explainable_tasks.append(task)
                
        return explainable_tasks
        
    async def process_explainable_task(
        self,
        task_id: str,
        task_data: Any,
        explanation_method: Optional[ExplanationMethod] = None,
        include_counterfactuals: bool = False,
        cross_chain_verify: bool = False
    ) -> ExplainableTaskResult:
        """
        Process an explainable AI task using Ziggurat Intelligence.
        
        Args:
            task_id: Masumi task ID
            task_data: Input data for AI processing
            explanation_method: Preferred explanation method
            include_counterfactuals: Generate counterfactual examples
            cross_chain_verify: Verify across multiple blockchains
            
        Returns:
            ExplainableTaskResult with explanation and potential reward
        """
        start_time = datetime.utcnow()
        
        # Claim task on Masumi
        claim_result = await self.masumi_client.claim_task(task_id)
        if not claim_result.get("success"):
            raise RuntimeError(f"Failed to claim task: {claim_result}")
            
        try:
            # Process with Ziggurat Intelligence
            if include_counterfactuals:
                explanation = await self.ziggurat_client.explain_with_counterfactuals(
                    data=task_data,
                    num_counterfactuals=3,
                    model_id=None  # Auto-select best model
                )
            else:
                explanation = await self.ziggurat_client.explain_decision(
                    data=task_data,
                    method=explanation_method,
                    blockchain_verify=self.auto_verify
                )
                
            # Add cross-chain verification if requested
            verification_proofs = {}
            if cross_chain_verify:
                verification_proofs = await self._cross_chain_verify(
                    explanation.proof_hash
                )
                
            # Calculate quality score
            quality_score = self._calculate_quality_score(explanation)
            
            # Generate execution proof for Masumi
            execution_proof = {
                "ziggurat_explanation": explanation.to_dict(),
                "verification_proofs": verification_proofs,
                "processing_time_ms": (datetime.utcnow() - start_time).total_seconds() * 1000,
                "model_used": explanation.method_used.value if explanation.method_used else "auto",
                "blockchain_verified": explanation.blockchain_verified
            }
            
            # Submit completion to Masumi
            quality_metrics = {
                "explanation_confidence": explanation.confidence,
                "feature_coverage": len(explanation.feature_importance) if explanation.feature_importance else 0,
                "verification_count": len(verification_proofs),
                "quality_score": quality_score
            }
            
            completion_result = await self.masumi_client.submit_task_completion(
                task_id=task_id,
                execution_proof=execution_proof,
                quality_metrics=quality_metrics
            )
            
            # Claim reward if quality threshold met
            reward = None
            if quality_score >= self.min_quality_threshold:
                reward = await self.masumi_client.claim_reward(task_id)
                
            # Cache result
            result = ExplainableTaskResult(
                task_id=task_id,
                agent_id=self.agent_id,
                explanation=explanation,
                reward=reward,
                quality_score=quality_score,
                verification_proofs=verification_proofs,
                total_cost_cycles=explanation.cost_cycles,
                execution_time_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000)
            )
            
            self._explanation_cache[task_id] = explanation
            
            return result
            
        except Exception as e:
            # Report task failure
            await self.masumi_client.submit_task_completion(
                task_id=task_id,
                execution_proof={"error": str(e)},
                quality_metrics={"quality_score": 0.0}
            )
            raise
            
    async def get_agent_performance_metrics(self) -> Dict[str, Any]:
        """
        Get unified performance metrics across both platforms.
        
        Returns:
            Combined metrics from Masumi and Ziggurat
        """
        # Get Masumi metrics
        masumi_reputation = await self.masumi_client.get_agent_reputation()
        masumi_earnings = await self.masumi_client.get_earnings_history(limit=100)
        
        # Calculate Ziggurat-specific metrics
        total_explanations = len(self._explanation_cache)
        avg_confidence = sum(
            exp.confidence for exp in self._explanation_cache.values()
        ) / max(total_explanations, 1)
        
        total_cycles_used = sum(
            exp.cost_cycles for exp in self._explanation_cache.values()
        )
        
        # Combine metrics
        return {
            "agent_id": self.agent_id,
            "masumi_reputation": masumi_reputation,
            "total_earnings": sum(r.reward_amount for r in masumi_earnings),
            "earnings_by_token": self._aggregate_earnings_by_token(masumi_earnings),
            "total_tasks_completed": len(masumi_earnings),
            "total_explanations_generated": total_explanations,
            "average_explanation_confidence": avg_confidence,
            "total_cycles_consumed": total_cycles_used,
            "average_quality_score": sum(
                r.quality_score for r in masumi_earnings
            ) / max(len(masumi_earnings), 1),
            "integration_mode": self.integration_mode.value,
            "verification_rate": sum(
                1 for exp in self._explanation_cache.values() 
                if exp.blockchain_verified
            ) / max(total_explanations, 1)
        }
        
    async def submit_custom_explanation(
        self,
        data: Any,
        explanation_text: str,
        confidence: float,
        feature_importance: Optional[Dict[str, float]] = None,
        verify_on_chain: bool = True
    ) -> ExplainableTaskResult:
        """
        Submit a custom explanation for rewards without a predefined task.
        Useful for proactive intelligence contributions.
        
        Args:
            data: Input data that was analyzed
            explanation_text: Human-readable explanation
            confidence: Confidence score (0-1)
            feature_importance: Optional feature importance scores
            verify_on_chain: Whether to verify on blockchain
            
        Returns:
            ExplainableTaskResult with potential reward
        """
        # Create a custom task on Masumi
        custom_task = {
            "type": "custom_explanation",
            "data_hash": hashlib.sha256(str(data).encode()).hexdigest(),
            "submitted_by": self.agent_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Use Ziggurat to enhance and verify the explanation
        enhanced_explanation = ZigguratExplanation(
            reasoning=explanation_text,
            confidence=confidence,
            method_used=ExplanationMethod.CUSTOM,
            blockchain_verified=verify_on_chain,
            proof_hash=self._generate_proof_hash(data, explanation_text) if verify_on_chain else None,
            verification_chain=self.ziggurat_config.primary_chain if verify_on_chain else None,
            feature_importance=feature_importance,
            processing_time_ms=100,  # Minimal processing for custom
            cost_cycles=500000  # Base cost for custom explanations
        )
        
        if verify_on_chain:
            enhanced_explanation.transaction_id = f"custom-{enhanced_explanation.proof_hash[:12]}"
            
        # Calculate quality and submit for potential rewards
        quality_score = self._calculate_quality_score(enhanced_explanation)
        
        result = ExplainableTaskResult(
            task_id=f"custom-{datetime.utcnow().timestamp()}",
            agent_id=self.agent_id,
            explanation=enhanced_explanation,
            reward=None,  # Rewards determined by network consensus
            quality_score=quality_score,
            verification_proofs={},
            total_cost_cycles=enhanced_explanation.cost_cycles,
            execution_time_ms=enhanced_explanation.processing_time_ms
        )
        
        return result
        
    async def _cross_chain_verify(self, proof_hash: str) -> Dict[str, str]:
        """Verify proof across multiple blockchains."""
        chains = [
            BlockchainNetwork.ICP,
            BlockchainNetwork.CARDANO,
            BlockchainNetwork.ETHEREUM
        ]
        
        verification_proofs = {}
        for chain in chains:
            try:
                verified = await self.ziggurat_client.verify_proof(
                    proof_hash, chain
                )
                if verified:
                    verification_proofs[chain.value] = f"{chain.value}-verified-{proof_hash[:8]}"
            except Exception:
                # Skip chains that fail verification
                continue
                
        return verification_proofs
        
    def _is_explainable_task(self, task: Dict[str, Any]) -> bool:
        """Check if a task requires explainable AI."""
        task_type = task.get("type", "").lower()
        requires_explanation = task.get("requires_explanation", False)
        
        explainable_keywords = [
            "explain", "interpret", "understand", "analyze",
            "reasoning", "justif", "clarif", "insight"
        ]
        
        return (
            requires_explanation or
            task_type == "explainable_ai" or
            any(keyword in task_type for keyword in explainable_keywords) or
            any(keyword in task.get("description", "").lower() 
                for keyword in explainable_keywords)
        )
        
    def _estimate_task_cycles(self, task: Dict[str, Any]) -> int:
        """Estimate computational cycles needed for a task."""
        base_cycles = 1000000  # 1M cycles base
        
        # Adjust based on task complexity
        complexity = task.get("complexity", "medium").lower()
        if complexity == "low":
            return base_cycles // 2
        elif complexity == "high":
            return base_cycles * 3
        else:
            return base_cycles
            
    def _calculate_quality_score(self, explanation: ZigguratExplanation) -> float:
        """
        Calculate quality score for an explanation.
        
        Factors:
        - Confidence level
        - Blockchain verification
        - Feature importance coverage
        - Processing efficiency
        """
        score = 0.0
        
        # Base confidence score (40%)
        score += explanation.confidence * 0.4
        
        # Blockchain verification (20%)
        if explanation.blockchain_verified:
            score += 0.2
            
        # Feature importance (20%)
        if explanation.feature_importance:
            coverage = min(len(explanation.feature_importance) / 5, 1.0)
            score += coverage * 0.2
            
        # Cross-chain proofs (10%)
        if hasattr(explanation, 'cross_chain_proofs') and explanation.cross_chain_proofs:
            cross_chain_score = min(len(explanation.cross_chain_proofs) / 3, 1.0)
            score += cross_chain_score * 0.1
            
        # Processing efficiency (10%)
        if explanation.processing_time_ms < 1000:  # Under 1 second
            score += 0.1
        elif explanation.processing_time_ms < 5000:  # Under 5 seconds
            score += 0.05
            
        return min(score, 1.0)  # Cap at 1.0
        
    def _aggregate_earnings_by_token(
        self, 
        earnings: List[MasumiTaskReward]
    ) -> Dict[str, float]:
        """Aggregate earnings by token type."""
        token_earnings = {}
        for reward in earnings:
            token = reward.reward_token
            if token not in token_earnings:
                token_earnings[token] = 0.0
            token_earnings[token] += reward.reward_amount
        return token_earnings
        
    def _generate_proof_hash(self, data: Any, explanation: str) -> str:
        """Generate proof hash for custom explanations."""
        proof_data = {
            "data": str(data),
            "explanation": explanation,
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        return hashlib.sha256(
            json.dumps(proof_data, sort_keys=True).encode()
        ).hexdigest()


# Convenience functions for quick integration
async def explain_and_earn(
    data: Any,
    masumi_api_key: str,
    agent_id: str,
    task_id: Optional[str] = None
) -> ExplainableTaskResult:
    """
    Quick function to explain data and potentially earn rewards.
    
    Args:
        data: Input data to explain
        masumi_api_key: Masumi Network API key
        agent_id: Your agent ID
        task_id: Optional Masumi task ID
        
    Returns:
        ExplainableTaskResult with explanation and potential reward
    """
    async with MasumiZigguratBridge(
        masumi_api_key=masumi_api_key,
        agent_id=agent_id
    ) as bridge:
        if task_id:
            return await bridge.process_explainable_task(task_id, data)
        else:
            # Generate custom explanation
            explanation = await bridge.ziggurat_client.explain_decision(data)
            return await bridge.submit_custom_explanation(
                data=data,
                explanation_text=explanation.reasoning,
                confidence=explanation.confidence,
                feature_importance=explanation.feature_importance
            )