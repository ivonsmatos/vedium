const ICON_PATHS: Record<string, string> = {
  "chevron-right": "M9 6l6 6-6 6",
  "chevron-down": "M6 9l6 6 6-6",
  check: "M20 6L9 17l-5-5",
  close: "M18 6L6 18M6 6l12 12",
  play: "M8 5v14l11-7z",
  "arrow-right": "M5 12h14M13 6l6 6-6 6",
  "arrow-down": "M12 5v14M6 13l6 6 6-6",
  whatsapp:
    "M12 2C6.48 2 2 6.48 2 12c0 1.85.5 3.58 1.35 5.06L2 22l5.06-1.33A9.94 9.94 0 0012 22c5.52 0 10-4.48 10-10S17.52 2 12 2z",
  image:
    "M4 5h16a1 1 0 011 1v12a1 1 0 01-1 1H4a1 1 0 01-1-1V6a1 1 0 011-1z M8 10a1 1 0 102 0 1 1 0 00-2 0 M3 16l5-5 3 3 4-4 5 5",
  instagram:
    "M7 2h10a5 5 0 015 5v10a5 5 0 01-5 5H7a5 5 0 01-5-5V7a5 5 0 015-5zm5 5a5 5 0 100 10 5 5 0 000-10zm5.5-.75a1.25 1.25 0 100 2.5 1.25 1.25 0 000-2.5z",
  linkedin:
    "M4.98 3.5A2.5 2.5 0 1 1 5 8.5a2.5 2.5 0 0 1-.02-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1V21h-4v-5.6c0-1.34-.03-3.07-1.87-3.07-1.87 0-2.16 1.46-2.16 2.97V21H9z",
};

const STROKE_ICONS = new Set(["chevron-right", "chevron-down", "arrow-right", "arrow-down", "image"]);

interface IconProps {
  name: string;
  decorative?: boolean;
  label?: string;
  size?: string;
  className?: string;
}

export function Icon({ name, decorative = true, label, size = "1.25em", className = "" }: IconProps) {
  const stroke = STROKE_ICONS.has(name);
  const accessibleProps = decorative
    ? { "aria-hidden": true as const }
    : { role: "img" as const, "aria-label": label };

  return (
    <span className={`v2-icon ${className}`.trim()} style={{ width: size, height: size }} {...accessibleProps}>
      <svg viewBox="0 0 24 24" aria-hidden={decorative || undefined} focusable="false">
        <path
          d={ICON_PATHS[name] ?? ""}
          fill={stroke ? "none" : undefined}
          stroke={stroke ? "currentColor" : undefined}
          strokeWidth={stroke ? 1.6 : undefined}
          strokeLinecap={stroke ? "round" : undefined}
          strokeLinejoin={stroke ? "round" : undefined}
        />
      </svg>
    </span>
  );
}
