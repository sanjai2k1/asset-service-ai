import { useParams } from "react-router-dom";
import CreateSrChat  from "@/pages/srcreate/CreateSrChat";
import AnalyzeExcelChat from "@/pages/analyzeexcel/AnalyzeExcelChat";

export default function DynamicDomain() {
  const { pathUrl } = useParams<{ pathUrl: string }>();

  // Decide component based on pathUrl
  switch (pathUrl) {
    case "srcreate":
      return <CreateSrChat />;
    case "analyze-excel":
      return <AnalyzeExcelChat/>;

    default:
      return <div>Page not found: {pathUrl}</div>;
  }
}