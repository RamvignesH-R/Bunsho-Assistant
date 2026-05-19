import ExportPDFButton from "./ExportPDFButton";

interface Props {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  globalLang: "en" | "jp";
  setGlobalLang: (lang: "en" | "jp") => void;
}

export default function Sidebar({
  activeTab,
  setActiveTab,
  globalLang,
  setGlobalLang,
}: Props) {

  const tabs = [
    "dashboard",
    "summary",
    "analysis",
    "chat",
  ];

  return (

    <div className="w-72 bg-[#111827] border-r border-cyan-900/50 p-6 flex flex-col justify-between shadow-[4px_0_24px_rgba(34,211,238,0.05)] print-hide">

      <div>
        <div className="flex items-center gap-3 mb-12">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          <h1 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
            Bunsho Assistant
          </h1>
        </div>

        <div className="space-y-4">

          {tabs.map((tab) => (

            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`
                w-full text-left px-5 py-4 rounded-2xl
                transition-all duration-300 font-semibold tracking-wide flex items-center gap-3
                ${
                  activeTab === tab
                    ? "bg-cyan-500 text-black shadow-[0_0_15px_rgba(34,211,238,0.4)]"
                    : "text-gray-300 hover:bg-[#1e293b] hover:text-cyan-400"
                }
              `}
            >

              {tab.toUpperCase()}

            </button>

          ))}

        </div>
      </div>

      <div>
        <div className="mb-6 bg-[#0f172a] p-1 rounded-xl flex items-center border border-cyan-900/30">
          <button
            onClick={() => setGlobalLang("en")}
            className={`flex-1 py-2 rounded-lg text-sm font-bold transition-all ${globalLang === "en" ? "bg-cyan-500 text-black shadow-lg" : "text-gray-400 hover:text-cyan-300"}`}
          >
            English
          </button>
          <button
            onClick={() => setGlobalLang("jp")}
            className={`flex-1 py-2 rounded-lg text-sm font-bold transition-all ${globalLang === "jp" ? "bg-cyan-500 text-black shadow-lg" : "text-gray-400 hover:text-cyan-300"}`}
          >
            日本語
          </button>
        </div>
        <ExportPDFButton />
      </div>

    </div>
  );
}