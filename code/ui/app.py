import os
import sys
from pathlib import Path
import streamlit as st

# Add the code directory to path to ensure imports work
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.classifier import classifier
from core.safety import safety_module
from core.retriever import retriever
from core.responder import responder
from core.evaluator import Evaluator

# Initialize session state for evaluator
if 'evaluator' not in st.session_state:
    st.session_state.evaluator = Evaluator()

st.set_page_config(page_title="AI Support Agent", layout="wide")

st.title("🎧 AI Support Agent")
st.markdown("Automated Customer Support Triage and Response System")

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Ticket Input")
    with st.form("ticket_form"):
        company = st.text_input("Company", placeholder="e.g., Hackerrank, Claude, Visa")
        subject = st.text_input("Subject", placeholder="Brief description of the issue")
        issue = st.text_area("Query / Issue Details", placeholder="Detailed explanation of the problem")
        
        submitted = st.form_submit_button("Submit Ticket")

with col2:
    st.subheader("Session Metrics")
    metrics = st.session_state.evaluator.get_metrics()
    
    st.metric("Total Queries", metrics["total_queries"])
    st.metric("Escalation Rate", f"{metrics['escalation_rate']}%")
    st.metric("Retrieval Success", f"{metrics['retrieval_success_rate']}%")

if submitted:
    if not issue or not subject:
        st.error("Please provide both Subject and Query/Issue Details.")
    else:
        st.divider()
        st.subheader("Processing Results")
        
        with st.spinner("Classifying request..."):
            req_type, prod_area = classifier.classify(subject, issue, company)
            
        with st.spinner("Checking safety..."):
            is_escalated = safety_module.evaluate(subject, issue, req_type)
            
        decision = "Replied"
        final_response = ""
        justification = ""
        retrieved_docs = []
        scores = []
        fallback_triggered = False

        if is_escalated:
            decision = "Escalated"
            final_response = "Escalate to a human"
            justification = "Escalated due to safety/risk evaluation."
        else:
            with st.spinner("Retrieving context..."):
                retrieved_docs, scores, fallback_triggered = retriever.retrieve(company, issue, subject, top_k=3)
                
            with st.spinner("Generating response..."):
                resp_dict = responder.generate_response(subject, issue, company, retrieved_docs, fallback_triggered)
                final_response = resp_dict["response"]
                decision = resp_dict["status"]
                justification = resp_dict["justification"]

        # Record metrics
        st.session_state.evaluator.record_query(decision, len(retrieved_docs))
        
        # Display Results
        st.success("Ticket Processed!")
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.info(f"**Status:** {decision}")
            st.info(f"**Product Area:** {prod_area}")
        with res_col2:
            st.info(f"**Justification:** {justification}")
            st.info(f"**Request Type:** {req_type}")
            
        st.write("### Response")
        st.write(final_response)
        
        # Debug Panel
        with st.expander("🔍 Debug Panel"):
            st.write(f"**Fallback Triggered:** {fallback_triggered}")
            st.write("**Retrieved Documents:**")
            if retrieved_docs:
                for i, (doc, score) in enumerate(zip(retrieved_docs, scores)):
                    st.markdown(f"**Document {i+1}** (Score: {score:.4f})")
                    st.text(doc[:300] + "..." if len(doc) > 300 else doc)
            else:
                st.write("No documents retrieved.")
                
            st.write("**Final Prompt Sent to Responder LLM:**")
            # Reconstruct the prompt for debugging
            context_text = ""
            for i, doc in enumerate(retrieved_docs):
                context_text += f"[Document {i+1}]\n{doc}\n\n"
            
            debug_prompt = responder.prompt.format(
                context=context_text,
                subject=subject,
                issue=issue,
                company=company
            )
            st.code(debug_prompt, language="text")
