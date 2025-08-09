"""
RAG System for ADGM Corporate Agent
Provides AI-powered responses using ADGM knowledge base
"""

import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class ADGMRAGSystem:
    """RAG system for ADGM legal knowledge"""
    
    def __init__(self):
        self.knowledge_base = self._load_adgm_knowledge()
        logger.info("ADGM RAG system initialized")
    
    def _load_adgm_knowledge(self) -> List[Dict]:
        """Load ADGM legal knowledge base"""
        return [
            {
                "id": "adgm_001",
                "title": "Company Incorporation Requirements",
                "content": """ADGM company incorporation requires these mandatory documents:
                1. Articles of Association - defining company structure and governance
                2. Board Resolution - incorporating shareholders' decisions
                3. Incorporation Application Form - official registration application
                4. UBO Declaration Form - declaring beneficial owners with 25%+ ownership
                5. Register of Members and Directors - listing company officers
                
                Per ADGM Companies Regulations 2020, all companies must have properly 
                structured Articles of Association with consecutive paragraph numbering.""",
                "category": "incorporation"
            },
            {
                "id": "adgm_002", 
                "title": "Jurisdiction and Governing Law",
                "content": """ADGM documents must specify ADGM jurisdiction and governing law:
                
                ✅ CORRECT: "This agreement shall be governed by ADGM law and subject 
                to the exclusive jurisdiction of ADGM Courts."
                
                ❌ INCORRECT: References to UAE Federal Courts, Dubai Courts, or 
                Abu Dhabi Courts (outside ADGM context) are non-compliant.
                
                ADGM has its own legal framework separate from UAE federal law.""",
                "category": "jurisdiction" 
            },
            {
                "id": "adgm_003",
                "title": "UBO Declaration Requirements", 
                "content": """Ultimate Beneficial Owner (UBO) declarations must include:
                
                - Any individual owning 25% or more of company shares
                - Natural persons with ultimate control over the entity
                - Complete personal details and current address
                - Passport copies for all current and previous nationalities
                - Signed declaration confirming accuracy of information
                
                Failure to properly declare UBOs violates ADGM beneficial ownership regulations.""",
                "category": "ubo"
            },
            {
                "id": "adgm_004",
                "title": "Employment Contract Standards",
                "content": """ADGM employment contracts must include:
                
                - Clear job title, duties, and reporting structure
                - Salary, benefits, and payment terms
                - Working hours (maximum 48 hours per week)
                - Annual leave entitlement (minimum 30 days)
                - Probationary period (maximum 6 months)
                - Termination procedures compliant with ADGM Employment Regulations
                - Confidentiality and non-compete clauses where appropriate
                
                Use ADGM Standard Employment Contract Template 2024.""",
                "category": "employment"
            },
            {
                "id": "adgm_005",
                "title": "Board Resolution Format",
                "content": """ADGM Board Resolutions must follow proper format:
                
                1. Company name and registration details
                2. Date and location of meeting/resolution
                3. Directors present or consenting
                4. Clear resolution language: "IT IS HEREBY RESOLVED THAT..."
                5. Specific actions authorized with full details
                6. Proper signatures of authorizing directors
                7. Corporate seal if applicable
                
                Template resolutions available on ADGM Registration Authority website.""",
                "category": "resolutions"
            }
        ]
    
    def generate_response(self, query: str, context: str = "") -> str:
        """Generate response to user query using knowledge base"""
        try:
            # Simple keyword matching for demo
            query_lower = query.lower()
            
            relevant_entries = []
            for entry in self.knowledge_base:
                # Check if query keywords match entry content
                content_lower = entry["content"].lower()
                title_lower = entry["title"].lower()
                
                if any(keyword in content_lower or keyword in title_lower 
                       for keyword in query_lower.split() if len(keyword) > 3):
                    relevant_entries.append(entry)
            
            if not relevant_entries:
                return self._default_response(query)
            
            # Format response
            response = f"Based on ADGM regulations, here's what you need to know:\n\n"
            
            for entry in relevant_entries[:2]:  # Limit to top 2 entries
                response += f"**{entry['title']}**\n\n"
                response += f"{entry['content']}\n\n"
                response += "---\n\n"
            
            response += "💡 **Note**: This guidance is based on ADGM regulations. "
            response += "Always consult qualified legal professionals for official advice."
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def _default_response(self, query: str) -> str:
        """Default response when no specific match found"""
        return f"""I understand you're asking about: "{query}"

While I don't have specific information matching your query, here are some general ADGM guidance points:

🏛️ **ADGM Jurisdiction**: Always ensure documents reference ADGM Courts and ADGM law, not UAE Federal Courts.

📋 **Company Incorporation**: Requires Articles of Association, Board Resolution, UBO Declaration, Incorporation Form, and Register of Members/Directors.

👥 **UBO Requirements**: Declare any individual with 25%+ ownership or control.

💼 **Employment**: Use ADGM Standard Employment Contract templates.

⚖️ **Legal Compliance**: All documents must comply with ADGM-specific regulations and templates.

For detailed guidance on your specific question, please consult ADGM official resources or qualified legal professionals."""

    def get_relevant_knowledge(self, document_type: str) -> List[Dict]:
        """Get knowledge relevant to specific document type"""
        relevant = []
        type_keywords = {
            'articles_of_association': ['incorporation', 'company'],
            'board_resolution': ['resolutions', 'board'],
            'ubo_declaration': ['ubo', 'beneficial'],
            'employment_contract': ['employment', 'contract']
        }
        
        keywords = type_keywords.get(document_type, [])
        for entry in self.knowledge_base:
            if any(keyword in entry['content'].lower() for keyword in keywords):
                relevant.append(entry)
        
        return relevant