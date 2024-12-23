import React, { useState } from "react";
import { Button, Input, Typography, message } from "antd";
import { generateCode } from "./examApi";

const { TextArea } = Input;

const ExamPage: React.FC = () => {
    const [description, setDescription] = useState<string>(""); // 输入的问题描述
    const [jsonContent, setJsonContent] = useState<string>(""); // 显示格式化后的 JSON 数据
    const [loading, setLoading] = useState<boolean>(false); // 按钮加载状态

    const handleGenerateCode = async () => {
        if (!description.trim()) {
            message.warning("Please enter a problem description.");
            return;
        }

        setLoading(true);
        try {
            const response = await generateCode(description);
            console.log("API Response:", response);

            // 格式化 JSON 内容
            const formattedContent = formatJsonContent(response);
            setJsonContent(formattedContent);
            message.success("Code generated successfully!");
        } catch (error) {
            console.error("Error generating code:", error);
            message.error("Failed to generate code. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    /**
     * 格式化 JSON 内容
     * @param data API 返回的 JSON 数据
     * @returns 格式化后的字符串
     */
    const formatJsonContent = (data: any): string => {
        if (typeof data !== "object") return String(data); // 如果不是对象，直接转换为字符串

        let formatted = "";

        if (data.code && typeof data.code === "object") {
            // 如果返回内容中包含嵌套的 code 对象
            formatted += `Original Description:\n${data.code.original_description}\n\n`;
            formatted += `Generated Code:\n${data.code.code.replace(/\\n/g, "\n").replace(/\\t/g, "    ")}\n`;
        } else {
            // 直接格式化整个 JSON 对象
            formatted = JSON.stringify(data, null, 2);
        }

        return formatted;
    };

    return (
        <div style={{ display: "flex", flexDirection: "row", height: "100vh", fontFamily: "Arial, sans-serif" }}>
            {/* 左侧：问题描述输入区域 */}
            <div style={{ flex: 2, padding: "20px", borderRight: "1px solid #ccc" }}>
                <Typography.Title level={4}>Describe Your Problem:</Typography.Title>
                <TextArea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Enter your problem description here..."
                    rows={20}
                    style={{ marginBottom: "20px" }}
                />
                <Button
                    type="primary"
                    onClick={handleGenerateCode}
                    loading={loading}
                    style={{ width: "100%" }}
                >
                    Generate Code
                </Button>
            </div>

            {/* 右侧：JSON 内容显示区域 */}
            <div style={{ flex: 8, padding: "20px" }}>
                <Typography.Title level={4}>Answer:</Typography.Title>
                <TextArea
                    value={jsonContent}
                    readOnly
                    rows={20} // 设置更高的行数以便显示更多内容
                    style={{
                        fontFamily: "monospace", // 等宽字体，适合代码和 JSON
                        whiteSpace: "pre-wrap", // 保留换行和缩进
                        backgroundColor: "#f6f8fa", // 背景颜色
                        height: "100%", // 填满父容器
                        overflowY: "auto", // 添加滚动支持
                    }}
                />
            </div>
        </div>
    );
};

export default ExamPage;