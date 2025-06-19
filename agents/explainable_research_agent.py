#!/usr/bin/env python3
"""
Explainable Research Agent - Intelligent research with AI explanations
Part of the Agent Forge framework with Ziggurat Intelligence integration

This agent demonstrates how to create research agents that can explain their
source evaluation, credibility assessment, and content ranking decisions.
"""

import asyncio
import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
import hashlib
from urllib.parse import urlparse

# Add parent directory to path for imports
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.agents.ziggurat_enhanced import ZigguratEnhancedAgent
from src.core.shared.ai.embeddings_client import EmbeddingsClient
from src.core.shared.web.analysis.content_analyzer import ContentAnalyzer


class ExplainableResearchAgent(ZigguratEnhancedAgent):
    """
    Research agent that explains its source evaluation and content ranking decisions.
    
    Features:
    - Explains source credibility scoring
    - Provides reasoning for content relevance rankings
    - Fact-checking explanations with source verification
    - Alternative source suggestions based on analysis
    - Blockchain verification of research methodology (community tier: educational)
    """
    
    name = "explainable_research_agent"
    description = "Intelligent research with explainable source evaluation and ranking"
    
    def __init__(
        self,
        explanation_method: str = "shap",
        enable_explanations: bool = True,
        max_sources: int = 10,
        **kwargs
    ):
        """
        Initialize Explainable Research Agent.
        
        Args:
            explanation_method: Method for generating explanations (shap, lime, gradient)
            enable_explanations: Whether to enable explanation generation
            max_sources: Maximum number of sources to analyze
            **kwargs: Additional arguments passed to base class
        """
        super().__init__(
            explanation_method=explanation_method,
            enable_explanations=enable_explanations,
            **kwargs
        )
        
        self.max_sources = max_sources
        self.embeddings_client = None
        self.content_analyzer = None
        self.source_authority_cache = {}
        
    async def initialize(self):
        """Initialize the research agent with analysis tools."""
        await super().initialize()
        
        # Initialize AI and analysis tools
        self.embeddings_client = EmbeddingsClient()
        self.content_analyzer = ContentAnalyzer()
        
        self.logger.info("🔍 Explainable Research Agent initialized")
        
    async def run(
        self,
        query: str,
        sources: Optional[List[str]] = None,
        research_depth: str = "standard",
        fact_check: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Conduct research with explainable source evaluation and ranking.
        
        Args:
            query: Research query or topic
            sources: Optional list of specific sources to analyze
            research_depth: Depth of research (quick, standard, comprehensive)
            fact_check: Whether to perform fact checking
            **kwargs: Additional research parameters
            
        Returns:
            Dict containing research results and explanations
        """
        
        self.logger.info(f"🔍 Researching: {query}")
        
        # Discover or validate sources
        if sources is None:
            sources = await self._discover_sources(query, research_depth)
        else:
            sources = sources[:self.max_sources]  # Limit to max sources
        
        # Conduct research across sources
        research_results = await self._conduct_research(query, sources, fact_check)
        
        # Prepare explanation data
        explanation_data = {
            "query": query,
            "num_sources": len(sources),
            "research_depth": research_depth,
            "fact_checking_enabled": fact_check,
            "source_authority_avg": research_results.get("source_authority_avg", 0.5),
            "content_relevance_avg": research_results.get("content_relevance_avg", 0.5),
            "factual_accuracy_score": research_results.get("factual_accuracy_score", 0.5),
            "information_completeness": research_results.get("information_completeness", 0.5),
            "source_diversity": research_results.get("source_diversity", 0.5),
            "temporal_relevance": research_results.get("temporal_relevance", 0.5)
        }
        
        # Run with explanation if enabled
        if self.enable_explanations:
            result = await self.run_with_explanation(
                action_name="research_analysis",
                explanation_data=explanation_data,
                query=query,
                sources=sources,
                research_depth=research_depth,
                fact_check=fact_check
            )
            
            # Add alternative sources and recommendations
            alternatives = await self._suggest_alternative_sources(query, sources, result.get("explanation"))
            result["alternative_sources"] = alternatives
            
            recommendations = await self._generate_research_recommendations(
                query, research_results, result.get("explanation")
            )
            result["recommendations"] = recommendations
            
            return result
        else:
            # Return basic result without explanations
            return {
                "action": "research_analysis",
                "success": True,
                "result": research_results,
                "explanation": None,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _discover_sources(self, query: str, depth: str) -> List[str]:
        """Discover relevant sources based on query and research depth."""
        
        # Source discovery strategy based on depth
        if depth == "quick":
            source_count = 3
        elif depth == "comprehensive":
            source_count = min(self.max_sources, 15)
        else:  # standard
            source_count = min(self.max_sources, 8)
        
        # Simulate source discovery (in production, this would use search APIs)
        discovered_sources = []
        
        # Academic and authoritative sources
        if "research" in query.lower() or "study" in query.lower():
            discovered_sources.extend([
                "https://scholar.google.com/search?q=" + query.replace(" ", "+"),
                "https://www.ncbi.nlm.nih.gov/pubmed/?term=" + query.replace(" ", "+"),
                "https://arxiv.org/search/?query=" + query.replace(" ", "+")
            ])
        
        # News and current events
        if any(term in query.lower() for term in ["news", "current", "latest", "recent"]):
            discovered_sources.extend([
                "https://news.google.com/search?q=" + query.replace(" ", "+"),
                "https://www.reuters.com/search/news?blob=" + query.replace(" ", "+"),
                "https://www.bbc.com/search?q=" + query.replace(" ", "+")
            ])
        
        # Technology and business
        if any(term in query.lower() for term in ["tech", "business", "startup", "ai", "crypto"]):
            discovered_sources.extend([
                "https://techcrunch.com/search/" + query.replace(" ", "+"),
                "https://www.wired.com/search/?q=" + query.replace(" ", "+"),
                "https://arstechnica.com/search/?query=" + query.replace(" ", "+")
            ])
        
        # Wikipedia for general knowledge
        discovered_sources.append("https://en.wikipedia.org/wiki/" + query.replace(" ", "_"))
        
        # Limit to requested count
        return discovered_sources[:source_count]
    
    async def _conduct_research(
        self, 
        query: str, 
        sources: List[str], 
        fact_check: bool
    ) -> Dict[str, Any]:
        """Conduct research across sources and compile results."""
        
        research_data = {
            "query": query,
            "sources_analyzed": [],
            "content_summary": "",
            "key_findings": [],
            "factual_claims": [],
            "source_authority_avg": 0.0,
            "content_relevance_avg": 0.0,
            "factual_accuracy_score": 0.0,
            "information_completeness": 0.0,
            "source_diversity": 0.0,
            "temporal_relevance": 0.0
        }
        
        source_analyses = []
        
        for source_url in sources:
            try:
                # Analyze individual source
                source_analysis = await self._analyze_source(query, source_url, fact_check)
                source_analyses.append(source_analysis)
                research_data["sources_analyzed"].append(source_analysis)
                
            except Exception as e:
                self.logger.warning(f"Failed to analyze source {source_url}: {e}")
                continue
        
        # Compile overall research metrics
        if source_analyses:
            research_data["source_authority_avg"] = sum(
                s.get("authority_score", 0.5) for s in source_analyses
            ) / len(source_analyses)
            
            research_data["content_relevance_avg"] = sum(
                s.get("relevance_score", 0.5) for s in source_analyses
            ) / len(source_analyses)
            
            research_data["factual_accuracy_score"] = sum(
                s.get("accuracy_score", 0.5) for s in source_analyses
            ) / len(source_analyses)
            
            # Calculate additional metrics
            research_data["information_completeness"] = min(len(source_analyses) / 5, 1.0)
            research_data["source_diversity"] = self._calculate_source_diversity(sources)
            research_data["temporal_relevance"] = self._calculate_temporal_relevance(source_analyses)
            
            # Generate content summary and key findings
            research_data["content_summary"] = self._generate_content_summary(source_analyses)
            research_data["key_findings"] = self._extract_key_findings(source_analyses)
            
            if fact_check:
                research_data["factual_claims"] = self._extract_factual_claims(source_analyses)
        
        return research_data
    
    async def _analyze_source(self, query: str, source_url: str, fact_check: bool) -> Dict[str, Any]:
        """Analyze individual source for authority, relevance, and accuracy."""
        
        source_analysis = {
            "url": source_url,
            "domain": urlparse(source_url).netloc,
            "authority_score": 0.0,
            "relevance_score": 0.0,
            "accuracy_score": 0.0,
            "content_quality": 0.0,
            "publication_date": None,
            "content_type": "unknown"
        }
        
        # Assess source authority
        source_analysis["authority_score"] = await self._assess_source_authority(source_url)
        
        # Calculate semantic relevance (simulate with domain and query analysis)
        source_analysis["relevance_score"] = await self._calculate_semantic_similarity(source_url, query)
        
        # Assess content quality
        source_analysis["content_quality"] = await self._assess_content_quality(source_url)
        
        # Fact checking if enabled
        if fact_check:
            source_analysis["accuracy_score"] = await self._verify_factual_accuracy(source_url, query)
        else:
            source_analysis["accuracy_score"] = 0.7  # Default assumption
        
        # Determine content type and freshness
        source_analysis["content_type"] = self._determine_content_type(source_url)
        source_analysis["publication_date"] = await self._estimate_publication_date(source_url)
        
        return source_analysis
    
    async def _assess_source_authority(self, source_url: str) -> float:
        """Assess the authority/credibility of a source."""
        
        domain = urlparse(source_url).netloc.lower()
        
        # Check cache first
        if domain in self.source_authority_cache:
            return self.source_authority_cache[domain]
        
        authority_score = 0.5  # Default score
        
        # High authority domains
        high_authority = [
            "scholar.google.com", "ncbi.nlm.nih.gov", "arxiv.org", "nature.com",
            "science.org", "ieee.org", "acm.org", "reuters.com", "bbc.com",
            "nytimes.com", "washingtonpost.com", "economist.com", "wikipedia.org"
        ]
        
        # Medium authority domains
        medium_authority = [
            "techcrunch.com", "wired.com", "arstechnica.com", "cnn.com",
            "guardian.co.uk", "wsj.com", "forbes.com", "businessinsider.com"
        ]
        
        # Low authority indicators
        low_authority_indicators = [
            "blog", "personal", "geocities", "wordpress.com", "blogspot.com"
        ]
        
        # Score based on domain reputation
        if any(auth_domain in domain for auth_domain in high_authority):
            authority_score = 0.9
        elif any(auth_domain in domain for auth_domain in medium_authority):
            authority_score = 0.7
        elif any(indicator in domain for indicator in low_authority_indicators):
            authority_score = 0.3
        elif domain.endswith(('.edu', '.gov')):
            authority_score = 0.85
        elif domain.endswith('.org'):
            authority_score = 0.6
        
        # Cache the result
        self.source_authority_cache[domain] = authority_score
        
        return authority_score
    
    async def _calculate_semantic_similarity(self, source_url: str, query: str) -> float:
        """Calculate semantic similarity between source and query."""
        
        # Extract domain and path for analysis
        parsed = urlparse(source_url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        
        # Simple keyword matching (in production, use embeddings)
        query_words = set(query.lower().split())
        source_words = set((domain + " " + path.replace("/", " ").replace("-", " ")).split())
        
        if not query_words or not source_words:
            return 0.5
        
        # Calculate Jaccard similarity
        intersection = len(query_words.intersection(source_words))
        union = len(query_words.union(source_words))
        
        if union == 0:
            return 0.5
        
        jaccard_similarity = intersection / union
        
        # Boost for exact matches in URL
        exact_matches = sum(1 for word in query_words if word in source_url.lower())
        exact_boost = min(exact_matches * 0.1, 0.3)
        
        return min(jaccard_similarity + exact_boost, 1.0)
    
    async def _assess_content_quality(self, source_url: str) -> float:
        """Assess content quality indicators."""
        
        # Simulate content quality assessment
        domain = urlparse(source_url).netloc.lower()
        
        quality_indicators = {
            "https": 0.1 if source_url.startswith("https") else 0.0,
            "professional_domain": 0.2 if any(tld in domain for tld in ['.edu', '.gov', '.org']) else 0.0,
            "established_site": 0.3 if any(site in domain for site in ['wikipedia', 'reuters', 'bbc']) else 0.1,
            "no_suspicious_elements": 0.2,  # Assume no suspicious elements
            "structured_content": 0.2  # Assume structured content
        }
        
        return sum(quality_indicators.values())
    
    async def _verify_factual_accuracy(self, source_url: str, query: str) -> float:
        """Verify factual accuracy of source content."""
        
        # Simulate fact checking (in production, use fact-checking APIs)
        domain = urlparse(source_url).netloc.lower()
        
        # Known reliable sources get higher accuracy scores
        if any(reliable in domain for reliable in ['gov', 'edu', 'scholar', 'ncbi']):
            return 0.9
        elif any(news in domain for reliable in ['reuters', 'bbc', 'npr']):
            return 0.8
        elif 'wikipedia' in domain:
            return 0.75
        else:
            return 0.6  # Default for unknown sources
    
    def _determine_content_type(self, source_url: str) -> str:
        """Determine the type of content based on URL patterns."""
        
        url_lower = source_url.lower()
        
        if 'scholar.google' in url_lower or 'arxiv' in url_lower or 'ncbi' in url_lower:
            return "academic"
        elif any(news in url_lower for news in ['news', 'reuters', 'bbc', 'cnn']):
            return "news"
        elif 'wikipedia' in url_lower:
            return "encyclopedia"
        elif any(blog in url_lower for blog in ['blog', 'medium', 'wordpress']):
            return "blog"
        elif any(social in url_lower for social in ['twitter', 'facebook', 'linkedin']):
            return "social_media"
        else:
            return "website"
    
    async def _estimate_publication_date(self, source_url: str) -> Optional[str]:
        """Estimate publication date of content."""
        
        # Simulate date extraction (in production, parse from page content)
        current_date = datetime.utcnow()
        
        # Assign recent dates to news sources
        if any(news in source_url.lower() for news in ['news', 'current', 'latest']):
            # Recent news
            pub_date = current_date - timedelta(days=7)
        elif 'arxiv' in source_url.lower():
            # Academic papers - random recent date
            pub_date = current_date - timedelta(days=30)
        else:
            # Other sources - older content
            pub_date = current_date - timedelta(days=180)
        
        return pub_date.isoformat()
    
    def _calculate_source_diversity(self, sources: List[str]) -> float:
        """Calculate diversity score based on source domains."""
        
        if not sources:
            return 0.0
        
        domains = set()
        for source in sources:
            domain = urlparse(source).netloc.lower()
            # Remove 'www.' prefix for diversity calculation
            if domain.startswith('www.'):
                domain = domain[4:]
            domains.add(domain)
        
        # Diversity is ratio of unique domains to total sources
        return len(domains) / len(sources)
    
    def _calculate_temporal_relevance(self, source_analyses: List[Dict[str, Any]]) -> float:
        """Calculate temporal relevance of sources."""
        
        if not source_analyses:
            return 0.0
        
        current_time = datetime.utcnow()
        relevance_scores = []
        
        for analysis in source_analyses:
            pub_date_str = analysis.get("publication_date")
            if pub_date_str:
                try:
                    pub_date = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00'))
                    days_old = (current_time - pub_date).days
                    
                    # Temporal relevance decreases with age
                    if days_old <= 7:
                        relevance = 1.0
                    elif days_old <= 30:
                        relevance = 0.8
                    elif days_old <= 180:
                        relevance = 0.6
                    elif days_old <= 365:
                        relevance = 0.4
                    else:
                        relevance = 0.2
                    
                    relevance_scores.append(relevance)
                except:
                    relevance_scores.append(0.5)  # Default for parsing errors
            else:
                relevance_scores.append(0.5)  # Default for missing dates
        
        return sum(relevance_scores) / len(relevance_scores)
    
    def _generate_content_summary(self, source_analyses: List[Dict[str, Any]]) -> str:
        """Generate a summary of research content."""
        
        if not source_analyses:
            return "No sources analyzed."
        
        total_sources = len(source_analyses)
        academic_sources = sum(1 for s in source_analyses if s.get("content_type") == "academic")
        news_sources = sum(1 for s in source_analyses if s.get("content_type") == "news")
        avg_authority = sum(s.get("authority_score", 0) for s in source_analyses) / total_sources
        
        summary = f"Analyzed {total_sources} sources including "
        
        if academic_sources > 0:
            summary += f"{academic_sources} academic sources, "
        if news_sources > 0:
            summary += f"{news_sources} news sources, "
        
        summary += f"with average authority score of {avg_authority:.2f}. "
        
        if avg_authority > 0.7:
            summary += "Sources demonstrate high credibility."
        elif avg_authority > 0.5:
            summary += "Sources show moderate credibility."
        else:
            summary += "Sources have mixed credibility - verify claims independently."
        
        return summary
    
    def _extract_key_findings(self, source_analyses: List[Dict[str, Any]]) -> List[str]:
        """Extract key findings from research."""
        
        findings = []
        
        if source_analyses:
            avg_relevance = sum(s.get("relevance_score", 0) for s in source_analyses) / len(source_analyses)
            avg_authority = sum(s.get("authority_score", 0) for s in source_analyses) / len(source_analyses)
            
            findings.append(f"Content relevance averages {avg_relevance:.2%} across sources")
            findings.append(f"Source authority averages {avg_authority:.2%}")
            
            # Content type distribution
            content_types = {}
            for analysis in source_analyses:
                content_type = analysis.get("content_type", "unknown")
                content_types[content_type] = content_types.get(content_type, 0) + 1
            
            if content_types:
                dominant_type = max(content_types, key=content_types.get)
                findings.append(f"Primary content type: {dominant_type} ({content_types[dominant_type]} sources)")
            
            # Authority insights
            high_authority = sum(1 for s in source_analyses if s.get("authority_score", 0) > 0.7)
            if high_authority > 0:
                findings.append(f"{high_authority} high-authority sources identified")
        
        return findings[:5]  # Limit to top 5 findings
    
    def _extract_factual_claims(self, source_analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract and verify factual claims."""
        
        claims = []
        
        for i, analysis in enumerate(source_analyses):
            accuracy_score = analysis.get("accuracy_score", 0.5)
            authority_score = analysis.get("authority_score", 0.5)
            
            # Simulate factual claim extraction
            claim = {
                "claim": f"Information from source {i+1}",
                "source_url": analysis.get("url", ""),
                "accuracy_score": accuracy_score,
                "authority_score": authority_score,
                "verification_status": "verified" if accuracy_score > 0.7 else "needs_verification",
                "confidence": (accuracy_score + authority_score) / 2
            }
            
            claims.append(claim)
        
        # Sort by confidence
        claims.sort(key=lambda x: x["confidence"], reverse=True)
        
        return claims[:10]  # Limit to top 10 claims
    
    async def _suggest_alternative_sources(
        self, 
        query: str, 
        current_sources: List[str], 
        explanation: Optional[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """Suggest alternative sources based on analysis."""
        
        alternatives = []
        
        # Analyze current source gaps
        current_domains = set()
        for source in current_sources:
            domain = urlparse(source).netloc.lower()
            current_domains.add(domain)
        
        # Suggest missing source types
        suggested_sources = []
        
        if not any('scholar' in domain for domain in current_domains):
            suggested_sources.append({
                "url": f"https://scholar.google.com/search?q={query.replace(' ', '+')}",
                "type": "academic",
                "reason": "Add academic research perspective"
            })
        
        if not any('news' in domain or 'reuters' in domain for domain in current_domains):
            suggested_sources.append({
                "url": f"https://news.google.com/search?q={query.replace(' ', '+')}",
                "type": "news",
                "reason": "Include current news coverage"
            })
        
        if not any('wikipedia' in domain for domain in current_domains):
            suggested_sources.append({
                "url": f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
                "type": "encyclopedia",
                "reason": "Add comprehensive background information"
            })
        
        # Domain-specific suggestions based on query
        if any(term in query.lower() for term in ['tech', 'ai', 'software']):
            suggested_sources.append({
                "url": f"https://arxiv.org/search/?query={query.replace(' ', '+')}",
                "type": "preprint",
                "reason": "Include latest technical research"
            })
        
        return suggested_sources[:5]  # Limit to 5 alternatives
    
    async def _generate_research_recommendations(
        self,
        query: str,
        research_results: Dict[str, Any],
        explanation: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Generate recommendations for improving research quality."""
        
        recommendations = []
        
        # Analyze research quality metrics
        source_authority_avg = research_results.get("source_authority_avg", 0.5)
        source_diversity = research_results.get("source_diversity", 0.5)
        information_completeness = research_results.get("information_completeness", 0.5)
        temporal_relevance = research_results.get("temporal_relevance", 0.5)
        
        # Authority recommendations
        if source_authority_avg < 0.6:
            recommendations.append("Include more authoritative sources (.edu, .gov, established publications)")
        
        # Diversity recommendations
        if source_diversity < 0.5:
            recommendations.append("Diversify sources across different domains and perspectives")
        
        # Completeness recommendations
        if information_completeness < 0.7:
            recommendations.append("Expand research to include more sources for comprehensive coverage")
        
        # Temporal recommendations
        if temporal_relevance < 0.6:
            recommendations.append("Include more recent sources to ensure current information")
        
        # Query-specific recommendations
        if len(query.split()) < 3:
            recommendations.append("Consider using more specific search terms for targeted results")
        
        # Content type recommendations
        content_types = set()
        for source in research_results.get("sources_analyzed", []):
            content_types.add(source.get("content_type", "unknown"))
        
        if "academic" not in content_types:
            recommendations.append("Include academic sources for research-backed information")
        
        if "news" not in content_types:
            recommendations.append("Add news sources for current developments and context")
        
        # Default recommendations if none specific
        if not recommendations:
            recommendations.extend([
                "Research quality is good - consider fact-checking key claims",
                "Cross-reference information across multiple source types",
                "Verify publication dates to ensure information currency"
            ])
        
        return recommendations[:6]  # Limit to top 6 recommendations


# CLI entry point
async def main():
    """CLI interface for Explainable Research Agent."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Explainable Research Agent - Intelligent research with AI explanations"
    )
    
    parser.add_argument(
        "query",
        help="Research query or topic"
    )
    
    parser.add_argument(
        "--sources",
        type=str,
        nargs="*",
        help="Specific sources to analyze"
    )
    
    parser.add_argument(
        "--depth",
        choices=["quick", "standard", "comprehensive"],
        default="standard",
        help="Research depth"
    )
    
    parser.add_argument(
        "--method",
        choices=["shap", "lime", "gradient"],
        default="shap",
        help="Explanation method"
    )
    
    parser.add_argument(
        "--no-explanations",
        action="store_true",
        help="Disable explanations"
    )
    
    parser.add_argument(
        "--no-fact-check",
        action="store_true",
        help="Disable fact checking"
    )
    
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run with demo query"
    )
    
    args = parser.parse_args()
    
    # Demo mode
    if args.demo:
        query = "artificial intelligence in healthcare"
        sources = None
    else:
        query = args.query
        sources = args.sources
    
    # Create agent
    agent = ExplainableResearchAgent(
        explanation_method=args.method,
        enable_explanations=not args.no_explanations,
        name="ExplainableResearchAgent"
    )
    
    # Run agent
    async with agent:
        result = await agent.run(
            query=query,
            sources=sources,
            research_depth=args.depth,
            fact_check=not args.no_fact_check
        )
        
        # Pretty print results
        print("\n" + "="*70)
        print("🔍  EXPLAINABLE RESEARCH AGENT - RESULTS")
        print("="*70 + "\n")
        
        print(f"Query: {query}")
        print(f"Success: {result['success']}")
        
        if result.get("result"):
            res = result["result"]
            print(f"Sources analyzed: {res.get('num_sources', 0)}")
            print(f"Average authority: {res.get('source_authority_avg', 0):.2%}")
            print(f"Average relevance: {res.get('content_relevance_avg', 0):.2%}")
            
            if res.get("content_summary"):
                print(f"\nSummary: {res['content_summary']}")
            
            if res.get("key_findings"):
                print(f"\nKey Findings:")
                for finding in res["key_findings"][:3]:
                    print(f"  • {finding}")
        
        if result.get("explanation"):
            exp = result["explanation"]
            print(f"\nExplanation: {exp['reasoning']}")
            print(f"Confidence: {exp['confidence']:.2%}")
            print(f"Method: {exp['method']}")
        
        if result.get("recommendations"):
            print(f"\nRecommendations:")
            for i, rec in enumerate(result["recommendations"][:3], 1):
                print(f"  {i}. {rec}")
        
        if result.get("alternative_sources"):
            print(f"\nAlternative Sources:")
            for alt in result["alternative_sources"][:3]:
                print(f"  • {alt['type']}: {alt['reason']}")
        
        print("\n" + "="*70)
        print("Explainable Research Complete")
        print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())