interface Props {
  setFile: (file: File) => void;
}

export default function UploadDropzone({
  setFile,
}: Props) {

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  return (

    <label
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      className="
        relative group
        border-2 border-dashed border-cyan-500/50
        rounded-3xl p-20 flex flex-col items-center
        justify-center cursor-pointer
        bg-cyan-500/5 hover:bg-cyan-500/10 hover:border-cyan-400
        transition-all duration-300
        overflow-hidden
      "
    >
      <div className="absolute inset-0 bg-gradient-to-b from-transparent to-cyan-500/5 pointer-events-none" />

      {/* Cute Animated Icon Container */}
      <div className="mb-6 transform group-hover:-translate-y-2 group-hover:scale-110 transition-all duration-300">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-20 w-20 text-cyan-400 drop-shadow-[0_0_15px_rgba(34,211,238,0.5)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
      </div>

      <div className="text-3xl font-bold mb-4 text-white drop-shadow-md">
        Drag & Drop Document
      </div>

      <div className="text-cyan-200/70 font-medium tracking-wide">
        or click to browse from desktop
      </div>

      <input
        type="file"
        className="hidden"
        onChange={(e) => {

          const selected =
            e.target.files?.[0];

          if (selected) {
            setFile(selected);
          }

        }}
      />

    </label>
  );
}