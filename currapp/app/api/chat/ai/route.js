import { NextResponse } from "next/server";

const url = "https://curriculumbotapi-rdf7.onrender.com/query";

export async function POST(req) {
  try {
    const { prompt } = await req.json();
    const userPrompt = { question: prompt };

    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userPrompt),
    });

    // if API fails
    if (!response.ok) {
      const text = await response.text(); // fallback
      return NextResponse.json({
        success: false,
        error: `API error: ${response.status} ${text}`,
      });
    }

    let curResponse;
    try {
      curResponse = await response.json(); // try parse json
    } catch {
      curResponse = await response.text(); // fallback to raw text
    }

    return NextResponse.json({
      success: true,
      data: {
        content:
          curResponse.Output ||
          curResponse?.toString?.() ||
          JSON.stringify(curResponse),
      },
    });
  } catch (err) {
    console.error("Route error:", err);
    return NextResponse.json({
      success: false,
      error: err.message || "Something went wrong",
    });
  }
}

