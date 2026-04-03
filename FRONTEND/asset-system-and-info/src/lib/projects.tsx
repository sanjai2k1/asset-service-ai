import { type LucideIcon,MessageCircle, Folder ,FileSpreadsheet} from "lucide-react";

export type Project = {
  id: string;
  name: string;
  shortDescription: string;
  icon: LucideIcon;
  pathUrl : string;
  linkText:string;
};

export const projects: Project[] = [
  {
    id: "1",
    name: "Service Request Chat",
    shortDescription: "Creates a Service Request based on user need",
    icon: MessageCircle,
    pathUrl : "srcreate",
    linkText:"Create a SR"
  },
  {
    id: "2",
    name: "Excel Analysis helper",
    shortDescription: "Analyze excel based on user need",
    icon: FileSpreadsheet,
    pathUrl : "analyze-excel",
    linkText:"Start Analysis"
  },
  
];