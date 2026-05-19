interface Props {
  title: string;
  items?: string[];
  color: string;
}

export default function ConcernCard({
  title,
  items,
  color,
}: Props) {

  const safeItems = items || [];

  return (

    <div
      className={`
        rounded-3xl
        border-l-8
        border-t border-b border-r border-gray-800
        p-8
        bg-gradient-to-r from-[#0f172a] to-[#1e293b]
        shadow-lg
        transition-all duration-300 hover:shadow-[0_0_20px_rgba(0,0,0,0.5)]
        ${color}
      `}
    >

      <h2 className="
        text-2xl
        font-bold
        mb-6
      ">
        {title}
      </h2>

      {safeItems.length === 0 ? (

        <p className="text-gray-400 text-[16px]">
          No issues detected.
        </p>

      ) : (

        <div className="space-y-4">

          {safeItems.map(
            (item, index) => (

              <div
                key={index}
                className="
                  bg-[#0a0f1a]
                  rounded-2xl
                  p-5
                  text-[15px]
                  text-gray-200
                  border border-gray-800/50
                  shadow-inner
                "
              >
                <div className="flex items-start gap-4">
                  <div className="mt-1">
                    <svg xmlns="http://www.w3.org/2000/svg" className={`h-6 w-6 ${color.replace('border-', 'text-')}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div className="flex-1 leading-relaxed">
                    {item}
                  </div>
                </div>
              </div>

            )
          )}

        </div>

      )}

    </div>
  );
}