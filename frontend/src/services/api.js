import axios from "axios";

const API = axios.create({
    baseURL: "https://explainable-ai-clinical-decision-support-l3xi.onrender.com",
    timeout: 120000
});

API.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access_token");

        if (token) {
            config.headers = config.headers || {};
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

API.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error("API ERROR:", error);
        return Promise.reject(error);
    }
);

export default API;