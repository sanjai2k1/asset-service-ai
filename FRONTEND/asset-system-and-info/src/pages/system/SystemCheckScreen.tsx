import { useState } from "react";
import { request } from "@/lib/api-client";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
type HealthResult = {
  name: string;
  status: "pending" | "success" | "error";
  data?: any;
};

const endpoints = [
  { name: "Health", url: "/system/health" },
  { name: "Postgres DB Health", url: "/system/postgresdbhealth" },
  { name: "Sql Server DB Health", url: "/system/sqlserverdbhealth" },

  { name: "LLM Health", url: "/system/llmhealth" },
  { name: "Cache Health", url: "/system/cachehealth" },
  { name: "Checkpointer Health", url: "/system/checkpointerhealth" },
];

export default function SystemCheckScreen() {
  const [results, setResults] = useState<HealthResult[]>([]);
  const [loading, setLoading] = useState(false);

  const runChecks = async () => {
    setLoading(true);

    const initial = endpoints.map((e) => ({
      name: e.name,
      status: "pending" as const,
    }));

    setResults(initial);

    // ✅ Sequential execution
    for (let i = 0; i < endpoints.length; i++) {
      const endpoint = endpoints[i];

      const res = await request<any>({
        method: "GET",
        url: endpoint.url,
      });

      setResults((prev) =>
        prev.map((item, idx) =>
          idx === i
            ? {
                ...item,
                status: res.success ? "success" : "error",
                data: res.success ? res.data : res.error,
              }
            : item
        )
      );
    }

    setLoading(false);
  };

  return (
    <div className="p-6">
    <h2 className="text-2xl font-semibold mb-4">System Health Check</h2>
  
    <Button onClick={runChecks} disabled={loading}>
      {loading ? "Running..." : "Run System Check"}
    </Button>
  
    <div className="mt-6 space-y-4">
      {results.map((res, index) => (
        <Card
          key={index}
          className={`
            border 
            ${
              res.status === "success"
                ? "bg-green-50 border-green-200"
                : res.status === "error"
                ? "bg-red-50 border-red-200"
                : "bg-yellow-50 border-yellow-200"
            }
          `}
        >
          <CardContent className="p-4">
            <div className="flex justify-between items-center">
              <span className="font-medium">{res.name}</span>
  
              <span
                className={`
                  font-semibold
                  ${
                    res.status === "success"
                      ? "text-green-600"
                      : res.status === "error"
                      ? "text-red-600"
                      : "text-yellow-600"
                  }
                `}
              >
                {res.status}
              </span>
            </div>
  
            {res.data && (
              <pre className="mt-3 text-xs bg-black text-green-400 p-3 rounded-md overflow-x-auto">
                {typeof res.data === "string"
                  ? res.data
                  : JSON.stringify(res.data, null, 2)}
              </pre>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  </div>
  );
}