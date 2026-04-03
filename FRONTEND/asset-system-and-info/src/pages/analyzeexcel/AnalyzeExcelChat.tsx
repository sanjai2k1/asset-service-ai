import { projects } from '@/lib/projects';
import React from 'react'
import { Link,useParams } from 'react-router-dom';

import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { ArrowRight } from 'lucide-react';
import { ProjectInfoCard } from './ProjectInfoCard';
import { ChatInterface } from './ChatInterface';




const AnalyzeExcelChat = () => {
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
  </div>

  <div className="lg:col-span-2 flex">
    <div className="w-full flex-1">
      <ChatInterface />
    </div>
  </div>
</div>
  );
};

export default AnalyzeExcelChat
