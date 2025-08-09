"""
Configuration settings for ADGM Corporate Agent
"""

import os
from typing import Dict, List

class Config:
    """Main configuration class"""
    
    # API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Model Settings
    DEFAULT_LLM_MODEL = "gpt-3.5-turbo"
    EMBEDDING_MODEL = "text-embedding-ada-002"
    MAX_TOKENS = 2000
    TEMPERATURE = 0.3
    
    # File Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    DATA_DIR = os.path.join(BASE_DIR, "data")
    
    # ADGM Document Types
    DOCUMENT_TYPES = {
        "articles_of_association": "Articles of Association",
        "memorandum_of_association": "Memorandum of Association",
        "board_resolution": "Board Resolution", 
        "shareholder_resolution": "Shareholder Resolution",
        "incorporation_form": "Incorporation Application Form",
        "ubo_declaration": "UBO Declaration Form",
        "register_members_directors": "Register of Members and Directors",
        "employment_contract": "Employment Contract",
        "commercial_agreement": "Commercial Agreement",
        "compliance_policy": "Compliance Policy Document"
    }
    
    # ADGM Process Requirements
    PROCESS_REQUIREMENTS = {
        "company_incorporation": {
            "name": "Company Incorporation",
            "required_docs": [
                "articles_of_association",
                "board_resolution",
                "incorporation_form", 
                "ubo_declaration",
                "register_members_directors"
            ]
        },
        "licensing": {
            "name": "Business Licensing",
            "required_docs": [
                "commercial_agreement",
                "compliance_policy"
            ]
        },
        "employment": {
            "name": "Employment Setup",
            "required_docs": [
                "employment_contract"
            ]
        }
    }
    
    # Red Flag Detection Patterns
    RED_FLAG_PATTERNS = {
        "jurisdiction_issues": {
            "patterns": [
                r"uae federal court",
                r"dubai court",
                r"abu dhabi court(?!.*global market)",
                r"federal law",
                r"emirates law"
            ],
            "severity": "high",
            "message": "Incorrect jurisdiction - should reference ADGM Courts"
        },
        "missing_adgm_reference": {
            "patterns": [
                r"(?i)governing law(?!.*adgm)(?!.*abu dhabi global market)"
            ],
            "severity": "high",
            "message": "Missing ADGM governing law reference"
        },
        "incomplete_signatures": {
            "patterns": [
                r"signature.*blank",
                r"\[signature\]",
                r"sign here",
                r"_+.*signature"
            ],
            "severity": "medium", 
            "message": "Incomplete signature sections found"
        },
        "missing_dates": {
            "patterns": [
                r"date.*blank",
                r"\[date\]",
                r"dd/mm/yyyy",
                r"_+.*date"
            ],
            "severity": "medium",
            "message": "Missing or placeholder dates found"
        }
    }

# Ensure required directories exist
def setup_directories():
    """Create necessary directories"""
    dirs = [Config.OUTPUT_DIR, Config.DATA_DIR]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)

if __name__ == "__main__":
    setup_directories()
    print("Configuration loaded and directories created")