"""ISBN validation, normalization, and extraction utilities."""

import re
from typing import Optional


def extract_isbn_from_excel_formula(cell_value: str) -> Optional[str]:
    """
    Extract ISBN from Excel formula format used in Goodreads CSV exports.

    Goodreads wraps ISBNs in formulas like: ="0262046482" or ="9780262046480"
    This function extracts the actual ISBN number.

    Args:
        cell_value: The raw cell value from the CSV

    Returns:
        The extracted ISBN string, or None if not found or empty

    Examples:
        >>> extract_isbn_from_excel_formula('="0262046482"')
        '0262046482'
        >>> extract_isbn_from_excel_formula('="9780262046480"')
        '9780262046480'
        >>> extract_isbn_from_excel_formula('=""')
        None
        >>> extract_isbn_from_excel_formula('0262046482')
        '0262046482'
    """
    if not cell_value or not isinstance(cell_value, str):
        return None

    # Handle Excel formula format: ="..."
    formula_match = re.search(r'="([^"]*)"', cell_value)
    if formula_match:
        isbn = formula_match.group(1).strip()
        return isbn if isbn else None

    # If no formula, try to extract ISBN directly
    # Remove common separators and whitespace
    cleaned = cell_value.strip().replace('-', '').replace(' ', '')

    # Check if it looks like an ISBN (10 or 13 digits, possibly with X at end for ISBN-10)
    if re.match(r'^\d{9}[\dX]$', cleaned) or re.match(r'^\d{13}$', cleaned):
        return cleaned

    return None


def normalize_isbn(isbn: str) -> Optional[str]:
    """
    Normalize an ISBN by removing hyphens, spaces, and converting to uppercase.

    Args:
        isbn: The ISBN string to normalize

    Returns:
        Normalized ISBN string, or None if invalid

    Examples:
        >>> normalize_isbn('0-262-04648-2')
        '0262046482'
        >>> normalize_isbn('978-0-262-04648-0')
        '9780262046480'
        >>> normalize_isbn('043942089X')
        '043942089X'
    """
    if not isbn:
        return None

    # Remove hyphens, spaces, and convert to uppercase
    normalized = isbn.strip().replace('-', '').replace(' ', '').upper()

    # Validate length (10 or 13 digits, with possible X at end for ISBN-10)
    if re.match(r'^\d{9}[\dX]$', normalized) or re.match(r'^\d{13}$', normalized):
        return normalized

    return None


def isbn10_to_isbn13(isbn10: str) -> Optional[str]:
    """
    Convert ISBN-10 to ISBN-13 format.

    ISBN-13 is formed by prepending "978" to the first 9 digits of ISBN-10,
    then calculating a new check digit.

    Args:
        isbn10: The ISBN-10 string (with or without check digit)

    Returns:
        ISBN-13 string, or None if invalid

    Examples:
        >>> isbn10_to_isbn13('0262046482')
        '9780262046480'
        >>> isbn10_to_isbn13('043942089X')
        '9780439420891'
    """
    normalized = normalize_isbn(isbn10)
    if not normalized or len(normalized) != 10:
        return None

    # Take first 9 digits and prepend 978
    base = '978' + normalized[:9]

    # Calculate ISBN-13 check digit
    check_sum = 0
    for i, digit in enumerate(base):
        weight = 1 if i % 2 == 0 else 3
        check_sum += int(digit) * weight

    check_digit = (10 - (check_sum % 10)) % 10

    return base + str(check_digit)


def validate_isbn(isbn: str) -> bool:
    """
    Validate an ISBN-10 or ISBN-13 checksum.

    Args:
        isbn: The ISBN string to validate

    Returns:
        True if valid, False otherwise

    Examples:
        >>> validate_isbn('0262046482')
        True
        >>> validate_isbn('9780262046480')
        True
        >>> validate_isbn('0262046483')
        False
    """
    normalized = normalize_isbn(isbn)
    if not normalized:
        return False

    if len(normalized) == 10:
        # ISBN-10 validation
        check_sum = 0
        for i, char in enumerate(normalized):
            if char == 'X':
                digit = 10
            else:
                digit = int(char)
            check_sum += digit * (10 - i)
        return check_sum % 11 == 0

    elif len(normalized) == 13:
        # ISBN-13 validation
        check_sum = 0
        for i, char in enumerate(normalized):
            weight = 1 if i % 2 == 0 else 3
            check_sum += int(char) * weight
        return check_sum % 10 == 0

    return False


def get_all_isbn_variants(isbn: str) -> list[str]:
    """
    Get all valid ISBN variants (both ISBN-10 and ISBN-13) for a given ISBN.

    Args:
        isbn: The ISBN string (either ISBN-10 or ISBN-13)

    Returns:
        List of ISBN variants (may include both formats)

    Examples:
        >>> get_all_isbn_variants('0262046482')
        ['0262046482', '9780262046480']
        >>> get_all_isbn_variants('9780262046480')
        ['9780262046480', '0262046482']
    """
    normalized = normalize_isbn(isbn)
    if not normalized:
        return []

    variants = [normalized]

    if len(normalized) == 10:
        # Convert ISBN-10 to ISBN-13
        isbn13 = isbn10_to_isbn13(normalized)
        if isbn13:
            variants.append(isbn13)
    elif len(normalized) == 13 and normalized.startswith('978'):
        # Convert ISBN-13 to ISBN-10 (only if it starts with 978)
        # This is a reverse operation - extract the 9 digits after 978
        base = normalized[3:12]

        # Calculate ISBN-10 check digit
        check_sum = 0
        for i, digit in enumerate(base):
            check_sum += int(digit) * (10 - i)
        check_digit = (11 - (check_sum % 11)) % 11

        if check_digit == 10:
            isbn10 = base + 'X'
        else:
            isbn10 = base + str(check_digit)

        variants.append(isbn10)

    return variants
