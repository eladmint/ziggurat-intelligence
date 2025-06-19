"""
Unified Payment Service for AI Services

Integrates multiple blockchain payment systems (ICP, TON, Cardano) with
Masumi rewards and Ziggurat AI service billing.
"""

import asyncio
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal

from ..billing.models import SubscriptionTier, PaymentMethod
from ..billing.services.transaction_processing_service import TransactionProcessingService
from ..blockchain.masumi_integration import MasumiTaskReward


class PaymentType(Enum):
    """Types of payments in the unified system."""
    AI_SERVICE = "ai_service"          # Ziggurat AI usage
    TASK_REWARD = "task_reward"        # Masumi task completion
    SUBSCRIPTION = "subscription"       # Premium tier subscription
    CROSS_CHAIN = "cross_chain"        # Cross-chain transfer
    EXPLANATION_FEE = "explanation_fee" # Fee for AI explanations


@dataclass
class UnifiedPayment:
    """Unified payment record across all platforms."""
    payment_id: str
    payment_type: PaymentType
    amount: Decimal
    currency: str
    source_platform: str
    destination_platform: str
    sender_id: str
    recipient_id: str
    blockchain_network: str
    transaction_hash: Optional[str]
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "payment_id": self.payment_id,
            "payment_type": self.payment_type.value,
            "amount": str(self.amount),
            "currency": self.currency,
            "source_platform": self.source_platform,
            "destination_platform": self.destination_platform,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "blockchain_network": self.blockchain_network,
            "transaction_hash": self.transaction_hash,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "metadata": self.metadata
        }


