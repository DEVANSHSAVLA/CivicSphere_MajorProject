import apiClient from "./api";
import { civicKnowledgeGraph } from "../data/mockData";

export const civicKnowledgeService = {
  async getKnowledgeGraph(nodeType = "all") {
    try {
      const params = nodeType && nodeType !== "all" ? { node_type: nodeType } : {};
      const res = await apiClient.get("/api/civic-knowledge/graph", { params });
      return {
        nodes: res.data.nodes || civicKnowledgeGraph.nodes,
        links: res.data.links || civicKnowledgeGraph.links,
        metadata: res.data.metadata || {}
      };
    } catch {
      return civicKnowledgeGraph;
    }
  },

  async getEntityDetails(entityId) {
    try {
      const res = await apiClient.get(`/api/civic-knowledge/entities/${entityId}`);
      return res.data.entity;
    } catch {
      return null;
    }
  }
};

