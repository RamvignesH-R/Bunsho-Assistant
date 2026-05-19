import ShieldStatus from "./ShieldStatus";
import UploadDropzone from "./UploadDropzone";

interface Props {
  file: File | null;
  setFile: any;
  handleUpload: any;
  loading: boolean;
  progress: number;
  analysis: any;
}

export default function DashboardTab({
  file,
  setFile,
  handleUpload,
  loading,
  progress,
  analysis,
}: Props) {

  return (

    <div className="grid lg:grid-cols-2 gap-10">

      <div className="bg-[#0f172a] rounded-3xl p-10 border border-cyan-500">

        <UploadDropzone
          setFile={setFile}
        />

        {file && (

          <div className="mt-6 text-xl">
            {file.name}
          </div>

        )}

        <button
          onClick={handleUpload}
          className="
            mt-8 w-full py-5 rounded-2xl
            bg-cyan-500 text-black
            text-2xl font-bold
          "
        >

          {loading
            ? "Analyzing..."
            : "Analyze"}

        </button>

        <div className="mt-8 text-cyan-400 text-center font-semibold text-lg">
          {progress > 0 && progress < 100 && `Analyzing... ${progress}%`}
          {progress === 100 && "Analysis Complete"}
        </div>

      </div>

      <div className="
        bg-[#0f172a]
        rounded-3xl
        border border-red-500
        p-10 flex justify-center items-center
      ">

        <ShieldStatus
          analysis={analysis}
          progress={progress}
        />

      </div>

    </div>
  );
}