import React from 'react';
import { projects } from '@/lib/projects';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { ChatInterface } from '@/pages/srcreate/ChatInterface';
import { Link, useParams } from 'react-router-dom';
import { ProjectInfoCard } from './ProjectInfoCard';
import { ArrowRight } from 'lucide-react';

const CreateSrChat = () => {
  const { pathUrl } = useParams<{ pathUrl: string }>();
  const project = projects.find((p) => p.pathUrl === pathUrl);
  if (!project) return <div>No project data available</div>;

  return (
<div className="container mx-auto p-4 md:p-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
<div className="lg:col-span-1 flex flex-col justify-center py-8">
    <ProjectInfoCard
      projectName={project.name}
      projectIcon={project.icon}
      shortDescription={project.shortDescription}
    />
  <Card className="flex flex-col w-full max-w-md mx-auto">
  <CardHeader className="flex-row items-center gap-4">
    <div className="bg-blue-500/10 p-3 rounded-lg">
      <ArrowRight className="w-6 h-6 text-blue-500" />
    </div>
    <CardTitle className="text-2xl font-bold">Service Requests</CardTitle>
  </CardHeader>

  <CardContent className="flex-1 overflow-y-auto">
    <p className="text-base text-foreground/80 mb-4">
      View all created service requests.
    </p>

    <Link to="/service-requests">
      <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
        View Service Requests
      </button>
    </Link>
  </CardContent>
</Card>
  </div>

  <div className="lg:col-span-2 flex">
    <div className="w-full flex-1">
      <ChatInterface />
    </div>
  </div>
</div>
  );
};

export default CreateSrChat;