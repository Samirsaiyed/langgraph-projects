from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any
from agents import ResearchAgent, AnalyzerAgent, WriterAgent

class ResearchState(TypedDict):
    topic: str
    research_data: Dict[str, Any]
    analysis_data: Dict[str, Any]
    report_data: Dict[str, Any]
    current_step: str
    progress: int

class MultiAgentWorkflow:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.analyzer_agent = AnalyzerAgent()
        self.writer_agent = WriterAgent()
        self.workflow = self._create_workflow()
    
    def _create_workflow(self):
        # Create the state graph
        workflow = StateGraph(ResearchState)
        
        # Add nodes for each agent
        workflow.add_node("research", self._research_node)
        workflow.add_node("analyze", self._analyze_node)
        workflow.add_node("write", self._write_node)
        
        # Define the flow
        workflow.set_entry_point("research")
        workflow.add_edge("research", "analyze")
        workflow.add_edge("analyze", "write")
        workflow.add_edge("write", END)
        
        return workflow.compile()
    
    def _research_node(self, state: ResearchState):
        print(f"🔍 Research phase starting...")
        research_result = self.research_agent.research(state["topic"])
        
        return {
            **state,
            "research_data": research_result,
            "current_step": "research",
            "progress": 33
        }
    
    def _analyze_node(self, state: ResearchState):
        print(f"📊 Analysis phase starting...")
        analysis_result = self.analyzer_agent.analyze(state["research_data"])
        
        return {
            **state,
            "analysis_data": analysis_result,
            "current_step": "analyze", 
            "progress": 66
        }
    
    def _write_node(self, state: ResearchState):
        print(f"✍️ Writing phase starting...")
        report_result = self.writer_agent.write_report(state["analysis_data"])
        
        return {
            **state,
            "report_data": report_result,
            "current_step": "write",
            "progress": 100
        }
    
    def run_research(self, topic: str):
        initial_state = {
            "topic": topic,
            "research_data": {},
            "analysis_data": {},
            "report_data": {},
            "current_step": "starting",
            "progress": 0
        }
        
        result = self.workflow.invoke(initial_state)
        return result

# Test the workflow
if __name__ == "__main__":
    workflow = MultiAgentWorkflow()
    
    print("🚀 Testing LangGraph Multi-Agent Workflow")
    result = workflow.run_research("Machine Learning in Finance")
    
    print(f"\n✅ Workflow Complete!")
    print(f"Final report word count: {result['report_data']['word_count']}")