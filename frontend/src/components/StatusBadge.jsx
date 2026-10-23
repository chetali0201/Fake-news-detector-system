import { useEffect, useState } from "react";
import { getHealth } from "../services/api";

// Checks /api/health on load and every 15 seconds.
export default function StatusBadge() {
  const [state, setState] = useState("checking");
  useEffect(() => {
    const check = () =>
      getHealth()
        .then((h) => setState(h.model_loaded ? "ready" : "untrained"))
        .catch(() => setState("offline"));
    check();
    const id = setInterval(check, 15000);
    return () => clearInterval(id);
  }, []);
  const map = {
    checking: ["Checking server…", "bg-ink/40"],
    ready: ["Backend online, model loaded", "bg-real"],
    untrained: ["Backend online, model NOT trained", "bg-amber-500"],
    offline: ["Backend offline", "bg-fake"],
  };
  const [label, dot] = map[state];
  return (
    <span className="inline-flex items-center gap-2 rounded-full border border-rule bg-white px-3 py-1 text-sm">
      <span className={`h-2.5 w-2.5 rounded-full ${dot}`} /> {label}
    </span>
  );
}
