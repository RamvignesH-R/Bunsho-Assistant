import { Shield, ShieldAlert, ShieldCheck } from "lucide-react";

interface Props {
  analysis: any;
  progress: number;
}

export default function ShieldStatus({
  analysis,
  progress,
}: Props) {

  let color = "text-green-500 shadow-green-500";
  let svgColor = "text-green-500";
  let dropShadow = "drop-shadow-[0_0_30px_rgba(34,197,94,0.6)]";
  
  // Default Checkmark
  let IconComponent = ShieldCheck;

  const isNeutral = !analysis && progress === 0;
  const score = analysis?.risk_score || 0;
  const isError = analysis?.japanese_summary === "Analysis failed" || analysis?.consumer_advice_en?.[0]?.includes("Quota exceeded") || analysis?.consumer_advice_en?.[0]?.includes("429");

  if (isNeutral) {
    color = "text-cyan-900 shadow-cyan-900";
    svgColor = "text-cyan-900";
    dropShadow = "drop-shadow-[0_0_20px_rgba(34,211,238,0.2)]";
    IconComponent = Shield;
  } else if (score > 40 && !isError) {
    color = "text-yellow-400 shadow-yellow-400";
    svgColor = "text-yellow-400";
    dropShadow = "drop-shadow-[0_0_30px_rgba(250,204,21,0.6)]";
    IconComponent = ShieldAlert;
  }

  if (score > 70 || isError) {
    color = "text-red-500 shadow-red-500";
    svgColor = "text-red-500";
    dropShadow = "drop-shadow-[0_0_30px_rgba(239,68,68,0.8)]";
    // Icon Path: Cross
    IconComponent = ShieldAlert;
  }

  const radius = 170;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  return (
    <div className="relative flex items-center justify-center w-[400px] h-[400px]">
      {/* Circular Progress */}
      <svg className="absolute inset-0 w-full h-full transform -rotate-90">
        {/* Background circle */}
        <circle
          cx="200"
          cy="200"
          r={radius}
          stroke="currentColor"
          strokeWidth="12"
          fill="transparent"
          className="text-gray-800"
        />
        {/* Progress circle */}
        <circle
          cx="200"
          cy="200"
          r={radius}
          stroke="currentColor"
          strokeWidth="12"
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          className={`${svgColor} transition-all duration-1000 ease-out`}
        />
      </svg>

      <div className={`z-10 flex flex-col items-center justify-center ${color} ${dropShadow}`}>
        <IconComponent className="w-48 h-48 transition-colors duration-500" strokeWidth={1.2} />
      </div>
    </div>
  );
}