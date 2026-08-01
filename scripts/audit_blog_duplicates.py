#!/usr/bin/env python3
"""Read-only duplicate-content audit for the Vedium blog.

The script compares the versioned article catalog with the live blog listing,
sitemap, rendered canonicals, and literal internal links. It never writes to
the database or changes remote content.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = ROOT / "vedium_core"
SITE_URL = "https://vediums.com"
DEFAULT_OUTPUT = ROOT / "docs" / "audits" / "blog-duplicates-20260725"
USER_AGENT = "Mozilla/5.0 (compatible; VediumBlogDuplicateAudit/1.0)"

TITLE_METADATA_RE = re.compile(
    r"(?i)(?:^|\s)(?:t[ií]tulo\s+seo:|title:|h1:)|"
    r"\.(?:md|docx?|txt)\s*$|\\"
)


def normalize_text(value: str) -> str:
    value = html.unescape(value or "")
    value = BeautifulSoup(value, "html.parser").get_text(" ", strip=True)
    value = unicodedata.normalize("NFKC", value)
    value = value.translate(
        str.maketrans(
            {
                "\u2018": "'",
                "\u2019": "'",
                "\u201c": '"',
                "\u201d": '"',
                "\u00a0": " ",
                "\u200b": "",
                "\ufeff": "",
            }
        )
    )
    return re.sub(r"\s+", " ", value).strip().casefold()


def content_text(post: dict) -> str:
    parts = [post.get("lead", "")]
    for section in post.get("sections", []):
        parts.append(section.get("heading", ""))
        parts.extend(section.get("body", []))
    for item in post.get("faqs", []):
        parts.extend((item.get("q", ""), item.get("a", "")))
    return normalize_text(" ".join(parts))


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def shingles(value: str, width: int = 5) -> set[tuple[str, ...]]:
    words = re.findall(r"\w+", value, flags=re.UNICODE)
    if len(words) < width:
        return {tuple(words)} if words else set()
    return {tuple(words[index : index + width]) for index in range(len(words) - width + 1)}


def jaccard(left: set, right: set) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 1.0


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def fetch(session: requests.Session, path_or_url: str) -> requests.Response:
    url = path_or_url if path_or_url.startswith("http") else urljoin(SITE_URL, path_or_url)
    response = session.get(url, timeout=30, allow_redirects=False)
    return response


def canonical_from_html(markup: str, response_url: str) -> str:
    soup = BeautifulSoup(markup, "html.parser")
    tag = soup.select_one('link[rel~="canonical"]')
    return urljoin(response_url, tag.get("href")) if tag and tag.get("href") else ""


def rendered_content(markup: str) -> tuple[str, str]:
    soup = BeautifulSoup(markup, "html.parser")
    h1 = soup.select_one("h1")
    article = soup.select_one(".vd-article")
    body = article.get_text(" ", strip=True) if article else ""
    return (h1.get_text(" ", strip=True) if h1 else "", normalize_text(body))


def load_catalog():
    sys.path.insert(0, str(APP_ROOT))
    from vedium_core.blog_content import BLOG_POSTS, _post_url  # noqa: PLC0415

    return BLOG_POSTS, _post_url


def catalog_inventory(blog_posts: dict, post_url) -> tuple[list[dict], list[dict], list[dict]]:
    rows: list[dict] = []
    anomalies: list[dict] = []
    exact_groups: dict[str, list[dict]] = defaultdict(list)
    for slug, post in blog_posts.items():
        normalized = content_text(post)
        digest = sha256(normalized)
        canonical_path = post_url(slug, post)
        row = {
            "article_id": f"code:{slug}",
            "database_id": "",
            "source": "versioned_code",
            "slug": slug,
            "title": post.get("title", ""),
            "h1": post.get("h1") or post.get("title", ""),
            "url": f"{SITE_URL}{canonical_path}",
            "language": post.get("lang") or "pt-BR",
            "category": post.get("category") or "",
            "tag": post.get("tag") or "",
            "content_hash": digest,
            "content_words": len(normalized.split()),
            "canonical": f"{SITE_URL}{canonical_path}",
            "indexable": "yes",
            "sitemap": "pending_live_check",
            "status": "catalog_record",
        }
        rows.append(row)
        exact_groups[digest].append(row)
        problems = []
        title = post.get("title", "")
        h1 = post.get("h1", "")
        for field, value in (("title", title), ("h1", h1)):
            if TITLE_METADATA_RE.search(value or ""):
                problems.append(f"{field}:import_metadata_or_extension")
            if re.search(r"\s{2,}", value or ""):
                problems.append(f"{field}:duplicate_spaces")
            if any(char in (value or "") for char in ("\u200b", "\ufeff")):
                problems.append(f"{field}:invisible_character")
        if problems:
            anomalies.append(
                {
                    "article_id": row["article_id"],
                    "slug": slug,
                    "url": row["url"],
                    "title": title,
                    "h1": h1,
                    "problems": "|".join(problems),
                }
            )

    exact_duplicates = []
    for digest, members in exact_groups.items():
        if len(members) > 1:
            for member in members:
                exact_duplicates.append(
                    {
                        "content_hash": digest,
                        "group_size": len(members),
                        "article_id": member["article_id"],
                        "url": member["url"],
                        "title": member["title"],
                    }
                )
    return rows, anomalies, exact_duplicates


def near_duplicate_pairs(blog_posts: dict, post_url) -> list[dict]:
    prepared = []
    for slug, post in blog_posts.items():
        text = content_text(post)
        prepared.append((slug, post, text, shingles(text), post_url(slug, post)))

    rows = []
    for left_index, left in enumerate(prepared):
        for right in prepared[left_index + 1 :]:
            similarity = jaccard(left[3], right[3])
            if similarity < 0.55:
                continue
            same_language = (left[1].get("lang") or "pt-BR") == (
                right[1].get("lang") or "pt-BR"
            )
            rows.append(
                {
                    "left_article_id": f"code:{left[0]}",
                    "left_url": f"{SITE_URL}{left[4]}",
                    "left_title": left[1].get("title", ""),
                    "right_article_id": f"code:{right[0]}",
                    "right_url": f"{SITE_URL}{right[4]}",
                    "right_title": right[1].get("title", ""),
                    "same_language": "yes" if same_language else "no",
                    "shingle_jaccard": round(similarity, 4),
                    "classification": (
                        "review_near_duplicate" if same_language else "likely_translation"
                    ),
                }
            )
    return sorted(rows, key=lambda row: row["shingle_jaccard"], reverse=True)


def crawl_listing(session: requests.Session) -> list[dict]:
    rows: list[dict] = []
    page = 1
    while page <= 100:
        path = "/blog" if page == 1 else f"/blog?page={page}"
        response = fetch(session, path)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.select(".vd-bl-card")
        if not cards:
            break
        for position, card in enumerate(cards, 1):
            anchor = card.select_one("h2 a") or card.select_one("a.vd-bl-more")
            tag = card.select_one(".vd-bl-tag")
            rows.append(
                {
                    "page": page,
                    "position": position,
                    "title": anchor.get_text(" ", strip=True),
                    "url": urljoin(SITE_URL, anchor.get("href")),
                    "path": urlparse(urljoin(SITE_URL, anchor.get("href"))).path,
                    "tag": tag.get_text(" ", strip=True) if tag else "",
                }
            )
        next_link = soup.select_one('.vd-bl-pager a[href*="page="]')
        page_numbers = [
            int(match.group(1))
            for link in soup.select('.vd-bl-pager a[href*="page="]')
            if (match := re.search(r"[?&]page=(\d+)", link.get("href", "")))
        ]
        maximum = max(page_numbers, default=page)
        if page >= maximum and not soup.find("a", string=re.compile("Próxima|Next", re.I)):
            break
        page += 1
    return rows


def listing_duplicate_groups(cards: list[dict]) -> list[dict]:
    parent = list(range(len(cards)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    by_title: dict[str, list[int]] = defaultdict(list)
    by_url: dict[str, list[int]] = defaultdict(list)
    for index, card in enumerate(cards):
        by_title[normalize_text(card["title"])].append(index)
        by_url[card["url"]].append(index)
    for members in (*by_title.values(), *by_url.values()):
        for index in members[1:]:
            union(members[0], index)

    components: dict[int, list[dict]] = defaultdict(list)
    for index, card in enumerate(cards):
        components[find(index)].append(card)

    rows = []
    group_number = 0
    for members in components.values():
        if len(members) < 2:
            continue
        group_number += 1
        unique_urls = {member["url"] for member in members}
        unique_titles = {normalize_text(member["title"]) for member in members}
        if len(unique_urls) == 1 and len(unique_titles) == 1:
            duplicate_kind = "same_href_repeated"
        elif len(unique_urls) == 1:
            duplicate_kind = "same_href_title_mismatch"
        elif len(unique_titles) == 1:
            duplicate_kind = "same_title_multiple_urls"
        else:
            duplicate_kind = "linked_title_and_href_duplicates"
        for member in members:
            rows.append(
                {
                    "group_id": f"live-title-{group_number:03d}",
                    "title": member["title"],
                    "occurrences": len(members),
                    "unique_urls": len(unique_urls),
                    "unique_titles": len(unique_titles),
                    "duplicate_kind": duplicate_kind,
                    "page": member["page"],
                    "position": member["position"],
                    "url": member["url"],
                    "tag": member["tag"],
                }
            )
    return rows


def cannibalization_review(blog_posts: dict, post_url) -> list[dict]:
    pairs = [
        (
            "A",
            "aprender-ioruba-lingua-e-cultura",
            "o-que-e-o-idioma-ioruba-e-por-que-ele-carrega-cultura-e-memoria",
            "keep_pending_human_review",
            "Broad learning motivation versus language, culture, and memory.",
        ),
        (
            "B",
            "alfabeto-ioruba",
            "alfabeto-ioruba-sons-marcas-e-primeiras-leituras",
            "human_review_required",
            "Both target the Yoruba alphabet; compare query intent and performance before merging.",
        ),
        (
            "C",
            "saudacoes-em-ioruba",
            "primeiras-saudacoes-em-ioruba-para-aprender-com-respeito",
            "human_review_required",
            "Both target beginner greetings; preserve both until Search Console evidence is reviewed.",
        ),
        (
            "D",
            "numeros-em-ioruba",
            "numeros-em-ioruba-logica-uso-e-pratica-inicial",
            "keep_pending_human_review",
            "Number lookup from 1 to 20 versus number-system logic and practice.",
        ),
    ]
    rows = []
    for group, left_slug, right_slug, recommendation, rationale in pairs:
        left, right = blog_posts[left_slug], blog_posts[right_slug]
        similarity = jaccard(shingles(content_text(left)), shingles(content_text(right)))
        rows.append(
            {
                "group": group,
                "left_article_id": f"code:{left_slug}",
                "left_title": left.get("title", ""),
                "left_url": f"{SITE_URL}{post_url(left_slug, left)}",
                "right_article_id": f"code:{right_slug}",
                "right_title": right.get("title", ""),
                "right_url": f"{SITE_URL}{post_url(right_slug, right)}",
                "shingle_jaccard": round(similarity, 4),
                "recommendation": recommendation,
                "rationale": rationale,
                "decision_status": "REVISÃO HUMANA",
            }
        )
    return rows


def check_duplicate_urls(
    session: requests.Session, duplicate_groups: list[dict], catalog_by_slug: dict
) -> list[dict]:
    groups_by_url: dict[str, set[str]] = defaultdict(set)
    for item in duplicate_groups:
        groups_by_url[item["url"]].add(item["group_id"])
    urls = sorted({row["url"] for row in duplicate_groups})
    rows = []
    for url in urls:
        response = fetch(session, url)
        markup = response.text if response.status_code == 200 else ""
        h1, body = rendered_content(markup)
        slug = urlparse(url).path.rstrip("/").split("/")[-1]
        expected = catalog_by_slug.get(slug, {})
        rows.append(
            {
                "group_ids": "|".join(sorted(groups_by_url[url])),
                "url": url,
                "status_code": response.status_code,
                "location": response.headers.get("location", ""),
                "canonical": canonical_from_html(markup, url) if markup else "",
                "expected_canonical": expected.get("canonical", ""),
                "canonical_matches_catalog": (
                    "yes"
                    if markup and canonical_from_html(markup, url) == expected.get("canonical", "")
                    else "no"
                ),
                "h1": h1,
                "rendered_content_hash": sha256(body) if body else "",
                "rendered_words": len(body.split()),
            }
        )
    return rows


def redirect_dry_run(
    duplicate_groups: list[dict], catalog_by_slug: dict
) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in duplicate_groups:
        grouped[row["group_id"]].append(row)

    rows = []
    for group_id, members in sorted(grouped.items()):
        occurrences = int(members[0]["occurrences"])
        unique_urls = sorted({member["url"] for member in members})
        for url in unique_urls:
            slug = urlparse(url).path.rstrip("/").split("/")[-1]
            catalog = catalog_by_slug.get(slug)
            canonical = catalog.get("canonical", "") if catalog else ""
            if not canonical:
                action = "human_review_no_catalog_match"
            elif url == canonical and len(unique_urls) == 1 and occurrences > 1:
                action = "deduplicate_listing_or_database_record"
            elif url == canonical:
                action = "keep_canonical"
            else:
                action = "planned_301_to_catalog_canonical"
            rows.append(
                {
                    "group_id": group_id,
                    "duplicate_kind": members[0]["duplicate_kind"],
                    "source_url": url,
                    "target_url": canonical,
                    "action": action,
                    "decision_status": "BLOCKED_PENDING_DATABASE_BACKUP_AND_GSC",
                    "evidence": (
                        "versioned catalog canonical plus live listing identity; "
                        "production database and Search Console evidence unavailable"
                    ),
                }
            )
    return rows


def crawl_sitemap(session: requests.Session) -> list[dict]:
    response = fetch(session, "/sitemap.xml")
    response.raise_for_status()
    root = ElementTree.fromstring(response.content)
    rows = []
    for item in root.findall("{*}url"):
        loc = item.findtext("{*}loc", default="")
        if "/blog" not in loc:
            continue
        rows.append(
            {
                "url": loc,
                "lastmod": item.findtext("{*}lastmod", default=""),
                "changefreq": item.findtext("{*}changefreq", default=""),
                "priority": item.findtext("{*}priority", default=""),
            }
        )
    return rows


def scan_internal_links(duplicate_groups: list[dict]) -> list[dict]:
    grouped_urls: dict[str, set[str]] = defaultdict(set)
    for row in duplicate_groups:
        grouped_urls[row["group_id"]].add(urlparse(row["url"]).path)
    canonical_preference = {}
    for group_id, paths in grouped_urls.items():
        canonical_preference[group_id] = max(
            paths,
            key=lambda path: (
                path.startswith(("/en/blog/", "/es/blog/")),
                path.count("/"),
                len(path),
            ),
        )

    rows = []
    extensions = {".html", ".py", ".js", ".md", ".json", ".xml"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        if any(part in {".git", "node_modules", ".pytest_cache"} for part in path.parts):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for group_id, paths in grouped_urls.items():
            canonical = canonical_preference[group_id]
            for candidate in paths:
                if candidate == canonical:
                    continue
                for line_number, line in enumerate(lines, 1):
                    if candidate in line:
                        rows.append(
                            {
                                "group_id": group_id,
                                "noncanonical_path": candidate,
                                "preferred_path": canonical,
                                "file": path.relative_to(ROOT).as_posix(),
                                "line": line_number,
                                "context": line.strip()[:240],
                            }
                        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    blog_posts, post_url = load_catalog()
    inventory, title_anomalies, exact_duplicates = catalog_inventory(blog_posts, post_url)
    near_duplicates = near_duplicate_pairs(blog_posts, post_url)
    cannibalization = cannibalization_review(blog_posts, post_url)
    catalog_by_slug = {row["slug"]: row for row in inventory}

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    cards = crawl_listing(session)
    duplicate_groups = listing_duplicate_groups(cards)
    url_checks = check_duplicate_urls(session, duplicate_groups, catalog_by_slug)
    redirect_plan = redirect_dry_run(duplicate_groups, catalog_by_slug)
    sitemap = crawl_sitemap(session)
    sitemap_urls = {row["url"] for row in sitemap}
    for row in inventory:
        row["sitemap"] = "yes" if row["url"] in sitemap_urls else "no"
    internal_links = scan_internal_links(duplicate_groups)

    write_csv(
        output / "article_inventory.csv",
        inventory,
        list(inventory[0]) if inventory else [],
    )
    write_csv(
        output / "live_blog_cards.csv",
        cards,
        ["page", "position", "title", "url", "path", "tag"],
    )
    write_csv(
        output / "duplicate_groups.csv",
        duplicate_groups,
        [
            "group_id",
            "title",
            "occurrences",
            "unique_urls",
            "unique_titles",
            "duplicate_kind",
            "page",
            "position",
            "url",
            "tag",
        ],
    )
    write_csv(
        output / "duplicate_url_checks.csv",
        url_checks,
        [
            "group_ids",
            "url",
            "status_code",
            "location",
            "canonical",
            "expected_canonical",
            "canonical_matches_catalog",
            "h1",
            "rendered_content_hash",
            "rendered_words",
        ],
    )
    write_csv(
        output / "redirect_dry_run.csv",
        redirect_plan,
        [
            "group_id",
            "duplicate_kind",
            "source_url",
            "target_url",
            "action",
            "decision_status",
            "evidence",
        ],
    )
    write_csv(
        output / "live_sitemap_blog_urls.csv",
        sitemap,
        ["url", "lastmod", "changefreq", "priority"],
    )
    write_csv(
        output / "title_anomalies.csv",
        title_anomalies,
        ["article_id", "slug", "url", "title", "h1", "problems"],
    )
    write_csv(
        output / "exact_content_duplicates.csv",
        exact_duplicates,
        ["content_hash", "group_size", "article_id", "url", "title"],
    )
    write_csv(
        output / "near_content_duplicates.csv",
        near_duplicates,
        [
            "left_article_id",
            "left_url",
            "left_title",
            "right_article_id",
            "right_url",
            "right_title",
            "same_language",
            "shingle_jaccard",
            "classification",
        ],
    )
    write_csv(
        output / "cannibalization_review.csv",
        cannibalization,
        [
            "group",
            "left_article_id",
            "left_title",
            "left_url",
            "right_article_id",
            "right_title",
            "right_url",
            "shingle_jaccard",
            "recommendation",
            "rationale",
            "decision_status",
        ],
    )
    write_csv(
        output / "internal_links_to_duplicate_urls.csv",
        internal_links,
        [
            "group_id",
            "noncanonical_path",
            "preferred_path",
            "file",
            "line",
            "context",
        ],
    )

    duplicate_card_groups = len({row["group_id"] for row in duplicate_groups})
    title_counts = Counter(normalize_text(row["title"]) for row in cards)
    duplicate_title_groups = sum(count > 1 for count in title_counts.values())
    same_href_groups = len(
        {
            row["group_id"]
            for row in duplicate_groups
            if row["duplicate_kind"] in {"same_href_repeated", "same_href_title_mismatch"}
        }
    )
    duplicate_components = {
        row["group_id"]: int(row["occurrences"]) for row in duplicate_groups
    }
    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "read_only_dry_run",
        "sources": {
            "versioned_catalog": "vedium_core/vedium_core/blog_content.py",
            "live_blog": f"{SITE_URL}/blog",
            "live_sitemap": f"{SITE_URL}/sitemap.xml",
        },
        "access_gaps": [
            "Database/bench unavailable: database IDs, unpublished records, and a database backup were not inspected.",
            "Google Search Console unavailable: clicks, impressions, position, and index coverage were not inspected.",
            "Backlink analytics unavailable: backlink authority was not used to choose canonical URLs.",
        ],
        "counts": {
            "versioned_articles": len(inventory),
            "live_cards": len(cards),
            "live_unique_card_urls": len({row["url"] for row in cards}),
            "live_unique_card_titles": len({normalize_text(row["title"]) for row in cards}),
            "duplicate_card_components": duplicate_card_groups,
            "duplicate_title_groups": duplicate_title_groups,
            "same_href_duplicate_groups": same_href_groups,
            "extra_duplicate_cards": sum(size - 1 for size in duplicate_components.values()),
            "live_blog_sitemap_urls": len(sitemap),
            "catalog_title_anomalies": len(title_anomalies),
            "exact_catalog_content_duplicate_groups": len(
                {row["content_hash"] for row in exact_duplicates}
            ),
            "near_duplicate_pairs_at_or_above_0_55": len(near_duplicates),
            "cannibalization_groups_for_human_review": len(cannibalization),
            "internal_link_occurrences_to_noncanonical_duplicates": len(internal_links),
            "planned_redirect_rows_blocked": sum(
                row["action"] == "planned_301_to_catalog_canonical"
                for row in redirect_plan
            ),
        },
    }
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
