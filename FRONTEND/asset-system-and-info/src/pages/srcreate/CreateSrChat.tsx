import React from 'react';
import { projects } from '@/lib/projects';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { ChatInterface } from '@/pages/srcreate/ChatInterface';
import { useParams } from 'react-router-dom';
import { ProjectInfoCard } from './ProjectInfoCard';

const CreateSrChat = () => {
  const { pathUrl } = useParams<{ pathUrl: string }>();
  const project = projects.find((p) => p.pathUrl === pathUrl);
  if (!project) return <div>No project data available</div>;
  const Icon = project.icon;
  const services = [
    { service: 'FEMS', requestType: 'T & C' },
    { service: 'FEMS', requestType: 'Unscheduled Maintenance' },
    { service: 'BEMS', requestType: 'T & C' },
    { service: 'BEMS', requestType: 'Unscheduled Maintenance' },
    { service: 'CLS', requestType: 'User Request' },
    { service: 'CLS', requestType: 'Incident' },
    { service: 'LLS', requestType: 'User Request' },
    { service: 'LLS', requestType: 'Incident' },
    { service: 'HWMS', requestType: 'General Request' },
  ];
  
  return (
<div className="container mx-auto p-4 md:p-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
<div className="lg:col-span-1 flex flex-col justify-center py-8">
    <ProjectInfoCard
      projectName={project.name}
      projectIcon={project.icon}
      shortDescription={project.shortDescription}
      services={services} // your array of service objects
    />
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