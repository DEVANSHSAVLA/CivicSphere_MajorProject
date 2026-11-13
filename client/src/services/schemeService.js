import apiClient, { simulateDelay } from "./api";
import { initialSchemes } from "../data/mockData";

const SCHEMES_STORAGE_KEY = "civicsphere_schemes";
const FEEDBACK_STORAGE_KEY = "civicsphere_feedback";

export const schemeService = {
  getSchemes() {
    const stored = localStorage.getItem(SCHEMES_STORAGE_KEY);
    if (stored) {
      try {
        return JSON.parse(stored);
      } catch (e) {
        console.error(e);
      }
    }
    localStorage.setItem(SCHEMES_STORAGE_KEY, JSON.stringify(initialSchemes));
    return initialSchemes;
  },

  async fetchLiveSchemes(filters = {}) {
    try {
      const params = {};
      if (filters.category && filters.category !== "All Categories") {
        params.category = filters.category;
      }
      if (filters.state && filters.state !== "All States") {
        params.state = filters.state;
      }
      if (filters.query) {
        params.q = filters.query;
      }

      const response = await apiClient.get("/api/schemes", { params });
      const liveList = response.data.schemes || [];
      if (liveList.length > 0) {
        // preserve saved state from local storage
        const currentSavedIds = new Set(
          this.getSchemes().filter((s) => s.isSaved).map((s) => s.id)
        );
        const merged = liveList.map((s) => ({
          ...s,
          isSaved: currentSavedIds.has(s.id),
        }));
        localStorage.setItem(SCHEMES_STORAGE_KEY, JSON.stringify(merged));
        return merged;
      }
      return this.getSchemes();
    } catch (err) {
      console.warn("Falling back to local schemes:", err);
      return this.getSchemes();
    }
  },

  async evaluateEligibility(schemeId, answers) {
    try {
      const res = await apiClient.post("/api/schemes/check-eligibility", {
        schemeId,
        answers,
      });
      return res.data.evaluation;
    } catch {
      await simulateDelay(300);
      return {
        eligible: true,
        verdict: "Eligible to Apply",
        reason: "You meet the primary criteria based on your self-declaration.",
        matchedCriteria: ["Indian Citizen", "Eligibility criteria satisfied"],
        unmetCriteria: [],
      };
    }
  },

  async toggleSaveScheme(schemeId) {
    try {
      await apiClient.post(`/api/schemes/${schemeId}/bookmark`);
    } catch {
      // offline fallback
      await simulateDelay(150);
    }
    const schemes = this.getSchemes().map((s) => {
      if (s.id === schemeId) {
        return { ...s, isSaved: !s.isSaved };
      }
      return s;
    });
    localStorage.setItem(SCHEMES_STORAGE_KEY, JSON.stringify(schemes));
    return schemes.find((s) => s.id === schemeId);
  },
};

export const feedbackService = {
  getFeedbacks() {
    const stored = localStorage.getItem(FEEDBACK_STORAGE_KEY);
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        const cleaned = parsed.filter((f) => !["fb-1", "fb-2"].includes(f.id));
        if (cleaned.length !== parsed.length) {
          localStorage.setItem(FEEDBACK_STORAGE_KEY, JSON.stringify(cleaned));
        }
        return cleaned;
      } catch (e) {
        console.error(e);
      }
    }
    return [];
  },

  async fetchFeedbacksFromServer() {
    try {
      const response = await apiClient.get("/api/feedback");
      const list = response.data.feedbacks || [];
      if (list.length > 0) {
        localStorage.setItem(FEEDBACK_STORAGE_KEY, JSON.stringify(list));
        return list;
      }
      return this.getFeedbacks();
    } catch {
      return this.getFeedbacks();
    }
  },

  async submitFeedback({ rating, category, comment, user }) {
    if (!rating) {
      throw new Error("Please select a star rating.");
    }
    const current = this.getFeedbacks();
    let newFeedback = {
      id: "fb-" + Date.now(),
      rating,
      category: category || "General",
      comment: comment || "",
      author: user?.name || "Anonymous Citizen",
      date: new Date().toLocaleDateString("en-GB", { day: 'numeric', month: 'short', year: 'numeric' }),
    };

    try {
      const response = await apiClient.post("/api/feedback", {
        rating,
        category: category || "General",
        comment: comment || "",
        author: user?.name || "Anonymous Citizen",
      });
      if (response.data?.feedback) {
        newFeedback = response.data.feedback;
      }
    } catch (err) {
      console.warn("Backend feedback submission fallback to local:", err);
      await simulateDelay(250);
    }

    const updated = [newFeedback, ...current];
    localStorage.setItem(FEEDBACK_STORAGE_KEY, JSON.stringify(updated));
    return newFeedback;
  }
};

