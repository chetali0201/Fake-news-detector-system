import Analyzer from "../components/Analyzer.jsx";
import MetricsPanel from "../components/MetricsPanel.jsx";
import About from "../components/About.jsx";

export default function Home() {
  return (
    <main className="mx-auto max-w-5xl space-y-14 px-5 pt-10">
      <Analyzer />
      <MetricsPanel />
      <About />
    </main>
  );
}
