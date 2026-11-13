import apiClient, { simulateDelay } from "./api";
import { popularLegalTopics } from "../data/mockData";

export const legalService = {
  async getTopics() {
    try {
      const res = await apiClient.get("/api/legal/topics");
      return res.data.topics || popularLegalTopics;
    } catch {
      return popularLegalTopics;
    }
  },

  async getNyaykoshCatalog() {
    try {
      const res = await apiClient.get("/api/legal/nyaykosh");
      return res.data.laws || [];
    } catch (err) {
      console.warn("Error fetching Nyaykosh laws:", err);
      return [];
    }
  },

  async getNyaykoshLawDetail(slug) {
    try {
      const res = await apiClient.get(`/api/legal/nyaykosh/${slug}`);
      return res.data.law;
    } catch (err) {
      console.warn(`Error fetching Nyaykosh law ${slug}:`, err);
      return null;
    }
  },

  async searchStatutes(query) {
    if (!query || query.length < 2) return [];
    try {
      const res = await apiClient.get("/api/legal/search", { params: { q: query } });
      return res.data.results || [];
    } catch {
      return [];
    }
  },

  async consultStatute(query, lawSlug = null) {
    try {
      const res = await apiClient.post("/api/legal/query", { query, lawSlug });
      return res.data.guidance;
    } catch {
      await simulateDelay(400);
      return null;
    }
  }
};

