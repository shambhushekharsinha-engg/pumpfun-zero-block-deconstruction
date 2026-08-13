export default function EvidenceBadge({ status, title, description }: { status: "observable" | "unobservable", title: string, description: string }) {
  const isObservable = status === "observable";
  return (
    <div className={`p-4 rounded-lg border ${isObservable ? 'border-green-500/30 bg-green-900/20' : 'border-red-500/30 bg-red-900/20'}`}>
      <div className="flex items-center gap-2 mb-2">
        <div className={`w-3 h-3 rounded-full ${isObservable ? 'bg-green-500' : 'bg-red-500'}`}></div>
        <span className={`text-xs font-bold tracking-wider ${isObservable ? 'text-green-400' : 'text-red-400'}`}>
          {isObservable ? 'OBSERVABLE' : 'NOT OBSERVABLE'}
        </span>
      </div>
      <h4 className="text-white font-semibold mb-1">{title}</h4>
      <p className="text-slate-400 text-sm">{description}</p>
    </div>
  );
}
