import asyncio
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from app.services.nyaykosh_service import (
    get_all_nyaykosh_laws,
    get_nyaykosh_law_by_slug,
    search_nyaykosh,
)
from app.services.gemini_service import generate_civic_guidance

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/legal", tags=["Legal Guidance & Nyaykosh"])

class LegalQueryRequest(BaseModel):
    query: str
    lawSlug: Optional[str] = None

LEGAL_TOPICS = [
    {
        "id": "property",
        "title": "Property & Tenancy Law",
        "icon": "Building",
        "color": "amber",
        "tagline": "Model Tenancy Act 2021, Transfer of Property Act 1882, RERA & Eviction",
        "description": "Statutory rights under Transfer of Property Act 1882, Model Tenancy Act, and RERA homebuyer safeguards.",
        "sampleQueries": [
            "What are tenant rights against sudden eviction without notice?",
            "What is the statutory ceiling on security deposits under Model Tenancy Act?",
            "Can a landlord cut off water or electricity during a rental dispute?"
        ],
        "relevantSections": [
            { "code": "Transfer of Property Act, 1882", "section": "Section 106 & 108", "summary": "Duration of leases, notice requirements, and rights/liabilities of lessor and lessee." },
            { "code": "Model Tenancy Act, 2021", "section": "Section 11 & 20", "summary": "Cap on security deposits (2 months) and strict prohibition of essential utility cutoffs." }
        ],
        "nyaykoshSlug": "model-tenancy-act-2021"
    },
    {
        "id": "consumer",
        "title": "Consumer Protection & E-Commerce",
        "icon": "ShieldAlert",
        "color": "purple",
        "tagline": "Consumer Protection Act 2019, Product Liability, CCPA & e-Daakhil",
        "description": "Protection against defective goods, unfair trade practices, misleading advertisements, and direct e-filing.",
        "sampleQueries": [
            "How to file an online consumer complaint on e-Daakhil?",
            "What are the remedies against e-commerce companies refusing refund for defective items?",
            "What penalties apply for deceptive endorsements and fake discount pricing?"
        ],
        "relevantSections": [
            { "code": "Consumer Protection Act, 2019", "section": "Section 35", "summary": "Direct e-filing before District Consumer Disputes Redressal Commission." },
            { "code": "Consumer Protection Act, 2019", "section": "Section 82-87", "summary": "Strict product liability against manufacturers, service providers, and sellers." }
        ],
        "nyaykoshSlug": "consumer-protection-act-2019"
    },
    {
        "id": "cyber",
        "title": "Cyber Law & Data Privacy",
        "icon": "ShieldCheck",
        "color": "cyan",
        "tagline": "DPDP Act 2023, IT Act 2000, 1930 Cyber Fraud Portal & Digital Rights",
        "description": "Statutory mechanisms addressing cyber scams, digital identity theft, non-consensual deepfakes, and corporate data protection.",
        "sampleQueries": [
            "What to do immediately after unauthorized UPI transaction fraud?",
            "What citizen rights are guaranteed under Digital Personal Data Protection Act 2023?",
            "How does Helpline 1930 freeze stolen bank accounts during the golden hour?"
        ],
        "relevantSections": [
            { "code": "Digital Personal Data Protection Act, 2023", "section": "Section 6 & 12", "summary": "Consent withdrawal, notice requirement, and right to correction and erasure." },
            { "code": "Information Technology Act, 2000", "section": "Section 66C & 66D", "summary": "Punishment for identity theft and cheating by personation using computer resources." }
        ],
        "nyaykoshSlug": "dpdp-act-2023"
    },
    {
        "id": "criminal",
        "title": "Criminal Justice & Civil Liberties",
        "icon": "Scale",
        "color": "emerald",
        "tagline": "Bharatiya Nyaya Sanhita (BNS) 2023, Zero FIR & Citizen Safeguards",
        "description": "Procedural rights under Bharatiya Nyaya Sanhita (BNS) and Bharatiya Nagarik Suraksha Sanhita (BNSS).",
        "sampleQueries": [
            "What is Zero FIR and can police refuse to register it?",
            "What are citizen rights during police inquiry, detention, or arrest?",
            "How does BNS Section 318 penalize organized digital cheating?"
        ],
        "relevantSections": [
            { "code": "Bharatiya Nagarik Suraksha Sanhita, 2023", "section": "Section 173", "summary": "Mandatory Zero FIR registration across any police station in India." },
            { "code": "Constitution of India", "section": "Article 22(1)", "summary": "Fundamental right to be informed of grounds of arrest and legal counsel." }
        ],
        "nyaykoshSlug": "bharatiya-nyaya-sanhita-2023"
    },
    {
        "id": "governance",
        "title": "RTI & Public Accountability",
        "icon": "Users",
        "color": "blue",
        "tagline": "Right to Information Act 2005, CPGRAMS & Citizen Charters",
        "description": "Statutory mechanisms for demanding transparency, accessing public records, and filing administrative grievances.",
        "sampleQueries": [
            "How to file an RTI application online for a Central or State Department?",
            "What is the statutory 30-day time limit and penalty on non-responsive PIOs?",
            "How to file a Second Appeal before the Central Information Commission (CIC)?"
        ],
        "relevantSections": [
            { "code": "Right to Information Act, 2005", "section": "Section 6 & 7", "summary": "Right to inspect works/documents and mandatory 30-day (or 48-hour) disposal." },
            { "code": "Right to Information Act, 2005", "section": "Section 20", "summary": "Personal daily penalty of ₹250/day up to ₹25,000 on defaulting Public Information Officers." }
        ],
        "nyaykoshSlug": "right-to-information-act-2005"
    }
]

@router.get("/nyaykosh")
async def get_nyaykosh_catalog():
    """
    Returns the codified Law-as-Code acts from the NeGD Nyaykosh initiative.
    """
    laws = get_all_nyaykosh_laws()
    return {
        "status": "success",
        "source": "National e-Governance Division (NeGD) - Nyaykosh Law as Code",
        "count": len(laws),
        "laws": laws
    }

@router.get("/nyaykosh/{slug}")
async def get_nyaykosh_law(slug: str):
    """
    Returns single codified law with sections, clauses, and penalty schedules.
    """
    law = get_nyaykosh_law_by_slug(slug)
    if not law:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Law '{slug}' not found in Nyaykosh repository."
        )
    return {
        "status": "success",
        "law": law
    }

@router.get("/topics")
async def get_legal_topics():
    """
    Returns structured legal guidance topics aligned with Indian codified statutes.
    """
    return {
        "status": "success",
        "topics": LEGAL_TOPICS
    }

@router.get("/search")
async def search_statutes(q: str = Query(..., min_length=2)):
    """
    Searches across Nyaykosh laws, provisions, and penalties.
    """
    results = search_nyaykosh(q)
    return {
        "status": "success",
        "query": q,
        "results": results
    }

@router.post("/query")
async def consult_statute(req: LegalQueryRequest):
    """
    Provides evidence-grounded legal analysis by feeding Nyaykosh statute context into Gemini AI.
    """
    context = ""
    if req.lawSlug:
        law = get_nyaykosh_law_by_slug(req.lawSlug)
        if law:
            context = f"Statute: {law['title']}\nOverview: {law['overview']}\nKey Provisions: {law['keyProvisions']}\nPenalties: {law['penalties']}"

    result = await asyncio.to_thread(generate_civic_guidance, query=req.query, document_context=context)
    return {
        "status": "success",
        "guidance": result
    }

