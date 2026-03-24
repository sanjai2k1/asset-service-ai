import { BrainCircuit } from "lucide-react";
import { JSX } from "react";
import { Link } from "react-router-dom";

export function Header(): JSX.Element {
  return (
    <header className="border-b sticky top-0 z-50 bg-background/95 backdrop-blur-sm">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link to="/" className="flex items-center gap-3">
          <BrainCircuit className="h-7 w-7 text-primary" />
          <span className="text-xl font-bold tracking-tight text-foreground">
            Asset Systems And Info - AI 
          </span>
        </Link>

        <div className="flex items-center gap-2">
          {/* Future navigation items */}
        </div>
      </div>
    </header>
  );
}