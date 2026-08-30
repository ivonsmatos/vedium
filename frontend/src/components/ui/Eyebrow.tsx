import { ReactNode } from "react";

interface EyebrowProps {
  children: ReactNode;
  onDark?: boolean;
  className?: string;
}

export function Eyebrow({ children, onDark = false, className = "" }: EyebrowProps) {
  const darkClass = onDark ? "v2-eyebrow--on-dark" : "";
  
  return (
    <p className={`v2-eyebrow ${darkClass} ${className}`.trim()}>
      {children}
    </p>
  );
}
