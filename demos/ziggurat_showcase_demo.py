#!/usr/bin/env python3
"""
🏛️ Ziggurat Intelligence: Beautiful Showcase Demo
Ancient Architecture, Infinite Intelligence

A comprehensive demonstration of Ziggurat's explainable AI capabilities
without external dependencies - pure Python beauty!
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import time

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Mock imports for demonstration (replace with actual imports)
class MockZigguratClient:
    """Mock Ziggurat client for demonstration"""
    
    async def explain_decision(self, data: Dict, method: str = "shap") -> Dict:
        """Mock explanation generation"""
        await asyncio.sleep(0.5)  # Simulate API call
        
        if method == "shap":
            return {
                "reasoning": "Decision based on feature importance analysis using SHAP values",
                "confidence": 0.89,
                "feature_importance": {
                    "credit_score": 0.35,
                    "annual_income": 0.28,
                    "employment_years": 0.22,
                    "debt_to_income": -0.15
                },
                "method_used": "shap",
                "processing_time_ms": 45,
                "blockchain_verified": True,
                "proof_hash": "0xabcdef1234567890"
            }
        elif method == "lime":
            return {
                "reasoning": "Local interpretation shows positive contribution from key features",
                "confidence": 0.86,
                "local_explanation": {
                    "credit_score": {"contribution": 0.32, "direction": "positive"},
                    "annual_income": {"contribution": 0.25, "direction": "positive"},
                    "employment_years": {"contribution": 0.20, "direction": "positive"},
                    "debt_to_income": {"contribution": -0.12, "direction": "negative"}
                },
                "method_used": "lime",
                "processing_time_ms": 67,
                "samples_used": 1000
            }
        else:
            return {
                "reasoning": "Neural network analysis shows strong positive signals",
                "confidence": 0.84,
                "gradient_analysis": {
                    "layer_contributions": [0.15, 0.28, 0.35, 0.22],
                    "attention_weights": [0.31, 0.27, 0.24, 0.18]
                },
                "method_used": method,
                "processing_time_ms": 89
            }
    
    async def verify_on_blockchain(self, explanation: Dict) -> Dict:
        """Mock blockchain verification"""
        await asyncio.sleep(1.0)  # Simulate blockchain transaction
        return {
            "verified": True,
            "chain": "ICP",
            "canister_id": "rdmx6-jaaaa-aaaah-qdrqq-cai",
            "proof_hash": f"0x{''.join([str(i) for i in range(32)])}",
            "timestamp": datetime.utcnow().isoformat(),
            "cost_cycles": 100000
        }
    
    async def analyze_quality(self, data: Dict) -> Dict:
        """Mock quality assessment"""
        await asyncio.sleep(0.3)
        return {
            "quality_score": 0.87,
            "components": {
                "accuracy": 0.91,
                "clarity": 0.85,
                "completeness": 0.88,
                "actionability": 0.84
            },
            "recommendations": [
                "Consider adding confidence intervals",
                "Include feature interaction analysis",
                "Provide counterfactual examples"
            ]
        }


def print_banner(text: str, char: str = "=", width: int = 80):
    """Print a beautiful banner"""
    print(f"\n{char * width}")
    print(f"{text.center(width)}")
    print(f"{char * width}\n")


def print_section(title: str, char: str = "-"):
    """Print a section header"""
    print(f"\n{char * 40}")
    print(f"  {title}")
    print(f"{char * 40}\n")


def print_result(title: str, data: Dict, indent: int = 2):
    """Pretty print results"""
    print(f"{' ' * indent}{title}:")
    for key, value in data.items():
        if isinstance(value, dict):
            print(f"{' ' * (indent + 2)}{key}:")
            for k, v in value.items():
                print(f"{' ' * (indent + 4)}{k}: {v}")
        elif isinstance(value, list):
            print(f"{' ' * (indent + 2)}{key}:")
            for item in value:
                print(f"{' ' * (indent + 4)}- {item}")
        else:
            print(f"{' ' * (indent + 2)}{key}: {value}")


def wait_for_user(message: str = "\n⏸️  Press Enter to continue..."):
    """Wait for user input before continuing"""
    input(message)


def print_with_typing_effect(text: str, delay: float = 0.03):
    """Print text with typing effect for emphasis"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # New line at the end


def clear_screen():
    """Clear the terminal screen"""
    import os
    os.system('clear' if os.name == 'posix' else 'cls')


