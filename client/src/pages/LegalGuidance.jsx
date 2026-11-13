import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Scale,
  Building,
  Users,
  Briefcase,
  ShieldAlert,
  ShieldCheck,
  Send,
  Search,
  BookOpen,
  ArrowRight,
  ExternalLink,
  Sparkles,
  Info,
  Layers,
  FileCode,
  AlertTriangle,
} from "lucide-react";
import PageHeader from "../components/common/PageHeader";
import Badge from "../components/common/Badge";
import Button from "../components/common/Button";
import Card from "../components/common/Card";
import { popularLegalTopics } from "../data/mockData";
import { legalService } from "../services/legalService";
import { useToast } from "../context/ToastContext";

export default function LegalGuidance() {
  const navigate = useNavigate();
  const { showToast } = useToast();

  const [activeTab, setActiveTab] = useState("topics"); // "topics" | "nyaykosh"
  const [topics, setTopics] = useState(popularLegalTopics);
  const [selectedTopic, setSelectedTopic] = useState(popularLegalTopics[0]);
  const [nyaykoshLaws, setNyaykoshLaws] = useState([]);
  const [selectedLaw, setSelectedLaw] = useState(null);
  const [query, setQuery] = useState("");

  useEffect(() => {
    let mounted = true;
    legalService.getTopics().then((res) => {
      if (mounted && res && res.length > 0) {
        setTopics(res);
        setSelectedTopic(res[0]);
      }
    });

    legalService.getNyaykoshCatalog().then((laws) => {
      if (mounted && laws && laws.length > 0) {
        setNyaykoshLaws(laws);
        setSelectedLaw(laws[0]);
      }
    });

    return () => {
      mounted = false;
    };
  }, []);

  const getTopicIcon = (iconName) => {
    switch (iconName) {
      case "Building":
        return Building;
      case "Users":
        return Users;
      case "Scale":
        return Scale;
      case "Briefcase":
        return Briefcase;
      case "ShieldAlert":
        return ShieldAlert;
      case "ShieldCheck":
        return ShieldCheck;
      default:
        return Scale;
    }
  };

  const getColorStyles = (color) => {
    switch (color) {
      case "amber":
        return {
          bg: "bg-amber-50",
          text: "text-amber-700",
          border: "border-amber-200",
        };
      case "blue":
        return {
          bg: "bg-blue-50",
          text: "text-blue-700",
          border: "border-blue-200",
        };
      case "emerald":
        return {
          bg: "bg-emerald-50",
          text: "text-[#15965B]",
          border: "border-emerald-200",
        };
      case "rose":
        return {
          bg: "bg-rose-50",
          text: "text-rose-700",
          border: "border-rose-200",
        };
      case "purple":
        return {
          bg: "bg-purple-50",
          text: "text-purple-700",
          border: "border-purple-200",
        };
      case "cyan":
        return {
          bg: "bg-cyan-50",
          text: "text-cyan-700",
          border: "border-cyan-200",
        };
      default:
        return {
          bg: "bg-slate-50",
          text: "text-slate-700",
          border: "border-slate-200",
        };
    }
  };

  const handleAskInChat = (customQuery = null) => {
    const text = customQuery || query;
    if (!text.trim()) {
      showToast("Please enter a legal query first.", "error");
      return;
    }
    navigate("/chat", { state: { initialPrompt: text } });
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Legal Guidance"
        subtitle="Explore verified codified statutes and AI legal intelligence"
        badge={
          <Badge variant="emerald" size="sm">
            Powered by NeGD Nyaykosh & India Code
          </Badge>
        }
      />

      {/* Search Input Box */}
      <div className="bg-white rounded-2xl border border-[#E5EAE8] p-2 shadow-xs">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleAskInChat();
          }}
          className="flex items-center gap-2"
        >
          <Search className="w-5 h-5 text-[#64748B] ml-3 shrink-0" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask any legal question (e.g. rights under DPDP Act 2023, tenant eviction notice, zero FIR)..."
            className="flex-1 bg-transparent border-0 text-xs sm:text-sm text-[#17212B] placeholder-[#94A3B8] outline-none py-2 px-1"
          />
          <button
            type="submit"
            className="w-10 h-10 rounded-xl bg-[#15965B] hover:bg-[#087443] text-white flex items-center justify-center transition shadow-xs shrink-0 cursor-pointer"
            title="Search statutory database"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>

      {/* Module Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-[#E5EAE8] pb-1">
        <button
          onClick={() => setActiveTab("topics")}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition cursor-pointer ${
            activeTab === "topics"
              ? "bg-[#15965B] text-white shadow-xs"
              : "bg-white text-[#64748B] hover:text-[#17212B] border border-[#E5EAE8]"
          }`}
        >
          <BookOpen className="w-4 h-4" />
          <span>Popular Legal Topics</span>
        </button>

        <button
          onClick={() => setActiveTab("nyaykosh")}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition cursor-pointer ${
            activeTab === "nyaykosh"
              ? "bg-[#15965B] text-white shadow-xs"
              : "bg-white text-[#64748B] hover:text-[#17212B] border border-[#E5EAE8]"
          }`}
        >
          <FileCode className="w-4 h-4 text-[#15965B]" />
          <span>Nyaykosh Codified Acts ("Law as Code")</span>
          <span className="text-[10px] bg-emerald-100 text-[#087443] px-2 py-0.5 rounded-full font-semibold">
            Live
          </span>
        </button>
      </div>

      {/* TAB 1: Popular Topics */}
      {activeTab === "topics" && (
        <div className="space-y-6">
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-[#64748B] mb-3">
              Browse by Legal Category
            </h3>

            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5">
              {topics.map((topic) => {
                const Icon = getTopicIcon(topic.icon);
                const style = getColorStyles(topic.color);
                const isSelected = selectedTopic?.id === topic.id;

                return (
                  <button
                    key={topic.id}
                    onClick={() => setSelectedTopic(topic)}
                    className={`bg-white rounded-2xl border p-4 text-center transition-all duration-200 flex flex-col items-center justify-center cursor-pointer group ${
                      isSelected
                        ? "border-[#15965B] shadow-md ring-1 ring-[#15965B]/20 bg-[#F5F8F7]"
                        : "border-[#E5EAE8] hover:border-[#CBD5E1] hover:shadow-xs"
                    }`}
                  >
                    <div
                      className={`w-12 h-12 rounded-xl ${style.bg} ${style.text} flex items-center justify-center mb-2.5 group-hover:scale-105 transition-transform`}
                    >
                      <Icon className="w-6 h-6" />
                    </div>
                    <h4 className="text-xs sm:text-sm font-bold text-[#17212B] group-hover:text-[#15965B] transition-colors">
                      {topic.title}
                    </h4>
                  </button>
                );
              })}
            </div>
          </div>

          {selectedTopic && (
            <div className="bg-white rounded-2xl border border-[#E5EAE8] p-6 shadow-xs space-y-5 animate-in fade-in duration-150">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-[#E5EAE8]">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-lg font-bold text-[#17212B]">
                      {selectedTopic.title} Knowledge Matrix
                    </h3>
                    <Badge variant={selectedTopic.color || "emerald"} size="xs">
                      Evidence Grounded
                    </Badge>
                  </div>
                  <p className="text-xs text-[#64748B] mt-1">{selectedTopic.tagline}</p>
                </div>

                <Button
                  variant="primary"
                  size="sm"
                  leftIcon={Sparkles}
                  onClick={() =>
                    handleAskInChat(`Legal consultation regarding ${selectedTopic.title}`)
                  }
                >
                  Consult in Chat
                </Button>
              </div>

              <p className="text-xs sm:text-sm text-[#17212B] leading-relaxed">
                {selectedTopic.description}
              </p>

              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#64748B] mb-3">
                  Key Codified Provisions & Precedents
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                  {selectedTopic.relevantSections.map((sec, idx) => (
                    <div
                      key={idx}
                      className="p-4 rounded-xl bg-[#F5F8F7] border border-[#E5EAE8] flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs font-bold text-[#15965B]">
                            {sec.section}
                          </span>
                          <span className="text-[10px] text-[#64748B] font-medium bg-white px-2 py-0.5 rounded border border-[#E5EAE8]">
                            Central Act
                          </span>
                        </div>
                        <p className="text-xs font-semibold text-[#17212B] mb-1.5">
                          {sec.code}
                        </p>
                        <p className="text-xs text-[#64748B] leading-relaxed">
                          {sec.summary}
                        </p>
                      </div>

                      <div className="mt-3 pt-2 border-t border-[#E5EAE8] flex justify-end">
                        <a
                          href="https://www.indiacode.nic.in"
                          target="_blank"
                          rel="noreferrer"
                          className="text-[11px] font-bold text-[#15965B] hover:underline inline-flex items-center gap-1"
                        >
                          <span>Read Section Text</span>
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#64748B] mb-2.5">
                  Frequently Inquired Citizen Questions
                </h4>
                <div className="space-y-2">
                  {selectedTopic.sampleQueries.map((q, idx) => (
                    <div
                      key={idx}
                      onClick={() => handleAskInChat(q)}
                      className="p-3 rounded-xl bg-white border border-[#E5EAE8] hover:border-[#15965B]/40 hover:bg-[#F5F8F7] transition cursor-pointer flex items-center justify-between group"
                    >
                      <span className="text-xs font-medium text-[#17212B] group-hover:text-[#15965B]">
                        "{q}"
                      </span>
                      <span className="text-xs font-bold text-[#15965B] inline-flex items-center gap-1">
                        <span>Ask AI</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 2: Nyaykosh Law-as-Code Explorer */}
      {activeTab === "nyaykosh" && (
        <div className="space-y-6">
          <div className="bg-[#15965B]/10 border border-[#15965B]/20 rounded-xl p-4 flex items-start gap-3">
            <FileCode className="w-5 h-5 text-[#15965B] shrink-0 mt-0.5" />
            <div className="text-xs text-[#087443] leading-relaxed">
              <strong className="font-bold">NeGD Nyaykosh "Law as Code" Initiative:</strong> Machine-readable codified central acts structured into sections, citizen rights, and statutory penalty schedules by the National e-Governance Division (MeitY).
            </div>
          </div>

          {/* Laws Selector Carousel */}
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-[#64748B] mb-3">
              Codified Acts Repository ({nyaykoshLaws.length} Acts)
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {nyaykoshLaws.map((law) => {
                const isSelected = selectedLaw?.slug === law.slug;
                return (
                  <div
                    key={law.slug}
                    onClick={() => setSelectedLaw(law)}
                    className={`p-4 rounded-xl border transition cursor-pointer flex flex-col justify-between ${
                      isSelected
                        ? "border-[#15965B] bg-[#15965B]/5 shadow-sm"
                        : "border-[#E5EAE8] bg-white hover:border-[#CBD5E1]"
                    }`}
                  >
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-[#15965B] bg-[#15965B]/10 px-2 py-0.5 rounded">
                          {law.category}
                        </span>
                        <span className="text-[11px] text-[#64748B]">
                          {law.commencementDate}
                        </span>
                      </div>
                      <h4 className="text-sm font-bold text-[#17212B] mt-1.5 line-clamp-1">
                        {law.title}
                      </h4>
                      <p className="text-xs text-[#64748B] mt-1 line-clamp-2">
                        {law.overview}
                      </p>
                    </div>

                    <div className="mt-3 pt-2 border-t border-[#E5EAE8] flex items-center justify-between text-xs">
                      <span className="text-[#64748B] text-[11px]">
                        {law.keyProvisions?.length || 0} Key Sections
                      </span>
                      <span className="font-semibold text-[#15965B]">
                        View Clauses →
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Selected Law Details */}
          {selectedLaw && (
            <div className="bg-white rounded-2xl border border-[#E5EAE8] p-6 shadow-xs space-y-6 animate-in fade-in duration-150">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[#E5EAE8]">
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <h3 className="text-lg font-bold text-[#17212B]">
                      {selectedLaw.title}
                    </h3>
                    <Badge variant="blue" size="xs">
                      {selectedLaw.ministry}
                    </Badge>
                  </div>
                  <p className="text-xs text-[#64748B] mt-1">
                    Commenced: {selectedLaw.commencementDate} • Source: {selectedLaw.source}
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <a
                    href={selectedLaw.indiaCodeUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center"
                  >
                    <Button variant="outline" size="sm" rightIcon={ExternalLink}>
                      India Code Text
                    </Button>
                  </a>
                  <Button
                    variant="primary"
                    size="sm"
                    leftIcon={Sparkles}
                    onClick={() =>
                      handleAskInChat(
                        `Explain my statutory citizen rights under the ${selectedLaw.title}`
                      )
                    }
                  >
                    Consult in Chat
                  </Button>
                </div>
              </div>

              {/* Law Overview */}
              <div className="p-4 bg-[#F5F8F7] rounded-xl border border-[#E5EAE8]">
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#64748B] mb-1">
                  Legislative Objective & Scope
                </h4>
                <p className="text-xs sm:text-sm text-[#17212B] leading-relaxed">
                  {selectedLaw.overview}
                </p>
              </div>

              {/* Section-by-Section Breakdown */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#64748B] mb-3 flex items-center gap-2">
                  <Layers className="w-4 h-4 text-[#15965B]" />
                  <span>Codified Sections & Citizen Rights</span>
                </h4>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                  {selectedLaw.keyProvisions?.map((prov, i) => (
                    <div
                      key={i}
                      className="p-4 rounded-xl border border-[#E5EAE8] bg-white hover:border-[#15965B]/40 transition space-y-2"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-[#15965B] bg-[#15965B]/10 px-2 py-0.5 rounded">
                          {prov.section}
                        </span>
                        <span className="text-[11px] font-semibold text-[#17212B]">
                          {prov.title}
                        </span>
                      </div>
                      <p className="text-xs text-[#64748B] leading-relaxed">
                        {prov.summary}
                      </p>
                      <div className="pt-2 border-t border-[#E5EAE8] flex items-center gap-1.5 text-[11px] font-semibold text-[#087443]">
                        <ShieldCheck className="w-3.5 h-3.5 text-[#15965B] shrink-0" />
                        <span>Citizen Right: {prov.citizenRight}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Penalty Schedules */}
              {selectedLaw.penalties?.length > 0 && (
                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-rose-700 mb-3 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-rose-600" />
                    <span>Statutory Penalty Schedules</span>
                  </h4>

                  <div className="divide-y divide-[#E5EAE8] border border-[#E5EAE8] rounded-xl overflow-hidden">
                    {selectedLaw.penalties.map((pen, i) => (
                      <div
                        key={i}
                        className="p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-2 bg-white hover:bg-rose-50/30 transition text-xs"
                      >
                        <span className="font-medium text-[#17212B]">
                          {pen.offence}
                        </span>
                        <span className="font-bold text-rose-700 bg-rose-50 border border-rose-200 px-2.5 py-1 rounded-lg shrink-0">
                          {pen.penalty}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
