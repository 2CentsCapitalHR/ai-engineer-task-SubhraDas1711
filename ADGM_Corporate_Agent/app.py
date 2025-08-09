"""
ADGM Corporate Agent - Main Application
AI-powered legal document review and compliance checking for Abu Dhabi Global Market
"""

import os
import sys
import json
import tempfile
from typing import List, Dict, Tuple
import gradio as gr
import logging
from datetime import datetime

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.document_parser import DocumentParser
    from src.rag_system import ADGMRAGSystem
    from src.document_validator import DocumentValidator
    from src.compliance_checker import ComplianceChecker
    from src.report_generator import ReportGenerator
    from config import Config
except ImportError as e:
    print(f"Import error: {e}")
    print("Using demo mode - some functionality may be limited")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ADGMCorporateAgent:
    """Main ADGM Corporate Agent Application"""
    
    def __init__(self):
        """Initialize the ADGM Corporate Agent"""
        # Create output directory
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize components
        self.document_parser = DocumentParser()
        self.rag_system = ADGMRAGSystem()
        self.document_validator = DocumentValidator()
        self.compliance_checker = ComplianceChecker()
        self.report_generator = ReportGenerator(self.output_dir)
        
        logger.info("ADGM Corporate Agent initialized successfully")
    
    def process_documents(self, files, progress=gr.Progress()):
        """Process uploaded documents and generate analysis"""
        if not files:
            return "❌ No files uploaded. Please upload DOCX documents.", "", "", ""
        
        try:
            progress(0.1, desc="Starting document analysis...")
            
            uploaded_documents = []
            document_analyses = []
            
            # Process each file
            for i, file in enumerate(files):
                progress(0.2 + (0.4 * i / len(files)), desc=f"Processing {os.path.basename(file.name)}...")
                
                try:
                    # Parse document
                    doc_info = self.document_parser.parse_document(file.name)
                    uploaded_documents.append(doc_info)
                    
                    # Validate document
                    validation = self.document_validator.validate_document(doc_info)
                    document_analyses.append(validation)
                    
                except Exception as e:
                    logger.error(f"Error processing {file.name}: {e}")
                    continue
            
            progress(0.6, desc="Checking compliance...")
            
            # Generate compliance report
            compliance_report = self.compliance_checker.generate_compliance_report(
                uploaded_documents, document_analyses
            )
            
            progress(0.8, desc="Generating reports...")
            
            # Create analysis results
            analysis_results = {
                "timestamp": datetime.now().isoformat(),
                "documents_processed": len(uploaded_documents),
                "compliance_report": compliance_report,
                "document_analyses": document_analyses
            }
            
            # Generate output files
            json_path = self.report_generator.generate_json_report(analysis_results)
            docx_path = self.report_generator.generate_docx_report(analysis_results)
            
            # Create commented document if possible
            commented_path = ""
            if uploaded_documents and document_analyses:
                try:
                    commented_path = self.report_generator.create_commented_document(
                        uploaded_documents[0]["file_path"], document_analyses[0]
                    )
                except Exception as e:
                    logger.warning(f"Could not create commented document: {e}")
            
            progress(1.0, desc="Analysis complete!")
            
            # Generate status message
            status = self._generate_status_message(compliance_report, len(uploaded_documents))
            
            return status, json_path, docx_path, commented_path
            
        except Exception as e:
            logger.error(f"Error in document processing: {e}")
            return f"❌ Error: {str(e)}", "", "", ""
    
    def answer_question(self, question: str, context: str = ""):
        """Answer ADGM-related questions"""
        if not question.strip():
            return "Please enter a question about ADGM requirements."
        
        try:
            response = self.rag_system.generate_response(question, context)
            return response
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _generate_status_message(self, compliance_report: Dict, doc_count: int) -> str:
        """Generate user-friendly status message"""
        process_name = compliance_report.get("process_name", "Document Analysis")
        status = compliance_report.get("overall_status", "completed")
        completion = compliance_report.get("completeness", {}).get("completion_percentage", 0)
        missing = compliance_report.get("completeness", {}).get("missing_documents", [])
        
        status_icons = {
            "ready_for_submission": "✅",
            "requires_attention": "⚠️", 
            "major_issues": "❌",
            "incomplete": "📋",
            "completed": "📄"
        }
        
        icon = status_icons.get(status, "📄")
        
        message = f"""
{icon} **Analysis Complete**

📊 **Process**: {process_name}
📈 **Completion**: {completion:.1f}%
📑 **Documents Analyzed**: {doc_count}
"""
        
        if missing:
            message += f"""
📋 **Missing Documents**:
{chr(10).join(f"   • {doc.replace('_', ' ').title()}" for doc in missing[:3])}
"""
        
        issues = compliance_report.get("issues_summary", {})
        high_issues = issues.get("high_severity", 0)
        if high_issues > 0:
            message += f"""
⚠️ **High Priority Issues**: {high_issues}
"""
        
        return message

