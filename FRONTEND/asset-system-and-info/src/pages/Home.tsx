import { ProjectList } from "@/components/projects/ProjectList";
import { projects } from "@/lib/projects";

export default function Home() {
  return (
    <div className="flex-1 relative">
      <div className="container mx-auto px-4 py-8 md:py-12 relative z-10">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tighter mb-4 text-foreground">
          AI-Powered Asset Systems & Information 
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground max-w-3xl mx-auto">
          Manage and interact with healthcare asset data using AI. Get insights, update information, and track services across facility engineering, biomedical equipment, maintenance operations, cleaning services, laundry & linen, and healthcare waste management.
          </p>
        </div>
        <ProjectList projects={projects} />
      </div>
    </div>
  );
}