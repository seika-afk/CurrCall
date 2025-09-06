"use client";

import axios from "axios";
import Image from "next/image";
import React, { useState } from "react";
import toast from "react-hot-toast";

const PromptBox = ({ isLoading, setIsLoading, setMessages }) => {
  const [prompt, setPrompt] = useState("");

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendPrompt(e);
    }
  };

  const sendPrompt = async (e) => {
    const promptCopy = prompt;
    try {
      e.preventDefault();
      if (isLoading) return toast.error("Wait for the previous prompt response");

      setIsLoading(true);
      setPrompt("");

      // add user message immediately
      const userPrompt = { role: "user", content: prompt, timestamp: Date.now() };
      setMessages((prev) => [...prev, userPrompt]);

      // call API
      const { data } = await axios.post("/api/chat/ai", { prompt });

      if (data.success) {
        const message = data.data.content;
        const messageTokens = message.split(" ");

        let assistantMessage = { role: "assistant", content: "", timestamp: Date.now() };
        setMessages((prev) => [...prev, assistantMessage]);

        for (let i = 0; i < messageTokens.length; i++) {
          setTimeout(() => {
            assistantMessage.content = messageTokens.slice(0, i + 1).join(" ");
            setMessages((prev) => {
              const updated = [...prev];
              updated[updated.length - 1] = { ...assistantMessage };
              return updated;
            });
          }, i * 50); // faster typing
        }
      } else {
        toast.error(data.error || "Failed to get AI response");
        setPrompt(promptCopy);
      }
    } catch (error) {
      toast.error(error.message || "Something went wrong");
      setPrompt(promptCopy);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form
      onSubmit={sendPrompt}
      className="w-full max-w-5xl backdrop-blur-lg border-l border-r border-gray-500 p-4 rounded-3xl mt-4 transition-all"
    >
      <textarea
        onKeyDown={handleKeyDown}
        className="outline-none w-full resize-none overflow-hidden break-words bg-transparent"
        rows={2}
        placeholder="Message CurrCall"
        required
        onChange={(e) => setPrompt(e.target.value)}
        value={prompt}
      />

      <div className="flex items-center justify-between text-sm">
        <div className="flex items-center gap-2"></div>
        <div className="flex items-center gap-2">
          <button
            type="submit"
            disabled={isLoading}
            className={`${prompt ? "bg-primary" : "bg-[#71717a]"} rounded-full p-2 cursor-pointer`}
          >
            <Image
              src={prompt ? "/assets/arrow_icon.svg" : "/assets/arrow_icon_dull.svg"}
              alt="arrow icon"
              width={14}
              height={14}
            />
          </button>
        </div>
      </div>
    </form>
  );
};

export default PromptBox;

