"use client";

import { useState } from "react";

import Sidebar from "@/components/Sidebar";
import DashboardTab from "@/components/DashboardTab";
import SummaryTab from "@/components/SummaryTab";
import AnalysisTab from "@/components/AnalysisTab";
import ContractChatTab from "@/components/ContractChatTab";

export default function Home() {

  const [activeTab, setActiveTab] =
    useState("dashboard");

  const [globalLang, setGlobalLang] =
    useState<"en" | "jp">("en");

  const [file, setFile] =
    useState<File | null>(null);

  const [analysis, setAnalysis] =
    useState<any>(null);

  const [documentText, setDocumentText] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [progress, setProgress] =
    useState(0);

  const handleUpload = async () => {

    if (!file) return;

    setLoading(true);

    setProgress(10);

    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) return prev;
        return prev + 2;
      });
    }, 500);

    const formData = new FormData();

    formData.append("file", file);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/analyze",
        {
          method: "POST",
          body: formData,
        }
      );

      clearInterval(interval);
      setProgress(95);

      const data = await response.json();

      setAnalysis(data.analysis);

      setDocumentText(data.extracted_text);

      setProgress(100);

    } catch {

      clearInterval(interval);
      alert("Analysis failed");

    }

    setLoading(false);
  };

  return (
    <main className="bg-black text-white min-h-screen">

      {/* INTERACTIVE APP - Hidden during print */}
      <div className="flex w-full h-screen print:hidden">
        
        <Sidebar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          globalLang={globalLang}
          setGlobalLang={setGlobalLang}
        />

        <div className="flex-1 p-10 overflow-y-auto">

          {activeTab === "dashboard" && (
            <DashboardTab
              file={file}
              setFile={setFile}
              handleUpload={handleUpload}
              loading={loading}
              progress={progress}
              analysis={analysis}
            />
          )}

          {activeTab === "summary" && (
            <SummaryTab
              analysis={analysis}
              lang={globalLang}
            />
          )}

          {activeTab === "analysis" && (
            <AnalysisTab
              analysis={analysis}
              lang={globalLang}
            />
          )}

          {activeTab === "chat" && (
            <ContractChatTab
              documentText={documentText}
              lang={globalLang}
            />
          )}

        </div>
      </div>

      {/* PRINTABLE REPORT - Visible ONLY during print */}
      <div className="hidden print:block w-full bg-white text-black p-10 font-sans">
        <h1 className="text-5xl font-extrabold mb-10 pb-4 border-b-4 border-gray-800">
          BureaucracyAI Document Report
        </h1>

        {analysis ? (
          <div className="space-y-12">
            
            {/* Risk Assessment */}
            <section>
              <h2 className="text-3xl font-bold mb-4 text-gray-800 border-b-2 pb-2">Risk Assessment</h2>
              <div className="text-xl">
                <strong>Risk Score:</strong> {analysis.risk_score} / 100<br/>
                <strong>Status:</strong> {analysis.japanese_summary === "Analysis failed" ? "Failed" : (analysis.risk_score > 70 ? "High Risk" : analysis.risk_score > 40 ? "Moderate Risk" : "Low Risk")}
              </div>
            </section>

            {/* Summaries */}
            <section>
              <h2 className="text-3xl font-bold mb-4 text-gray-800 border-b-2 pb-2">Detailed Summary</h2>
              <h3 className="text-xl font-bold mt-4 mb-2">English</h3>
              <p className="text-lg leading-relaxed whitespace-pre-wrap">{analysis.english_summary}</p>
              <h3 className="text-xl font-bold mt-6 mb-2">日本語</h3>
              <p className="text-lg leading-relaxed whitespace-pre-wrap">{analysis.japanese_summary}</p>
            </section>

            {/* Analysis Data */}
            <section className="break-inside-avoid">
              <h2 className="text-3xl font-bold mb-4 text-gray-800 border-b-2 pb-2">Key Findings (English)</h2>
              
              {analysis.dangerous_clauses_en?.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-xl font-bold mb-2">Dangerous Clauses</h3>
                  <ul className="list-disc pl-8 space-y-2 text-lg">
                    {analysis.dangerous_clauses_en.map((item: string, i: number) => <li key={i}>{item}</li>)}
                  </ul>
                </div>
              )}

              {analysis.financial_obligations_en?.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-xl font-bold mb-2">Financial Obligations</h3>
                  <ul className="list-disc pl-8 space-y-2 text-lg">
                    {analysis.financial_obligations_en.map((item: string, i: number) => <li key={i}>{item}</li>)}
                  </ul>
                </div>
              )}

              {analysis.hidden_risks_en?.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-xl font-bold mb-2">Hidden Risks</h3>
                  <ul className="list-disc pl-8 space-y-2 text-lg">
                    {analysis.hidden_risks_en.map((item: string, i: number) => <li key={i}>{item}</li>)}
                  </ul>
                </div>
              )}

            </section>
          </div>
        ) : (
          <p className="text-xl italic text-gray-500">No document analyzed.</p>
        )}
      </div>

    </main>
  );
}