import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { getMetrics } from "../services/api";

const pct = (v) => `${(v * 100).toFixed(2)}%`;

export default function MetricsPanel() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => { getMetrics().then(setData).catch((e) => setError(e.message)); }, []);

  if (error) return <Section><p className="rounded border border-rule bg-white p-4 text-ink/70">Metrics unavailable: {error}</p></Section>;
  if (!data) return <Section><p className="text-ink/60">Loading metrics…</p></Section>;

  const t = data.selected_test;
  const cards = [["Accuracy", t.accuracy], ["Precision", t.precision], ["Recall", t.recall], ["F1-score", t.f1]];
  const labels = ["FAKE", "REAL"];
  const max = Math.max(...t.confusion_matrix.flat(), 1);
  const chartData = Object.entries(data.models).map(([name, m]) => ({
    name, Accuracy: +(m.test.accuracy * 100).toFixed(2), Precision: +(m.test.precision * 100).toFixed(2),
    Recall: +(m.test.recall * 100).toFixed(2), F1: +(m.test.f1 * 100).toFixed(2),
  }));

  return (
    <Section>
      {data.dataset.is_sample && (
        <p className="mb-4 rounded border border-amber-500 bg-amber-50 p-3 text-sm">
          These metrics come from the tiny sample file and say nothing about real-world accuracy. Train on the full dataset.
        </p>
      )}
      <p className="mb-4 text-sm text-ink/70">
        Selected model: <strong>{data.selected_model}</strong>. Scores are on the held-out test set
        ({data.dataset.test} articles); FAKE is the positive class.
      </p>
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        {cards.map(([n, v]) => (
          <div key={n} className="rounded border border-rule bg-white p-4">
            <p className="text-sm text-ink/60">{n}</p>
            <p className="font-serif text-3xl font-bold">{pct(v)}</p>
          </div>
        ))}
      </div>

      <div className="mt-8 grid gap-8 md:grid-cols-2">
        <div>
          <h3 className="mb-2 font-semibold">Confusion matrix (test set)</h3>
          <div className="grid grid-cols-[auto_1fr_1fr] gap-1 text-center text-sm">
            <div />
            {labels.map((l) => <div key={l} className="font-medium">Predicted {l}</div>)}
            {t.confusion_matrix.map((row, i) => (
              <Row key={i} label={`Actual ${labels[i]}`} row={row} max={max} good={i} />
            ))}
          </div>
        </div>
        <div>
          <h3 className="mb-2 font-semibold">Model comparison (test set, %)</h3>
          <div className="h-64">
            <ResponsiveContainer>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e4dfd3" />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis domain={[0, 100]} />
                <Tooltip /><Legend />
                <Bar dataKey="Accuracy" fill="#14213d" />
                <Bar dataKey="Precision" fill="#4a5a85" />
                <Bar dataKey="Recall" fill="#2e7d4f" />
                <Bar dataKey="F1" fill="#b3261e" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </Section>
  );
}

// One matrix row; diagonal cells (correct predictions) are green, off-diagonal red.
function Row({ label, row, max, good }) {
  return (
    <>
      <div className="flex items-center pr-2 font-medium">{label}</div>
      {row.map((n, j) => {
        const rgb = j === good ? "46,125,79" : "179,38,30";
        return (
          <div key={j} className="rounded p-5 text-lg font-bold"
            style={{ background: `rgba(${rgb},${0.12 + 0.7 * (n / max)})` }}>{n}</div>
        );
      })}
    </>
  );
}

function Section({ children }) {
  return <section><h2 className="mb-4 font-serif text-2xl font-bold">Model performance</h2>{children}</section>;
}
