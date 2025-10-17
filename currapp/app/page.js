"use client";

import PromptBox from "@/components/PromptBox";
import Image from "next/image";
import { useEffect, useRef, useState } from "react";

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const containerRef = useRef(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTo({
        top: containerRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages]);

  return (
    <div className="relative h-screen w-screen overflow-hidden text-[#e0ddcf]">
      {/* Background Image */}
      <Image
        src="/img.jpeg"
        alt="Background"
        fill
        className="object-cover"
        priority
      />

      {/* Overlay with blur */}
      <div className="absolute inset-0 bg-black/30 backdrop-blur-sm"></div>

      {/* Main content */}
      <div className="relative flex flex-col h-screen px-4 pb-4">
        {/* Chat container */}
        <div
          ref={containerRef}
          className="flex-1 flex flex-col items-center overflow-y-auto"
        >
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="flex items-center gap-3 cursor-pointer">
                <Image
                  src="/favic/apple-touch-icon.png"
                  alt="Logo"
                  width={64}
                  height={64}
                  className="h-16 w-16 filter grayscale"
                />
                <p className="text-2xl font-kode font-medium">CurrCall</p>
              </div>
              <p className="text-sm mt-4 opacity-80">Curriculum at your call</p>
            </div>
          ) : (
            <div className="relative flex flex-col w-full max-w-3xl mt-4">
              {/* Messages */}
         {messages.map((msg, idx) => (
  <p
    key={idx}
    className={`py-2 px-3 rounded-lg mb-3 text-sm border border-transparent hover:border-gray-500/50 ${
      msg.role === "user"
        ? "bg-blue-600/70 text-white self-end"  
        : "bg-[#404045]/80 text-white self-start"
    }`}
  >
    {msg.content}
  </p>
))}


              {isLoading && (
                <div className="flex gap-4 py-3">
                  <Image
                    className="h-9 w-9 p-1  border border-white/15 rounded-full"
                    src="/favic/favicon.png"
                    alt="Logo"
                    width={36}
                    height={36}
                  />
                  <div className="flex gap-1 items-center">
                    <span className="w-2 h-2 rounded-full bg-white animate-bounce [animation-delay:0ms]" />
                    <span className="w-2 h-2 rounded-full bg-white animate-bounce [animation-delay:200ms]" />
                    <span className="w-2 h-2 rounded-full bg-white animate-bounce [animation-delay:400ms]" />
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

      
        <div className="flex justify-center px-4">
          <div className="w-full max-w-3xl">
            <PromptBox
              isLoading={isLoading}
              setIsLoading={setIsLoading}
              setMessages={setMessages}
            />
          </div>
        </div>

        {/* Footer */}
        <p className="text-xs text-gray-300 text-center pb-1">
          Contact{" "}
          <a
            href="mailto:24bec036@nith.ac.in"
            className="underline hover:text-gray-400"
          >
            Me
          </a>{" "}
          for any issues.
        </p>
      </div>
    </div>
  );
}

