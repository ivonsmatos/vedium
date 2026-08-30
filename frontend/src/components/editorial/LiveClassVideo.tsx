"use client";

import { useEffect, useRef } from "react";

interface LiveClassVideoProps {
  src: string;
  poster: string;
}

export function LiveClassVideo({ src, poster }: LiveClassVideoProps) {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video || !("IntersectionObserver" in window)) return;
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting && !video.paused) video.pause();
        });
      },
      { threshold: 0.1 }
    );
    observer.observe(video);
    return () => observer.disconnect();
  }, []);

  return (
    <video ref={videoRef} controls preload="metadata" poster={poster} playsInline>
      <source src={src} type="video/mp4" />
    </video>
  );
}
