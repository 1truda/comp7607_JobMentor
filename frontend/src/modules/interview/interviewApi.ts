import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000";

// API 封装

/**
 * 选择面试主题
 * @param theme 面试主题
 * @returns 会话 ID
 */
export const selectTheme = async (theme: string): Promise<{ session_id: number }> => {
    const response = await axios.post(`${BASE_URL}/select_theme`, { theme });
    return response.data;
};

/**
 * 开始面试，获取第一个问题
 * @param sessionId 会话 ID
 * @returns 第一个问题
 */
export const startInterview = async (sessionId: number): Promise<{ question: string }> => {
    const response = await axios.post(`${BASE_URL}/start_interview`, { session_id: sessionId });
    return response.data;
};

/**
 * 提交用户回答并获取下一个问题
 * @param sessionId 会话 ID
 * @param answer 用户回答
 * @returns 下一个问题或提示面试结束
 */
export const submitAnswer = async (sessionId: number, answer: string): Promise<{ question?: string; message?: string }> => {
    const response = await axios.post(`${BASE_URL}/submit_answer`, { session_id: sessionId, answer });
    return response.data;
};

/**
 * 总结面试
 * @param sessionId 会话 ID
 * @returns 面试总结
 */
export const summarizeInterview = async (sessionId: number): Promise<{ summary: string }> => {
    const response = await axios.post(`${BASE_URL}/summarize_interview`, { session_id: sessionId });
    return response.data;
};