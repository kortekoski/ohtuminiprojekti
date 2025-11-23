INSERT INTO reference_values (citation_key, year, author, title, reftype)
SELECT * FROM (
  VALUES
    ("vihavainen2011",2011, 'Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti', 'Extreme Apprenticeship Method in Teaching Programming for Beginners.', 'book'),
    ("collins1991",1991, 'Allan Collins and John Seely Brown and Ann Holum', 'Cognitive apprenticeship: making thinking visible', 'article'),
    ("martin2008",2008, 'Martin, Robert', 'Clean Code: A Handbook of Agile Software Craftsmanship', 'inproceedings')
) AS v(citation_key, year, author, title, reftype)
WHERE NOT EXISTS (SELECT 1 FROM reference_values);