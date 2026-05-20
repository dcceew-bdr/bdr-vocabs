#!/usr/bin/env python3

import re
import sys
import urllib.parse
import urllib.request

BASE = "https://test.biodiversity.org.au"


def search_afd(name: str):
    encoded = urllib.parse.quote_plus(name)

    url = (
        f"{BASE}/afd/search/names"
        f"?search=true&keyword={encoded}"
    )

    with urllib.request.urlopen(url) as response:
        html = response.read().decode("utf-8", errors="replace")

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

    return [
        f"{BASE}/afd/taxa/{m}"
        for m in taxon_links
    ]


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

            search_name = re.sub(
    r"\s*\([^)]*\)\s*$",
    "",
    name
).strip()

# Remove trailing population qualifiers after a binomial or trinomial.
            search_name = re.sub(
                r"\s*\([^)]*\)\s*$",
                "",
                name
            ).strip()

            parts = search_name.split()

            if len(parts) >= 3 and parts[2].islower():
                search_name = " ".join(parts[:3])
            else:
                search_name = " ".join(parts[:2])
                
            # Remove trailing population qualifiers after
            # a binomial or trinomial.
            uris = search_afd(search_name)

            if uris:
                for uri in uris:
                    print(f'"{name}","{search_name}","{uri}",{len(uris)}')
            else:
                print(f'"{name}","{search_name}","",0')


if __name__ == "__main__":
    main()