#!/usr/bin/env python3
"""
Ziggurat Intelligence Community Agent Example
Demonstrates decentralized explainable AI with educational blockchain verification

Community Tier Features:
- Basic explainable AI methods (LIME, SHAP, gradient)
- Educational blockchain verification on ICP
- Rate limited to 100 requests/hour
- 2 community AI models
- Free for learning and development

For production use, consider Professional or Enterprise tiers.
"""

import asyncio
import argparse
import json
from typing import Dict, Any

# Add parent directory to path for imports
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.core.agents.base import AsyncContextAgent
from src.core.blockchain.ziggurat import ZigguratCommunity, CommunityConfig, ExplanationMethod


class ZigguratBasicAgent(AsyncContextAgent):
    """
    Community-tier agent demonstrating Ziggurat Intelligence.
    
    Features:
    - Basic explainable AI (LIME, SHAP, gradient)
    - Educational blockchain verification
    - Rate limited to 100 requests/hour
    - Free for learning and development
    
    For production applications requiring advanced features,
    consider upgrading to Professional or Enterprise tiers.
    """
    
    name = "ziggurat_basic"
    description = "Community-tier decentralized explainable AI agent"
    
    def __init__(self, explanation_method: ExplanationMethod = ExplanationMethod.SHAP):
        super().__init__()
        self.explanation_method = explanation_method
        self.ziggurat = None
        
    async def initialize(self):
        """Initialize Ziggurat Intelligence community client"""
        await super().initialize()
        
        # Configure community tier
        config = CommunityConfig(
            rate_limit_per_hour=100,
            enable_cache=True,
            fallback_mode=True
        )
        
        self.ziggurat = ZigguratCommunity(config)
        await self.ziggurat.initialize()
        
    async def cleanup(self):
        """Cleanup resources"""
        if self.ziggurat:
            await self.ziggurat.cleanup()
        await super().cleanup()
        
    async def run(self, data: Any = None) -> Dict[str, Any]:
        """
        Process data with Ziggurat Intelligence Community tier.
        
        Args:
            data: Input data to analyze (text, dict, or any format)
            
        Returns:
            Dict containing analysis results and educational blockchain proof
            
        Community Tier Limitations:
        - Rate limited to 100 requests/hour
        - Basic explanation methods only
        - Educational blockchain verification
        - 2 community AI models available
        """
        
        # Default data if none provided
        if data is None:
            data = {
                "transaction_amount": 5000,
                "account_age_days": 365,
                "previous_transactions": 150,
                "location": "US",
                "device_fingerprint": "desktop_chrome_win"
            }
            
        self.logger.info(f"Processing data with Ziggurat Intelligence Community tier ({self.explanation_method.value} method)")
        
        # Check rate limit status
        rate_status = await self.ziggurat.get_rate_limit_status()
        if rate_status["requests_remaining"] < 10:
            self.logger.warning(f"Rate limit approaching: {rate_status['requests_remaining']} requests remaining")
        
        # Get explainable AI analysis
        try:
            explanation = await self.ziggurat.explain_decision(
                data=data,
                method=self.explanation_method,
                blockchain_verify=True
            )
        except Exception as e:
            if "rate limit exceeded" in str(e):
                # Add upgrade messaging for rate limit hits
                upgrade_info = self.ziggurat.get_upgrade_info()
                return {
                    "status": "rate_limited",
                    "error": str(e),
                    "upgrade_info": upgrade_info
                }
            raise
        
        # Format results
        result = {
            "status": "success",
            "tier": "community",
            "analysis": {
                "reasoning": explanation.reasoning,
                "confidence": explanation.confidence,
                "method": explanation.method_used.value
            },
            "explanation": {
                "feature_importance": explanation.feature_importance,
                "note": "Community tier - basic feature importance only"
            },
            "blockchain": {
                "verified": explanation.blockchain_verified,
                "proof_hash": explanation.proof_hash,
                "chain": explanation.verification_chain.value if explanation.verification_chain else None,
                "note": "Educational blockchain verification (community tier)"
            },
            "metadata": {
                "processing_time_ms": explanation.processing_time_ms,
                "cost_cycles": explanation.cost_cycles,
                "tier": explanation.tier,
                "requests_remaining": rate_status["requests_remaining"]
            }
        }
        
        # Add upgrade prompt for users approaching limits
        if rate_status["requests_remaining"] < 20:
            result["upgrade_suggestion"] = {
                "message": "Approaching rate limit. Consider upgrading for higher limits.",
                "professional_tier": "10,000 requests/hour + 15+ models ($199-999/month)",
                "contact": "sales@agentforge.ai"
            }
            
        self.logger.info(f"Analysis complete. Confidence: {explanation.confidence:.2%}")
        self.logger.info(f"Educational blockchain proof: {explanation.proof_hash}")
        
        return result


