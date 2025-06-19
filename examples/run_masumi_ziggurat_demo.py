#!/usr/bin/env python3
"""
🤝 Masumi-Ziggurat Integration Demo Launcher

This script provides multiple ways to experience the Masumi-Ziggurat integration:
1. Interactive web demo (opens in browser)
2. Command-line visual demo
3. Live simulation demo

Usage:
    python run_masumi_ziggurat_demo.py [--mode web|cli|live]
"""

import os
import sys
import webbrowser
import subprocess
from pathlib import Path

def run_web_demo():
    """Launch the web-based demo in browser"""
    print("🌐 Launching Masumi-Ziggurat Web Demo...")
    
    demo_file = Path(__file__).parent / "masumi_ziggurat_web_demo.html"
    
    if not demo_file.exists():
        print("❌ Web demo file not found!")
        return False
    
    # Open in default browser
    webbrowser.open(f"file://{demo_file.absolute()}")
    print(f"✅ Demo opened in browser: {demo_file.absolute()}")
    print("\n🎯 Demo Features:")
    print("   • Interactive task discovery and claiming")
    print("   • Real-time AI processing simulation")
    print("   • Multi-chain blockchain verification")
    print("   • Quality-based reward calculation")
    print("   • Performance analytics dashboard")
    print("\n💡 Try claiming different tasks to see varying rewards and complexity!")
    return True

def run_cli_demo():
    """Run the command-line visual demo"""
    print("🖥️  Launching Command-Line Visual Demo...")
    
    demo_file = Path(__file__).parent / "agent_forge" / "examples" / "masumi_ziggurat_visual_demo.py"
    
    if not demo_file.exists():
        print("❌ CLI demo file not found!")
        return False
    
    try:
        os.chdir(Path(__file__).parent)
        subprocess.run([sys.executable, str(demo_file)], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running CLI demo: {e}")
        return False

def run_live_demo():
    """Run the live interactive demo"""
    print("🔄 Launching Live Interactive Demo...")
    
    demo_file = Path(__file__).parent / "agent_forge" / "examples" / "masumi_ziggurat_live_demo.py"
    
    if not demo_file.exists():
        print("❌ Live demo file not found!")
        return False
    
    try:
        os.chdir(Path(__file__).parent)
        subprocess.run([sys.executable, str(demo_file), "--interactive"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running live demo: {e}")
        return False

def show_menu():
    """Show interactive menu for demo selection"""
    print("\n" + "="*60)
    print("🤝 MASUMI-ZIGGURAT INTEGRATION DEMO LAUNCHER")
    print("="*60)
    print("\nAvailable Demo Options:")
    print("\n1. 🌐 Web Demo (Recommended)")
    print("   • Full interactive browser experience")
    print("   • Visual task claiming and processing")
    print("   • Real-time blockchain verification")
    print("   • Analytics dashboard")
    
    print("\n2. 🖥️  Command-Line Demo")
    print("   • Terminal-based visual presentation")
    print("   • Animated explanations and scenarios")
    print("   • Progress bars and emoji feedback")
    
    print("\n3. 🔄 Live Interactive Demo")
    print("   • Interactive task selection")
    print("   • Real-time simulation")
    print("   • Performance metrics")
    
    print("\n4. 📊 Show All Available Demos")
    print("   • List all integration demos")
    
    print("\n0. ❌ Exit")
    print("\n" + "-"*60)
    
    while True:
        try:
            choice = input("Select demo option (0-4): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                return
            elif choice == "1":
                if run_web_demo():
                    input("\n⏸️  Press Enter when done viewing web demo...")
                break
            elif choice == "2":
                run_cli_demo()
                break
            elif choice == "3":
                run_live_demo()
                break
            elif choice == "4":
                show_all_demos()
                input("\n⏸️  Press Enter to continue...")
            else:
                print("❌ Invalid choice. Please select 0-4.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return

def show_all_demos():
    """Show all available demo files"""
    print("\n📊 Available Masumi-Ziggurat Demos:")
    print("-" * 50)
    
    demos = [
        {
            "name": "Web Demo",
            "file": "masumi_ziggurat_web_demo.html", 
            "description": "Interactive browser-based demo with full UI"
        },
        {
            "name": "Visual Demo",
            "file": "agent_forge/examples/masumi_ziggurat_visual_demo.py",
            "description": "Command-line demo with animated scenarios"
        },
        {
            "name": "Live Demo", 
            "file": "agent_forge/examples/masumi_ziggurat_live_demo.py",
            "description": "Interactive simulation with user input"
        },
        {
            "name": "Integration Demo",
            "file": "agent_forge/examples/masumi_ziggurat_integration_demo.py", 
            "description": "Basic integration workflow demonstration"
        },
        {
            "name": "Ziggurat Showcase",
            "file": "agent_forge/examples/ziggurat_showcase_demo.py",
            "description": "Ziggurat Intelligence standalone demo"
        }
    ]
    
    for i, demo in enumerate(demos, 1):
        file_path = Path(__file__).parent / demo["file"]
        status = "✅" if file_path.exists() else "❌"
        print(f"{i}. {status} {demo['name']}")
        print(f"   📁 {demo['file']}")
        print(f"   📝 {demo['description']}")
        print()

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower().replace('--mode=', '').replace('--', '')
        
        if mode == "web":
            run_web_demo()
        elif mode == "cli":
            run_cli_demo()
        elif mode == "live":
            run_live_demo()
        else:
            print(f"❌ Unknown mode: {mode}")
            print("Available modes: web, cli, live")
            sys.exit(1)
    else:
        show_menu()

if __name__ == "__main__":
    main()