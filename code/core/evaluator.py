class Evaluator:
    def __init__(self):
        self.total_queries = 0
        self.escalations = 0
        self.successful_retrievals = 0

    def record_query(self, status, retrieved_docs_count):
        self.total_queries += 1
        
        if status.lower() == "escalated":
            self.escalations += 1
            
        if retrieved_docs_count > 0:
            self.successful_retrievals += 1

    def get_metrics(self):
        escalation_rate = (self.escalations / self.total_queries * 100) if self.total_queries > 0 else 0
        retrieval_success_rate = (self.successful_retrievals / self.total_queries * 100) if self.total_queries > 0 else 0
        
        return {
            "total_queries": self.total_queries,
            "escalation_rate": round(escalation_rate, 2),
            "retrieval_success_rate": round(retrieval_success_rate, 2)
        }
