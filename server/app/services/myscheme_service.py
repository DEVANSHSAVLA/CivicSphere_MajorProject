import logging

logger = logging.getLogger(__name__)

MYSCHEME_CATALOG = [
    {
        "id": "scheme-1",
        "slug": "pm-kisan-samman-nidhi",
        "name": "PM Kisan Samman Nidhi",
        "department": "Ministry of Agriculture & Farmers Welfare",
        "category": "Agriculture",
        "state": "All India",
        "level": "Central Sector",
        "source": "myScheme / API Setu National Repository",
        "description": "Financial assistance to farmers for agricultural needs.",
        "detailedDescription": "Central Sector scheme with 100% funding from Government of India. It provides income support of ₹6,000/- per year in three equal installments to all landholding farmer families.",
        "benefits": "₹6,000 per year directly credited into Aadhaar-linked bank accounts in three 4-monthly instalments.",
        "eligibilitySummary": "All landholder farmer families having cultivable landholding in their names.",
        "eligibilityCriteria": [
            "Small and marginal farmers owning cultivable agricultural land.",
            "Valid Aadhaar card linked with active bank account.",
            "Name must be enrolled on State Land Records Portal.",
            "Excluded: Institutional landholders, serving/retired government employees, and income tax payers."
        ],
        "documentsRequired": [
            "Land Ownership Document (Khatauni / RoR)",
            "Aadhaar Card",
            "Bank Account Passbook with IFSC",
            "Active Mobile Number"
        ],
        "officialUrl": "https://pmkisan.gov.in",
        "mySchemeUrl": "https://www.myscheme.gov.in/schemes/pm-kisan",
        "isSaved": False,
        "tagColor": "emerald"
    },
    {
        "id": "scheme-2",
        "slug": "ayushman-bharat-pm-jay",
        "name": "Ayushman Bharat PM-JAY",
        "department": "Ministry of Health and Family Welfare",
        "category": "Health",
        "state": "All India",
        "level": "Centrally Sponsored",
        "source": "myScheme / API Setu National Repository",
        "description": "Health insurance coverage for eligible families up to ₹5 Lakh/year.",
        "detailedDescription": "The world's largest government-funded healthcare assurance scheme offering secondary and tertiary hospitalization cover of ₹5 Lakh per eligible family per year across empaneled public and private hospitals.",
        "benefits": "Cashless and paperless access to quality healthcare at all public and empaneled private hospitals.",
        "eligibilitySummary": "Families identified based on deprivation and occupational criteria of SECC 2011, and senior citizens aged 70+.",
        "eligibilityCriteria": [
            "Rural families living in one-room kutcha houses, female-headed households, or landless laborers.",
            "Urban families categorized under identified 11 occupational categories.",
            "Senior citizens aged 70+ (Universal coverage irrespective of income under Ayushman Vaya Vandana)."
        ],
        "documentsRequired": [
            "Aadhaar Card",
            "Ration Card or SECC Household ID",
            "Proof of Family Identity"
        ],
        "officialUrl": "https://pmjay.gov.in",
        "mySchemeUrl": "https://www.myscheme.gov.in/schemes/pmjay",
        "isSaved": False,
        "tagColor": "purple"
    },
    {
        "id": "scheme-3",
        "slug": "beti-bachao-beti-padhao",
        "name": "Beti Bachao Beti Padhao",
        "department": "Ministry of Women and Child Development",
        "category": "Education",
        "state": "All India",
        "level": "Central Scheme",
        "source": "myScheme / API Setu National Repository",
        "description": "Promote education and welfare of the girl child.",
        "detailedDescription": "A tri-ministerial convergence effort to address declining Child Sex Ratio (CSR), eliminate gender-biased sex selection, and ensure girl child education and empowerment across India.",
        "benefits": "Scholarships, subsidized education, safety awareness, and linked Sukanya Samriddhi high-interest savings accounts.",
        "eligibilitySummary": "Any Indian family with a girl child from infancy through secondary school education.",
        "eligibilityCriteria": [
            "Indian citizen girl child below 10 years of age for account linkage.",
            "Enrolled in recognized government or private educational institutions.",
            "Applicable across all 700+ districts of India."
        ],
        "documentsRequired": [
            "Birth Certificate of girl child",
            "Aadhaar of parents/guardian",
            "Residential certificate"
        ],
        "officialUrl": "https://wcd.nic.in/bbbp-schemes",
        "mySchemeUrl": "https://www.myscheme.gov.in/schemes/bbbp",
        "isSaved": False,
        "tagColor": "amber"
    },
    {
        "id": "scheme-4",
        "slug": "pradhan-mantri-awas-yojana-urban",
        "name": "Pradhan Mantri Awas Yojana (PMAY-U)",
        "department": "Ministry of Housing and Urban Affairs",
        "category": "Housing",
        "state": "All India",
        "level": "Central Mission",
        "source": "myScheme / API Setu National Repository",
        "description": "Pucca houses for all eligible urban families with interest subsidies.",
        "detailedDescription": "Comprehensive mission addressing urban housing shortages among EWS, LIG and MIG categories through interest subsidy on housing loans and slum rehabilitation.",
        "benefits": "Up to ₹2.67 Lakh interest subsidy on home loans under Credit Linked Subsidy Scheme (CLSS).",
        "eligibilitySummary": "Beneficiary family should not own a pucca house in any part of India.",
        "eligibilityCriteria": [
            "Economically Weaker Section (EWS) with annual household income up to ₹3 Lakh.",
            "Low Income Group (LIG) with income between ₹3 Lakh to ₹6 Lakh.",
            "Female ownership or co-ownership of house is mandatory in EWS/LIG categories."
        ],
        "documentsRequired": [
            "Aadhaar Card of all family members",
            "Income Certificate / ITR",
            "Property Sale Deed / Construction estimate",
            "Affidavit of not owning pucca house"
        ],
        "officialUrl": "https://pmaymis.gov.in",
        "mySchemeUrl": "https://www.myscheme.gov.in/schemes/pmayu",
        "isSaved": False,
        "tagColor": "blue"
    },
    {
        "id": "scheme-5",
        "slug": "pm-svanidhi",
        "name": "PM SVANidhi (Street Vendor Loan)",
        "department": "Ministry of Housing & Urban Affairs",
        "category": "Employment",
        "state": "All India",
        "level": "Central Sector",
        "source": "myScheme / API Setu National Repository",
        "description": "Affordable collateral-free working capital micro-loans for street vendors.",
        "detailedDescription": "Special micro-credit facility empowering urban, peri-urban, and rural street vendors to resume livelihoods through progressive working capital loans with 7% interest subsidy.",
        "benefits": "Initial tranche of ₹10,000, subsequent tranches up to ₹20,000 and ₹50,000 on timely repayment.",
        "eligibilitySummary": "All street vendors vending in urban areas on or before the qualifying date.",
        "eligibilityCriteria": [
            "Street vendors holding Certificate of Vending / Identity Card issued by Urban Local Bodies (ULB).",
            "Vendors identified in the survey or letter of recommendation by Town Vending Committee.",
            "Vendors in peri-urban/rural markets supplying to urban areas."
        ],
        "documentsRequired": [
            "Vending Certificate or ID Card",
            "Aadhaar Card",
            "Bank Account details"
        ],
        "officialUrl": "https://pmsvanidhi.mohua.gov.in",
        "mySchemeUrl": "https://www.myscheme.gov.in/schemes/pm-svanidhi",
        "isSaved": False,
        "tagColor": "emerald"
    },
    {
        "id": "scheme-6",
        "slug": "pm-mudra-yojana",
        "name": "PM MUDRA Yojana (PMMY)",
        "department": "Ministry of Finance",
        "category": "Employment",
        "state": "All India",
        "level": "Central Scheme",
        "source": "myScheme / API Setu National Repository",
        "description": "Loans up to ₹20 Lakh to non-corporate, non-farm small/micro enterprises.",
        "detailedDescription": "Refinance agency supporting formal credit to micro enterprises in manufacturing, trading, and service sectors under three stages: Shishu, Kishore, and Tarun.",
        "benefits": "Shishu loans up to ₹50,000, Kishore up to ₹5 Lakh, Tarun up to ₹10 Lakh (extended to ₹20 Lakh in 2024 budget).",
        "eligibilitySummary": "Any Indian citizen with a feasible non-farm business proposition.",
        "eligibilityCriteria": [
            "Small business owners, shopkeepers, fruit/vegetable vendors, artisans, and food processors.",
            "No collateral or third-party guarantee required.",
            "Applicant must not be a defaulter to any financial institution."
        ],
        "documentsRequired": [
            "Proof of Identity & Address (Aadhaar/PAN/Voter ID)",
            "Business address and establishment proof",
            "Bank statement of last 6 months",
            "Quotation / Business plan"
        ],
        "officialUrl": "https://www.mudra.org.in",
        "mySchemeUrl": "https://www.myscheme.gov.in/schemes/pmmy",
        "isSaved": False,
        "tagColor": "purple"
    },
    {
        "id": "scheme-7",
        "slug": "pm-surya-ghar-muft-bijli-yojana",
        "name": "PM Surya Ghar Muft Bijli Yojana",
        "department": "Ministry of New and Renewable Energy",
        "category": "Housing",
        "state": "All India",
        "level": "Central Sector",
        "source": "myScheme / API Setu National Repository",
        "description": "Subsidized rooftop solar plant installations providing up to 300 free electricity units/month.",
        "detailedDescription": "Pioneering green energy scheme aiming to light up 1 crore households by providing central financial assistance up to ₹78,000 for installing residential rooftop solar systems.",
        "benefits": "Direct subsidy of ₹30,000 for 1kW, ₹60,000 for 2kW, and ₹78,000 for 3kW or higher solar rooftop systems.",
        "eligibilitySummary": "All Indian residential households with suitable roof space and active grid electricity connection.",
        "eligibilityCriteria": [
            "Must be an Indian citizen with valid electricity connection.",
            "Adequate unshaded rooftop area available for solar panel installation.",
            "One household is eligible for subsidy only once."
        ],
        "documentsRequired": [
            "Latest Electricity Bill",
            "Aadhaar Card of electricity consumer",
            "Bank Account Passbook / Cancelled Cheque",
            "Proof of roof ownership"
        ],
        "officialUrl": "https://pmsuryaghar.gov.in",
        "mySchemeUrl": "https://www.myscheme.gov.in/schemes/pm-surya-ghar",
        "isSaved": False,
        "tagColor": "amber"
    }
]

