import { Link } from "react-router-dom";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import type { Project } from "@/lib/projects";
import { cn } from "@/lib/utils";

export function ProjectCard({ project }: { project: Project }) {
  const Icon = project.icon;

  return (
    <Card className="flex flex-col hover:shadow-lg transition-shadow duration-300 border-primary/20 hover:border-primary/50">
      <CardHeader className="flex-row items-start gap-4 space-y-0 pb-4">
        <div className="bg-primary/10 p-3 rounded-lg">
          <Icon className="w-6 h-6 text-primary" />
        </div>

        <div>
          <CardTitle className="text-lg font-semibold">
            {project.name}
          </CardTitle>
          <CardDescription className="text-sm mt-1">
            {project.shortDescription}
          </CardDescription>
        </div>
      </CardHeader>

      <CardContent className="flex-grow" />

      <CardFooter className="pt-4">
        <Button asChild className="w-full" variant="outline">
          <Link to={`/domain/${project.pathUrl}`} >
            {project.linkText}
            <ArrowRight className="ml-2 h-4 w-4" />
          </Link>
        </Button>
      </CardFooter>
    </Card>
  );
}