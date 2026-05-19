"use client";

import { useState } from "react";

interface Props {
  documentText: string;
  lang: "en" | "jp";
}

export default function ContractChatTab({
  documentText,
  lang,
}: Props) {
  const [question, setQuestion] =
    useState("");

  const [messages, setMessages] =
    useState<any[]>([]);

  const askQuestion = async () => {

    if (!question) return;

    const userMessage = {
      role: "user",
      text: question,
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
    ]);

    try {

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      const response = await fetch(
        `${apiUrl}/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            document_text: documentText,
            question,
          }),
        }
      );

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: data.answer,
        },
      ]);

    } catch {

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: {
            english: "Failed to get response.",
            japanese: "エラーが発生しました。",
          }
        },
      ]);

    }

    setQuestion("");

  };

  return (

    <div className="
      bg-[#0f172a]
      rounded-3xl
      border border-cyan-500
      p-10
    ">

      <div className="mb-10">
        <h1 className="
          text-3xl
          text-cyan-400
          font-bold
        ">
          AI Contract Chat
        </h1>
      </div>

      <div className="
        space-y-5
        mb-8
        max-h-[500px]
        overflow-y-auto
      ">

        {messages.map(
          (msg, index) => (

            <div
              key={index}
              className={`
                p-4 rounded-2xl text-[16px]
                ${
                  msg.role === "user"
                    ? "bg-cyan-500 text-black ml-20"
                    : "bg-[#111827] mr-20"
                }
              `}
            >

              {msg.role === "user" ? msg.text : (lang === "en" ? msg.text.english : msg.text.japanese)}

            </div>

          )
        )}

      </div>

      <div className="flex gap-4">

        <input
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          placeholder="Ask about the contract..."
          className="
            flex-1
            bg-[#111827]
            border border-cyan-500
            rounded-2xl
            p-4
            text-[16px]
          "
        />

        <button
          onClick={askQuestion}
          className="
            bg-cyan-500
            text-black
            px-8
            rounded-2xl
            font-bold
            text-[16px]
          "
        >
          Ask
        </button>

      </div>

    </div>
  );
}