class UnifiedPaymentService:
    """
    Unified payment service coordinating payments across:
    - Masumi Network (task rewards)
    - Ziggurat Intelligence (AI service fees)
    - Multi-chain billing (TON, ICP, Cardano)
    - Cross-platform settlements
    """
    
    def __init__(
        self,
        transaction_service: TransactionProcessingService,
        enable_cross_chain: bool = True,
        settlement_interval_hours: int = 24
    ):
        """
        Initialize unified payment service.
        
        Args:
            transaction_service: Multi-chain transaction processor
            enable_cross_chain: Enable cross-chain transfers
            settlement_interval_hours: Batch settlement interval
        """
        self.transaction_service = transaction_service
        self.enable_cross_chain = enable_cross_chain
        self.settlement_interval = timedelta(hours=settlement_interval_hours)
        
        # Payment tracking
        self._payments: Dict[str, UnifiedPayment] = {}
        self._pending_settlements: List[UnifiedPayment] = []
        self._exchange_rates: Dict[str, Dict[str, float]] = {
            "MASUMI": {"USD": 0.10, "ICP": 0.02, "TON": 0.05, "ADA": 0.25},
            "ICP": {"USD": 5.0, "MASUMI": 50.0, "TON": 2.5, "ADA": 12.5},
            "TON": {"USD": 2.0, "MASUMI": 20.0, "ICP": 0.4, "ADA": 5.0},
            "ADA": {"USD": 0.40, "MASUMI": 4.0, "ICP": 0.08, "TON": 0.2}
        }
        
        # Settlement configuration
        self._settlement_task: Optional[asyncio.Task] = None
        self._last_settlement: Optional[datetime] = None
        
    async def start(self):
        """Start the payment service with auto-settlement."""
        if not self._settlement_task:
            self._settlement_task = asyncio.create_task(self._auto_settlement_loop())
            
    async def stop(self):
        """Stop the payment service."""
        if self._settlement_task:
            self._settlement_task.cancel()
            try:
                await self._settlement_task
            except asyncio.CancelledError:
                pass
            self._settlement_task = None
            
    async def process_ai_service_payment(
        self,
        user_id: str,
        service_type: str,
        cycles_used: int,
        payment_method: PaymentMethod,
        explanation_id: Optional[str] = None
    ) -> UnifiedPayment:
        """
        Process payment for AI service usage (Ziggurat).
        
        Args:
            user_id: User requesting service
            service_type: Type of AI service
            cycles_used: Computational cycles consumed
            payment_method: Payment method to use
            explanation_id: Optional explanation ID
            
        Returns:
            UnifiedPayment record
        """
        # Calculate cost based on cycles
        cost_per_million_cycles = {
            PaymentMethod.ICP: Decimal("0.1"),    # 0.1 ICP per 1M cycles
            PaymentMethod.TON: Decimal("0.25"),   # 0.25 TON per 1M cycles
            PaymentMethod.CARDANO: Decimal("1.25") # 1.25 ADA per 1M cycles
        }
        
        currency = payment_method.value.upper()
        rate = cost_per_million_cycles.get(payment_method, Decimal("1.0"))
        amount = (Decimal(cycles_used) / Decimal(1_000_000)) * rate
        
        # Create payment record
        payment = UnifiedPayment(
            payment_id=self._generate_payment_id("ai", user_id),
            payment_type=PaymentType.AI_SERVICE,
            amount=amount,
            currency=currency,
            source_platform="user_wallet",
            destination_platform="ziggurat",
            sender_id=user_id,
            recipient_id="ziggurat_treasury",
            blockchain_network=currency.lower(),
            transaction_hash=None,
            status="pending",
            created_at=datetime.utcnow(),
            completed_at=None,
            metadata={
                "service_type": service_type,
                "cycles_used": cycles_used,
                "explanation_id": explanation_id
            }
        )
        
        # Process through transaction service
        result = await self.transaction_service.process_payment(
            user_id=user_id,
            amount=amount,
            payment_method=payment_method,
            description=f"AI Service: {service_type}"
        )
        
        if result["success"]:
            payment.transaction_hash = result["transaction_id"]
            payment.status = "completed"
            payment.completed_at = datetime.utcnow()
        else:
            payment.status = "failed"
            
        self._payments[payment.payment_id] = payment
        return payment
        
    async def distribute_task_reward(
        self,
        task_reward: MasumiTaskReward,
        recipient_wallet: Dict[str, str]
    ) -> UnifiedPayment:
        """
        Distribute Masumi task reward to agent.
        
        Args:
            task_reward: Masumi reward details
            recipient_wallet: Wallet addresses by currency
            
        Returns:
            UnifiedPayment record
        """
        # Create payment record
        payment = UnifiedPayment(
            payment_id=self._generate_payment_id("reward", task_reward.agent_id),
            payment_type=PaymentType.TASK_REWARD,
            amount=Decimal(str(task_reward.reward_amount)),
            currency=task_reward.reward_token,
            source_platform="masumi",
            destination_platform="agent_wallet",
            sender_id="masumi_treasury",
            recipient_id=task_reward.agent_id,
            blockchain_network=self._get_blockchain_for_token(task_reward.reward_token),
            transaction_hash=task_reward.transaction_hash,
            status="completed" if task_reward.transaction_hash else "pending",
            created_at=datetime.utcnow(),
            completed_at=datetime.utcnow() if task_reward.transaction_hash else None,
            metadata={
                "task_id": task_reward.task_id,
                "quality_score": task_reward.quality_score,
                "completion_time": task_reward.completion_time.isoformat()
            }
        )
        
        self._payments[payment.payment_id] = payment
        
        # Add to settlement queue if cross-chain needed
        if self.enable_cross_chain and payment.status == "pending":
            self._pending_settlements.append(payment)
            
        return payment
        
    async def process_cross_chain_transfer(
        self,
        from_currency: str,
        to_currency: str,
        amount: Decimal,
        user_id: str,
        reason: str = "currency_conversion"
    ) -> Tuple[UnifiedPayment, UnifiedPayment]:
        """
        Process cross-chain currency transfer.
        
        Args:
            from_currency: Source currency
            to_currency: Destination currency
            amount: Amount to transfer
            user_id: User ID
            reason: Transfer reason
            
        Returns:
            Tuple of (source_payment, destination_payment)
        """
        # Calculate exchange
        exchange_rate = self._get_exchange_rate(from_currency, to_currency)
        converted_amount = amount * Decimal(str(exchange_rate))
        
        # Create source payment (debit)
        source_payment = UnifiedPayment(
            payment_id=self._generate_payment_id("cross_out", user_id),
            payment_type=PaymentType.CROSS_CHAIN,
            amount=amount,
            currency=from_currency,
            source_platform=f"{from_currency.lower()}_wallet",
            destination_platform="cross_chain_bridge",
            sender_id=user_id,
            recipient_id="bridge_escrow",
            blockchain_network=self._get_blockchain_for_token(from_currency),
            transaction_hash=None,
            status="pending",
            created_at=datetime.utcnow(),
            completed_at=None,
            metadata={
                "reason": reason,
                "exchange_rate": float(exchange_rate),
                "destination_currency": to_currency
            }
        )
        
        # Create destination payment (credit)
        dest_payment = UnifiedPayment(
            payment_id=self._generate_payment_id("cross_in", user_id),
            payment_type=PaymentType.CROSS_CHAIN,
            amount=converted_amount,
            currency=to_currency,
            source_platform="cross_chain_bridge",
            destination_platform=f"{to_currency.lower()}_wallet",
            sender_id="bridge_escrow",
            recipient_id=user_id,
            blockchain_network=self._get_blockchain_for_token(to_currency),
            transaction_hash=None,
            status="pending",
            created_at=datetime.utcnow(),
            completed_at=None,
            metadata={
                "reason": reason,
                "source_currency": from_currency,
                "source_amount": str(amount),
                "exchange_rate": float(exchange_rate)
            }
        )
        
        # Add to payments
        self._payments[source_payment.payment_id] = source_payment
        self._payments[dest_payment.payment_id] = dest_payment
        
        # Queue for settlement
        self._pending_settlements.extend([source_payment, dest_payment])
        
        return source_payment, dest_payment
        
    async def get_payment_history(
        self,
        user_id: str,
        payment_type: Optional[PaymentType] = None,
        limit: int = 100
    ) -> List[UnifiedPayment]:
        """
        Get payment history for a user.
        
        Args:
            user_id: User ID
            payment_type: Optional filter by type
            limit: Maximum records
            
        Returns:
            List of payments
        """
        user_payments = [
            p for p in self._payments.values()
            if p.sender_id == user_id or p.recipient_id == user_id
        ]
        
        if payment_type:
            user_payments = [
                p for p in user_payments
                if p.payment_type == payment_type
            ]
            
        # Sort by date descending
        user_payments.sort(key=lambda p: p.created_at, reverse=True)
        
        return user_payments[:limit]
        
    async def get_balance_summary(self, user_id: str) -> Dict[str, Decimal]:
        """
        Get balance summary across all currencies.
        
        Args:
            user_id: User ID
            
        Returns:
            Balance by currency
        """
        balances = {
            "MASUMI": Decimal("0"),
            "ICP": Decimal("0"),
            "TON": Decimal("0"),
            "ADA": Decimal("0")
        }
        
        for payment in self._payments.values():
            # Credits
            if payment.recipient_id == user_id and payment.status == "completed":
                if payment.currency in balances:
                    balances[payment.currency] += payment.amount
                    
            # Debits
            if payment.sender_id == user_id and payment.status == "completed":
                if payment.currency in balances:
                    balances[payment.currency] -= payment.amount
                    
        return balances
        
    async def estimate_service_cost(
        self,
        service_type: str,
        estimated_cycles: int,
        preferred_currency: str = "ICP"
    ) -> Dict[str, Any]:
        """
        Estimate cost for an AI service.
        
        Args:
            service_type: Type of service
            estimated_cycles: Estimated cycles needed
            preferred_currency: Preferred payment currency
            
        Returns:
            Cost estimation details
        """
        # Base costs per million cycles
        costs_per_million = {
            "ICP": Decimal("0.1"),
            "TON": Decimal("0.25"),
            "ADA": Decimal("1.25"),
            "MASUMI": Decimal("10.0")
        }
        
        # Calculate for all currencies
        estimates = {}
        for currency, rate in costs_per_million.items():
            cost = (Decimal(estimated_cycles) / Decimal(1_000_000)) * rate
            estimates[currency] = {
                "amount": str(cost),
                "usd_equivalent": str(cost * Decimal(str(self._exchange_rates[currency]["USD"])))
            }
            
        return {
            "service_type": service_type,
            "estimated_cycles": estimated_cycles,
            "cost_estimates": estimates,
            "preferred_currency": preferred_currency,
            "preferred_cost": estimates[preferred_currency]
        }
        
    async def process_batch_settlement(self) -> Dict[str, Any]:
        """
        Process pending settlements in batch.
        
        Returns:
            Settlement summary
        """
        if not self._pending_settlements:
            return {
                "settlements_processed": 0,
                "total_amount_settled": "0",
                "status": "no_pending_settlements"
            }
            
        settlements_by_chain = {}
        for payment in self._pending_settlements:
            chain = payment.blockchain_network
            if chain not in settlements_by_chain:
                settlements_by_chain[chain] = []
            settlements_by_chain[chain].append(payment)
            
        # Process each chain's settlements
        results = {
            "settlements_processed": 0,
            "settlements_by_chain": {},
            "failed_settlements": []
        }
        
        for chain, payments in settlements_by_chain.items():
            try:
                # Batch process on chain
                success_count = 0
                total_amount = Decimal("0")
                
                for payment in payments:
                    # Simulate settlement (would call actual blockchain APIs)
                    payment.status = "completed"
                    payment.completed_at = datetime.utcnow()
                    payment.transaction_hash = f"{chain}-batch-{datetime.utcnow().timestamp()}"
                    success_count += 1
                    total_amount += payment.amount
                    
                results["settlements_by_chain"][chain] = {
                    "count": success_count,
                    "total_amount": str(total_amount)
                }
                results["settlements_processed"] += success_count
                
            except Exception as e:
                results["failed_settlements"].append({
                    "chain": chain,
                    "error": str(e),
                    "payment_count": len(payments)
                })
                
        # Clear processed settlements
        self._pending_settlements = [
            p for p in self._pending_settlements
            if p.status != "completed"
        ]
        
        self._last_settlement = datetime.utcnow()
        return results
        
    def _generate_payment_id(self, prefix: str, user_id: str) -> str:
        """Generate unique payment ID."""
        timestamp = datetime.utcnow().timestamp()
        data = f"{prefix}-{user_id}-{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
        
    def _get_blockchain_for_token(self, token: str) -> str:
        """Get blockchain network for a token."""
        token_chains = {
            "MASUMI": "cardano",
            "ICP": "icp",
            "TON": "ton",
            "ADA": "cardano",
            "NURU": "cardano"
        }
        return token_chains.get(token.upper(), "unknown")
        
    def _get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """Get exchange rate between currencies."""
        if from_currency == to_currency:
            return 1.0
            
        from_rates = self._exchange_rates.get(from_currency.upper(), {})
        return from_rates.get(to_currency.upper(), 1.0)
        
    async def _auto_settlement_loop(self):
        """Background task for automatic settlement."""
        while True:
            try:
                await asyncio.sleep(self.settlement_interval.total_seconds())
                await self.process_batch_settlement()
            except asyncio.CancelledError:
                break
            except Exception:
                # Log error but continue
                await asyncio.sleep(300)  # Retry after 5 minutes