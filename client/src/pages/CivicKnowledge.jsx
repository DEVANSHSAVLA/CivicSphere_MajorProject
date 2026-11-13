import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  Share2,
  Search,
  Filter,
  Info,
  ExternalLink,
  ShieldCheck,
  Sparkles,
  Layers,
  ArrowRight,
  Globe,
  Database,
} from "lucide-react";
import PageHeader from "../components/common/PageHeader";
import Badge from "../components/common/Badge";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import { civicKnowledgeService } from "../services/civicKnowledgeService";
import { civicKnowledgeGraph as defaultGraph } from "../data/mockData";

export default function CivicKnowledge() {
  const [graphData, setGraphData] = useState(defaultGraph);
  const [selectedNode, setSelectedNode] = useState(defaultGraph.nodes[0]);
  const [filterType, setFilterType] = useState("all");
  const [search, setSearch] = useState("");

  const types = [
    "all",
    "Supreme Law",
    "Constitutional Article",
    "Legislation",
    "Authority",
    "Scheme",
    "Judicial Forum",
    "Redressal Portal",
  ];

  useEffect(() => {
    let active = true;
    civicKnowledgeService
      .getKnowledgeGraph(filterType)
      .then((data) => {
        if (active && data?.nodes) {
          setGraphData(data);
          setSelectedNode((prev) => {
            if (prev && data.nodes.some((n) => n.id === prev.id)) {
              return prev;
            }
            return data.nodes[0] || null;
          });
        }
      });

    return () => {
      active = false;
    };
  }, [filterType]);

  const filteredNodes = graphData.nodes.filter((node) => {
    const matchesSearch =
      node.label.toLowerCase().includes(search.toLowerCase()) ||
      (node.category && node.category.toLowerCase().includes(search.toLowerCase()));
    const matchesType =
      filterType === "all" ||
      node.type.toLowerCase() === filterType.toLowerCase() ||
      (node.category && node.category.toLowerCase() === filterType.toLowerCase());
    return matchesSearch && matchesType;
  });

  const connectedLinks = graphData.links.filter(
    (l) => l.source === selectedNode?.id || l.target === selectedNode?.id
  );

  return (
    <div className="space-y-6">
      <PageHeader
        title="Civic Knowledge Graph"
        subtitle="Explore interconnected Indian legal codes, welfare schemes, and civil liberties"
        badge={
          <Badge variant="emerald" size="sm">
            Live Linked Graph (NeGD & myScheme)
          </Badge>
        }
      >
        <Link to="/chat">
          <Button variant="primary" size="sm" leftIcon={Sparkles}>
            Query Graph in Chat
          </Button>
        </Link>
      </PageHeader>

      {/* Info Notice */}
      <div className="bg-[#15965B]/10 border border-[#15965B]/20 rounded-xl p-3.5 flex items-start gap-3">
        <ShieldCheck className="w-5 h-5 text-[#15965B] shrink-0 mt-0.5" />
        <div className="text-xs text-[#087443] leading-relaxed">
          <strong>Evidence Grounded Civic Graph:</strong> Real-time mapping linking the Constitution of India, codified Central Acts (from <strong>NeGD Nyaykosh</strong>), central welfare schemes (from <strong>myScheme / API Setu</strong>), and statutory citizen grievance portals (CPGRAMS / 1930).
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Interactive Node Explorer (8 cols) */}
        <div className="lg:col-span-8 space-y-4">
          <div className="bg-white rounded-2xl border border-[#E5EAE8] p-5 shadow-xs">
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 mb-4">
              <h3 className="text-sm font-bold text-[#17212B] flex items-center gap-2">
                <Layers className="w-4 h-4 text-[#15965B]" />
                <span>Statutory Entities & Nodes ({filteredNodes.length})</span>
              </h3>

              <div className="flex items-center gap-2">
                <input
                  type="text"
                  placeholder="Filter entities..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="bg-[#F5F8F7] border border-[#E5EAE8] rounded-lg px-2.5 py-1 text-xs outline-none focus:border-[#15965B]"
                />
                <select
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value)}
                  className="bg-[#F5F8F7] border border-[#E5EAE8] rounded-lg px-2.5 py-1 text-xs outline-none font-semibold text-[#17212B]"
                >
                  {types.map((t) => (
                    <option key={t} value={t}>
                      {t === "all" ? "All Types" : t}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Nodes Grid Canvas */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 min-h-[360px] bg-[#F5F8F7]/50 p-4 rounded-xl border border-dashed border-[#E5EAE8]">
              {filteredNodes.length === 0 ? (
                <div className="col-span-2 text-center py-12 text-xs text-[#64748B]">
                  No statutory nodes match your filter criteria.
                </div>
              ) : (
                filteredNodes.map((node) => {
                  const isSelected = selectedNode?.id === node.id;
                  return (
                    <div
                      key={node.id}
                      onClick={() => setSelectedNode(node)}
                      className={`p-3.5 rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
                        isSelected
                          ? "bg-white border-[#15965B] shadow-md ring-2 ring-[#15965B]/20 scale-[1.01]"
                          : "bg-white border-[#E5EAE8] hover:border-[#CBD5E1] hover:shadow-xs"
                      }`}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <span className="text-xs font-bold text-[#17212B] line-clamp-1">
                            {node.label}
                          </span>
                          <span className="text-[10px] text-[#64748B] block mt-0.5">
                            {node.category || node.type}
                          </span>
                        </div>
                        <span
                          className="w-3 h-3 rounded-full shrink-0 mt-0.5"
                          style={{ backgroundColor: node.color }}
                        />
                      </div>
                      <div className="mt-3 flex items-center justify-between text-[11px] text-[#64748B]">
                        <span className="bg-[#F5F8F7] px-2 py-0.5 rounded text-[10px] font-semibold text-[#17212B] border border-[#E5EAE8]">
                          {node.type}
                        </span>
                        <span className="text-[#15965B] font-semibold">Inspect →</span>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>

        {/* Selected Entity Details Panel (4 cols) */}
        <div className="lg:col-span-4">
          <Card className="p-5 space-y-4">
            {selectedNode ? (
              <>
                <div className="pb-3 border-b border-[#E5EAE8]">
                  <div className="flex items-center gap-2 mb-1">
                    <span
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: selectedNode.color }}
                    />
                    <Badge variant="emerald" size="xs">
                      {selectedNode.type}
                    </Badge>
                  </div>
                  <h3 className="text-base font-bold text-[#17212B]">
                    {selectedNode.label}
                  </h3>
                  {selectedNode.description && (
                    <p className="text-xs text-[#64748B] mt-1.5 leading-relaxed">
                      {selectedNode.description}
                    </p>
                  )}
                  {selectedNode.portal && (
                    <a
                      href={selectedNode.portal}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-1 text-[11px] font-bold text-[#15965B] hover:underline mt-2"
                    >
                      <Globe className="w-3 h-3" />
                      <span>Official Portal Source</span>
                      <ExternalLink className="w-2.5 h-2.5" />
                    </a>
                  )}
                </div>

                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-[#64748B] mb-2 flex items-center gap-1.5">
                    <Database className="w-3.5 h-3.5 text-[#15965B]" />
                    <span>Interconnected Statutory Links</span>
                  </h4>
                  {connectedLinks.length === 0 ? (
                    <p className="text-xs text-[#64748B]">No direct relationships mapped.</p>
                  ) : (
                    <div className="space-y-2">
                      {connectedLinks.map((link, idx) => {
                        const targetNode = graphData.nodes.find(
                          (n) => n.id === (link.source === selectedNode.id ? link.target : link.source)
                        );
                        return (
                          <div
                            key={idx}
                            onClick={() => targetNode && setSelectedNode(targetNode)}
                            className="p-2.5 rounded-lg bg-[#F5F8F7] border border-[#E5EAE8] hover:border-[#15965B]/40 transition cursor-pointer text-xs"
                          >
                            <span className="text-[10px] text-[#64748B] uppercase font-bold block">
                              {link.relationship}
                            </span>
                            <span className="font-semibold text-[#17212B] flex items-center justify-between mt-0.5">
                              <span>{targetNode?.label}</span>
                              <ArrowRight className="w-3 h-3 text-[#15965B]" />
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>

                <div className="pt-2">
                  <Link to="/chat">
                    <Button variant="outline" size="sm" className="w-full">
                      Ask Questions About {selectedNode.label.split(" ")[0]}
                    </Button>
                  </Link>
                </div>
              </>
            ) : (
              <div className="text-center py-8 text-xs text-[#64748B]">
                Select an entity to explore statutory connections.
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
}
