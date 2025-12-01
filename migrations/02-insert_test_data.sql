INSERT INTO reference_values (citation_key, year, author, title, reftype, extra)
SELECT * FROM (
  VALUES
    -- 1. Vihavainen 2011 (BOOK)
    (
      'vihavainen2011',
      2011,
      'Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti',
      'Extreme Apprenticeship Method in Teaching Programming for Beginners.',
      'book',
      '{
        "editor": "",
        "volume": "",
        "number": "",
        "series": "",
        "address": "Helsinki, Finland",
        "edition": "1",
        "month": "01",
        "note": "",
        "isbn": "978-952-000-000-0",
        "publisher": "University of Helsinki",
        "url": "https://example.com/vihavainen2011",
        "doi": ""
      }'::jsonb
    ),

    -- 2. Collins et al. 1991 (ARTICLE)
    (
      'collins1991',
      1991,
      'Allan Collins and John Seely Brown and Ann Holum',
      'Cognitive apprenticeship: making thinking visible',
      'article',
      '{
        "journal": "American Educator",
        "volume": "15",
        "number": "3",
        "pages": "6–11",
        "month": "09",
        "note": "",
        "doi": "10.1000/182",
        "url": "https://example.com/collins1991"
      }'::jsonb
    ),

    -- 3. Martin 2008 (BOOK)
    (
      'martin2008',
      2008,
      'Martin, Robert',
      'Clean Code: A Handbook of Agile Software Craftsmanship',
      'book',
      '{
        "editor": "",
        "volume": "",
        "number": "",
        "series": "",
        "address": "Boston, MA",
        "edition": "1",
        "month": "08",
        "note": "",
        "isbn": "978-0132350884",
        "publisher": "Prentice Hall",
        "url": "https://example.com/cleancode",
        "doi": ""
      }'::jsonb
    )
) AS v(citation_key, year, author, title, reftype, extra)
WHERE NOT EXISTS (SELECT 1 FROM reference_values);
