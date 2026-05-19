import { useState } from "react";

interface Props {
  analysis: any;
  lang: "en" | "jp";
}

export default function SummaryTab({
  analysis,
  lang,
}: Props) {

  if (!analysis) {
    return (
      <div className="text-gray-400 text-2xl">
        No analysis available.
      </div>
    );
  }

  return (

    <div className="
      bg-[#0f172a]
      border border-cyan-500
      rounded-3xl
      p-10
      space-y-8
    ">

      <div className="mb-8">
        <h1 className="text-3xl font-bold text-cyan-400">
          Detailed Summary
        </h1>
      </div>

      <div className="
        text-[16px]
        leading-[1.8rem]
        text-gray-200
        whitespace-pre-wrap
      ">

        {lang === "en" ? analysis.english_summary : analysis.japanese_summary}

      </div>

    </div>
  );
}