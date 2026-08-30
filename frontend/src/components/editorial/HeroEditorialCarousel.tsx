"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/Button";
import { Icon } from "@/components/ui/Icon";
import type { HeroSlide } from "@/content/home/hero";

interface HeroEditorialCarouselProps {
  slides: HeroSlide[];
}

const AUTOPLAY_MS = 9000;

export function HeroEditorialCarousel({ slides }: HeroEditorialCarouselProps) {
  const [current, setCurrent] = useState(0);
  const [paused, setPaused] = useState(false);
  const reducedMotionRef = useRef(false);
  const heroRef = useRef<HTMLElement>(null);

  useEffect(() => {
    reducedMotionRef.current =
      typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }, []);

  const goTo = useCallback(
    (index: number) => {
      setCurrent(((index % slides.length) + slides.length) % slides.length);
    },
    [slides.length]
  );

  useEffect(() => {
    if (reducedMotionRef.current || paused) return;
    const timer = setTimeout(() => goTo(current + 1), AUTOPLAY_MS);
    return () => clearTimeout(timer);
  }, [current, paused, goTo]);

  useEffect(() => {
    function onVisibilityChange() {
      setPaused(document.hidden);
    }
    document.addEventListener("visibilitychange", onVisibilityChange);
    return () => document.removeEventListener("visibilitychange", onVisibilityChange);
  }, []);

  function onTabKeyDown(event: React.KeyboardEvent<HTMLButtonElement>, index: number) {
    let target: number | null = null;
    if (event.key === "ArrowRight") target = (index + 1) % slides.length;
    else if (event.key === "ArrowLeft") target = (index - 1 + slides.length) % slides.length;
    else if (event.key === "Home") target = 0;
    else if (event.key === "End") target = slides.length - 1;
    if (target === null) return;
    event.preventDefault();
    goTo(target);
  }

  return (
    <section
      ref={heroRef}
      className="v2-editorial-hero"
      aria-roledescription="carrossel"
      aria-label="Destaques Vedium"
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
      onFocus={() => setPaused(true)}
      onBlur={(event) => {
        if (!event.currentTarget.contains(event.relatedTarget as Node)) setPaused(false);
      }}
    >
      <div className="v2-editorial-hero__slides">
        {slides.map((slide, index) => {
          const isActive = index === current;
          return (
            <div
              key={slide.navLabel}
              className={`v2-editorial-hero__slide${isActive ? " is-active" : ""}`}
              id={`v2-hero-slide-${index}`}
              role="group"
              aria-roledescription="slide"
              aria-label={`${index + 1} de ${slides.length}`}
              aria-hidden={isActive ? undefined : true}
            >
              <div className="v2-editorial-hero__media">
                <img
                  src={slide.imageSrc}
                  alt={slide.imageAlt}
                  width={slide.imageWidth}
                  height={slide.imageHeight}
                  loading={index === 0 ? "eager" : "lazy"}
                  fetchPriority={index === 0 ? "high" : undefined}
                />
              </div>
              <div className="v2-editorial-hero__overlay" aria-hidden="true" />
              <div className="v2-editorial-hero__content">
                <div className="v2-container v2-container--wide">
                  <div className="v2-editorial-hero__copy">
                    {slide.eyebrow ? (
                      <p className="v2-eyebrow v2-eyebrow--on-dark v2-editorial-hero__eyebrow">{slide.eyebrow}</p>
                    ) : null}
                    {index === 0 ? (
                      <h1 className="v2-heading v2-editorial-hero__title">{slide.headline}</h1>
                    ) : (
                      <p className="v2-heading v2-editorial-hero__title">{slide.headline}</p>
                    )}
                    <p className="v2-body v2-editorial-hero__support">{slide.support}</p>
                    <Button href={slide.ctaHref} variant="secondary" onDark icon="arrow-right">
                      {slide.ctaLabel}
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <span className="v2-editorial-hero__scroll" aria-hidden="true">
        <span>Scroll</span>
        <Icon name="arrow-down" size="1em" />
      </span>

      <div className="v2-editorial-hero__nav" role="tablist" aria-label="Slides do destaque">
        {slides.map((slide, index) => {
          const isActive = index === current;
          return (
            <button
              key={slide.navLabel}
              type="button"
              className={`v2-editorial-hero__tab${isActive ? " is-active" : ""}`}
              role="tab"
              id={`v2-hero-tab-${index}`}
              aria-selected={isActive}
              aria-controls={`v2-hero-slide-${index}`}
              tabIndex={isActive ? 0 : -1}
              onClick={() => goTo(index)}
              onKeyDown={(event) => onTabKeyDown(event, index)}
            >
              <span className="v2-editorial-hero__tab-track" aria-hidden="true">
                <span className="v2-editorial-hero__tab-fill" />
              </span>
              <span className="v2-editorial-hero__tab-label">{slide.navLabel}</span>
            </button>
          );
        })}
      </div>
    </section>
  );
}
