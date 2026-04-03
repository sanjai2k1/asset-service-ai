import { useEffect, useState } from "react";
import { request } from "@/lib/api-client"; // ✅ your global handler
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

type ServiceRequest = {
  id: string;
  service: string;
  request_type: string;
  data: Record<string, any>;
  final_summary: string;
  created_at: string;
  updated_at: string;
};

export default function SrDataGrid() {
  const [records, setRecords] = useState<ServiceRequest[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [limit] = useState(5);
  const [loading, setLoading] = useState(false);

  const fetchRecords = async () => {
    setLoading(true);
    try {
      const res = await request<{
        total_count: number;
        records: ServiceRequest[];
      }>({
        method: "POST",
        url: "/srcreation/service-requests",
        data: {
          limit,
          offset: (page - 1) * limit,
        },
      });

      if (res.success) {
        setRecords(res.data.records);
        setTotal(res.data.total_count);
      } else {
        console.error("Failed to fetch records:", res.error);
      }
    } catch (err) {
      console.error("Unexpected error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecords();
  }, [page]);

  const totalPages = Math.ceil(total / limit);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-semibold mb-4">Service Requests</h2>

      <div className="flex gap-2 mb-4">
        <Button
          onClick={() => setPage((p) => Math.max(p - 1, 1))}
          disabled={page === 1 || loading}
        >
          Previous
        </Button>
        <Button
          onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
          disabled={page === totalPages || loading}
        >
          Next
        </Button>
        <span className="ml-4 self-center">
          Page {page} of {totalPages}
        </span>
      </div>

      {loading ? (
        
  <div className="flex justify-center py-10">
  <div className="w-10 h-10 border-4 border-blue-500 border-dashed rounded-full animate-spin"></div>
</div>    
  ) : (
        <div className="space-y-4">
          {records.map((r) => (
            <Card key={r.id} className="border border-gray-200">
              <CardContent className="p-4">
                <div className="flex justify-between items-center">
                  <span className="font-medium">{r.service}</span>
                  <span className="text-sm text-gray-500">{r.request_type}</span>
                </div>

                <div className="mt-2 text-sm">
                {r.data && Object.entries(r.data).map(([key, value]) => (
          <div key={key}>
            <strong>{key.replace(/_/g, ' ')}:</strong> {value}
          </div>
        ))}
                  
                  <div className="mt-1">
                    <strong>Summary:</strong> {r.final_summary}
                  </div>
                  <div className="mt-1 text-xs text-gray-400">
                    Created: {new Date(r.created_at).toLocaleString()} | Updated:{" "}
                    {new Date(r.updated_at).toLocaleString()}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}