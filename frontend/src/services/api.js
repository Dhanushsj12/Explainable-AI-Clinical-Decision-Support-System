import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:5000",
    timeout: 120000
});


// ============================================================
// ADD JWT TOKEN TO EVERY REQUEST
// ============================================================

API.interceptors.request.use(
    (config) => {

        const token =
            localStorage.getItem("access_token");

        if (token) {

            config.headers = config.headers || {};

            config.headers.Authorization =
                `Bearer ${token}`;

        }

        return config;

    },

    (error) => {

        return Promise.reject(error);

    }
);


// ============================================================
// HANDLE RESPONSE ERRORS
// ============================================================

API.interceptors.response.use(

    (response) => {

        return response;

    },

    (error) => {

        console.error(
            "API ERROR:",
            error
        );

        return Promise.reject(
            error
        );

    }

);


export default API;