import React, { useState, useEffect } from "react";

interface TimerProps {
    initialTime: number; // 初始时间（以秒为单位）
    onTimeUp?: () => void; // 时间结束时触发的回调函数
    mode?: "countdown" | "stopwatch"; // 模式："countdown"（倒计时）或 "stopwatch"（计时器）
}

const Timer: React.FC<TimerProps> = ({ initialTime, onTimeUp, mode = "countdown" }) => {
    const [time, setTime] = useState(initialTime);

    useEffect(() => {
        let timerId: NodeJS.Timeout;

        if (mode === "countdown" && time > 0) {
            timerId = setInterval(() => {
                setTime((prevTime) => prevTime - 1);
            }, 1000);
        } else if (mode === "stopwatch") {
            timerId = setInterval(() => {
                setTime((prevTime) => prevTime + 1);
            }, 1000);
        }

        // 时间结束时触发回调
        if (time === 0 && mode === "countdown" && onTimeUp) {
            onTimeUp();
        }

        return () => clearInterval(timerId); // 清理定时器
    }, [time, mode, onTimeUp]);

    // 格式化时间为 MM:SS
    const formatTime = (time: number) => {
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
    };

    return (
        <div style={{ fontFamily: "Arial, sans-serif", fontSize: "20px", textAlign: "center" }}>
            <p>{formatTime(time)}</p>
        </div>
    );
};

export default Timer;