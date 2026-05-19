import ConcernCard from "./ConcernCard";

interface Props {
  analysis: any;
  lang: "en" | "jp";
}

export default function AnalysisTab({
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

    <div className="space-y-10">

      <ConcernCard
        title={lang === "jp" ? "危険な条項" : "Dangerous Clauses"}
        items={lang === "jp" ? analysis.dangerous_clauses_jp : (analysis.dangerous_clauses_en || analysis.dangerous_clauses)}
        color="border-red-500"
      />

      <ConcernCard
        title={lang === "jp" ? "金銭的義務" : "Financial Obligations"}
        items={lang === "jp" ? analysis.financial_obligations_jp : (analysis.financial_obligations_en || analysis.financial_obligations)}
        color="border-yellow-500"
      />

      <ConcernCard
        title={lang === "jp" ? "隠れたリスク" : "Hidden Risks"}
        items={lang === "jp" ? analysis.hidden_risks_jp : (analysis.hidden_risks_en || analysis.hidden_risks)}
        color="border-blue-500"
      />

      <ConcernCard
        title={lang === "jp" ? "罰則リスク" : "Penalty Risks"}
        items={lang === "jp" ? analysis.penalty_risks_jp : (analysis.penalty_risks_en || analysis.penalty_risks)}
        color="border-orange-500"
      />

      <ConcernCard
        title={lang === "jp" ? "キャンセルポリシー" : "Cancellation Policies"}
        items={lang === "jp" ? analysis.cancellation_policies_jp : (analysis.cancellation_policies_en || analysis.cancellation_policies)}
        color="border-purple-500"
      />

      <ConcernCard
        title={lang === "jp" ? "重要な日付" : "Important Dates"}
        items={lang === "jp" ? analysis.important_dates_jp : (analysis.important_dates_en || analysis.important_dates)}
        color="border-cyan-500"
      />

      <ConcernCard
        title={lang === "jp" ? "消費者へのアドバイス" : "Consumer Advice"}
        items={lang === "jp" ? analysis.consumer_advice_jp : (analysis.consumer_advice_en || analysis.consumer_advice)}
        color="border-green-500"
      />

    </div>
  );
}