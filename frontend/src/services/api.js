import axios from "axios";

const API = axios.create({
    baseURL: "https://clinical-cdss-backend.onrender.com"
});

export default API;