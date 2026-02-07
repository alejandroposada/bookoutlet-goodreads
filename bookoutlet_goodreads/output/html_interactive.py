"""Interactive HTML output formatter using Jinja2."""

from typing import List, Dict, Any
from pathlib import Path

from jinja2 import Template

from .formatters import OutputFormatter


class HTMLInteractiveFormatter(OutputFormatter):
    """Format results as interactive HTML with sorting and filtering."""

    def format(self, results: List[Dict], metadata: Dict[str, Any]) -> str:
        """
        Format results as interactive HTML report.

        Features:
        - Sortable columns
        - Search filter
        - Score filter
        - Separate sections for certain vs potential matches
        - Book cover thumbnails
        - Clickable links
        - Responsive design
        """
        # Load template
        template_path = Path(__file__).parent.parent / 'templates' / 'report.html'
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        template = Template(template_content)

        # Build full metadata
        full_metadata = self._get_default_metadata()
        full_metadata.update(metadata)
        full_metadata['total_matches'] = len(results)

        # Convert results to template-friendly format and separate by certainty
        certain_matches = []
        potential_matches = []

        for item in results:
            score_str = item.get('Score', '0%')
            score_num = int(score_str.rstrip('%')) if score_str else 0
            match_type = item.get('MatchType', 'fuzzy')

            match = {
                'goodreads_title': item.get('Query', ''),
                'bookoutlet_match': item.get('Match', ''),
                'score': score_num,
                'score_pct': score_str,
                'price': item.get('Price', ''),
                'url': item.get('URL', ''),
                'cover_url': item.get('CoverURL', ''),
                'match_type': match_type
            }

            # Categorize as certain or potential
            # Certain: ISBN exact match OR 100% score OR 95%+ with author verification
            is_certain = (
                match_type == 'isbn_exact' or
                score_num == 100 or
                (score_num >= 95 and 'author' in match_type)
            )

            if is_certain:
                certain_matches.append(match)
            else:
                potential_matches.append(match)

        # Update metadata with counts
        full_metadata['certain_matches'] = len(certain_matches)
        full_metadata['potential_matches'] = len(potential_matches)

        # Render template
        html = template.render(
            certain_matches=certain_matches,
            potential_matches=potential_matches,
            metadata=full_metadata
        )

        return html

    def get_extension(self) -> str:
        """Return 'html' extension."""
        return 'html'
