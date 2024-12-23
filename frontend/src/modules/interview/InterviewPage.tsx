import React, { useState, useEffect } from "react";
import { Button, Layout, Typography, message } from "antd";
import { AudioOutlined } from "@ant-design/icons";
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";
import {
    selectTheme,
    startInterview,
    submitAnswer,
    summarizeInterview,
} from "./interviewApi";

const { Header, Content } = Layout;

const InterviewPage: React.FC = () => {
    const [sessionId, setSessionId] = useState<number | null>(null);
    const [theme, setTheme] = useState<string | null>(null); // 动态主题
    const [chatHistory, setChatHistory] = useState<
        { type: "system" | "question" | "answer" | "summary"; content: string }[]
    >([]);
    const [isListening, setIsListening] = useState(false);
    const [isInterviewFinished, setIsInterviewFinished] = useState(false);
    const [isThemeSelected, setIsThemeSelected] = useState(false); // 主题是否已选
    const { transcript, resetTranscript } = useSpeechRecognition();

    // 初始化语音主题选择
    const startThemeSelection = () => {
        resetTranscript();
        SpeechRecognition.startListening({ language: "zh-CN" }); // 启动语音识别，捕获主题
        setIsListening(true);
    };

    const stopThemeSelection = () => {
        SpeechRecognition.stopListening();
        setIsListening(false);
        const userTheme = transcript.trim();
        if (userTheme) {
            const formattedTheme = userTheme.toUpperCase(); // 转换为大写英文
            setTheme(formattedTheme); // 设置主题
            message.success(`Recognized theme: ${formattedTheme}`);
        } else {
            message.warning("No theme detected. Please try again.");
        }
    };

    useEffect(() => {
        if (theme && !isThemeSelected) {
            const initializeInterview = async () => {
                try {
                    const { session_id } = await selectTheme(theme); // 动态传入格式化后的主题
                    setSessionId(session_id);

                    const { question } = await startInterview(session_id);
                    setChatHistory([
                        { type: "system", content: `模拟面试开始. 主题: ${theme}` },
                        { type: "question", content: question },
                    ]);
                    setIsThemeSelected(true); // 标记主题已选定
                } catch (error) {
                    message.error("Failed to start the interview.");
                }
            };

            initializeInterview();
        }
    }, [theme, isThemeSelected]);

    const loadNextQuestion = async () => {
        if (!sessionId) return;
        try {
            const response = await submitAnswer(sessionId, transcript.trim());
            if (response.message) {
                setIsInterviewFinished(true);
                fetchSummary();
            } else if (response.question) {
                setChatHistory((prev) => [
                    ...prev,
                    { type: "question", content: response.question },
                ]);
            }
        } catch (error) {
            message.error("Failed to load the next question.");
        }
    };

    const fetchSummary = async () => {
        if (!sessionId) return;
        try {
            const { summary } = await summarizeInterview(sessionId);
            setChatHistory((prev) => [
                ...prev,
                { type: "summary", content: summary },
            ]);
        } catch (error) {
            message.error("Failed to fetch interview summary.");
        }
    };

    const handleStartListening = () => {
        SpeechRecognition.startListening({ language: "zh-CN" });
        setIsListening(true);
    };

    const handleStopListening = async () => {
        SpeechRecognition.stopListening();
        setIsListening(false);

        const userAnswer = transcript.trim();
        if (userAnswer) {
            setChatHistory((prev) => [
                ...prev,
                { type: "answer", content: userAnswer },
            ]);
            resetTranscript();
            loadNextQuestion();
        } else {
            message.warning("No response detected. Please try again.");
        }
    };

    const handleReset = () => {
        setChatHistory([]);
        setIsInterviewFinished(false);
        resetTranscript();
        setIsListening(false);
        setSessionId(null);
        setTheme(null);
        setIsThemeSelected(false);
    };

    return (
        <Layout style={{ minHeight: "100vh", fontFamily: "Arial, sans-serif" }}>
            <Header style={{ backgroundColor: "#007BFF", color: "#fff", textAlign: "center" }}>
                <Typography.Title level={3} style={{ color: "#fff", margin: 0 }}>
                    Interview Simulation
                </Typography.Title>
            </Header>

            <Content style={{ padding: "20px" }}>
                {!isThemeSelected ? (
                    <div style={{ textAlign: "center" }}>
                        <Typography.Text type="secondary" style={{ display: "block", marginBottom: "20px" }}>
                            Please specify a theme for the interview using voice input.
                        </Typography.Text>
                        {isListening ? (
                            <Button type="primary" onClick={stopThemeSelection} icon={<AudioOutlined />}>
                                Stop Listening
                            </Button>
                        ) : (
                            <Button type="primary" onClick={startThemeSelection} icon={<AudioOutlined />}>
                                Start Theme Selection
                            </Button>
                        )}
                        {theme && (
                            <Typography.Text type="success" style={{ display: "block", marginTop: "10px" }}>
                                Selected Theme: {theme}
                            </Typography.Text>
                        )}
                    </div>
                ) : (
                    <>
                        <div
                            style={{
                                border: "1px solid #ccc",
                                borderRadius: "8px",
                                padding: "10px",
                                height: "600px",
                                overflowY: "auto",
                                marginBottom: "20px",
                            }}
                        >
                            {chatHistory.map((entry, index) => (
                                <div
                                    key={index}
                                    style={{
                                        textAlign:
                                            entry.type === "question" || entry.type === "system" || entry.type === "summary"
                                                ? "left"
                                                : "right",
                                        marginBottom: "10px",
                                    }}
                                >
                                    <div
                                        style={{
                                            display: "inline-block",
                                            padding: "10px",
                                            borderRadius: "8px",
                                            backgroundColor:
                                                entry.type === "question" || entry.type === "system" || entry.type === "summary"
                                                    ? "#f1f1f1"
                                                    : "#007BFF",
                                            color:
                                                entry.type === "question" || entry.type === "system" || entry.type === "summary"
                                                    ? "#000"
                                                    : "#fff",
                                            maxWidth: "70%",
                                        }}
                                    >
                                        {entry.content}
                                    </div>
                                </div>
                            ))}
                        </div>

                        {!isInterviewFinished ? (
                            <div style={{ display: "flex", justifyContent: "center" }}>
                                {isListening ? (
                                    <Button type="primary" onClick={handleStopListening} icon={<AudioOutlined />}>
                                        Stop Listening
                                    </Button>
                                ) : (
                                    <Button type="primary" onClick={handleStartListening} icon={<AudioOutlined />}>
                                        Start Listening
                                    </Button>
                                )}
                            </div>
                        ) : (
                            <div style={{ textAlign: "center" }}>
                                <Typography.Text type="success" style={{ display: "block", marginBottom: "20px" }}>
                                    The interview has ended. Thank you!
                                </Typography.Text>
                                <Button type="primary" onClick={handleReset}>
                                    Reset Interview
                                </Button>
                            </div>
                        )}
                    </>
                )}
            </Content>
        </Layout>
    );
};

export default InterviewPage;