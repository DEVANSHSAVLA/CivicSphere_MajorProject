import logging
from app.config import settings

logger = logging.getLogger(__name__)

# Canonical Nyaykosh "Law as Code" (NeGD / MeitY) structured acts catalog
NYAYKOSH_LAWS = [
    {
        "id": "law-dpdp-2023",
        "slug": "dpdp-act-2023",
        "title": "Digital Personal Data Protection Act, 2023",
        "shortTitle": "DPDP Act 2023",
        "enactedBy": "Parliament of India",
        "ministry": "Ministry of Electronics and Information Technology (MeitY)",
        "commencementDate": "11 August 2023",
        "category": "Technology & Privacy",
        "source": "NeGD Nyaykosh Law-as-Code Repository",
        "officialUrl": "https://www.meity.gov.in/data-protection-framework",
        "indiaCodeUrl": "https://www.indiacode.nic.in/handle/123456789/20831",
        "overview": "Establishes a comprehensive legal framework for the processing of digital personal data that recognizes both the right of individuals to protect their personal data and the need to process such personal data for lawful purposes.",
        "keyProvisions": [
            {
                "section": "Section 4",
                "title": "Grounds for Processing Personal Data",
                "summary": "Personal data may be processed only for lawful purposes with citizen consent or for specified legitimate uses (government subsidies, medical emergencies, court orders).",
                "citizenRight": "Right to refuse processing for purposes beyond what was consented."
            },
            {
                "section": "Section 6",
                "title": "Consent Framework & Notice Requirement",
                "summary": "Consent must be free, specific, informed, unconditional, and unambiguous with clear affirmative action. Data fiduciaries must provide notice in English or any 8th Schedule language.",
                "citizenRight": "Right to withdraw consent at any time as easily as giving consent."
            },
            {
                "section": "Section 11",
                "title": "Right to Access Information about Personal Data",
                "summary": "Citizens (Data Principals) have the statutory right to obtain a summary of personal data being processed, identities of all data fiduciaries with whom data was shared, and other specified details.",
                "citizenRight": "Right to demand complete disclosure of data handling."
            },
            {
                "section": "Section 12",
                "title": "Right to Correction and Erasure of Personal Data",
                "summary": "Citizens can mandate correction of inaccurate data, completion of incomplete data, and erasure of personal data that is no longer necessary for the specified purpose.",
                "citizenRight": "Right to erasure / Right to be forgotten when purpose is fulfilled."
            },
            {
                "section": "Section 13",
                "title": "Right of Grievance Redressal",
                "summary": "Data Fiduciary must establish readily available grievance redressal mechanisms with defined resolution timelines before complaints can be taken to the Data Protection Board.",
                "citizenRight": "Direct appeal to the Data Protection Board of India."
            }
        ],
        "penalties": [
            {
                "offence": "Breach in observing obligation of Data Fiduciary in taking reasonable security safeguards to prevent personal data breach (Section 8(5))",
                "penalty": "Up to ₹250 Crore"
            },
            {
                "offence": "Failure to notify Data Protection Board and affected citizens of a personal data breach (Section 8(6))",
                "penalty": "Up to ₹200 Crore"
            },
            {
                "offence": "Breach in observance of additional obligations in relation to children (Section 9)",
                "penalty": "Up to ₹200 Crore"
            },
            {
                "offence": "Non-compliance with Data Principal duties (Section 15)",
                "penalty": "Up to ₹10,000"
            }
        ]
    },
    {
        "id": "law-cpa-2019",
        "slug": "consumer-protection-act-2019",
        "title": "Consumer Protection Act, 2019",
        "shortTitle": "CPA 2019",
        "enactedBy": "Parliament of India",
        "ministry": "Ministry of Consumer Affairs, Food and Public Distribution",
        "commencementDate": "20 July 2020",
        "category": "Consumer Rights",
        "source": "NeGD Nyaykosh Law-as-Code Repository",
        "officialUrl": "https://consumeraffairs.nic.in",
        "indiaCodeUrl": "https://www.indiacode.nic.in/handle/123456789/15256",
        "overview": "Codifies modernized protection of consumer interests, establishes the Central Consumer Protection Authority (CCPA), introduces product liability against manufacturers/sellers, and creates simplified online e-filing (e-Daakhil).",
        "keyProvisions": [
            {
                "section": "Section 2(7)",
                "title": "Definition of Consumer (Covers E-Commerce)",
                "summary": "Includes any person who buys goods or hires services through offline or online transactions, electronic means, teleshopping, direct selling, or multi-level marketing.",
                "citizenRight": "Online buyers have identical statutory standing as physical shoppers."
            },
            {
                "section": "Section 35",
                "title": "Filing Complaint before District Commission (e-Daakhil)",
                "summary": "A consumer can file a complaint with the District Commission having territorial jurisdiction where the complainant resides or works, eliminating requirement to travel to seller's location.",
                "citizenRight": "File disputes online from home via edaakhil.nic.in."
            },
            {
                "section": "Section 82-87",
                "title": "Product Liability Safeguards",
                "summary": "Product manufacturers, service providers, and product sellers are held strictly liable to compensate for any harm caused by a defective product or deficient service.",
                "citizenRight": "Right to claim full compensation for damages caused by defective goods."
            },
            {
                "section": "Section 21",
                "title": "Penalties for False or Misleading Advertisements",
                "summary": "Empowers CCPA to impose directions and penalties on manufacturers or endorsers for false claims affecting consumer choices.",
                "citizenRight": "Protection from misleading celebrity endorsements and fake dark patterns."
            }
        ],
        "penalties": [
            {
                "offence": "Manufacturing, storing, selling, or importing products containing adulterants (causing death)",
                "penalty": "Imprisonment for minimum 7 years extending to life, and fine not less than ₹10 Lakh"
            },
            {
                "offence": "False or misleading advertisement by manufacturer/endorser",
                "penalty": "Penalty up to ₹10 Lakh for first offence; up to ₹50 Lakh for subsequent offences"
            },
            {
                "offence": "Failure to comply with direction of Central Consumer Protection Authority",
                "penalty": "Imprisonment up to 6 months or fine up to ₹20 Lakh, or both"
            }
        ]
    },
    {
        "id": "law-bns-2023",
        "slug": "bharatiya-nyaya-sanhita-2023",
        "title": "Bharatiya Nyaya Sanhita, 2023",
        "shortTitle": "BNS 2023",
        "enactedBy": "Parliament of India",
        "ministry": "Ministry of Home Affairs",
        "commencementDate": "1 July 2024",
        "category": "Criminal Law & Public Order",
        "source": "NeGD Nyaykosh Law-as-Code Repository",
        "officialUrl": "https://www.mha.gov.in",
        "indiaCodeUrl": "https://www.indiacode.nic.in/handle/123456789/20833",
        "overview": "Replaces the colonial Indian Penal Code 1860 with a citizen-centric criminal justice code prioritizing victim rights, community service for minor offences, and explicit provisions against cyber fraud and organized crime.",
        "keyProvisions": [
            {
                "section": "Section 318",
                "title": "Cheating & Digital Financial Fraud",
                "summary": "Defines cheating including fraudulent inducement to deliver property or intentional deception through electronic means and UPI channels.",
                "citizenRight": "Criminal prosecution against online financial scammers."
            },
            {
                "section": "Section 69",
                "title": "Sexual Exploitation by Deceitful Means",
                "summary": "Criminalizes consensual relationships obtained through deceitful means such as false promise of employment, promotion, or marriage.",
                "citizenRight": "Statutory protection against deceitful marital or employment inducements."
            },
            {
                "section": "Section 4",
                "title": "Community Service for Petty Offences",
                "summary": "Introduces community service as a formal reformative punishment for first-time petty theft, public defamation, or non-violent minor infractions.",
                "citizenRight": "Reformative justice alternative to custodial incarceration."
            },
            {
                "section": "BNSS Section 173",
                "title": "Mandatory Registration of Zero FIR",
                "summary": "Mandates that every police station must register information of a cognizable offence regardless of territorial jurisdiction (Zero FIR) and immediately transfer it to the competent jurisdiction.",
                "citizenRight": "Police cannot refuse filing an FIR citing jurisdictional boundaries."
            }
        ],
        "penalties": [
            {
                "offence": "Cheating and dishonestly inducing delivery of property (Section 318(4))",
                "penalty": "Imprisonment up to 7 years and fine"
            },
            {
                "offence": "Organized Crime causing death (Section 111)",
                "penalty": "Death or imprisonment for life, and fine not less than ₹10 Lakh"
            },
            {
                "offence": "Snatching with force (Section 304)",
                "penalty": "Rigorous imprisonment up to 3 years and fine"
            }
        ]
    },
    {
        "id": "law-it-2000",
        "slug": "information-technology-act-2000",
        "title": "Information Technology Act, 2000",
        "shortTitle": "IT Act 2000",
        "enactedBy": "Parliament of India",
        "ministry": "Ministry of Electronics and Information Technology (MeitY)",
        "commencementDate": "17 October 2000",
        "category": "Cyber & Digital Law",
        "source": "NeGD Nyaykosh Law-as-Code Repository",
        "officialUrl": "https://www.meity.gov.in",
        "indiaCodeUrl": "https://www.indiacode.nic.in/handle/123456789/1999",
        "overview": "Provides legal recognition for transactions carried out by means of electronic data interchange and other means of electronic communication, and addresses cyber crimes, data interception, and intermediary liability.",
        "keyProvisions": [
            {
                "section": "Section 43A",
                "title": "Compensation for Failure to Protect Data",
                "summary": "Corporate entities possessing sensitive personal data must maintain reasonable security practices. Failure to prevent wrongful loss or gain obligates compensation to affected citizens.",
                "citizenRight": "Right to claim civil compensation from negligent corporations."
            },
            {
                "section": "Section 66C",
                "title": "Punishment for Identity Theft",
                "summary": "Penalizes anyone who fraudulently or dishonestly makes use of the electronic signature, password, or any other unique identification feature of any other person.",
                "citizenRight": "Criminal remedy against unauthorized password, OTP, or identity usage."
            },
            {
                "section": "Section 66D",
                "title": "Cheating by Personation using Computer Resource",
                "summary": "Specifically punishes online impersonation, phishing, fake customer support handles, or spoofed banking portals to deceive individuals.",
                "citizenRight": "Statutory prosecution against phishing and cyber impersonators."
            },
            {
                "section": "Section 79",
                "title": "Intermediary Due Diligence & Takedown Rules",
                "summary": "Social media and digital intermediaries must take down unlawful content (deepfakes, non-consensual imagery, copyright violations) within prescribed timelines upon government or court notice.",
                "citizenRight": "Right to grievance officer review and 24-hour non-consensual content removal."
            }
        ],
        "penalties": [
            {
                "offence": "Identity Theft (Section 66C)",
                "penalty": "Imprisonment up to 3 years and fine up to ₹1 Lakh"
            },
            {
                "offence": "Cheating by Personation using computer resources (Section 66D)",
                "penalty": "Imprisonment up to 3 years and fine up to ₹1 Lakh"
            },
            {
                "offence": "Cyber Terrorism (Section 66F)",
                "penalty": "Imprisonment which may extend to imprisonment for life"
            }
        ]
    },
    {
        "id": "law-rti-2005",
        "slug": "right-to-information-act-2005",
        "title": "Right to Information Act, 2005",
        "shortTitle": "RTI Act 2005",
        "enactedBy": "Parliament of India",
        "ministry": "Ministry of Personnel, Public Grievances and Pensions (DoPT)",
        "commencementDate": "12 October 2005",
        "category": "Governance & Civil Liberties",
        "source": "NeGD Nyaykosh Law-as-Code Repository",
        "officialUrl": "https://rtionline.gov.in",
        "indiaCodeUrl": "https://www.indiacode.nic.in/handle/123456789/2065",
        "overview": "Sets out the practical regime of right to information for citizens to secure access to information under the control of public authorities, in order to promote transparency and accountability in the working of every public authority.",
        "keyProvisions": [
            {
                "section": "Section 6",
                "title": "Request for Obtaining Information",
                "summary": "Any Indian citizen can submit a written or electronic request to a Central/State Public Information Officer (CPIO/SPIO) accompanied by the prescribed nominal fee (₹10). No reason for asking information needs to be given.",
                "citizenRight": "Right to inspect works, documents, records, and certified samples of material."
            },
            {
                "section": "Section 7",
                "title": "Disposal of Request & 30-Day Mandatory Limit",
                "summary": "Information must be provided within 30 days of application. If the information sought concerns the life or liberty of a person, it must be provided within 48 hours.",
                "citizenRight": "Emergency 48-hour turnaround for life and personal liberty matters."
            },
            {
                "section": "Section 19",
                "title": "Appeals Mechanism",
                "summary": "Provides First Appeal to a senior departmental officer within 30 days of rejection or delay, and a Second Appeal directly to the Central Information Commission (CIC) or State Information Commission.",
                "citizenRight": "Independent appellate review against administrative withholding."
            }
        ],
        "penalties": [
            {
                "offence": "CPIO refusing to receive application, delaying beyond 30 days without reasonable cause (Section 20(1))",
                "penalty": "Personal penalty of ₹250 per day up to maximum of ₹25,000 on the officer"
            },
            {
                "offence": "Persistent failure or knowingly giving false or misleading information",
                "penalty": "Recommendation for disciplinary action under applicable service rules"
            }
        ]
    },
    {
        "id": "law-mta-2021",
        "slug": "model-tenancy-act-2021",
        "title": "Model Tenancy Act, 2021",
        "shortTitle": "Model Tenancy Act",
        "enactedBy": "Ministry of Housing and Urban Affairs (Union Cabinet Approved)",
        "ministry": "Ministry of Housing and Urban Affairs (MoHUA)",
        "commencementDate": "2 June 2021",
        "category": "Property & Tenancy",
        "source": "NeGD Nyaykosh Law-as-Code Repository",
        "officialUrl": "https://mohua.gov.in/cms/model-tenancy-act.php",
        "indiaCodeUrl": "https://mohua.gov.in",
        "overview": "Establishes a balanced tenancy ecosystem regulating residential and commercial leasing, mandatory written rent agreements, cap on security deposits, and specialized fast-track Rent Courts.",
        "keyProvisions": [
            {
                "section": "Section 4",
                "title": "Mandatory Written Tenancy Agreement",
                "summary": "No person shall let or take on rent any premises except by an agreement in writing, which must be jointly informed to the Rent Authority within two months.",
                "citizenRight": "Protection against unwritten, arbitrary oral agreements."
            },
            {
                "section": "Section 11",
                "title": "Ceiling on Security Deposit",
                "summary": "Security deposit for residential premises cannot exceed a maximum of 2 months' rent, and for non-residential premises cannot exceed 6 months' rent.",
                "citizenRight": "Landlords prohibited from demanding exorbitant advance deposits."
            },
            {
                "section": "Section 20",
                "title": "Essential Services Protection",
                "summary": "Landlord cannot withhold any essential supply or service (water, electricity, elevator, sanitary access) to the tenant on grounds of non-payment or dispute.",
                "citizenRight": "Statutory guarantee against utility disconnection during tenancy dispute."
            }
        ],
        "penalties": [
            {
                "offence": "Tenant failing to vacate premises after expiration of tenancy order",
                "penalty": "Enhanced compensation: 2x monthly rent for first two months, and 4x monthly rent thereafter"
            },
            {
                "offence": "Landlord cutting off water or electricity unlawfully",
                "penalty": "Rent Authority penalty compensating the tenant and restoring supply immediately"
            }
        ]
    }
]

def get_all_nyaykosh_laws():
    """Returns the list of codified laws available under Nyaykosh."""
    return NYAYKOSH_LAWS

def get_nyaykosh_law_by_slug(slug: str):
    """Finds a specific law by slug."""
    for law in NYAYKOSH_LAWS:
        if law["slug"] == slug or law["id"] == slug:
            return law
    return None

def search_nyaykosh(query: str):
    """Searches laws, provisions, and penalties for matching statutory evidence."""
    q = query.lower().strip()
    results = []
    for law in NYAYKOSH_LAWS:
        matched_provisions = [
            p for p in law["keyProvisions"]
            if q in p["section"].lower() or q in p["title"].lower() or q in p["summary"].lower()
        ]
        matched_penalties = [
            pen for pen in law["penalties"]
            if q in pen["offence"].lower() or q in pen["penalty"].lower()
        ]
        if q in law["title"].lower() or q in law["overview"].lower() or matched_provisions or matched_penalties:
            results.append({
                "law": law["title"],
                "slug": law["slug"],
                "category": law["category"],
                "matchedProvisions": matched_provisions,
                "matchedPenalties": matched_penalties
            })
    return results

