import { useState } from "react";
import { predict } from "../services/api";

const MAX_CHARS = 20000; // keep in sync with MAX_INPUT_CHARS in backend/.env
// Invented examples only to try the UI. They are NOT ground truth.
const SAMPLES = [
  "Shocking secret cure doctors don't want you to know about, share before it is deleted",
  "City council approves budget for new public library branch after public consultation",
];

export default function Analyzer() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function analyze() {
    const t = text.trim();
    if (!t) return setError("Please paste a headline or article first.");
    if (t.split(/\s+/).length < 3) return setError("Please enter at least 3 words.");
    if (t.length > MAX_CHARS) return setError(`Text is too long (max ${MAX_CHARS} characters).`);
    setError(""); setResult(null); setLoading(true);
    try {
      setResult(await predict(t));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  function clearAll() { setText(""); setResult(null); setError(""); }

  const isFake = result?.label === "FAKE";
  const color = isFake ? "text-fake border-fake" : "text-real border-real";

  return (
    <section>
      <h2 className="font-serif text-2xl font-bold">Analyze a news item</h2>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={8}
        placeholder="Paste a headline or full news article here…"
        className="mt-4 w-full rounded border border-rule bg-white p-4 outline-none focus:border-ink"
      />
      <div className="mt-1 text-right text-xs text-ink/50">{text.length} / {MAX_CHARS}</div>
      <div className="mt-3 flex flex-wrap gap-3">
        <button onClick={analyze} disabled={loading}
          className="rounded bg-ink px-5 py-2 font-medium text-white disabled:opacity-50">
          {loading ? "Analyzing…" : "Analyze News"}
        </button>
        <button onClick={clearAll} className="rounded border border-ink px-5 py-2">Clear</button>
        {SAMPLES.map((s, i) => (
          <button key={i} onClick={() => { setText(s); setResult(null); setError(""); }}
            className="rounded border border-rule bg-white px-4 py-2 text-sm">Sample {i + 1}</button>
        ))}
      </div>

      {loading && (
        <div className="mt-5 flex items-center gap-3 text-ink/70">
          <span className="h-5 w-5 animate-spin rounded-full border-2 border-ink border-t-transparent" />
          Running the model…
        </div>
      )}
      {error && <p role="alert" className="mt-5 rounded border border-fake bg-fake/5 p-3 text-fake">{error}</p>}

      {result && (
        <div className={`mt-6 rounded border-l-8 bg-white p-6 ${color}`}>
          <p className="text-sm uppercase tracking-widest text-ink/60">Model prediction</p>
          <p className="font-serif text-4xl font-bold">{isFake ? "FAKE NEWS" : "REAL NEWS"}</p>
          <p className="mt-2 text-ink">
            Model confidence: <strong>{(result.confidence * 100).toFixed(1)}%</strong>
            <span className="text-ink/60"> ({result.model})</span>
          </p>
          <div className="mt-3 space-y-1 text-sm text-ink">
            {Object.entries(result.probabilities).map(([k, v]) => (
              <div key={k} className="flex items-center gap-2">
                <span className="w-10">{k}</span>
                <div className="h-2 flex-1 rounded bg-rule">
                  <div className={`h-2 rounded ${k === "FAKE" ? "bg-fake" : "bg-real"}`} style={{ width: `${v * 100}%` }} />
                </div>
                <span className="w-14 text-right">{(v * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
          <p className="mt-4 text-sm text-ink/70">
            Confidence shows how sure the model is about its own label. It is <strong>not</strong> the
            probability that the claim is true. {result.disclaimer}
          </p>
        </div>
      )}
    </section>
  );
}
