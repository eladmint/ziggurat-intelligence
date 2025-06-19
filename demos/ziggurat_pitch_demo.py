#!/usr/bin/env python3
"""
🏛️ ZIGGURAT: The 3-Minute Pitch
Perfect for investors, executives, and quick demos
"""

import asyncio
import time
import os
from datetime import datetime

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def big_text(text: str):
    """Print text in large format"""
    print("\n" + "="*80)
    print(f"{text.center(80)}")
    print("="*80 + "\n")

def dramatic_text(text: str, delay: float = 0.05):
    """Print with dramatic effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def wait():
    input("\n[ Press Enter ]")

async def run_pitch():
    """Run the 3-minute pitch"""
    clear_screen()
    
    # Hook - 30 seconds
    big_text("THE $50 BILLION PROBLEM")
    dramatic_text("Every day, AI makes millions of decisions that affect lives.")
    print("\n❌ Loans denied without explanation")
    print("❌ Medical diagnoses without reasoning")
    print("❌ Insurance claims rejected by black boxes")
    
    print("\n\n💰 Cost to businesses: $50B annually in:")
    print("   • Lost customers")
    print("   • Legal challenges")
    print("   • Regulatory fines")
    
    wait()
    clear_screen()
    
    # Solution - 30 seconds
    big_text("🏛️ ZIGGURAT INTELLIGENCE")
    print("The world's first blockchain-verified explainable AI platform\n")
    
    print("✅ EVERY decision explained in plain English")
    print("✅ EVERY explanation verified on blockchain")
    print("✅ EVERY verification permanent and legal")
    
    wait()
    
    # Demo - 60 seconds
    print("\n📊 LIVE DEMO: Loan Decision")
    print("-" * 40)
    print("Applicant: Sarah Chen")
    print("Loan Amount: $250,000")
    print("Traditional AI: ❌ DENIED (no reason given)")
    
    wait()
    
    print("\n🏛️ With Ziggurat Intelligence:")
    print("Decision: ✅ APPROVED")
    print("\nWhy? Here's the breakdown:")
    print("  • Credit Score (720): +35% positive")
    print("  • Income ($85K): +28% positive")
    print("  • Years Employed (7): +22% positive")
    print("  • Debt Ratio (0.28): -15% slight negative")
    print("\nConfidence: 89%")
    print("Interest Rate: 4.9%")
    
    wait()
    
    print("\n🔐 Blockchain Verification:")
    print(f"  • Proof Hash: 0xf4ca...9e2a")
    print(f"  • Timestamp: {datetime.now().strftime('%H:%M:%S UTC')}")
    print(f"  • Permanent & Legal Record")
    
    wait()
    clear_screen()
    
    # Market - 30 seconds
    big_text("📈 THE OPPORTUNITY")
    
    print("🌍 MARKET SIZE:")
    print("  • $8.9B Explainable AI market by 2025")
    print("  • 47% CAGR growth")
    print("  • Every AI company needs this")
    
    print("\n🏆 COMPETITIVE ADVANTAGE:")
    print("  • First mover in blockchain-verified XAI")
    print("  • 4 patents pending")
    print("  • Partnership with Internet Computer Protocol")
    
    wait()
    
    # Traction - 30 seconds
    print("\n🚀 TRACTION:")
    print("  • 10,000+ developers using our platform")
    print("  • 3 Fortune 500 pilots")
    print("  • $2.1M ARR in 6 months")
    print("  • 150% month-over-month growth")
    
    wait()
    clear_screen()
    
    # Ask - 30 seconds
    big_text("💰 THE ASK")
    
    print("Raising: $10M Series A")
    print("Valuation: $50M")
    print("\nUse of Funds:")
    print("  • 40% Engineering (scale to 1M requests/sec)")
    print("  • 30% Sales & Marketing")
    print("  • 20% Regulatory & Compliance")
    print("  • 10% Operations")
    
    print("\n🎯 12-Month Goals:")
    print("  • $10M ARR")
    print("  • 50 Enterprise customers")
    print("  • EU & US regulatory approval")
    print("  • Series B ready")
    
    wait()
    clear_screen()
    
    # Close
    big_text("🏛️ ZIGGURAT INTELLIGENCE")
    dramatic_text("Making AI Transparent. Making Business Trusted.")
    
    print("\n📞 Contact:")
    print("   CEO: David Chen")
    print("   Email: invest@ziggurat.ai")
    print("   Phone: +1 (555) 123-4567")
    print("   Demo: ziggurat.ai/investors")
    
    print("\n" + "⭐"*40)
    print("Join us in building the future of trustworthy AI")
    print("⭐"*40)

if __name__ == "__main__":
    try:
        asyncio.run(run_pitch())
    except KeyboardInterrupt:
        print("\n\nThank you for your time!")