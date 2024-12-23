import React, { useState } from "react";
import { runEmailPipeline } from "./scheduleApi";

const SchedulePage: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null); // 用于显示错误消息

    const handleButtonClick = async () => {
        setLoading(true);
        setError(null); // 重置错误状态

        try {
            const response = await runEmailPipeline();

            if (response.success) {
                // 提示成功，并跳转到指定页面
                alert("Pipeline completed successfully! Redirecting...");
                window.location.href = "https://tcngwjbzogvc.feishu.cn/calendar/week";
            } else {
                throw new Error("Pipeline execution failed");
            }
        } catch (error: any) {
            setError(error.message || "An unknown error occurred.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: "20px" }}>
            <h1>Schedule</h1>
            {/* 主题输入框 */}
            <div style={{marginBottom: "10px"}}>
                <label style={{marginRight: "10px", fontWeight: "bold"}}>
                    Interviews Subject:
                </label>
                <input
                    type="text"
                    placeholder="All" // 默认显示 "All"
                    style={{
                        padding: "8px",
                        borderRadius: "4px",
                        border: "1px solid #ccc",
                        width: "440px",
                    }}
                />
            </div>
            {/* 面试时间输入框 */}
            <div style={{marginBottom: "20px"}}>
                <label style={{marginRight: "10px", fontWeight: "bold"}}>
                    Interviews Arrangement :
                </label>
                <input
                    type="text"
                    placeholder="Please input the date you would like to get the schedule"
                     style={{
                        padding: "8px",
                        borderRadius: "4px",
                        border: "1px solid #ccc",
                        width: "400px",
                    }}
                />
            </div>
            <button
                onClick={handleButtonClick}
                style={{
                    display: "inline-block",
                    padding: "10px 20px",
                    backgroundColor: loading ? "#6c757d" : "#007bff",
                    color: "#fff",
                    textDecoration: "none",
                    borderRadius: "4px",
                    textAlign: "center",
                    fontWeight: "bold",
                    border: "none",
                    cursor: loading ? "not-allowed" : "pointer",
                }}
                disabled={loading}
            >
                {loading ? "Waiting..." : "Open Calendar"}
            </button>

            {/* 显示错误消息 */}
            {error && (
                <div style={{ marginTop: "20px", color: "red", fontWeight: "bold" }}>
                    {error}
                </div>
            )}
        </div>
    );
};

export default SchedulePage;