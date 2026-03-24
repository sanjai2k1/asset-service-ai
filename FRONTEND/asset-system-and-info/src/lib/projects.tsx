import { type LucideIcon,MessageCircle, Folder } from "lucide-react";

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
];