class ZigguratShowcase:
    """Main showcase demonstration class"""
    
    def __init__(self, presentation_mode: bool = False, auto_advance: bool = False):
        self.client = MockZigguratClient()
        self.demos_run = 0
        self.presentation_mode = presentation_mode
        self.auto_advance = auto_advance
        
    async def run_complete_showcase(self):
        """Run the complete Ziggurat showcase"""
        if self.presentation_mode:
            clear_screen()
            
        print_banner("🏛️  ZIGGURAT INTELLIGENCE SHOWCASE", "=", 80)
        print_with_typing_effect("Ancient Architecture, Infinite Intelligence")
        print("\nExperience the power of explainable AI with blockchain verification")
        
        if self.presentation_mode:
            wait_for_user("\n🎯 Press Enter to begin the demonstration...")
        
        await self.demo_introduction()
        await self.demo_service_tiers()
        await self.demo_explanation_methods()
        await self.demo_real_world_scenarios()
        await self.demo_blockchain_verification()
        await self.demo_quality_assessment()
        await self.demo_multi_chain_capabilities()
        await self.demo_performance_metrics()
        await self.demo_conclusion()
        
    async def demo_introduction(self):
        """Introduction to Ziggurat Intelligence"""
        if self.presentation_mode:
            clear_screen()
            
        print_section("📚 Introduction to Ziggurat Intelligence")
        
        print_with_typing_effect("Ziggurat Intelligence is a revolutionary explainable AI platform that provides:")
        
        features = [
            "✅ Transparent AI decision-making",
            "✅ Multiple explanation methods (SHAP, LIME, Gradient, Attention)",
            "✅ Blockchain-verified inference on ICP",
            "✅ Enterprise-grade performance and reliability",
            "✅ Multi-chain support through Chain Fusion"
        ]
        
        for feature in features:
            await asyncio.sleep(0.5)  # Small delay between features
            print(f"  {feature}")
        
        if self.presentation_mode:
            wait_for_user("\n📖 Press Enter to see Service Tiers...")
        else:
            await asyncio.sleep(2)
        
    async def demo_service_tiers(self):
        """Demonstrate service tier capabilities"""
        if self.presentation_mode:
            clear_screen()
            
        print_section("💎 Service Tiers Overview")
        
        tiers = [
            {
                "name": "Community (Free)",
                "emoji": "🆓",
                "features": [
                    "100 requests/hour",
                    "SHAP explanations only",
                    "3 pre-trained models",
                    "Basic support"
                ],
                "best_for": "Developers, researchers, small projects"
            },
            {
                "name": "Professional ($199-999/mo)",
                "emoji": "💼",
                "features": [
                    "10,000 requests/hour",
                    "All explanation methods",
                    "15+ models including GPT-4",
                    "Priority support",
                    "Custom model fine-tuning"
                ],
                "best_for": "Startups, growing businesses, production apps"
            },
            {
                "name": "Enterprise ($2000+/mo)",
                "emoji": "🏢",
                "features": [
                    "Unlimited requests",
                    "Custom model deployment",
                    "Dedicated infrastructure",
                    "99.9% SLA guarantee",
                    "24/7 phone support"
                ],
                "best_for": "Large organizations, critical applications"
            }
        ]
        
        for i, tier in enumerate(tiers):
            if self.presentation_mode and i > 0:
                print("\n" + "-" * 60 + "\n")
                
            print(f"\n{tier['emoji']} {tier['name']}")
            print("  Features:")
            for feature in tier['features']:
                await asyncio.sleep(0.3)  # Animate feature appearance
                print(f"    • {feature}")
            print(f"\n  📎 Best for: {tier['best_for']}")
            
            if self.presentation_mode and i < len(tiers) - 1:
                wait_for_user("\n⏭️  Press Enter for next tier...")
        
        if self.presentation_mode:
            wait_for_user("\n🧠 Press Enter to see Explanation Methods...")
        else:
            await asyncio.sleep(2)
        
    async def demo_explanation_methods(self):
        """Demonstrate different explanation methods"""
        if self.presentation_mode:
            clear_screen()
            
        print_section("🧠 Explanation Methods Demonstration")
        
        # Sample data for all demos
        sample_data = {
            "credit_score": 720,
            "annual_income": 85000,
            "debt_to_income": 0.28,
            "employment_years": 7,
            "loan_amount": 250000
        }
        
        print_with_typing_effect("Analyzing loan application with multiple explanation methods...")
        print(f"\n📋 Input data:")
        for key, value in sample_data.items():
            print(f"   • {key}: {value:,}" if isinstance(value, int) else f"   • {key}: {value}")
        
        # Demo each method
        methods = [
            {"name": "shap", "emoji": "📊", "description": "SHapley Additive exPlanations"},
            {"name": "lime", "emoji": "🍋", "description": "Local Interpretable Model-agnostic Explanations"},
            {"name": "gradient", "emoji": "📈", "description": "Gradient-based Neural Network Analysis"}
        ]
        
        for i, method_info in enumerate(methods):
            method = method_info["name"]
            
            if self.presentation_mode:
                wait_for_user(f"\n🔍 Press Enter to see {method.upper()} explanation...")
                print()
            
            print(f"\n{method_info['emoji']} {method.upper()} - {method_info['description']}")
            print("-" * 60)
            
            # Simulate processing
            print("\n⏳ Processing...", end='', flush=True)
            result = await self.client.explain_decision(sample_data, method)
            print(" Done! ✅")
            
            await asyncio.sleep(0.5)
            
            print(f"\n📊 Confidence: {result['confidence']:.2%}")
            print(f"💭 Reasoning: {result['reasoning']}")
            print(f"⚡ Processing time: {result.get('processing_time_ms', 0)}ms")
            
            if 'feature_importance' in result:
                print("\n📈 Feature Importance:")
                for feature, importance in result['feature_importance'].items():
                    bar_length = int(abs(importance) * 30)
                    bar = "█" * bar_length
                    color = "🟢" if importance > 0 else "🔴"
                    print(f"  {feature:20} {importance:+.2f} {color} {bar}")
                    await asyncio.sleep(0.2)  # Animate bars
            
            if not self.presentation_mode:
                await asyncio.sleep(1.5)
        
        if self.presentation_mode:
            wait_for_user("\n🌍 Press Enter to see Real-World Use Cases...")
        else:
            await asyncio.sleep(2)
            
    async def demo_real_world_scenarios(self):
        """Demonstrate real-world use cases"""
        print_section("🌍 Real-World Use Cases")
        
        scenarios = [
            {
                "title": "🏦 Financial Services - Credit Risk Assessment",
                "description": "AI-powered loan approval with full transparency",
                "data": {
                    "application_id": "LOAN-2025-1234",
                    "risk_score": 0.23,
                    "approval": True,
                    "confidence": 0.91
                },
                "impact": "Reduced approval time from 3 days to 3 minutes"
            },
            {
                "title": "🏥 Healthcare - Treatment Recommendation",
                "description": "Explainable medical diagnosis assistance",
                "data": {
                    "patient_id": "P-5678",
                    "condition_probability": 0.87,
                    "recommended_action": "Further testing",
                    "confidence": 0.84
                },
                "impact": "Improved diagnostic accuracy by 23%"
            },
            {
                "title": "🛡️ Cybersecurity - Threat Detection",
                "description": "Real-time threat analysis with explanations",
                "data": {
                    "threat_level": "HIGH",
                    "attack_vector": "Brute force attempt",
                    "blocked": True,
                    "confidence": 0.94
                },
                "impact": "Prevented 99.8% of security breaches"
            },
            {
                "title": "🏭 Manufacturing - Quality Control",
                "description": "AI-powered defect detection with reasoning",
                "data": {
                    "batch_id": "MFG-2025-789",
                    "defect_probability": 0.12,
                    "action": "Pass with monitoring",
                    "confidence": 0.88
                },
                "impact": "Reduced defect rate by 45%"
            }
        ]
        
        for scenario in scenarios:
            print(f"\n{scenario['title']}")
            print(f"  {scenario['description']}")
            print(f"  Results: {json.dumps(scenario['data'], indent=4)}")
            print(f"  Business Impact: {scenario['impact']}")
            await asyncio.sleep(2)
            
    async def demo_blockchain_verification(self):
        """Demonstrate blockchain verification process"""
        if self.presentation_mode:
            clear_screen()
            
        print_section("🔐 Blockchain Verification Process")
        
        print_with_typing_effect("Demonstrating end-to-end blockchain verification...")
        
        steps = [
            {
                "emoji": "1️⃣",
                "title": "Generating AI explanation",
                "action": self._step_generate_explanation,
                "result": "Explanation generated"
            },
            {
                "emoji": "2️⃣",
                "title": "Creating cryptographic proof",
                "action": self._step_create_proof,
                "result": "Proof created using zero-knowledge cryptography"
            },
            {
                "emoji": "3️⃣",
                "title": "Submitting to ICP blockchain",
                "action": self._step_submit_blockchain,
                "result": "Transaction submitted"
            },
            {
                "emoji": "4️⃣",
                "title": "Verification Complete",
                "action": self._step_verify_complete,
                "result": "Proof permanently stored"
            }
        ]
        
        for i, step in enumerate(steps):
            if self.presentation_mode and i > 0:
                wait_for_user("\n⏭️  Press Enter for next step...")
                
            print(f"\n{step['emoji']} {step['title']}...")
            
            # Animated progress bar
            for j in range(20):
                print("█", end='', flush=True)
                await asyncio.sleep(0.05)
            print(" ✅")
            
            result = await step['action']()
            print(f"   → {step['result']}")
            
            if isinstance(result, dict):
                for key, value in result.items():
                    print(f"      • {key}: {value}")
        
        print("\n" + "="*60)
        print_with_typing_effect("✨ This proof is now permanently stored and publicly verifiable!")
        print("="*60)
        
        if self.presentation_mode:
            wait_for_user("\n📊 Press Enter to see Quality Assessment...")
        else:
            await asyncio.sleep(2)
            
    async def _step_generate_explanation(self):
        explanation = await self.client.explain_decision({"test_data": "sample"}, "shap")
        return {"confidence": f"{explanation['confidence']:.2%}"}
        
    async def _step_create_proof(self):
        await asyncio.sleep(0.5)
        return {"method": "Zero-knowledge proof"}
        
    async def _step_submit_blockchain(self):
        verification = await self.client.verify_on_blockchain({})
        return {
            "Chain": verification['chain'],
            "Canister": verification['canister_id'][:16] + "...",
            "Cost": f"{verification['cost_cycles']:,} cycles"
        }
        
    async def _step_verify_complete(self):
        return {
            "Proof Hash": "0xabcdef...7890",
            "Timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        
    async def demo_quality_assessment(self):
        """Demonstrate quality assessment features"""
        print_section("📊 Quality Assessment System")
        
        print("Analyzing explanation quality and providing recommendations...")
        
        sample_explanation = {
            "method": "shap",
            "confidence": 0.87,
            "features_explained": 5,
            "processing_time": 45
        }
        
        quality = await self.client.analyze_quality(sample_explanation)
        
        print("\n🎯 Quality Assessment Results:")
        print(f"   Overall Score: {quality['quality_score']:.2%}")
        
        print("\n📈 Component Scores:")
        for component, score in quality['components'].items():
            bar = "█" * int(score * 20)
            print(f"   {component.capitalize():15} {score:.2%} {bar}")
        
        print("\n💡 Recommendations for Improvement:")
        for i, rec in enumerate(quality['recommendations'], 1):
            print(f"   {i}. {rec}")
            
        await asyncio.sleep(2)
        
    async def demo_multi_chain_capabilities(self):
        """Demonstrate multi-chain support"""
        print_section("⛓️ Multi-Chain Capabilities")
        
        print("Ziggurat supports verification across multiple blockchains:")
        
        chains = [
            {"name": "Internet Computer (ICP)", "status": "Primary", "features": "Native integration, lowest latency"},
            {"name": "Cardano", "status": "Active", "features": "Treasury monitoring, stake pool analysis"},
            {"name": "Ethereum", "status": "Active", "features": "DeFi analysis, smart contract verification"},
            {"name": "Bitcoin", "status": "Active", "features": "Transaction analysis, wallet monitoring"},
            {"name": "Avalanche", "status": "Coming Soon", "features": "Subnet analysis, validator monitoring"}
        ]
        
        for chain in chains:
            status_emoji = "✅" if chain['status'] == "Active" else "🔷" if chain['status'] == "Primary" else "🔄"
            print(f"\n{status_emoji} {chain['name']} - {chain['status']}")
            print(f"   Features: {chain['features']}")
            
        print("\n🌐 Cross-Chain Verification:")
        print("   • Single API for all chains")
        print("   • Unified proof format")
        print("   • Chain Fusion technology for seamless integration")
        
        await asyncio.sleep(2)
        
    async def demo_performance_metrics(self):
        """Show performance benchmarks"""
        print_section("⚡ Performance Metrics")
        
        metrics = {
            "Average Inference Time": {
                "Community": "120ms",
                "Professional": "45ms",
                "Enterprise": "15ms (GPU)"
            },
            "Throughput": {
                "Community": "100 req/hour",
                "Professional": "10,000 req/hour",
                "Enterprise": "Unlimited"
            },
            "Uptime (Last 90 days)": {
                "All Tiers": "99.97%"
            },
            "Model Accuracy": {
                "SHAP": "98.5%",
                "LIME": "96.2%",
                "Average": "97.8%"
            }
        }
        
        for category, values in metrics.items():
            print(f"\n📊 {category}:")
            for tier, value in values.items():
                print(f"   {tier}: {value}")
                
        await asyncio.sleep(2)
        
    async def demo_conclusion(self):
        """Show conclusion and next steps"""
        print_section("🎉 Demo Complete!")
        
        print("You've just experienced the power of Ziggurat Intelligence!")
        
        print("\n🚀 Ready to Get Started?")
        print("   1. Sign up for free at: https://ziggurat.ai/signup")
        print("   2. Get your API key instantly")
        print("   3. Install the SDK: pip install ziggurat-intelligence")
        print("   4. Start building explainable AI applications!")
        
        print("\n📚 Resources:")
        print("   • Documentation: https://docs.ziggurat.ai")
        print("   • GitHub Examples: https://github.com/agent-forge/ziggurat-examples")
        print("   • Discord Community: https://discord.gg/ziggurat")
        print("   • Support: support@ziggurat.ai")
        
        print("\n🏛️ Thank you for exploring Ziggurat Intelligence!")
        print("Ancient Architecture, Infinite Intelligence")
        
        print_banner("END OF DEMONSTRATION", "=", 80)


# Interactive menu system
async def interactive_menu(presentation_mode: bool = False):
    """Interactive menu for selecting demos"""
    showcase = ZigguratShowcase(presentation_mode=presentation_mode)
    
    while True:
        if presentation_mode:
            clear_screen()
            
        print("\n" + "=" * 60)
        print("🏛️  ZIGGURAT INTELLIGENCE - INTERACTIVE DEMO MENU")
        print("=" * 60)
        
        if presentation_mode:
            print("\n🎭 PRESENTATION MODE ENABLED")
            print("   • Clear screens between sections")
            print("   • User-controlled progression")
            print("   • Enhanced visual effects")
        
        print("\nSelect a demonstration:")
        print("  1. 🎯 Quick Overview (2 minutes)")
        print("  2. 🧠 Explanation Methods Deep Dive")
        print("  3. 🌍 Real-World Use Cases")
        print("  4. 🔐 Blockchain Verification Demo")
        print("  5. 📊 Quality Assessment System")
        print("  6. ⛓️ Multi-Chain Capabilities")
        print("  7. ⚡ Performance Benchmarks")
        print("  8. 🚀 Complete Showcase (10 minutes)")
        print("  9. 🎭 Toggle Presentation Mode")
        print("  0. ❌ Exit")
        
        try:
            choice = input("\nEnter your choice (0-9): ").strip()
            
            if choice == "1":
                await showcase.demo_introduction()
                await showcase.demo_service_tiers()
            elif choice == "2":
                await showcase.demo_explanation_methods()
            elif choice == "3":
                await showcase.demo_real_world_scenarios()
            elif choice == "4":
                await showcase.demo_blockchain_verification()
            elif choice == "5":
                await showcase.demo_quality_assessment()
            elif choice == "6":
                await showcase.demo_multi_chain_capabilities()
            elif choice == "7":
                await showcase.demo_performance_metrics()
            elif choice == "8":
                await showcase.run_complete_showcase()
            elif choice == "9":
                presentation_mode = not presentation_mode
                showcase = ZigguratShowcase(presentation_mode=presentation_mode)
                print(f"\n🎭 Presentation mode: {'ON' if presentation_mode else 'OFF'}")
                await asyncio.sleep(1)
            elif choice == "0":
                print("\n✨ Thank you for exploring Ziggurat Intelligence!")
                break
            else:
                print("\n❌ Invalid choice. Please select 0-9.")
                
            if choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                wait_for_user("\n🏠 Press Enter to return to menu...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Thank you for your time!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


# Main entry point
async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Ziggurat Intelligence - Beautiful Showcase Demo"
    )
    
    parser.add_argument(
        "--mode",
        choices=["full", "interactive", "quick", "presentation"],
        default="interactive",
        help="Demo mode: full, interactive, quick, or presentation"
    )
    
    parser.add_argument(
        "--no-delay",
        action="store_true",
        help="Run without delays between sections"
    )
    
    parser.add_argument(
        "--presentation",
        action="store_true",
        help="Enable presentation mode (clear screens, user-controlled progression)"
    )
    
    args = parser.parse_args()
    
    # Determine if presentation mode should be enabled
    presentation_mode = args.presentation or args.mode == "presentation"
    
    # Create showcase instance
    showcase = ZigguratShowcase(presentation_mode=presentation_mode)
    
    # Run appropriate mode
    if args.mode == "full" or (args.mode == "presentation" and not args.presentation):
        await showcase.run_complete_showcase()
    elif args.mode == "quick":
        await showcase.demo_introduction()
        await showcase.demo_service_tiers()
        await showcase.demo_conclusion()
    else:
        await interactive_menu(presentation_mode=presentation_mode)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Thank you for exploring Ziggurat Intelligence!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()