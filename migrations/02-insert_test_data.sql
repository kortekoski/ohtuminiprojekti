-- Insert test data only if the tables are empty
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM reference_values) THEN
    
    -- 1. Insert references without authors
    INSERT INTO reference_values (citation_key, year, title, reftype, extra)
    VALUES
      -- 1. Vihavainen 2011 (BOOK)
      (
        'vihavainen2011',
        2011,
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
      );

    -- 2. Insert authors
    INSERT INTO authors (name)
    VALUES
      ('Vihavainen, Arto'),
      ('Paksula, Matti'),
      ('Luukkainen, Matti'),
      ('Collins, Allan'),
      ('Seely Brown, John'),
      ('Holum, Ann'),
      ('Martin, Robert')
    ON CONFLICT (name) DO NOTHING;

    -- 3. Create reference-author mappings
    -- Vihavainen 2011
    INSERT INTO reference_authors (reference_id, author_id, author_order)
    SELECT 
      (SELECT id FROM reference_values WHERE citation_key = 'vihavainen2011'),
      (SELECT id FROM authors WHERE name = 'Vihavainen, Arto'),
      0
    UNION ALL
    SELECT 
      (SELECT id FROM reference_values WHERE citation_key = 'vihavainen2011'),
      (SELECT id FROM authors WHERE name = 'Paksula, Matti'),
      1
    UNION ALL
    SELECT 
      (SELECT id FROM reference_values WHERE citation_key = 'vihavainen2011'),
      (SELECT id FROM authors WHERE name = 'Luukkainen, Matti'),
      2
    UNION ALL
    -- Collins 1991
    SELECT 
      (SELECT id FROM reference_values WHERE citation_key = 'collins1991'),
      (SELECT id FROM authors WHERE name = 'Collins, Allan'),
      0
    UNION ALL
    SELECT 
      (SELECT id FROM reference_values WHERE citation_key = 'collins1991'),
      (SELECT id FROM authors WHERE name = 'Seely Brown, John'),
      1
    UNION ALL
    SELECT 
      (SELECT id FROM reference_values WHERE citation_key = 'collins1991'),
      (SELECT id FROM authors WHERE name = 'Holum, Ann'),
      2
    UNION ALL
    -- Martin 2008
    SELECT 
      (SELECT id FROM reference_values WHERE citation_key = 'martin2008'),
      (SELECT id FROM authors WHERE name = 'Martin, Robert'),
      0;

  END IF;
END $$;