def create_interface():
    """Create the Gradio interface"""
    agent = ADGMCorporateAgent()
    
    with gr.Blocks(
        title="ADGM Corporate Agent",
        theme=gr.themes.Soft(),
        css="""
        .main-header { 
            background: linear-gradient(90deg, #1e40af, #3b82f6);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
        }
        """
    ) as demo:
        
        # Header
        gr.HTML("""
        <div class="main-header">
            <h1>🏛️ ADGM Corporate Agent</h1>
            <p>AI-Powered Legal Document Intelligence for Abu Dhabi Global Market</p>
            <p><em>Automated document review, compliance checking, and expert guidance</em></p>
        </div>
        """)
        
        with gr.Tabs():
            # Document Analysis Tab
            with gr.TabItem("📄 Document Analysis"):
                gr.Markdown("""
                ### Upload ADGM Documents for Analysis
                
                **The system will:**
                - 🔍 Parse and analyze document content
                - 🚩 Detect red flags and compliance issues
                - ✅ Validate against ADGM requirements  
                - 📊 Generate comprehensive reports
                - 💬 Add review comments to documents
                """)
                
                with gr.Row():
                    with gr.Column(scale=2):
                        files = gr.File(
                            label="📤 Upload DOCX Documents",
                            file_count="multiple",
                            file_types=[".docx"],
                            height=150
                        )
                        
                        analyze_btn = gr.Button(
                            "🔍 Analyze Documents",
                            variant="primary",
                            size="lg"
                        )
                    
                    with gr.Column(scale=1):
                        gr.Markdown("""
                        **Supported Documents:**
                        
                        📋 **Company Formation**
                        • Articles of Association
                        • Board Resolutions
                        • UBO Declarations
                        • Incorporation Forms
                        
                        💼 **Other Documents**
                        • Employment Contracts
                        • Commercial Agreements
                        • Compliance Policies
                        """)
                
                # Results
                status_output = gr.Textbox(
                    label="📊 Analysis Results",
                    lines=8,
                    interactive=False
                )
                
                with gr.Row():
                    json_report = gr.File(label="📋 JSON Report")
                    docx_report = gr.File(label="📄 Detailed Report")
                    commented_doc = gr.File(label="💬 Reviewed Document")
                
                analyze_btn.click(
                    agent.process_documents,
                    inputs=[files],
                    outputs=[status_output, json_report, docx_report, commented_doc]
                )
            
            # Q&A Assistant Tab
            with gr.TabItem("💬 ADGM Assistant"):
                gr.Markdown("""
                ### Ask Questions About ADGM Requirements
                
                Get expert guidance on ADGM regulations, processes, and compliance requirements.
                """)
                
                with gr.Row():
                    with gr.Column(scale=2):
                        question = gr.Textbox(
                            label="❓ Your Question",
                            placeholder="e.g., What documents are required for ADGM company incorporation?",
                            lines=3
                        )
                        
                        context = gr.Textbox(
                            label="📝 Additional Context (Optional)",
                            placeholder="Provide any relevant context...",
                            lines=2
                        )
                        
                        ask_btn = gr.Button("🤔 Get Answer", variant="primary")
                    
                    with gr.Column(scale=1):
                        gr.Markdown("""
                        **Quick Questions:**
                        """)
                        
                        quick_btns = [
                            ("📋 Incorporation Docs", "What documents are required for ADGM company incorporation?"),
                            ("🏛️ Articles Requirements", "What should be included in Articles of Association?"),
                            ("👥 UBO Rules", "What are the UBO declaration requirements?"),
                            ("⚖️ Jurisdiction", "Which courts have jurisdiction in ADGM?")
                        ]
                
                answer = gr.Textbox(
                    label="💡 Expert Answer",
                    lines=12,
                    interactive=False
                )
                
                ask_btn.click(
                    agent.answer_question,
                    inputs=[question, context],
                    outputs=[answer]
                )
                
                # Quick question buttons
                for btn_text, btn_question in quick_btns:
                    btn = gr.Button(btn_text, size="sm")
                    btn.click(
                        lambda q=btn_question: agent.answer_question(q),
                        outputs=[answer]
                    )
            
            # Help & Information Tab
            with gr.TabItem("ℹ️ Help & Info"):
                gr.Markdown("""
                ## ADGM Corporate Agent - User Guide
                
                ### 🎯 What This System Does
                
                The ADGM Corporate Agent is an AI-powered legal assistant that helps with:
                
                - **Document Analysis**: Automatically reviews DOCX documents for ADGM compliance
                - **Red Flag Detection**: Identifies potential issues like wrong jurisdiction, missing clauses
                - **Process Validation**: Checks if you have all required documents for your ADGM process
                - **Expert Guidance**: Answers questions about ADGM regulations and requirements
                
                ### 📋 How to Use
                
                1. **Upload Documents**: Use the Document Analysis tab to upload your DOCX files
                2. **Review Results**: Check the analysis results and download reports
                3. **Ask Questions**: Use the ADGM Assistant for specific guidance
                4. **Fix Issues**: Address any red flags or missing documents identified
                
                ### 🚩 Common Issues Detected
                
                - **Jurisdiction Errors**: References to UAE Federal Courts instead of ADGM
                - **Missing UBO Info**: Incomplete Ultimate Beneficial Owner declarations  
                - **Wrong Templates**: Non-ADGM compliant document formats
                - **Incomplete Data**: Missing dates, signatures, or required clauses
                
                ### 🔧 Technical Requirements
                
                - **File Format**: Only DOCX files are supported
                - **File Size**: Keep files under 10MB for best performance
                - **Internet**: Required for AI analysis and knowledge retrieval
                
                ### ⚠️ Important Disclaimers
                
                - This tool provides guidance only and does not constitute legal advice
                - Always consult qualified legal professionals for official ADGM submissions
                - The system may not catch all potential issues - human review is recommended
                
                ### 📞 Support
                
                For technical issues or questions about the system, please refer to the documentation
                or contact your system administrator.
                """)
    
    return demo

if __name__ == "__main__":
    # Create and launch the application
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        debug=True,
        share=False
    )