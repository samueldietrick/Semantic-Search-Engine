import { useMemo } from "react";

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

type Props = {
  text: string;
  highlights: string[];
  className?: string;
};

export function HighlightedText({ text, highlights, className }: Props) {
  const nodes = useMemo(() => {
    if (!text) return null;
    const uniq = [...new Set(highlights.filter(Boolean))].sort((a, b) => b.length - a.length);
    if (uniq.length === 0) return text;
    const pattern = uniq.map(escapeRegExp).join("|");
    if (!pattern) return text;
    const re = new RegExp(`(${pattern})`, "gi");
    const parts = text.split(re);
    return parts.map((part, i) => {
      const match = uniq.some((h) => part.toLowerCase() === h.toLowerCase());
      if (match) {
        return (
          <mark
            key={i}
            className="rounded bg-amber-400/25 px-0.5 font-medium text-amber-100 ring-1 ring-amber-400/40"
          >
            {part}
          </mark>
        );
      }
      return <span key={i}>{part}</span>;
    });
  }, [text, highlights]);

  return <span className={className}>{nodes}</span>;
}
