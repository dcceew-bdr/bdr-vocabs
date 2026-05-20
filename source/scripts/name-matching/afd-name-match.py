#!/usr/bin/env python3

import re
import sys
import urllib.parse
import urllib.request

BASE = "https://test.biodiversity.org.au"


def fetch_html(url: str) -> str:
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8", errors="replace")


def extract_afd_taxon_iri(html: str):
    matches = re.findall(
        r'http://biodiversity\.org\.au/afd\.taxon/[a-f0-9-]+',
        html
    )
    return sorted(set(matches))


def resolve_taxon_page(page_url: str):
    html = fetch_html(page_url)
    iris = extract_afd_taxon_iri(html)

    if iris:
        return iris[0]

    return page_url


def normalise_name(name: str) -> str:
    # Remove trailing parenthetical qualifiers.
    search_name = re.sub(
        r"\s*\([^)]*\)\s*$",
        "",
        name
    ).strip()

    parts = search_name.split()

    # Keep trinomial names where the third word looks like a subspecies.
    if len(parts) >= 3 and parts[2].islower():
        return " ".join(parts[:3])

    # Otherwise reduce to binomial.
    return " ".join(parts[:2])


def search_afd(name: str):
    encoded = urllib.parse.quote_plus(name)

    url = (
        f"{BASE}/afd/search/names"
        f"?search=true&keyword={encoded}"
    )

    html = fetch_html(url)

    concept_uris = sorted(
        set(
            re.findall(
                r'id="afdTaxonURI".*?href="([^"]+)"',
                html,
                flags=re.DOTALL
            )
        )
    )

    if concept_uris:
        return concept_uris

    genus = name.split()[0]

    taxon_links = sorted(
        set(
            re.findall(
                r'<td><a href="../taxa/([^"]+)">',
                html
            )
        )
    )

    taxon_links = [
        m for m in taxon_links
        if m.startswith(genus + "_")
    ]

    resolved_uris = []

    for m in taxon_links:
        page_url = f"{BASE}/afd/taxa/{m}"
        resolved_uris.append(resolve_taxon_page(page_url))

    return resolved_uris


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python3 afd-name-match.py input-file",
            file=sys.stderr
        )
        sys.exit(1)

    infile = sys.argv[1]

    with open(infile, encoding="utf-8-sig") as f:
        print("input_name,search_name,matched_uri,match_count")

        for line in f:
            name = line.strip()

            if not name:
                continue

            search_name = normalise_name(name)

            uris = search_afd(search_name)

            if uris:
                for uri in uris:
                    print(f'"{name}","{search_name}","{uri}",{len(uris)}')
            else:
                print(f'"{name}","{search_name}","",0')


if __name__ == "__main__":
    main()