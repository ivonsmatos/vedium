import Image from "next/image";

interface MediaProps {
  src?: string | null;
  alt?: string;
  width?: number;
  height?: number;
  priority?: boolean;
  objectPosition?: string;
  className?: string;
}

export function Media({
  src,
  alt = "",
  width = 800,
  height = 600,
  priority = false,
  objectPosition = "center",
  className = "",
}: MediaProps) {
  if (!src) {
    return (
      <div className={`v2-media-empty ${className}`.trim()}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="2rem"
          height="2rem"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <rect width="18" height="18" x="3" y="3" rx="2" ry="2" />
          <circle cx="9" cy="9" r="2" />
          <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21" />
        </svg>
      </div>
    );
  }

  return (
    <Image
      src={src}
      alt={alt}
      width={width}
      height={height}
      priority={priority}
      className={className}
      style={{ objectPosition }}
    />
  );
}
