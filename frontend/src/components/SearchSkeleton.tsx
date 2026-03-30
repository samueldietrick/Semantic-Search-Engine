export function SearchSkeleton() {
  return (
    <div className="space-y-4 animate-pulse" aria-hidden>
      {[1, 2, 3].map((i) => (
        <div
          key={i}
          className="rounded-2xl border border-slate-800/80 bg-slate-900/50 p-5 shadow-lg shadow-black/20"
        >
          <div className="mb-3 h-5 w-2/3 rounded bg-slate-700/80" />
          <div className="mb-2 h-4 w-full rounded bg-slate-800/80" />
          <div className="mb-4 h-4 w-5/6 rounded bg-slate-800/60" />
          <div className="flex gap-2">
            <div className="h-6 w-16 rounded-full bg-slate-800" />
            <div className="h-6 w-20 rounded-full bg-slate-800" />
          </div>
        </div>
      ))}
    </div>
  );
}