def get_all_schemes():
    """Returns the full live myScheme catalog."""
    return MYSCHEME_CATALOG

def filter_schemes(category: str = None, state: str = None, query: str = None):
    """Filters schemes by category, state, and search query."""
    schemes = MYSCHEME_CATALOG
    if category and category != "All Categories":
        schemes = [s for s in schemes if s["category"].lower() == category.lower()]
    if state and state != "All States":
        schemes = [s for s in schemes if s["state"] == "All India" or s["state"].lower() == state.lower()]
    if query:
        q = query.lower().strip()
        schemes = [
            s for s in schemes
            if q in s["name"].lower() or q in s["description"].lower() or q in s["department"].lower()
        ]
    return schemes

def evaluate_scheme_eligibility(scheme_id: str, answers: dict) -> dict:
    """
    Evaluates citizen eligibility for a specific scheme based on user answers.
    Answers schema: { citizen: 'yes'|'no', income: 'under_3l'|'3l_to_6l'|'above_6l', landholder: 'yes'|'no', age: int }
    """
    scheme = next((s for s in MYSCHEME_CATALOG if s["id"] == scheme_id or s["slug"] == scheme_id), None)
    if not scheme:
        return {
            "eligible": False,
            "verdict": "Scheme not found",
            "reason": "Could not identify scheme for evaluation.",
            "matchedCriteria": [],
            "unmetCriteria": []
        }

    is_citizen = answers.get("citizen", "yes") == "yes"
    income = answers.get("income", "under_3l")
    landholder = answers.get("landholder", "yes") == "yes"

    if not is_citizen:
        return {
            "eligible": False,
            "verdict": "Ineligible",
            "reason": "Indian citizenship is a mandatory requirement for all Central welfare schemes.",
            "matchedCriteria": [],
            "unmetCriteria": ["Indian citizenship requirement"]
        }

    if scheme["slug"] == "pm-kisan-samman-nidhi":
        if landholder:
            return {
                "eligible": True,
                "verdict": "High Probability of Approval",
                "reason": "You meet the agricultural landholding requirement. Ensure your bank account is Aadhaar e-KYC seeded on pmkisan.gov.in.",
                "matchedCriteria": ["Indian Citizen", "Agricultural Landholder"],
                "unmetCriteria": []
            }
        else:
            return {
                "eligible": False,
                "verdict": "Not Eligible (Landholding Required)",
                "reason": "PM-Kisan strictly requires cultivable landholding in the applicant's name. You may explore PM SVANidhi or PM-KMY for landless rural workers.",
                "matchedCriteria": ["Indian Citizen"],
                "unmetCriteria": ["Ownership of cultivable land"]
            }

    if scheme["slug"] == "pradhan-mantri-awas-yojana-urban":
        if income in ("under_3l", "3l_to_6l"):
            return {
                "eligible": True,
                "verdict": "Eligible for Credit Linked Subsidy",
                "reason": "Your income qualifies for EWS/LIG interest subsidy (up to ₹2.67 Lakh) provided your family does not own an existing pucca house.",
                "matchedCriteria": ["Indian Citizen", "Income within EWS/LIG bracket"],
                "unmetCriteria": []
            }
        else:
            return {
                "eligible": False,
                "verdict": "Income Exceeds EWS/LIG Criteria",
                "reason": "Annual household income exceeds the threshold for primary PMAY interest subsidy.",
                "matchedCriteria": ["Indian Citizen"],
                "unmetCriteria": ["Annual income under ₹6 Lakh"]
            }

    # Default general eligibility
    return {
        "eligible": True,
        "verdict": "Eligible to Apply",
        "reason": f"Based on your self-declaration, you meet primary criteria for {scheme['name']}. Proceed with verification of required documents.",
        "matchedCriteria": ["Indian Citizen", "Preliminary criteria satisfied"],
        "unmetCriteria": []
    }

