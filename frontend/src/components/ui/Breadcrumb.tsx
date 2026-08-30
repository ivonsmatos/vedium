import Link from "next/link";
import { Icon } from "./Icon";
import type { BreadcrumbItem } from "@/types/language";

interface BreadcrumbProps {
  items: BreadcrumbItem[];
}

export function Breadcrumb({ items }: BreadcrumbProps) {
  return (
    <nav className="v2-breadcrumb" aria-label="breadcrumb">
      <ol style={{ display: "flex", alignItems: "center", gap: "inherit", listStyle: "none", margin: 0, padding: 0, flexWrap: "wrap" }}>
        {items.map((item, index) => {
          const isLast = index === items.length - 1;
          return (
            <li key={item.label} style={{ display: "flex", alignItems: "center", gap: "inherit" }}>
              {item.href && !isLast ? (
                <>
                  <Link href={item.href}>{item.label}</Link>
                  <span className="v2-breadcrumb__sep" aria-hidden="true">
                    <Icon name="chevron-right" size="0.85em" />
                  </span>
                </>
              ) : (
                <span className="v2-breadcrumb__current" aria-current="page">
                  {item.label}
                </span>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
