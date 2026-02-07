"""JSON output formatter."""

import json
from typing import List, Dict, Any

from .formatters import OutputFormatter


class JSONFormatter(OutputFormatter):
    """Format results as JSON."""

    def format(self, results: List[Dict], metadata: Dict[str, Any]) -> str:
        """
        Format results as pretty-printed JSON.

        Structure:
        {
            "metadata": {
                "generated_at": "2025-06-24T10:30:00",
                "total_matches": 45,
                "total_searched": 230,
                "threshold": 90
            },
            "matches": [
                {
                    "goodreads_title": "...",
                    "bookoutlet_match": "...",
                    "score": 98,
                    "score_pct": "98%",
                    "price": "$9.99",
                    "url": "https://..."
                }
            ]
        }
        """
        # Build metadata
        full_metadata = self._get_default_metadata()
        full_metadata.update(metadata)
        full_metadata['total_matches'] = len(results)

        # Convert results to JSON-friendly format
        matches = []
        for item in results:
            score_str = item.get('Score', '0%')
            score_num = int(score_str.rstrip('%')) if score_str else 0

            match = {
                'goodreads_title': item.get('Query', ''),
                'bookoutlet_match': item.get('Match', ''),
                'score': score_num,
                'score_pct': score_str,
            }

            # Add optional fields if present
            if 'Price' in item:
                match['price'] = item['Price']
            if 'URL' in item:
                match['url'] = item['URL']
            if 'CoverURL' in item:
                match['cover_url'] = item['CoverURL']

            matches.append(match)

        output = {
            'metadata': full_metadata,
            'matches': matches
        }

        return json.dumps(output, indent=2, ensure_ascii=False) + '\n'

    def get_extension(self) -> str:
        """Return 'json' extension."""
        return 'json'