class ZigguratAdvancedAgent(AsyncContextAgent):
    """
    Advanced features demonstration (Community tier limitations apply).
    
    Note: Advanced features like counterfactuals and batch processing
    require Professional or Enterprise tiers. This agent demonstrates
    the APIs but with community tier limitations.
    """
    
    name = "ziggurat_advanced"
    description = "Advanced Ziggurat features demo (upgrade required for full functionality)"
    
    def __init__(self):
        super().__init__()
        self.ziggurat = None
        
    async def initialize(self):
        """Initialize community client"""
        await super().initialize()
        config = CommunityConfig(fallback_mode=True)
        self.ziggurat = ZigguratCommunity(config)
        await self.ziggurat.initialize()
        
    async def cleanup(self):
        """Cleanup resources"""
        if self.ziggurat:
            await self.ziggurat.cleanup()
        await super().cleanup()
        
    async def run(self, data: Any = None) -> Dict[str, Any]:
        """Demonstrate advanced features with community tier limitations"""
        
        # Default financial data
        if data is None:
            data = {
                "loan_amount": 50000,
                "income": 75000,
                "credit_score": 720,
                "debt_to_income": 0.35,
                "employment_years": 5
            }
            
        self.logger.info("Running advanced features demo with community tier")
        
        # Get basic explanation (community tier)
        explanation = await self.ziggurat.explain_decision(data, ExplanationMethod.SHAP)
        
        # Simulate what advanced features would look like
        # (These would be real in Professional/Enterprise tiers)
        mock_counterfactuals = [
            {
                "change": "Increase credit score by 50 points",
                "new_prediction": "Higher approval confidence",
                "confidence_change": "+15%"
            },
            {
                "change": "Reduce debt-to-income by 10%",
                "new_prediction": "Improved terms available", 
                "confidence_change": "+8%"
            }
        ]
        
        # Mock sensitivity analysis (would be real batch processing in higher tiers)
        mock_sensitivity = [
            {"credit_score": 650, "confidence": 0.65, "reasoning": "Moderate risk profile"},
            {"credit_score": 700, "confidence": 0.78, "reasoning": "Good credit standing"},
            {"credit_score": 750, "confidence": 0.89, "reasoning": "Excellent credit profile"},
            {"credit_score": 800, "confidence": 0.95, "reasoning": "Premium credit status"}
        ]
        
        # Get available models (community tier limited)
        available_models = await self.ziggurat.list_available_models()
        upgrade_info = self.ziggurat.get_upgrade_info()
        
        return {
            "tier": "community",
            "main_analysis": explanation.to_dict(),
            "counterfactuals_preview": {
                "note": "Preview only - upgrade required for real counterfactuals",
                "mock_examples": mock_counterfactuals,
                "upgrade_required": "Professional tier for real counterfactual analysis"
            },
            "sensitivity_analysis_preview": {
                "note": "Preview only - upgrade required for batch processing",
                "mock_examples": mock_sensitivity,
                "upgrade_required": "Professional tier for batch processing"
            },
            "available_models": [
                {
                    "name": model.name,
                    "model_type": model.model_type,
                    "tier": "community"  # All models in community tier are community tier
                }
                for model in available_models
            ],
            "upgrade_info": upgrade_info,
            "limitations": [
                "Community tier: 2 basic models only",
                "No real counterfactual analysis",
                "No batch processing capabilities", 
                "Rate limited to 100 requests/hour",
                "Educational blockchain proofs only"
            ]
        }


