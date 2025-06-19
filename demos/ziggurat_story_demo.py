#!/usr/bin/env python3
"""
🏛️ ZIGGURAT INTELLIGENCE: The Story
A narrative journey through the future of explainable AI
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import time
import os

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Utility functions for beautiful presentation
def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_big_title(text: str, subtitle: str = ""):
    """Print large ASCII art title"""
    print("\n" + "="*80)
    print(f"{text.center(80)}")
    if subtitle:
        print(f"{subtitle.center(80)}")
    print("="*80 + "\n")

def print_chapter(chapter_num: int, title: str):
    """Print chapter header"""
    print("\n\n" + "━"*80)
    print(f"  CHAPTER {chapter_num}: {title}".upper())
    print("━"*80 + "\n")

def type_text(text: str, delay: float = 0.03):
    """Print text with typing effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def wait_for_user(message: str = "\n[ Press Enter to continue ]"):
    """Wait for user input"""
    input(message)

def print_dramatic_pause(seconds: int = 2):
    """Create dramatic pause with dots"""
    for i in range(seconds):
        print(".", end='', flush=True)
        time.sleep(1)
    print("\n")

class ZigguratStoryDemo:
    """Story-driven demonstration of Ziggurat Intelligence"""
    
    def __init__(self):
        self.current_chapter = 0
        
    async def start_journey(self):
        """Begin the Ziggurat story"""
        clear_screen()
        
        # Opening scene
        print_big_title(
            "🏛️  ZIGGURAT INTELLIGENCE",
            "Ancient Architecture, Infinite Intelligence"
        )
        
        type_text("The year is 2025.")
        await asyncio.sleep(1)
        type_text("AI has transformed every industry.")
        await asyncio.sleep(1)
        type_text("But there's one problem...")
        print_dramatic_pause(3)
        
        print("\n" + " "*20 + "🤔 NOBODY KNOWS WHY AI MAKES DECISIONS 🤔")
        
        wait_for_user("\n\n[ Press Enter to discover the solution ]")
        
        await self.chapter_1_the_problem()
        await self.chapter_2_real_stories()
        await self.chapter_3_the_solution()
        await self.chapter_4_how_it_works()
        await self.chapter_5_the_proof()
        await self.chapter_6_your_journey()
        
    async def chapter_1_the_problem(self):
        """Chapter 1: The Problem with Black Box AI"""
        clear_screen()
        print_chapter(1, "The Black Box Problem")
        
        stories = [
            {
                "title": "🏦 THE LOAN REJECTION",
                "story": "Sarah, a small business owner with perfect credit,\nwas rejected for a loan by an AI system.\nNo explanation. No recourse. Just 'DENIED'.",
                "impact": "She lost her dream of expanding her bakery."
            },
            {
                "title": "🏥 THE MISDIAGNOSIS",
                "story": "Dr. Chen's AI diagnostic tool flagged a patient\nfor immediate surgery. But why?\nThe AI couldn't explain its reasoning.",
                "impact": "Hours of uncertainty and stress for everyone."
            },
            {
                "title": "🚗 THE INSURANCE NIGHTMARE",
                "story": "Marcus's insurance claim was auto-rejected.\nThe AI said 'fraud risk' but couldn't say why.\nHe had a perfect driving record.",
                "impact": "Stuck without a car for weeks."
            }
        ]
        
        for story in stories:
            print(f"\n{story['title']}")
            print("─" * 50)
            type_text(story['story'], delay=0.02)
            print(f"\n💔 {story['impact']}")
            wait_for_user()
            
        print("\n\n" + "="*60)
        type_text("THIS IS THE WORLD WITHOUT EXPLAINABLE AI", delay=0.05)
        print("="*60)
        
        wait_for_user("\n[ Press Enter to see how we're changing this ]")
        
    async def chapter_2_real_stories(self):
        """Chapter 2: Success Stories with Ziggurat"""
        clear_screen()
        print_chapter(2, "Real Success Stories")
        
        type_text("Now imagine a different world...\n")
        await asyncio.sleep(1)
        
        success_stories = [
            {
                "title": "🏦 SARAH'S LOAN APPROVED",
                "before": "AI: Application DENIED",
                "after": "AI: Application APPROVED because:",
                "explanation": [
                    "✅ Credit score (720) → +35% positive impact",
                    "✅ Business revenue trend → +28% positive impact", 
                    "✅ Years in business (7) → +22% positive impact",
                    "⚠️ Industry volatility → -15% negative impact",
                    "Overall confidence: 89%"
                ],
                "outcome": "💚 Sarah opened her second bakery location!"
            },
            {
                "title": "🏥 DR. CHEN'S CONFIDENCE",
                "before": "AI: High risk detected",
                "after": "AI: High risk detected because:",
                "explanation": [
                    "🔴 Glucose level (126) → Diabetes indicator",
                    "🔴 Family history → Genetic predisposition",
                    "🟡 Weight trend → Increasing risk",
                    "🟢 Age (45) → Early intervention possible",
                    "Recommendation: Immediate screening, not surgery"
                ],
                "outcome": "💚 Patient diagnosed early, avoided complications!"
            },
            {
                "title": "🚗 MARCUS'S CLAIM PROCESSED",
                "before": "AI: Claim rejected - Fraud risk",
                "after": "AI: Initial flag resolved:",
                "explanation": [
                    "⚠️ Unusual location → System flagged",
                    "✅ GPS data verified → Legitimate travel",
                    "✅ Clean history → No fraud patterns",
                    "✅ Photos authentic → Damage confirmed",
                    "Claim approved in 10 minutes"
                ],
                "outcome": "💚 Marcus got his car fixed the next day!"
            }
        ]
        
        for story in success_stories:
            print(f"\n{'='*60}")
            print(f"{story['title'].center(60)}")
            print(f"{'='*60}\n")
            
            print("❌ BEFORE (Black Box AI):")
            print(f"   {story['before']}\n")
            
            await asyncio.sleep(1)
            
            print("✅ AFTER (Ziggurat Intelligence):")
            print(f"   {story['after']}")
            for line in story['explanation']:
                await asyncio.sleep(0.5)
                print(f"   {line}")
                
            print(f"\n{story['outcome']}")
            wait_for_user()
            
        print("\n\n" + "🌟"*30)
        type_text("EVERY DECISION. EXPLAINED. VERIFIED. TRUSTED.", delay=0.05)
        print("🌟"*30)
        
        wait_for_user("\n[ Press Enter to learn how it works ]")
        
    async def chapter_3_the_solution(self):
        """Chapter 3: Introducing Ziggurat Intelligence"""
        clear_screen()
        print_chapter(3, "The Ziggurat Solution")
        
        print_big_title("🏛️  ZIGGURAT INTELLIGENCE", "Making AI Transparent")
        
        type_text("Built on ancient principles of transparency and trust...\n")
        await asyncio.sleep(1)
        
        print("\n🎯 OUR MISSION:")
        print("─" * 40)
        principles = [
            "1️⃣  Every AI decision must be explainable",
            "2️⃣  Every explanation must be verifiable", 
            "3️⃣  Every verification must be permanent",
            "4️⃣  Every user deserves transparency"
        ]
        
        for principle in principles:
            await asyncio.sleep(0.7)
            print(f"\n   {principle}")
            
        wait_for_user("\n[ Press Enter to see the technology ]")
        
        # Technology showcase
        clear_screen()
        print("\n🧠 THE TECHNOLOGY BEHIND THE MAGIC\n")
        
        methods = [
            {
                "name": "SHAP",
                "title": "SHapley Additive exPlanations",
                "description": "Like a financial audit for AI decisions",
                "use_case": "Perfect for: Loans, Insurance, Risk Assessment"
            },
            {
                "name": "LIME", 
                "title": "Local Interpretable Model-agnostic Explanations",
                "description": "Like a magnifying glass for specific decisions",
                "use_case": "Perfect for: Medical diagnosis, Fraud detection"
            },
            {
                "name": "GRADIENT",
                "title": "Neural Network Analysis",
                "description": "Like an X-ray for deep learning models",
                "use_case": "Perfect for: Image analysis, Complex patterns"
            }
        ]
        
        for method in methods:
            print(f"\n{'─'*60}")
            print(f"📊 {method['name']} - {method['title']}")
            print(f"   {method['description']}")
            print(f"   {method['use_case']}")
            await asyncio.sleep(1)
            
        wait_for_user("\n[ Press Enter to see it in action ]")
        
    async def chapter_4_how_it_works(self):
        """Chapter 4: Live Demonstration"""
        clear_screen()
        print_chapter(4, "See It In Action")
        
        print("🏦 LIVE DEMO: Loan Application Analysis\n")
        
        # Sample application
        applicant = {
            "name": "Jennifer Chen",
            "credit_score": 695,
            "income": 92000,
            "debt_ratio": 0.31,
            "employment_years": 5,
            "loan_amount": 280000
        }
        
        print("📋 APPLICATION DETAILS:")
        print("─" * 40)
        for key, value in applicant.items():
            if key != "name":
                print(f"   {key.replace('_', ' ').title()}: {value:,}" if isinstance(value, int) else f"   {key.replace('_', ' ').title()}: {value}")
        
        wait_for_user("\n[ Press Enter to analyze ]")
        
        # Processing animation
        print("\n🔍 ANALYZING WITH ZIGGURAT INTELLIGENCE...")
        for i in range(3):
            for j in range(4):
                print(f"\r   {'▓' * (j+1)}{'░' * (3-j)} Processing{'. ' * j}  ", end='', flush=True)
                await asyncio.sleep(0.3)
        print("\r   ▓▓▓▓ Complete! ✅                    ")
        
        # Results
        print("\n\n📊 DECISION: APPROVED WITH CONDITIONS")
        print("="*50)
        print("\n🎯 Confidence Score: 76%\n")
        
        print("✅ POSITIVE FACTORS:")
        positive = [
            ("Income stability", "+32%", "Strong income relative to loan"),
            ("Employment history", "+24%", "5 years shows stability"),
            ("Credit improving", "+18%", "Upward trend last 12 months")
        ]
        
        for factor, impact, reason in positive:
            await asyncio.sleep(0.5)
            print(f"   • {factor}: {impact}")
            print(f"     → {reason}")
            
        print("\n⚠️ RISK FACTORS:")
        negative = [
            ("Credit score", "-15%", "Below 700 threshold"),
            ("Debt ratio", "-9%", "Slightly above ideal 30%")
        ]
        
        for factor, impact, reason in negative:
            await asyncio.sleep(0.5)
            print(f"   • {factor}: {impact}")
            print(f"     → {reason}")
            
        print("\n💡 RECOMMENDATION:")
        print("   Approve with 5.2% interest rate (0.3% above base)")
        print("   Condition: 25% down payment instead of 20%")
        
        wait_for_user("\n[ Press Enter to verify on blockchain ]")
        
    async def chapter_5_the_proof(self):
        """Chapter 5: Blockchain Verification"""
        clear_screen()
        print_chapter(5, "Permanent Proof")
        
        print("🔐 BLOCKCHAIN VERIFICATION PROCESS\n")
        
        steps = [
            ("Creating cryptographic proof", "🔑"),
            ("Submitting to Internet Computer Protocol", "🌐"),
            ("Recording on immutable ledger", "📜"),
            ("Generating verification hash", "🔗")
        ]
        
        for step, icon in steps:
            print(f"\n{icon} {step}...")
            for i in range(20):
                print("▓", end='', flush=True)
                await asyncio.sleep(0.05)
            print(" ✅")
            
        print("\n\n" + "="*60)
        print("🎉 VERIFICATION COMPLETE")
        print("="*60)
        
        print(f"""
📋 PROOF CERTIFICATE:
   Chain: Internet Computer Protocol (ICP)
   Hash: 0xf4ca9a7b3d2e8c1f...9e2a
   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
   Cost: 0.0001 ICP (~$0.001)
   
✅ This decision is now:
   • Permanently recorded
   • Publicly verifiable
   • Legally admissible
   • Tamper-proof
""")
        
        wait_for_user("\n[ Press Enter to see pricing ]")
        
    async def chapter_6_your_journey(self):
        """Chapter 6: Your Journey Begins"""
        clear_screen()
        print_chapter(6, "Your Journey Begins")
        
        print_big_title("🚀 READY TO TRANSFORM YOUR AI?")
        
        # Pricing tiers with visual representation
        print("\n💎 CHOOSE YOUR PATH:\n")
        
        tiers = [
            {
                "name": "COMMUNITY",
                "price": "FREE",
                "color": "🟢",
                "features": [
                    "100 explanations/hour",
                    "SHAP analysis",
                    "Basic models",
                    "Community support"
                ],
                "perfect_for": "Developers & Startups"
            },
            {
                "name": "PROFESSIONAL", 
                "price": "$199-999/mo",
                "color": "🔵",
                "features": [
                    "10,000 explanations/hour",
                    "All methods (SHAP, LIME, Gradient)",
                    "15+ AI models",
                    "Priority support",
                    "Custom training"
                ],
                "perfect_for": "Growing Businesses"
            },
            {
                "name": "ENTERPRISE",
                "price": "$2000+/mo",
                "color": "🟣",
                "features": [
                    "Unlimited explanations",
                    "Custom models",
                    "Dedicated infrastructure",
                    "99.9% SLA",
                    "24/7 phone support"
                ],
                "perfect_for": "Large Organizations"
            }
        ]
        
        for tier in tiers:
            print(f"\n{tier['color']} {tier['name']} - {tier['price']}")
            print("─" * 40)
            for feature in tier['features']:
                print(f"   ✓ {feature}")
            print(f"\n   Perfect for: {tier['perfect_for']}")
            await asyncio.sleep(1)
            
        print("\n\n" + "🌟"*30)
        print("\n📈 JOIN 10,000+ COMPANIES ALREADY USING ZIGGURAT\n")
        print("🌟"*30)
        
        wait_for_user("\n[ Press Enter for next steps ]")
        
        # Call to action
        clear_screen()
        print_big_title("🎯 YOUR NEXT STEPS")
        
        print("""
1️⃣  START FREE TODAY
    → Visit: ziggurat.ai/signup
    → Get API key instantly
    → 100 free explanations to start

2️⃣  TRY OUR DEMOS
    → Python SDK: pip install ziggurat-intelligence
    → Run: python -m ziggurat.demo
    → See real explanations in seconds

3️⃣  JOIN THE COMMUNITY
    → Discord: discord.gg/ziggurat
    → GitHub: github.com/ziggurat-ai
    → Twitter: @ZigguratAI

4️⃣  TALK TO AN EXPERT
    → Book a demo: ziggurat.ai/demo
    → Email: hello@ziggurat.ai
    → Phone: 1-800-ZIGGURAT
""")
        
        print("\n" + "="*60)
        type_text("MAKE EVERY AI DECISION EXPLAINABLE", delay=0.05)
        type_text("MAKE EVERY USER TRUST YOUR AI", delay=0.05)
        type_text("MAKE THE FUTURE TRANSPARENT", delay=0.05)
        print("="*60)
        
        print("\n\n🏛️  ZIGGURAT INTELLIGENCE")
        print("    Ancient Architecture, Infinite Intelligence\n")
        
        wait_for_user("\n[ Press Enter to restart journey ]")


# Main entry point
async def main():
    """Run the Ziggurat story"""
    while True:
        demo = ZigguratStoryDemo()
        await demo.start_journey()
        
        print("\n\nWould you like to experience the journey again?")
        choice = input("Enter 'yes' to restart or any other key to exit: ").lower()
        if choice != 'yes':
            print("\n✨ Thank you for exploring Ziggurat Intelligence!")
            print("🏛️  Ancient Architecture, Infinite Intelligence\n")
            break
        clear_screen()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n✨ Thank you for your time!")
        print("🏛️  Visit us at ziggurat.ai\n")