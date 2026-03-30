export type SearchHit = {
  id: string;
  titulo: string | null;
  score: number;
  score_semantic: number;
  score_lexical: number;
  highlights: string[];
  reasons: string[];
  metadata: Record<string, unknown>;
  descricao: string | null;
  tags: string[];
};

export type SearchResponse = {
  total: number;
  results: SearchHit[];
};

const base = import.meta.env.VITE_API_URL?.replace(/\/$/, "") ?? "";

export async function searchApi(
  q: string,
  limit: number,
  offset: number,
): Promise<SearchResponse> {
  const url = `${base}/search`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ q, limit, offset }),
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(t || `HTTP ${res.status}`);
  }
  return res.json() as Promise<SearchResponse>;
}