async def main():
    """Main function for CLI usage"""
    parser = argparse.ArgumentParser(
        description="Ziggurat Intelligence Agent - Decentralized Explainable AI"
    )
    
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demo with sample data"
    )
    
    parser.add_argument(
        "--data",
        type=str,
        help="JSON file path or JSON string with input data"
    )
    
    parser.add_argument(
        "--method",
        choices=["shap", "lime", "gradient", "attention"],
        default="shap",
        help="Explanation method to use"
    )
    
    parser.add_argument(
        "--advanced",
        action="store_true",
        help="Use advanced agent with counterfactuals"
    )
    
    args = parser.parse_args()
    
    # Parse input data
    data = None
    if args.data:
        try:
            # Try as JSON string first
            data = json.loads(args.data)
        except json.JSONDecodeError:
            # Try as file path
            try:
                with open(args.data, 'r') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error loading data: {e}")
                return
                
    # Select agent
    if args.advanced:
        agent = ZigguratAdvancedAgent()
    else:
        method = ExplanationMethod(args.method)
        agent = ZigguratBasicAgent(explanation_method=method)
        
    # Run agent
    async with agent:
        result = await agent.run(data)
        
        # Handle rate limiting
        if result.get("status") == "rate_limited":
            print("\n" + "="*60)
            print("⚠️  RATE LIMIT EXCEEDED")
            print("="*60 + "\n")
            print(f"Error: {result['error']}")
            print("\n🚀 Upgrade Options:")
            upgrade = result["upgrade_info"]
            print(f"Professional: {upgrade['professional_tier']['price']}")
            print("  • 10,000 requests/hour")
            print("  • 15+ professional AI models")
            print("  • Priority processing")
            print(f"Enterprise: {upgrade['enterprise_tier']['price']}")
            print("  • Unlimited requests")
            print("  • 50+ enterprise models")
            print("  • SLA guarantees")
            print(f"\nContact: {upgrade['contact']}")
            return
        
        # Pretty print results
        print("\n" + "="*60)
        print("🏛️  ZIGGURAT INTELLIGENCE RESULTS (COMMUNITY TIER)")
        print("="*60 + "\n")
        
        if args.advanced:
            # Advanced output with upgrade messaging
            main_analysis = result["main_analysis"]
            print(f"📊 Analysis: {main_analysis['reasoning']}")
            print(f"🎯 Confidence: {main_analysis['confidence']:.2%}")
            print(f"🔐 Educational Proof: {main_analysis['proof_hash']}")
            
            print("\n📈 Counterfactuals (Preview Only - Upgrade Required):")
            for cf in result["counterfactuals_preview"]["mock_examples"]:
                print(f"  • {cf['change']} → {cf['new_prediction']} ({cf['confidence_change']})")
            print(f"  ⚠️  {result['counterfactuals_preview']['upgrade_required']}")
                
            print("\n📉 Sensitivity Analysis (Preview Only - Upgrade Required):")
            for analysis in result["sensitivity_analysis_preview"]["mock_examples"]:
                print(f"  • Score {analysis['credit_score']}: {analysis['confidence']:.2%}")
            print(f"  ⚠️  {result['sensitivity_analysis_preview']['upgrade_required']}")
                
            print("\n🤖 Available Models (Community Tier):")
            for model in result["available_models"]:
                print(f"  • {model['name']} ({model['model_type']}) - {model['tier']} tier")
                
            print("\n🚀 Upgrade Info:")
            upgrade = result["upgrade_info"]
            print(f"Professional: {upgrade['professional_tier']['price']}")
            print(f"Enterprise: {upgrade['enterprise_tier']['price']}")
        else:
            # Basic output
            print(f"📊 Analysis: {result['analysis']['reasoning']}")
            print(f"🎯 Confidence: {result['analysis']['confidence']:.2%}")
            print(f"🧮 Method: {result['analysis']['method']}")
            print(f"🏷️  Tier: {result['tier']}")
            
            print("\n📐 Feature Importance:")
            for feature, importance in (result['explanation']['feature_importance'] or {}).items():
                print(f"  • {feature}: {importance:.2%}")
                
            print("\n🔐 Blockchain Verification (Educational):")
            print(f"  • Verified: {result['blockchain']['verified']}")
            print(f"  • Chain: {result['blockchain']['chain']}")
            print(f"  • Proof: {result['blockchain']['proof_hash']}")
            print(f"  • Note: {result['blockchain']['note']}")
            
            print(f"\n⚡ Performance:")
            print(f"  • Processing Time: {result['metadata']['processing_time_ms']}ms")
            print(f"  • Cost: {result['metadata']['cost_cycles']:,} cycles")
            print(f"  • Requests Remaining: {result['metadata']['requests_remaining']}")
            
            # Show upgrade suggestion if approaching limits
            if "upgrade_suggestion" in result:
                print(f"\n🚀 Upgrade Suggestion:")
                print(f"  • {result['upgrade_suggestion']['message']}")
                print(f"  • {result['upgrade_suggestion']['professional_tier']}")
                print(f"  • Contact: {result['upgrade_suggestion']['contact']}")
            
        print("\n" + "="*60)
        print("Ancient Architecture, Infinite Intelligence")
        print("Community Tier - Upgrade for Production Features")
        print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())