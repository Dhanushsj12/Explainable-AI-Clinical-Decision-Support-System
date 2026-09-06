import axios from "axios";

const API = axios.create({
    baseURL: "https://clinical-cdss-backend.onrender.com"
});


// =========================================================
// ADD JWT TOKEN TO API REQUESTS
// =========================================================

API.interceptors.request.use(
    (config) => {

        const token = localStorage.getItem("access_token");

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },

    (error) => {
        return Promise.reject(error);
    }
);


export default API;