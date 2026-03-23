import { useState } from "react";
import axios from "axios";

interface Violation {
  id: string;
  impact: string;
  description: string;
  help: string;
  helpUrl: string;
  nodes_affected: number;
}

interface ScanResult {
  screenshot: string;
  url: string;
  violation_count: number;
  violations: Violation[];
}

const impactColor: Record<string, string> = {
  critical: "bg-red-100 text-red-800 border-red-200",
  serious:  "bg-orange-100 text-orange-800 border-orange-200",
  moderate: "bg-yellow-100 text-yellow-800 border-yellow-200",
  minor:    "bg-blue-100 text-blue-800 border-blue-200",
};

export default function App() {
  const [url, setUrl]         = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult]   = useState<ScanResult | null>(null);
  const [error, setError]     = useState("");

  async function handleScan() {
    if (!url) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await axios.post("http://localhost:8000/scan", { url });
      setResult(res.data);
    } catch {
      setError("Scan failed. Make sure the URL is correct and the backend is running.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">

      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <span className="text-2xl">🔍</span>
          <div>
            <h1 className="text-xl font-semibold text-gray-900">AccessLens</h1>
            <p className="text-sm text-gray-500">AI-powered web accessibility auditor</p>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-10">

        {/* Scan input */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
          <h2 className="text-lg font-medium text-gray-800 mb-1">
            Scan any website for accessibility violations
          </h2>
          <p className="text-sm text-gray-500 mb-4">
            Paste a URL below — AccessLens will check it against WCAG 2.1 standards.
          </p>
          <div className="flex gap-3">
            <input
              type="url"
              placeholder="https://example.com"
              value={url}
              onChange={e => setUrl(e.target.value)}
              onKeyDown={e => e.key === "Enter" && handleScan()}
              className="flex-1 border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleScan}
              disabled={loading || !url}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? "Scanning..." : "Scan"}
            </button>
          </div>
          {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
        </div>

        {/* Loading state */}
        {loading && (
          <div className="text-center py-16 text-gray-500">
            <div className="text-4xl mb-4">⏳</div>
            <p className="text-lg font-medium">Scanning {url}...</p>
            <p className="text-sm mt-1">This takes about 10 seconds</p>
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <div>

            {/* Summary bar */}
            <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6 flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Scanned</p>
                <p className="text-base font-medium text-gray-800 break-all">{result.url}</p>
              </div>
              <div className="text-right">
                <p className="text-4xl font-bold text-red-600">{result.violation_count}</p>
                <p className="text-sm text-gray-500">
                  {result.violation_count === 1 ? "violation" : "violations"} found
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

              {/* Screenshot */}
              <div className="bg-white rounded-xl border border-gray-200 p-4">
                <h3 className="text-sm font-medium text-gray-700 mb-3">Page screenshot</h3>
                <img
                  src={`data:image/png;base64,${result.screenshot}`}
                  alt="Screenshot of scanned page"
                  className="w-full rounded-lg border border-gray-100"
                />
              </div>

              {/* Violations list */}
              <div className="bg-white rounded-xl border border-gray-200 p-4">
                <h3 className="text-sm font-medium text-gray-700 mb-3">
                  Violations ({result.violation_count})
                </h3>
                {result.violations.length === 0 ? (
                  <div className="text-center py-8">
                    <p className="text-2xl mb-2">✅</p>
                    <p className="text-sm text-gray-500">No violations found!</p>
                  </div>
                ) : (
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {result.violations.map((v, i) => (
                      <div
                        key={i}
                        className={`rounded-lg border p-3 ${impactColor[v.impact] || "bg-gray-100 text-gray-800 border-gray-200"}`}
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs font-semibold uppercase tracking-wide">
                            {v.impact}
                          </span>
                          <span className="text-xs">
                            {v.nodes_affected} element{v.nodes_affected !== 1 ? "s" : ""}
                          </span>
                        </div>
                        <p className="text-sm font-medium">{v.help}</p>
                        <p className="text-xs mt-1 opacity-80">{v.description}</p>
                        <a
                          href={v.helpUrl}
                          target="_blank"
                          rel="noreferrer"
                          className="text-xs underline mt-1 inline-block opacity-70 hover:opacity-100"
                        >
                          Learn more
                        </a>
                      </div>
                    ))}
                  </div>
                )}
              </div>

            </div>
          </div>
        )}

      </main>
    </div>
  );
}
