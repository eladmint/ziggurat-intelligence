#!/usr/bin/env python3
"""
Explainable Treasury Monitor Agent
Demonstrates transparent AI decision-making for treasury monitoring and risk assessment
"""

import asyncio
import sys
import os
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from decimal import Decimal

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.agents.ziggurat_enhanced import ZigguratEnhancedAgent
from src.core.blockchain.ziggurat.models import ExplanationMethod


class ExplainableTreasuryMonitorAgent(ZigguratEnhancedAgent):
    """
    Treasury monitor that explains its risk assessments and alert decisions.
    
    This agent demonstrates how to build transparent financial monitoring tools that:
    - Explain risk assessment decisions
    - Justify alert levels and thresholds
    - Provide confidence scores for predictions
    - Document compliance and audit trails
    - Offer blockchain-verified monitoring proofs
    """
    
    def __init__(self):
        """Initialize the explainable treasury monitor"""
        super().__init__(
            name="ExplainableTreasuryMonitor",
            explanation_method="shap",  # SHAP for financial feature importance
            enable_explanations=True,
            enable_blockchain=True
        )
        
        # Risk thresholds and parameters
        self.risk_thresholds = {
            "critical": 0.8,
            "high": 0.6,
            "medium": 0.4,
            "low": 0.0
        }
        
        # Alert parameters
        self.alert_config = {
            "balance_drop_threshold": 0.15,  # 15% drop triggers alert
            "large_transaction_threshold": 100000,  # $100k+ transactions
            "unusual_activity_multiplier": 3.0,  # 3x normal volume
            "stale_data_hours": 6  # Alert if data older than 6 hours
        }
        
        # Compliance requirements
        self.compliance_rules = {
            "minimum_balance_usd": 50000,  # Minimum treasury balance
            "diversification_threshold": 0.6,  # Max 60% in single asset
            "audit_trail_required": True,
            "real_time_monitoring": True
        }
    
    async def run(
        self,
        treasury_data: Dict[str, Any],
        explain_assessment: bool = True
    ) -> Dict[str, Any]:
        """
        Monitor treasury and provide explainable risk assessment.
        
        Args:
            treasury_data: Current treasury state and transaction history
            explain_assessment: Whether to generate detailed explanations
            
        Returns:
            Dict containing risk assessment, alerts, and explanations
        """
        if not self.is_ready():
            raise RuntimeError("Agent is not ready")
        
        self.logger.info("💰 Starting explainable treasury monitoring")
        
        # Step 1: Calculate risk metrics
        risk_metrics = await self._calculate_risk_metrics(treasury_data)
        
        # Step 2: Assess overall risk level
        risk_assessment = await self._assess_risk_level(risk_metrics, treasury_data)
        
        # Step 3: Generate alerts based on conditions
        alerts = await self._generate_alerts(treasury_data, risk_metrics)
        
        # Step 4: Check compliance status
        compliance_status = await self._check_compliance(treasury_data, risk_metrics)
        
        # Step 5: Generate explanation if requested
        if explain_assessment:
            explanation = await self._explain_assessment(
                treasury_data=treasury_data,
                risk_metrics=risk_metrics,
                risk_assessment=risk_assessment,
                alerts=alerts,
                compliance_status=compliance_status
            )
        else:
            explanation = None
        
        # Build comprehensive result
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "treasury_summary": {
                "total_value_usd": treasury_data.get("total_value_usd", 0),
                "asset_count": len(treasury_data.get("assets", {})),
                "last_updated": treasury_data.get("last_updated")
            },
            "risk_assessment": risk_assessment,
            "risk_metrics": risk_metrics,
            "alerts": alerts,
            "compliance_status": compliance_status,
            "explanation": explanation,
            "recommendations": await self._generate_recommendations(
                risk_assessment, alerts, compliance_status
            )
        }
        
        return result
    
    async def _calculate_risk_metrics(self, treasury_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate various risk metrics"""
        assets = treasury_data.get("assets", {})
        transactions = treasury_data.get("recent_transactions", [])
        
        # 1. Concentration risk (diversification)
        total_value = sum(asset.get("value_usd", 0) for asset in assets.values())
        if total_value > 0:
            max_concentration = max(
                asset.get("value_usd", 0) / total_value 
                for asset in assets.values()
            ) if assets else 0
        else:
            max_concentration = 1.0
        
        # 2. Liquidity risk
        liquid_assets = sum(
            asset.get("value_usd", 0) 
            for asset in assets.values() 
            if asset.get("is_liquid", False)
        )
        liquidity_ratio = liquid_assets / total_value if total_value > 0 else 0
        
        # 3. Volatility risk (based on recent price changes)
        volatility_scores = []
        for asset in assets.values():
            price_changes = asset.get("price_history", [])
            if len(price_changes) >= 2:
                changes = [
                    abs(price_changes[i] - price_changes[i-1]) / price_changes[i-1]
                    for i in range(1, len(price_changes))
                ]
                avg_volatility = sum(changes) / len(changes) if changes else 0
                volatility_scores.append(avg_volatility)
        
        portfolio_volatility = sum(volatility_scores) / len(volatility_scores) if volatility_scores else 0
        
        # 4. Transaction risk (unusual patterns)
        if transactions:
            transaction_amounts = [tx.get("amount_usd", 0) for tx in transactions]
            avg_amount = sum(transaction_amounts) / len(transaction_amounts)
            large_transactions = sum(1 for amount in transaction_amounts if amount > avg_amount * 5)
            transaction_risk = large_transactions / len(transaction_amounts)
        else:
            transaction_risk = 0
        
        # 5. Staleness risk (data freshness)
        last_updated = treasury_data.get("last_updated")
        if last_updated:
            hours_old = (datetime.utcnow() - datetime.fromisoformat(last_updated)).total_seconds() / 3600
            staleness_risk = min(1.0, hours_old / 24)  # Risk increases over 24 hours
        else:
            staleness_risk = 1.0  # Maximum risk if no timestamp
        
        return {
            "concentration_risk": max_concentration,
            "liquidity_risk": 1.0 - liquidity_ratio,  # Higher when less liquid
            "volatility_risk": min(1.0, portfolio_volatility * 10),  # Scale to 0-1
            "transaction_risk": transaction_risk,
            "staleness_risk": staleness_risk
        }
    
    async def _assess_risk_level(
        self, 
        risk_metrics: Dict[str, float], 
        treasury_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess overall risk level with weighted scoring"""
        
        # Risk weights (should sum to 1.0)
        weights = {
            "concentration_risk": 0.25,
            "liquidity_risk": 0.20,
            "volatility_risk": 0.20,
            "transaction_risk": 0.15,
            "staleness_risk": 0.20
        }
        
        # Calculate weighted risk score
        overall_score = sum(
            risk_metrics.get(metric, 0) * weight
            for metric, weight in weights.items()
        )
        
        # Determine risk level
        risk_level = "low"
        for level, threshold in sorted(self.risk_thresholds.items(), key=lambda x: x[1], reverse=True):
            if overall_score >= threshold:
                risk_level = level
                break
        
        return {
            "overall_score": overall_score,
            "risk_level": risk_level,
            "weighted_components": {
                metric: risk_metrics.get(metric, 0) * weight
                for metric, weight in weights.items()
            },
            "risk_factors": [
                metric for metric, score in risk_metrics.items() 
                if score > 0.6  # High individual risk factors
            ]
        }
    
    async def _generate_alerts(
        self, 
        treasury_data: Dict[str, Any], 
        risk_metrics: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Generate alerts based on treasury conditions"""
        alerts = []
        
        # Alert 1: Low balance
        total_value = treasury_data.get("total_value_usd", 0)
        if total_value < self.compliance_rules["minimum_balance_usd"]:
            alerts.append({
                "type": "low_balance",
                "severity": "critical",
                "message": f"Treasury balance (${total_value:,.2f}) below minimum threshold",
                "threshold": self.compliance_rules["minimum_balance_usd"],
                "current_value": total_value
            })
        
        # Alert 2: High concentration
        if risk_metrics.get("concentration_risk", 0) > self.compliance_rules["diversification_threshold"]:
            alerts.append({
                "type": "concentration_risk",
                "severity": "high",
                "message": f"Asset concentration ({risk_metrics['concentration_risk']:.1%}) exceeds threshold",
                "threshold": self.compliance_rules["diversification_threshold"],
                "current_value": risk_metrics["concentration_risk"]
            })
        
        # Alert 3: Stale data
        if risk_metrics.get("staleness_risk", 0) > 0.25:  # More than 6 hours old
            alerts.append({
                "type": "stale_data",
                "severity": "medium",
                "message": "Treasury data is becoming stale",
                "last_updated": treasury_data.get("last_updated")
            })
        
        # Alert 4: High volatility
        if risk_metrics.get("volatility_risk", 0) > 0.7:
            alerts.append({
                "type": "high_volatility",
                "severity": "medium",
                "message": "Portfolio experiencing high volatility",
                "volatility_score": risk_metrics["volatility_risk"]
            })
        
        # Alert 5: Unusual transactions
        if risk_metrics.get("transaction_risk", 0) > 0.5:
            alerts.append({
                "type": "unusual_transactions",
                "severity": "high",
                "message": "Unusual transaction patterns detected",
                "risk_score": risk_metrics["transaction_risk"]
            })
        
        return alerts
    
    async def _check_compliance(
        self, 
        treasury_data: Dict[str, Any], 
        risk_metrics: Dict[str, float]
    ) -> Dict[str, Any]:
        """Check compliance with treasury management rules"""
        
        compliance_checks = {}
        
        # Check minimum balance
        total_value = treasury_data.get("total_value_usd", 0)
        compliance_checks["minimum_balance"] = {
            "compliant": total_value >= self.compliance_rules["minimum_balance_usd"],
            "current": total_value,
            "required": self.compliance_rules["minimum_balance_usd"]
        }
        
        # Check diversification
        concentration = risk_metrics.get("concentration_risk", 1.0)
        compliance_checks["diversification"] = {
            "compliant": concentration <= self.compliance_rules["diversification_threshold"],
            "current": concentration,
            "threshold": self.compliance_rules["diversification_threshold"]
        }
        
        # Check data freshness
        staleness = risk_metrics.get("staleness_risk", 1.0)
        compliance_checks["data_freshness"] = {
            "compliant": staleness < 0.25,  # Less than 6 hours old
            "staleness_score": staleness,
            "last_updated": treasury_data.get("last_updated")
        }
        
        # Overall compliance
        all_compliant = all(check["compliant"] for check in compliance_checks.values())
        
        return {
            "overall_compliant": all_compliant,
            "checks": compliance_checks,
            "violations": [
                check_name for check_name, check in compliance_checks.items()
                if not check["compliant"]
            ]
        }
    
    async def _explain_assessment(
        self,
        treasury_data: Dict[str, Any],
        risk_metrics: Dict[str, float],
        risk_assessment: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        compliance_status: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive explanation of the assessment"""
        
        # Prepare data for AI explanation
        explanation_data = {
            "total_value_usd": treasury_data.get("total_value_usd", 0),
            "asset_count": len(treasury_data.get("assets", {})),
            "risk_metrics": risk_metrics,
            "overall_risk_score": risk_assessment["overall_score"],
            "risk_level": risk_assessment["risk_level"],
            "alert_count": len(alerts),
            "compliance_violations": len(compliance_status["violations"]),
            "high_risk_factors": risk_assessment["risk_factors"]
        }
        
        # Get AI explanation
        ai_explanation = await self.explain_decision(
            decision_data=explanation_data,
            method=ExplanationMethod.SHAP,
            cache_key=f"treasury_assessment_{treasury_data.get('treasury_id', 'unknown')}"
        )
        
        # Build comprehensive explanation
        explanation = {
            "assessment_summary": self._build_assessment_narrative(
                risk_metrics, risk_assessment, alerts
            ),
            "risk_factor_analysis": self._analyze_risk_factors(risk_metrics),
            "ai_reasoning": ai_explanation['reasoning'] if ai_explanation else None,
            "confidence": ai_explanation['confidence'] if ai_explanation else 0.9,
            "blockchain_proof": ai_explanation['proof_hash'] if ai_explanation else None,
            "decision_factors": ai_explanation.get('feature_importance', {}) if ai_explanation else {},
            "compliance_analysis": self._build_compliance_narrative(compliance_status)
        }
        
        return explanation
    
    def _build_assessment_narrative(
        self,
        risk_metrics: Dict[str, float],
        risk_assessment: Dict[str, Any],
        alerts: List[Dict[str, Any]]
    ) -> str:
        """Build narrative explanation of the risk assessment"""
        
        narrative = f"Treasury Risk Assessment Summary:\n\n"
        
        # Overall assessment
        risk_level = risk_assessment["risk_level"]
        overall_score = risk_assessment["overall_score"]
        narrative += f"Overall Risk Level: {risk_level.upper()} (Score: {overall_score:.2f})\n\n"
        
        # Risk factors
        narrative += "Risk Factor Analysis:\n"
        for factor, score in risk_metrics.items():
            risk_desc = self._get_risk_description(factor, score)
            narrative += f"• {factor.replace('_', ' ').title()}: {score:.2f} - {risk_desc}\n"
        
        # Alerts
        if alerts:
            narrative += f"\nActive Alerts ({len(alerts)}):\n"
            for alert in alerts:
                narrative += f"• {alert['severity'].upper()}: {alert['message']}\n"
        else:
            narrative += "\nNo active alerts.\n"
        
        # Key contributors
        if risk_assessment["risk_factors"]:
            narrative += f"\nPrimary Risk Drivers: {', '.join(risk_assessment['risk_factors'])}\n"
        
        return narrative
    
    def _analyze_risk_factors(self, risk_metrics: Dict[str, float]) -> Dict[str, Any]:
        """Provide detailed analysis of risk factors"""
        
        analysis = {}
        
        for factor, score in risk_metrics.items():
            analysis[factor] = {
                "score": score,
                "level": "high" if score > 0.6 else "medium" if score > 0.3 else "low",
                "description": self._get_risk_description(factor, score),
                "recommendations": self._get_risk_recommendations(factor, score)
            }
        
        return analysis
    
    def _build_compliance_narrative(self, compliance_status: Dict[str, Any]) -> str:
        """Build narrative for compliance status"""
        
        if compliance_status["overall_compliant"]:
            return "Treasury is fully compliant with all management policies."
        
        narrative = f"Compliance Issues Detected ({len(compliance_status['violations'])}):\n\n"
        
        for violation in compliance_status["violations"]:
            check = compliance_status["checks"][violation]
            narrative += f"• {violation.replace('_', ' ').title()}: "
            
            if violation == "minimum_balance":
                narrative += f"Current balance ${check['current']:,.2f} below required ${check['required']:,.2f}\n"
            elif violation == "diversification":
                narrative += f"Concentration {check['current']:.1%} exceeds limit {check['threshold']:.1%}\n"
            elif violation == "data_freshness":
                narrative += f"Data staleness score {check['staleness_score']:.2f} indicates stale information\n"
        
        return narrative
    
    def _get_risk_description(self, factor: str, score: float) -> str:
        """Get human-readable description of risk factor"""
        
        descriptions = {
            "concentration_risk": {
                "high": "Portfolio heavily concentrated in single asset",
                "medium": "Moderate concentration risk present",
                "low": "Well-diversified portfolio"
            },
            "liquidity_risk": {
                "high": "Limited liquid assets available",
                "medium": "Some liquidity constraints",
                "low": "Adequate liquidity available"
            },
            "volatility_risk": {
                "high": "High price volatility in holdings",
                "medium": "Moderate price fluctuations",
                "low": "Stable asset prices"
            },
            "transaction_risk": {
                "high": "Unusual transaction patterns detected",
                "medium": "Some irregular transactions",
                "low": "Normal transaction patterns"
            },
            "staleness_risk": {
                "high": "Data significantly outdated",
                "medium": "Data somewhat stale",
                "low": "Data is current"
            }
        }
        
        level = "high" if score > 0.6 else "medium" if score > 0.3 else "low"
        return descriptions.get(factor, {}).get(level, f"Score: {score:.2f}")
    
    def _get_risk_recommendations(self, factor: str, score: float) -> List[str]:
        """Get recommendations for managing specific risk factors"""
        
        if score <= 0.3:  # Low risk
            return []
        
        recommendations = {
            "concentration_risk": [
                "Consider diversifying into additional assets",
                "Gradually rebalance portfolio allocation",
                "Set maximum concentration limits"
            ],
            "liquidity_risk": [
                "Increase allocation to liquid assets",
                "Establish emergency liquidity reserves",
                "Review asset liquidity profiles"
            ],
            "volatility_risk": [
                "Consider hedging volatile positions",
                "Increase allocation to stable assets",
                "Implement volatility monitoring"
            ],
            "transaction_risk": [
                "Review recent transaction patterns",
                "Implement additional authorization controls",
                "Monitor for unauthorized access"
            ],
            "staleness_risk": [
                "Update treasury data immediately",
                "Implement real-time monitoring",
                "Check data feed connections"
            ]
        }
        
        return recommendations.get(factor, ["Monitor this risk factor closely"])
    
    async def _generate_recommendations(
        self,
        risk_assessment: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        compliance_status: Dict[str, Any]
    ) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        # Risk-based recommendations
        risk_level = risk_assessment["risk_level"]
        if risk_level in ["critical", "high"]:
            recommendations.append("Immediate review of treasury strategy required")
            recommendations.append("Consider reducing risk exposure in high-risk assets")
        
        # Alert-based recommendations
        for alert in alerts:
            if alert["type"] == "low_balance":
                recommendations.append("Replenish treasury funds to meet minimum requirements")
            elif alert["type"] == "concentration_risk":
                recommendations.append("Diversify portfolio to reduce concentration risk")
            elif alert["type"] == "stale_data":
                recommendations.append("Update treasury monitoring systems")
        
        # Compliance-based recommendations
        if not compliance_status["overall_compliant"]:
            recommendations.append("Address compliance violations immediately")
            for violation in compliance_status["violations"]:
                if violation == "minimum_balance":
                    recommendations.append("Increase treasury funding to meet minimum balance")
                elif violation == "diversification":
                    recommendations.append("Rebalance portfolio to improve diversification")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Continue current treasury management strategy")
            recommendations.append("Monitor for changes in risk profile")
        
        return recommendations


async def demonstrate_treasury_monitoring():
    """Demonstrate the explainable treasury monitor"""
    
    monitor = ExplainableTreasuryMonitorAgent()
    
    # Sample treasury data
    sample_treasury = {
        "treasury_id": "nuru_ai_treasury",
        "total_value_usd": 247500.00,
        "last_updated": datetime.utcnow().isoformat(),
        "assets": {
            "ADA": {
                "symbol": "ADA",
                "amount": 500000,
                "value_usd": 175000.00,
                "is_liquid": True,
                "price_history": [0.35, 0.34, 0.36, 0.35]  # Recent prices
            },
            "BTC": {
                "symbol": "BTC",
                "amount": 1.5,
                "value_usd": 67500.00,
                "is_liquid": True,
                "price_history": [45000, 44500, 45500, 45000]
            },
            "AGIX": {
                "symbol": "AGIX",
                "amount": 25000,
                "value_usd": 5000.00,
                "is_liquid": False,
                "price_history": [0.20, 0.19, 0.21, 0.20]
            }
        },
        "recent_transactions": [
            {
                "type": "deposit",
                "amount_usd": 50000,
                "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat()
            },
            {
                "type": "withdrawal",
                "amount_usd": 25000,
                "timestamp": (datetime.utcnow() - timedelta(hours=6)).isoformat()
            }
        ]
    }
    
    async with monitor:
        print("💰 Explainable Treasury Monitor Demo")
        print("=" * 60)
        
        # Demo 1: Normal treasury assessment
        print("\n📊 Demo 1: Treasury Risk Assessment")
        print("-" * 60)
        
        result = await monitor.run(
            treasury_data=sample_treasury,
            explain_assessment=True
        )
        
        # Display results
        summary = result["treasury_summary"]
        print(f"\n💼 Treasury Summary:")
        print(f"  Total Value: ${summary['total_value_usd']:,.2f}")
        print(f"  Assets: {summary['asset_count']}")
        print(f"  Last Updated: {summary['last_updated']}")
        
        risk = result["risk_assessment"]
        print(f"\n⚠️ Risk Assessment:")
        print(f"  Risk Level: {risk['risk_level'].upper()}")
        print(f"  Overall Score: {risk['overall_score']:.2f}")
        
        if risk["risk_factors"]:
            print(f"  Primary Risks: {', '.join(risk['risk_factors'])}")
        
        # Show risk metrics
        print(f"\n📈 Risk Metrics:")
        for metric, score in result["risk_metrics"].items():
            print(f"  {metric.replace('_', ' ').title()}: {score:.2f}")
        
        # Show alerts
        if result["alerts"]:
            print(f"\n🚨 Active Alerts ({len(result['alerts'])}):")
            for alert in result["alerts"]:
                print(f"  • {alert['severity'].upper()}: {alert['message']}")
        else:
            print(f"\n✅ No active alerts")
        
        # Show compliance
        compliance = result["compliance_status"]
        print(f"\n📋 Compliance: {'✅ COMPLIANT' if compliance['overall_compliant'] else '❌ VIOLATIONS'}")
        if compliance["violations"]:
            print(f"  Violations: {', '.join(compliance['violations'])}")
        
        # Show explanation
        if result["explanation"]:
            exp = result["explanation"]
            print(f"\n🧠 AI Explanation:")
            print(f"  Confidence: {exp['confidence']:.2%}")
            print(f"\n  Assessment Summary:\n{exp['assessment_summary']}")
            
            if exp['blockchain_proof']:
                print(f"\n  🔐 Blockchain Proof: {exp['blockchain_proof'][:32]}...")
        
        # Show recommendations
        if result["recommendations"]:
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(result["recommendations"], 1):
                print(f"  {i}. {rec}")
        
        # Demo 2: High-risk scenario
        print("\n\n📊 Demo 2: High-Risk Treasury Scenario")
        print("-" * 60)
        
        # Create high-risk treasury
        risky_treasury = {
            **sample_treasury,
            "total_value_usd": 25000.00,  # Low balance
            "last_updated": (datetime.utcnow() - timedelta(hours=10)).isoformat(),  # Stale data
            "assets": {
                "VOLATILE_COIN": {
                    "symbol": "VOLATILE",
                    "amount": 100000,
                    "value_usd": 25000.00,  # 100% concentration
                    "is_liquid": False,
                    "price_history": [0.30, 0.25, 0.35, 0.20, 0.25]  # High volatility
                }
            }
        }
        
        risky_result = await monitor.run(
            treasury_data=risky_treasury,
            explain_assessment=True
        )
        
        print(f"\n⚠️ High-Risk Assessment:")
        risk = risky_result["risk_assessment"]
        print(f"  Risk Level: {risk['risk_level'].upper()}")
        print(f"  Overall Score: {risk['overall_score']:.2f}")
        
        print(f"\n🚨 Critical Alerts ({len(risky_result['alerts'])}):")
        for alert in risky_result["alerts"]:
            print(f"  • {alert['severity'].upper()}: {alert['message']}")
        
        if risky_result["explanation"]:
            exp = risky_result["explanation"]
            print(f"\n🧠 Risk Analysis:\n{exp['assessment_summary']}")
        
        # Show explanation statistics
        stats = monitor.get_explanation_stats()
        print(f"\n\n📈 Monitor Statistics:")
        print(f"  Total Assessments: {stats['total_decisions']}")
        print(f"  Cached Explanations: {stats['cached_explanations']}")
        print(f"  Blockchain Verified: {stats['blockchain_enabled']}")


if __name__ == "__main__":
    asyncio.run(demonstrate_treasury_monitoring())