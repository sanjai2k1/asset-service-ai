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
};

export const ProjectInfoCard: React.FC<ProjectInfoCardProps> = ({
  projectName,
  projectIcon: Icon,
  shortDescription,
}) => {
  return (
<Card className="flex flex-col w-full max-w-md mx-auto">
  <CardHeader className="flex-row items-center gap-4">
    <div className="bg-primary/10 p-3 rounded-lg">
      <Icon className="w-6 h-6 text-primary" />
    </div>
    <CardTitle className="text-2xl font-bold">{projectName}</CardTitle>
  </CardHeader>

  <CardContent className="flex-1 overflow-y-auto">
    <p className="text-base text-foreground/80 mb-6">
      {shortDescription}
    </p>

    {/* Steps Section */}
    <div className="space-y-4">
      <div className="flex items-start gap-3">
        <div className="bg-primary text-white w-6 h-6 flex items-center justify-center rounded-full text-sm font-semibold">
          1
        </div>
        <p className="text-sm text-foreground/90">
          Upload your Excel file
        </p>
      </div>

      <div className="flex items-start gap-3">
        <div className="bg-primary text-white w-6 h-6 flex items-center justify-center rounded-full text-sm font-semibold">
          2
        </div>
        <p className="text-sm text-foreground/90">
          AI analyzes the data automatically
        </p>
      </div>

      <div className="flex items-start gap-3">
        <div className="bg-primary text-white w-6 h-6 flex items-center justify-center rounded-full text-sm font-semibold">
          3
        </div>
        <p className="text-sm text-foreground/90">
          Start asking analysis questions.
        </p>
      </div>
    </div>
  </CardContent>
</Card>
  );
};