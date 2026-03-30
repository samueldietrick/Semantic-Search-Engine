import { useCallback, useState } from "react";
import { searchApi } from "./api";
import type { SearchHit } from "./api";
import { ResultCard } from "./components/ResultCard";
import { SearchSkeleton } from "./components/SearchSkeleton";

const PAGE = 10;

export default function App() {
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<SearchHit[]>([]);
  const [total, setTotal] = useState(0);
  const [offset, setOffset] = useState(0);
  const [hasSearched, setHasSearched] = useState(false);

  const runSearch = useCallback(
    async (nextOffset: number) => {
      const query = q.trim();
      if (!query) {
        setError("Digite uma busca.");
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const data = await searchApi(query, PAGE, nextOffset);
        setHasSearched(true);
        setResults(data.results);
        setTotal(data.total);
        setOffset(nextOffset);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Falha na busca");
        setResults([]);
        setTotal(0);
      } finally {
        setLoading(false);
      }
    },
    [q],
  );

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    void runSearch(0);
  };

  const canPrev = offset > 0 && !loading;
  const canNext = offset + PAGE < total && !loading;

  return (
    <div className="min-h-screen bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-slate-950 to-black">
      <header className="border-b border-slate-800/80 bg-slate-950/50 backdrop-blur">
        <div className="mx-auto max-w-3xl px-4 py-10">
          <p className="mb-1 text-xs font-medium uppercase tracking-widest text-emerald-400/90">
            Semantic Search Engine
          </p>
          <h1 className="text-balance text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Busca em linguagem natural
          </h1>
          <p className="mt-2 max-w-xl text-slate-400">
            Híbrida (semântica + palavras-chave), com scores e explicações por resultado.
          </p>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-4 py-8">
        <form onSubmit={onSubmit} className="mb-8 flex flex-col gap-3 sm:flex-row sm:items-stretch">
          <label className="sr-only" htmlFor="q">
            Consulta
          </label>
          <input
            id="q"
            name="q"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder='Ex.: "produto barato com boa avaliação"'
            className="min-h-12 flex-1 rounded-xl border border-slate-700 bg-slate-900/80 px-4 text-slate-100 placeholder:text-slate-500 focus:border-emerald-500/50 focus:outline-none focus:ring-2 focus:ring-emerald-500/30"
            autoComplete="off"
          />
          <button
            type="submit"
            disabled={loading}
            className="min-h-12 rounded-xl bg-emerald-600 px-6 font-semibold text-white shadow-lg shadow-emerald-950/40 transition hover:bg-emerald-500 disabled:opacity-60"
          >
            {loading ? "Buscando…" : "Buscar"}
          </button>
        </form>

        {error ? (
          <div
            role="alert"
            className="mb-6 rounded-xl border border-red-500/40 bg-red-950/40 px-4 py-3 text-sm text-red-200"
          >
            {error}
          </div>
        ) : null}

        {loading ? <SearchSkeleton /> : null}

        {!loading && results.length > 0 ? (
          <>
            <p className="mb-4 text-sm text-slate-500">
              {total} resultado(s) no conjunto ranqueado · página {Math.floor(offset / PAGE) + 1}
            </p>
            <ul className="space-y-4">
              {results.map((hit) => (
                <li key={hit.id}>
                  <ResultCard hit={hit} />
                </li>
              ))}
            </ul>
            {(canPrev || canNext) && (
              <nav className="mt-8 flex justify-center gap-3" aria-label="Paginação">
                <button
                  type="button"
                  disabled={!canPrev}
                  onClick={() => void runSearch(Math.max(0, offset - PAGE))}
                  className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 disabled:opacity-40"
                >
                  Anterior
                </button>
                <button
                  type="button"
                  disabled={!canNext}
                  onClick={() => void runSearch(offset + PAGE)}
                  className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300 hover:bg-slate-800 disabled:opacity-40"
                >
                  Próxima
                </button>
              </nav>
            )}
          </>
        ) : null}

        {!loading && results.length === 0 && !error && !hasSearched ? (
          <p className="text-center text-slate-500">
            Nenhuma busca ainda. Experimente descrever o que procura em português.
          </p>
        ) : null}
        {!loading && results.length === 0 && !error && hasSearched ? (
          <p className="text-center text-slate-500">Nenhum resultado encontrado para esta consulta.</p>
        ) : null}
      </main>

      <footer className="border-t border-slate-800/60 py-6 text-center text-xs text-slate-600">
        API FastAPI + Qdrant · sentence-transformers
      </footer>
    </div>
  );
}
