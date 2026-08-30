import { ReactNode } from "react";

interface ContainerProps {
  children: ReactNode;
  width?: "default" | "narrow" | "wide" | "full";
  className?: string;
}

export function Container({ children, width = "default", className = "" }: ContainerProps) {
  const widthClass = width === "default" ? "v2-container" : `v2-container v2-container--${width}`;
  
  return (
    <div className={`${widthClass} ${className}`.trim()}>
      {children}
    </div>
  );
}
