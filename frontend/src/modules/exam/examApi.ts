import axios from "axios";

const API_BASE = "http://127.0.0.1:5000/api/code";

export const generateCode = async (description: string) => {
    try {
        console.log("Sending request to API:", { description }); // 调试日志
        const response = await axios.post(`${API_BASE}/generate`, { description });
        console.log("Response from API:", response.data); // 调试日志
        return response.data;
    } catch (error) {
        console.error("Failed to generate code:", error); // 错误日志
        throw new Error(error.response?.data?.error || "Failed to connect to server.");
    }
};