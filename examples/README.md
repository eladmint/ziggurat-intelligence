# 🎯 Ziggurat Intelligence - Integration Examples

**Working demonstrations of ICP x OpenXAI x Masumi x TON integrations**

---

## 🚀 Hackathon Integration Examples

### 🤖 **Masumi Network Integration**

#### `masumi_ziggurat_integration_demo.py`
- **Purpose**: Complete Masumi-Ziggurat bridge demonstration
- **Features**:
  - Task discovery on Masumi marketplace
  - Explainable AI task processing
  - Quality-based reward calculations
  - Cross-chain verification
- **Run**: `python examples/masumi_ziggurat_integration_demo.py`

#### `run_masumi_ziggurat_demo.py`
- **Purpose**: Main demo launcher with multiple interfaces
- **Features**:
  - Web-based interactive demo
  - Command-line visual demo
  - Technical and teen-friendly versions
  - Complete workflow simulation
- **Run**: `python examples/run_masumi_ziggurat_demo.py`

### 💰 **TON Payment Integration**

#### `ton_payment_integration_demo.py`
- **Purpose**: TON payment system demonstration
- **Features**:
  - Telegram native payments
  - Multi-tier subscription processing
  - Real-time payment verification
  - Subscription management
- **Run**: `python examples/ton_payment_integration_demo.py`

---

## 🎭 Demo Scenarios

### 1. **Masumi Agent Workflow**
```python
# Example workflow from masumi_ziggurat_integration_demo.py

# 1. Agent discovers explainable AI task
task = await bridge.discover_tasks({"domain": "financial", "complexity": "medium"})

# 2. Process task with explainable AI
explanation = await ziggurat.generate_explanation(
    data=task.data,
    method="shap",
    model="financial_risk_assessment"
)

# 3. Submit explanation for verification
result = await bridge.submit_explanation(task.id, explanation)

# 4. Receive quality-based rewards
reward = calculate_reward(explanation.quality_score, task.complexity)
```

### 2. **TON Payment Flow**
```python
# Example from ton_payment_integration_demo.py

# 1. User initiates premium subscription
subscription_request = {
    "user_id": "telegram_user_123",
    "tier": "intelligence_premium",
    "payment_method": "ton"
}

# 2. Generate payment invoice
invoice = await payment_service.create_ton_invoice(
    amount=0.5,  # 0.5 TON
    description="Intelligence Premium - Monthly"
)

# 3. Process payment verification
payment_result = await payment_service.verify_ton_payment(invoice.id)

# 4. Activate premium features
await subscription_service.activate_premium(user_id, "intelligence_premium")
```

### 3. **Multi-Chain Integration**
```python
# Combined ICP + TON + Masumi workflow

# 1. Masumi task discovery
tasks = await masumi_bridge.discover_tasks()

# 2. Generate explanations (processed via ICP-OpenXAI)
explanations = await ziggurat_engine.batch_explain(tasks)

# 3. Store explanations on ICP blockchain
verification_hashes = await icp_client.store_explanations(explanations)

# 4. Process payments (TON for users, rewards via Masumi)
for explanation in explanations:
    if explanation.quality_score > 0.8:
        await masumi_bridge.distribute_rewards(explanation.agent_id)
```

---

## 🎮 Interactive Demos

### **Web-Based Demos**
The `run_masumi_ziggurat_demo.py` includes interactive web demos:

#### 🧑‍💼 **Technical Version**
- **Audience**: Developers, professionals, technical evaluators
- **Features**: Detailed technical explanations, performance metrics
- **UI**: Professional interface with advanced controls

#### 🎓 **Teen-Friendly Version**  
- **Audience**: Beginners, students, general public
- **Features**: Simple explanations, relatable examples
- **UI**: Colorful, engaging interface with clear benefits

### **Command-Line Demos**
- **Visual Demo**: Animated progress bars and status updates
- **Interactive Demo**: User input for different scenarios
- **Batch Demo**: Multiple task processing demonstration

---

