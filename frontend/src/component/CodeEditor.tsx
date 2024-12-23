import React from "react";
import Editor from "@monaco-editor/react";

interface CodeEditorProps {
    value: string; // 当前编辑器内容
    onChange: (value: string) => void; // 当编辑器内容变化时触发的回调函数
    language?: string; // 可选的编程语言 (默认: JavaScript)
}

const CodeEditor: React.FC<CodeEditorProps> = ({ value, onChange, language = "javascript" }) => {
    return (
        <div style={{ height: "100%", border: "1px solid #ccc", borderRadius: "4px" }}>
            <Editor
                height="400px"
                defaultLanguage={language}
                value={value}
                theme="vs-dark"
                options={{
                    selectOnLineNumbers: true, // 显示行号
                    automaticLayout: true, // 自动布局
                    scrollBeyondLastLine: false, // 禁止滚动超过最后一行
                    minimap: { enabled: true }, // 显示代码缩略图
                }}
                onChange={(newValue) => {
                    onChange(newValue || "");
                }}
            />
        </div>
    );
};

export default CodeEditor;