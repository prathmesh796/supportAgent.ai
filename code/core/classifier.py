import json
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from config import GROQ_API_KEY, GROQ_MODEL
from core.prod_area_classifier import product_area_extractor

class TicketClassifier:
    def __init__(self):
        # We use a temperature of 0 for more deterministic classification
        self.llm = ChatGroq(
            model=GROQ_MODEL,
            temperature=0,
            groq_api_key=GROQ_API_KEY
        )
        
        self.prompt = PromptTemplate(
            input_variables=["subject", "issue", "company", "valid_product_areas"],
            template="""You are an expert customer support triage system. 
Analyze the following support ticket and classify it.

Company: {company}
Subject: {subject}
Issue: {issue}

Determine the 'request_type' (AS: product_issue, feature_request, bug, invalid) 
and the 'product_area'.
The 'product_area' MUST be exactly one of the following valid areas for this company: {valid_product_areas}
If none perfectly match, choose the closest or return 'Unknown'.

Respond ONLY with a valid JSON object with exact keys: "request_type" and "product_area". Do not include markdown formatting like ```json.
"""
        )
        
        self.chain = self.prompt | self.llm

    def classify(self, subject, issue, company):
        valid_areas = product_area_extractor.get_valid_areas(company)
        valid_areas_str = ", ".join(valid_areas) if valid_areas else "Unknown"
        try:
            result = self.chain.invoke({
                "subject": subject,
                "issue": issue,
                "company": company,
                "valid_product_areas": valid_areas_str
            })
            
            content = result.content.strip()
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            
            parsed = json.loads(content)
            return parsed.get("request_type", "Unknown"), parsed.get("product_area", "Unknown")
        except Exception as e:
            print(f"Classification Error: {e}")
            return "Unknown", "Unknown"

classifier = TicketClassifier()
