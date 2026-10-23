import Home from "./pages/Home.jsx";
import StatusBadge from "./components/StatusBadge.jsx";

export default function App() {
  return (
    <div className="min-h-screen">
      <header className="border-b border-rule">
        <div className="mx-auto flex max-w-5xl flex-wrap items-end justify-between gap-3 px-5 py-6">
          <div>
            <h1 className="font-serif text-4xl font-bold tracking-tight">Fake News Detector</h1>
            <p className="mt-1 text-ink/70">Analyze news text using NLP and Machine Learning</p>
          </div>
          <StatusBadge />
        </div>
      </header>
      <Home />
      <footer className="mt-16 border-t border-rule py-6 text-center text-sm text-ink/60">
        College project by a B.Tech Computer Science (Data Science) student. For learning purposes only.
      </footer>
    </div>
  );
}
