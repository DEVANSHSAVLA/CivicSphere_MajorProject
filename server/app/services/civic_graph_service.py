import logging

logger = logging.getLogger(__name__)

GRAPH_DATA = {
    "metadata": {
        "title": "CivicSphere National Civic & Legal Knowledge Graph",
        "version": "2.0",
        "dataSources": ["Constitution of India", "NeGD Nyaykosh", "myScheme / API Setu", "India Code", "CPGRAMS"],
    },
    "nodes": [
        {
            "id": "n-constitution",
            "label": "Constitution of India",
            "type": "Supreme Law",
            "category": "Constitutional Law",
            "color": "#15965B",
            "description": "The supreme lex of the Republic of India adopted on 26 November 1949, empowering citizen rights and establishing government institutions.",
            "portal": "https://www.india.gov.in/my-government/constitution-india",
        },
        {
            "id": "n-art21",
            "label": "Article 21: Protection of Life, Liberty & Privacy",
            "type": "Constitutional Article",
            "category": "Fundamental Rights",
            "color": "#10B981",
            "description": "No person shall be deprived of his life or personal liberty except according to procedure established by law. Encompasses Right to Privacy (Puttaswamy 2017) and Right to Clean Environment.",
            "portal": "https://www.indiacode.nic.in",
        },
        {
            "id": "n-art19",
            "label": "Article 19(1)(a): Freedom of Speech & Right to Know",
            "type": "Constitutional Article",
            "category": "Fundamental Rights",
            "color": "#10B981",
            "description": "Guarantees freedom of speech and expression, out of which the Supreme Court derived the citizen's fundamental right to obtain public information.",
            "portal": "https://www.indiacode.nic.in",
        },
        {
            "id": "n-art14",
            "label": "Article 14: Equality before Law",
            "type": "Constitutional Article",
            "category": "Fundamental Rights",
            "color": "#10B981",
            "description": "Prohibits arbitrary state actions and guarantees equal protection of the laws to all citizens and residents of India.",
            "portal": "https://www.indiacode.nic.in",
        },
        {
            "id": "n-dpdp",
            "label": "Digital Personal Data Protection Act, 2023",
            "type": "Legislation",
            "category": "Technology & Privacy",
            "color": "#3B82F6",
            "description": "Codified under NeGD Nyaykosh Law-as-Code. Protects citizen digital personal data and penalizes unauthorized corporate data breaches up to ₹250 Crore.",
            "portal": "https://www.meity.gov.in",
        },
        {
            "id": "n-cpa",
            "label": "Consumer Protection Act, 2019",
            "type": "Legislation",
            "category": "Consumer Rights",
            "color": "#3B82F6",
            "description": "Codified under NeGD Nyaykosh. Empowers buyers against misleading advertisements, defective products, e-commerce frauds, and enables online dispute e-filing via e-Daakhil.",
            "portal": "https://edaakhil.nic.in",
        },
        {
            "id": "n-bns",
            "label": "Bharatiya Nyaya Sanhita, 2023",
            "type": "Legislation",
            "category": "Criminal Law",
            "color": "#3B82F6",
            "description": "Modern criminal code replacing the IPC. Explicitly penalizes financial cyber scams (Section 318), protects women, and mandates Zero FIR across India.",
            "portal": "https://www.mha.gov.in",
        },
        {
            "id": "n-rti",
            "label": "Right to Information Act, 2005",
            "type": "Legislation",
            "category": "Civil Liberties",
            "color": "#3B82F6",
            "description": "Mandates public authorities to reply to citizen information queries within 30 days (or 48 hours for matters of life and liberty).",
            "portal": "https://rtionline.gov.in",
        },
        {
            "id": "n-meity",
            "label": "Ministry of Electronics & IT (MeitY)",
            "type": "Authority",
            "category": "Central Ministry",
            "color": "#8B5CF6",
            "description": "Executing nodal authority for Digital India, Nyaykosh Law as Code, API Setu, and the Data Protection Board of India.",
            "portal": "https://www.meity.gov.in",
        },
        {
            "id": "n-mha",
            "label": "Ministry of Home Affairs & Cyber Cell (1930)",
            "type": "Authority",
            "category": "Central Ministry",
            "color": "#8B5CF6",
            "description": "Manages internal security, police reforms under BNS/BNSS, and the National Cyber Crime Reporting Portal (1930 / cybercrime.gov.in).",
            "portal": "https://cybercrime.gov.in",
        },
        {
            "id": "n-cic",
            "label": "Central Information Commission (CIC)",
            "type": "Judicial Forum",
            "category": "Statutory Commission",
            "color": "#EC4899",
            "description": "Independent statutory tribunal adjudicating Second Appeals filed by citizens against non-responsive public authorities under RTI Act.",
            "portal": "https://cic.gov.in",
        },
        {
            "id": "n-ncdrc",
            "label": "National Consumer Disputes Redressal Commission",
            "type": "Judicial Forum",
            "category": "Statutory Commission",
            "color": "#EC4899",
            "description": "Quasi-judicial commission established under Consumer Protection Act dealing with claims exceeding ₹2 Crore and appellate matters.",
            "portal": "http://ncdrc.nic.in",
        },
        {
            "id": "n-pmkisan",
            "label": "PM Kisan Samman Nidhi",
            "type": "Scheme",
            "category": "Agriculture",
            "color": "#F59E0B",
            "description": "Direct benefit cash assistance of ₹6,000/year to landholder farmer families under the Ministry of Agriculture.",
            "portal": "https://pmkisan.gov.in",
        },
        {
            "id": "n-pmjay",
            "label": "Ayushman Bharat PM-JAY",
            "type": "Scheme",
            "category": "Health",
            "color": "#F59E0B",
            "description": "National health assurance scheme providing up to ₹5 Lakh/year cashless coverage for hospitalization.",
            "portal": "https://pmjay.gov.in",
        },
        {
            "id": "n-cpgrams",
            "label": "CPGRAMS Public Grievance Portal",
            "type": "Redressal Portal",
            "category": "Citizen Service",
            "color": "#06B6D4",
            "description": "Centralized online platform run by DARPG for citizens to lodge grievances against any Central or State government department.",
            "portal": "https://pgportal.gov.in",
        }
    ],
    "links": [
        {"source": "n-constitution", "target": "n-art21", "relationship": "enshrines"},
        {"source": "n-constitution", "target": "n-art19", "relationship": "enshrines"},
        {"source": "n-constitution", "target": "n-art14", "relationship": "enshrines"},
        {"source": "n-art21", "target": "n-dpdp", "relationship": "constitutional basis for"},
        {"source": "n-art21", "target": "n-bns", "relationship": "liberty safeguarded by"},
        {"source": "n-art19", "target": "n-rti", "relationship": "right to know derived from"},
        {"source": "n-meity", "target": "n-dpdp", "relationship": "administers & codifies under Nyaykosh"},
        {"source": "n-mha", "target": "n-bns", "relationship": "enforces through police"},
        {"source": "n-rti", "target": "n-cic", "relationship": "appellate authority"},
        {"source": "n-cpa", "target": "n-ncdrc", "relationship": "dispute resolution forum"},
        {"source": "n-art21", "target": "n-pmjay", "relationship": "right to health realization"},
        {"source": "n-art14", "target": "n-pmkisan", "relationship": "equitable welfare allocation"},
        {"source": "n-constitution", "target": "n-cpgrams", "relationship": "democratic accountability platform"},
    ]
}

def get_civic_knowledge_graph():
    """Returns the entire interconnected civic knowledge graph."""
    return GRAPH_DATA

def get_entity_connections(entity_id: str):
    """Finds all incoming and outgoing connections for a specific node."""
    nodes = {n["id"]: n for n in GRAPH_DATA["nodes"]}
    selected = nodes.get(entity_id)
    if not selected:
        return None

    connected_links = [
        l for l in GRAPH_DATA["links"]
        if l["source"] == entity_id or l["target"] == entity_id
    ]

    related_nodes = []
    for l in connected_links:
        neighbor_id = l["target"] if l["source"] == entity_id else l["source"]
        if neighbor_id in nodes:
            related_nodes.append({
                "node": nodes[neighbor_id],
                "relationship": l["relationship"],
                "direction": "outgoing" if l["source"] == entity_id else "incoming"
            })

    return {
        "selectedNode": selected,
        "connections": related_nodes
    }

