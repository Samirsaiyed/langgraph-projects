import streamlit as st
from workflow import MultiAgentWorkflow
import time

# Page config
st.set_page_config(
    page_title="Multi-Agent Research Assistant", 
    page_icon="🔬",
    layout="wide"
)

# Initialize workflow
@st.cache_resource
def load_workflow():
    return MultiAgentWorkflow()

def main():
    st.title("🔬 Multi-Agent Research Assistant")
    st.markdown("*Powered by LangGraph & Multiple AI Agents*")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This system uses three specialized AI agents:
        - 🔍 **Research Agent**: Gathers information
        - 📊 **Analyzer Agent**: Extracts insights  
        - ✍️ **Writer Agent**: Creates reports
        
        Built with LangGraph for workflow orchestration.
        """)
        
        st.header("Example Topics")
        example_topics = [
            "Blockchain in Supply Chain",
            "Remote Work Trends 2024",
            "Renewable Energy Market",
            "Cybersecurity Threats",
            "AI Ethics and Governance"
        ]
        
        for topic in example_topics:
            if st.button(topic, key=f"example_{topic}"):
                st.session_state.research_topic = topic
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        research_topic = st.text_input(
            "Enter Research Topic:", 
            value=st.session_state.get('research_topic', ''),
            placeholder="e.g., Artificial Intelligence in Education"
        )
        
        if st.button("🚀 Start Research", type="primary"):
            if research_topic:
                st.session_state.research_topic = research_topic
                run_research(research_topic)
            else:
                st.error("Please enter a research topic!")
    
    with col2:
        st.markdown("### Quick Stats")
        if 'last_result' in st.session_state:
            result = st.session_state.last_result
            st.metric("Word Count", result['report_data']['word_count'])
            st.metric("Key Insights", len(result['analysis_data']['key_insights']))
            st.metric("Trends", len(result['analysis_data']['trends']))

def run_research(topic):
    workflow = load_workflow()
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Create containers for results
    research_container = st.container()
    analysis_container = st.container()
    report_container = st.container()
    
    status_text.text("🔍 Initializing research...")
    progress_bar.progress(10)
    
    # Run the workflow
    with st.spinner("Running multi-agent research..."):
        result = workflow.run_research(topic)
    
    progress_bar.progress(100)
    status_text.text("✅ Research Complete!")
    
    # Store result
    st.session_state.last_result = result
    
    # Display results
    display_results(result, research_container, analysis_container, report_container)

def display_results(result, research_container, analysis_container, report_container):
    # Research Results
    with research_container:
        st.header("🔍 Research Phase")
        
        with st.expander("Research Questions Generated", expanded=False):
            research_data = result['research_data']
            for i, question in enumerate(research_data['questions'], 1):
                st.write(f"{i}. {question}")
        
        with st.expander("Research Findings", expanded=False):
            st.write(research_data['findings'])
    
    # Analysis Results  
    with analysis_container:
        st.header("📊 Analysis Phase")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Key Insights")
            analysis_data = result['analysis_data']
            for insight in analysis_data['key_insights']:
                st.write(f"• {insight}")
        
        with col2:
            st.subheader("Major Trends")
            for trend in analysis_data['trends']:
                st.write(f"• {trend}")
        
        st.subheader("Recommendations")
        for rec in analysis_data['recommendations']:
            st.write(f"• {rec}")
    
    # Final Report
    with report_container:
        st.header("✍️ Final Report")
        
        report_data = result['report_data']
        
        # Executive Summary
        with st.expander("Executive Summary", expanded=True):
            st.write(report_data['executive_summary'])
        
        # Download button
        st.download_button(
            label="📄 Download Full Report",
            data=report_data['full_report'],
            file_name=f"{result['topic'].replace(' ', '_')}_report.md",
            mime="text/markdown"
        )
        
        # Full report display
        with st.expander("View Full Report", expanded=False):
            st.markdown(report_data['full_report'])

if __name__ == "__main__":
    main()