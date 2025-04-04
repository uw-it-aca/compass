import { ref } from "vue";
import { useTokenStore } from "@/stores/token";

export function useCustomFetch(url, options = {}) {
  const data = ref(null);
  const error = ref(null);
  const loading = ref(false);
  const tokenStore = useTokenStore();

  async function fetchData() {
    loading.value = true;
    error.value = null;

    // Set default headers
    const defaultHeaders = {
      "Access-Control-Allow-Origin": "*",
      "X-CSRFToken": tokenStore.csrfToken,
      "X-Requested-With": "XMLHttpRequest",
    };

    // Merge headers with options
    const fetchOptions = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, fetchOptions);

      if (response.status === 403) {
        alert(
          "Your session has expired. Refresh the page to start a new session."
        );
        return;
      }

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      data.value = await response.json();
    } catch (err) {
      error.value = err.message || "An unknown error occurred.";
      console.error("Fetch error:", err);
    } finally {
      loading.value = false;
    }
  }

  return { data, error, loading, fetchData };
}
