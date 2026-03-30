import type { SearchHit } from "../api";
import { HighlightedText } from "./HighlightedText";

type Props = { hit: SearchHit };

export function ResultCard({ hit }: Props) {
  const title = hit.titulo ?? hit.id;
  const desc = hit.descricao ?? "";

  return (
    <article className="group rounded-2xl border border-slate-800/80 bg-gradient-to-br from-slate-900/90 to-slate-950/90 p-5 shadow-lg shadow-black/30 transition hover:border-emerald-500/30 hover:shadow-emerald-950/20">
      <div className="mb-3 flex flex-wrap items-start justify-between gap-2">
        <h2 className="text-balance text-lg font-semibold text-slate-50">
          <HighlightedText text={title} highlights={hit.highlights} />
        </h2>
        <div className="flex shrink-0 flex-col items-end gap-1 text-right text-xs">
          <span className="rounded-full bg-emerald-500/15 px-2.5 py-1 font-mono text-emerald-300 ring-1 ring-emerald-500/30">
            {hit.score.toFixed(3)}
          </span>
          <span className="text-slate-500">
            sem {hit.score_semantic.toFixed(2)} · lex {hit.score_lexical.toFixed(2)}
          </span>
        </div>
      </div>

      {desc ? (
        <p className="mb-4 line-clamp-3 text-sm leading-relaxed text-slate-400">
          <HighlightedText text={desc} highlights={hit.highlights} />
        </p>
      ) : null}

      {hit.tags.length > 0 ? (
        <div className="mb-4 flex flex-wrap gap-2">
          {hit.tags.map((t) => (
            <span
              key={t}
              className="rounded-full bg-slate-800/80 px-2.5 py-0.5 text-xs text-slate-300 ring-1 ring-slate-700/80"
            >
              {t}
            </span>
          ))}
        </div>
      ) : null}

      {hit.reasons.length > 0 ? (
        <ul className="space-y-1.5 border-t border-slate-800/80 pt-3 text-sm text-slate-400">
          {hit.reasons.map((r, i) => (
            <li key={i} className="flex gap-2">
              <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-500/80" />
              <span>{r}</span>
            </li>
          ))}
        </ul>
      ) : null}

      {Object.keys(hit.metadata).length > 0 ? (
        <dl className="mt-3 grid gap-1 text-xs text-slate-500 sm:grid-cols-2">
          {Object.entries(hit.metadata).map(([k, v]) => (
            <div key={k} className="flex gap-1">
              <dt className="font-medium text-slate-600">{k}:</dt>
              <dd className="truncate">{String(v)}</dd>
            </div>
          ))}
        </dl>
      ) : null}
    </article>
  );
}
