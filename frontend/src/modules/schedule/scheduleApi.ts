export const runEmailPipeline = async (): Promise<{ success: boolean }> => {
    const response = await fetch("/api/run-email-pipeline", {
        method: "POST",
    });

    if (!response.ok) {
        throw new Error("Failed to run email pipeline");
    }

    try {
        const data = await response.json(); // 解析固定 JSON 响应
        return { success: data.message === "Pipeline executed. Check backend logs for details." };
    } catch (error) {
        console.error("Error processing response:", error);
        return { success: false };
    }
};