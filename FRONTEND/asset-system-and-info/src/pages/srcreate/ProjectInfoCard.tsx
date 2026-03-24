import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

type ProjectService = {
  service: string;
  requestType: string;
};

type ProjectInfoCardProps = {
  projectName: string;
  projectIcon: React.ElementType;
  shortDescription: string;
  services: ProjectService[];
};

export const ProjectInfoCard: React.FC<ProjectInfoCardProps> = ({
  projectName,
  projectIcon: Icon,
  shortDescription,
  services,
}) => {
  return (
    <Card className="flex flex-col w-full max-w-md mx-auto">
               <CardHeader className="flex-row items-center gap-4">
        <div className="bg-primary/10 p-3 rounded-lg">
          <Icon className="w-6 h-6 text-primary" />
        </div>
        <CardTitle className="text-2xl font-bold">{projectName}</CardTitle>
      </CardHeader>

      {/* Scrollable content */}
      <CardContent className="flex-1 overflow-y-auto">
        <p className="text-base text-foreground/80 mb-4">{shortDescription}</p>
      </CardContent>
    </Card>
  );
};