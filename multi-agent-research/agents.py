from langchain_openai import ChatOpenAI
from typing import Dict, Any
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()

class ResearchAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
    
    def research(self, topic: str) -> Dict[str, Any]:
        print(f"🔍 Researching: {topic}")
        
        # Generate research questions
        questions = self._generate_research_questions(topic)
        
        # Simulate web research (we'll use the LLM's knowledge for now)
        research_data = self._conduct_research(topic, questions)
        
        return {
            "topic": topic,
            "questions": questions,
            "findings": research_data,
            "agent": "ResearchAgent"
        }
    
    def _generate_research_questions(self, topic: str) -> list:
        prompt = f"""Generate 5 specific research questions about "{topic}".
        These questions should cover different aspects like:
        - Current trends
        - Key challenges
        - Future outlook
        - Important statistics
        - Main players/companies
        
        Return only the questions, one per line."""
        
        response = self.llm.invoke([{"role": "user", "content": prompt}])
        questions = [q.strip() for q in response.content.split('\n') if q.strip()]
        return questions[:5]  # Limit to 5 questions
    
    def _conduct_research(self, topic: str, questions: list) -> str:
        prompt = f"""As a research expert, provide comprehensive information about "{topic}".
        
        Address these specific questions:
        {chr(10).join(f"- {q}" for q in questions)}
        
        Provide detailed, factual information with specific examples and data where possible.
        Structure your response clearly with key findings."""
        
        response = self.llm.invoke([{"role": "user", "content": prompt}])
        return response.content


class AnalyzerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

    def analyze(self, research_result: Dict[str, Any])-> Dict[str, Any]:
        print(f"📊 Analyzing research on: {research_result['topic']}")

        # Extract key insights
        insights = self._extra_insights(research_result)

        # Identify trends and patterns
        trends = self._identify_trends(research_result)

        # Generate recommendations
        recommendations = self._generate_recommendations(research_result, insights, trends)

        return {
            "topic": research_result["topic"],
            "key_insights": insights,
            "trends": trends,
            "recommendations": recommendations,
            "agent": "AnalyzerAgent"

        }

    def _extra_insights(self, research_result: Dict[str, Any])-> str:
        prompt = f"""Analyze this research data and extract 5 key insights:

            Topic: {research_result['topic']}
            Research Findings: {research_result['findings']}
            
            Extract the most important insights, focusing on:
            - Key statistics or numbers
            - Major opportunities
            - Significant challenges
            - Important trends
            - Critical success factors
            
            Return only the insights, one per line, starting with a bullet point."""

        response = self.llm.invoke([{"role":"user", "content": prompt}])
        insights = [line.strip() for line in response.content.split('\n') if line.strip() and ('*' in line or '-' in line)]
        return insights[:5]

    def _identify_trends(self, research_result: Dict[str, Any])-> list:
        prompt = f"""Based on this research about "{research_result['topic']}", identify 3 major trends:

        {research_result['findings']}
        
        Focus on:
        - Emerging patterns
        - Market movements
        - Technology developments
        - Future directions
        
        Return only the trends, one per line with bullet points."""

        response = self.llm.invoke([{"role":"user", "content": prompt}])
        trends = [line.strip() for line in response.content.split('\n') if line.strip() and ('*' in line or '-' in line)]
        return trends[:3]

    def _generate_recommendations(self, research_result: Dict[str, Any], insights: list, trends: list)-> str:
        prompt = f"""Based on this analysis of "{research_result['topic']}", provide 3 actionable recommendations:

            Key Insights: {chr(10).join(insights)}
            Trends: {chr(10).join(trends)}
            
            Provide specific, actionable recommendations for someone interested in this field.
            Return only the recommendations, one per line with bullet points."""
            

        response = self.llm.invoke([{"role":"user", "content": prompt}])
        recommendations = [line.strip() for line in response.content.split('\n') if line.strip() and ('*' in line or '-' in line)]
        return recommendations[:5]


class WriterAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
    
    def write_report(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        print(f"✍️ Writing report on: {analysis_result['topic']}")
        
        # Generate executive summary
        exec_summary = self._write_executive_summary(analysis_result)
        
        # Write detailed sections
        detailed_analysis = self._write_detailed_analysis(analysis_result)
        
        # Create final recommendations section
        recommendations_section = self._write_recommendations_section(analysis_result)
        
        # Compile full report
        full_report = self._compile_full_report(
            analysis_result['topic'], 
            exec_summary, 
            detailed_analysis, 
            recommendations_section
        )
        
        return {
            "topic": analysis_result['topic'],
            "executive_summary": exec_summary,
            "detailed_analysis": detailed_analysis,
            "recommendations": recommendations_section,
            "full_report": full_report,
            "word_count": len(full_report.split()),
            "agent": "WriterAgent"
        }
    
    def _write_executive_summary(self, analysis_result: Dict[str, Any]) -> str:
        prompt = f"""Write a professional executive summary for a report on "{analysis_result['topic']}".

        Key Insights: {chr(10).join(analysis_result['key_insights'])}
        Major Trends: {chr(10).join(analysis_result['trends'])}
        
        Write a concise 2-3 paragraph executive summary that captures the most important points.
        Use professional business language."""
        
        response = self.llm.invoke([{"role": "user", "content": prompt}])
        return response.content
    
    def _write_detailed_analysis(self, analysis_result: Dict[str, Any]) -> str:
        prompt = f"""Write a detailed analysis section for a report on "{analysis_result['topic']}".

        Key Insights: {chr(10).join(analysis_result['key_insights'])}
        Trends: {chr(10).join(analysis_result['trends'])}
        
        Structure this as:
        1. Current State Analysis
        2. Key Findings
        3. Market Trends & Opportunities
        
        Write 4-5 paragraphs with professional depth and analysis."""
        
        response = self.llm.invoke([{"role": "user", "content": prompt}])
        return response.content
    
    def _write_recommendations_section(self, analysis_result: Dict[str, Any]) -> str:
        prompt = f"""Write a recommendations section based on this analysis of "{analysis_result['topic']}":

        Recommendations: {chr(10).join(analysis_result['recommendations'])}
        
        Expand each recommendation with:
        - Why it's important
        - How to implement it
        - Expected outcomes
        
        Write in a professional, actionable format."""
        
        response = self.llm.invoke([{"role": "user", "content": prompt}])
        return response.content
    
    def _compile_full_report(self, topic: str, exec_summary: str, detailed_analysis: str, recommendations: str) -> str:
        report = f"""# Research Report: {topic}

        ## Executive Summary
        {exec_summary}

        ## Detailed Analysis
        {detailed_analysis}

        ## Recommendations
        {recommendations}

        ---
        *Report generated by Multi-Agent Research Assistant*
        """
        return report

# Test the agents
if __name__ == "__main__":
    researcher = ResearchAgent()
    analyzer = AnalyzerAgent()
    writer = WriterAgent()
    
    # Full pipeline test
    print("🚀 Running full multi-agent pipeline...")
    
    research_result = researcher.research("Artificial Intelligence in Healthcare")
    analysis_result = analyzer.analyze(research_result)
    report_result = writer.write_report(analysis_result)
    
    print(f"✅ COMPLETE REPORT GENERATED")
    print(f"Word count: {report_result['word_count']}")
    print(f"Report preview: {report_result['full_report'][:500]}...")