## 🔧 Running the Examples

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (if needed)
export MASUMI_API_KEY="your-api-key"
export ICP_PRINCIPAL="your-principal-id"
export TON_API_TOKEN="your-ton-token"
```

### Quick Start
```bash
# Run main demo launcher
python examples/run_masumi_ziggurat_demo.py

# Run specific integration demos
python examples/masumi_ziggurat_integration_demo.py
python examples/ton_payment_integration_demo.py

# Run with specific scenarios
python examples/masumi_ziggurat_integration_demo.py --scenario financial
python examples/ton_payment_integration_demo.py --tier premium
```

### Demo Options
```bash
# Masumi integration options
python examples/masumi_ziggurat_integration_demo.py --help
  --scenario: financial, healthcare, research, defi
  --complexity: low, medium, high
  --method: shap, lime, gradient, attention
  --interactive: Enable interactive mode

# TON payment options  
python examples/ton_payment_integration_demo.py --help
  --tier: basic, intelligence, enterprise
  --amount: Custom payment amount
  --simulate: Run in simulation mode
```

---

## 📊 Example Output

### Masumi Integration Demo Output
```
🤖 MASUMI-ZIGGURAT INTEGRATION DEMO
===================================

🔍 Discovering Tasks on Masumi Network...
✅ Found 3 explainable AI tasks:
   • Financial Risk Assessment (Medium complexity)
   • Healthcare Diagnosis Explanation (High complexity)  
   • Research Paper Analysis (Low complexity)

🧠 Processing Financial Risk Assessment...
   Method: SHAP
   Confidence: 87%
   Quality Score: 0.91
   
⛓️ Storing explanation on ICP blockchain...
   Verification Hash: 0xf4ca...9e2a
   Block Height: 12,345
   
💰 Calculating Rewards...
   Base Reward: 10 MASUMI
   Quality Multiplier: 1.8x (Gold tier)
   Final Reward: 18 MASUMI tokens
   
✅ Task completed successfully!
```

### TON Payment Demo Output
```
💰 TON PAYMENT INTEGRATION DEMO
================================

🎯 Creating Intelligence Premium subscription...
   Tier: Intelligence Premium (0.5 ICP/month)
   Payment Method: TON
   
📱 Generating Telegram payment invoice...
   Amount: 5 TON (~$25)
   Invoice ID: ton_inv_abc123
   Payment URL: https://t.me/invoice/abc123
   
⏳ Waiting for payment confirmation...
✅ Payment confirmed!
   Transaction Hash: 0xa1b2c3d4...
   Block: 8,765,432
   
🚀 Activating premium features...
   • AI-powered explanations: ✅ Enabled
   • Blockchain verification: ✅ Enabled  
   • Priority support: ✅ Enabled
   
✨ Intelligence Premium activated successfully!
```

---

## 🏆 Hackathon Achievement Showcase

These examples demonstrate our complete hackathon achievement:

### ✅ **ICP Integration**
- Direct canister communication
- Chain Fusion cross-chain capabilities
- Cryptographic verification
- Persistent storage (500GiB per canister)

### ✅ **OpenXAI Integration**  
- Decentralized AI inference
- Real-time explanation generation
- Multiple XAI methods (SHAP, LIME, etc.)
- Openmesh compatibility

### ✅ **Masumi Network Integration**
- Task marketplace integration
- Quality-based rewards
- Autonomous agent operation
- Cross-platform synchronization

### ✅ **TON Payment Integration**
- Telegram native payments
- Multi-tier subscriptions
- Instant payment processing
- User-friendly crypto payments

---

## 🎯 Try It Yourself

1. **Clone the repository**
   ```bash
   git clone https://github.com/eladmint/ziggurat-intelligence.git
   cd ziggurat-intelligence
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the main demo**
   ```bash
   python examples/run_masumi_ziggurat_demo.py
   ```

4. **Explore specific integrations**
   ```bash
   python examples/masumi_ziggurat_integration_demo.py
   python examples/ton_payment_integration_demo.py
   ```

---

**🏛️ These examples prove that we've built the world's first true decentralized explainable AI platform - and it works!**