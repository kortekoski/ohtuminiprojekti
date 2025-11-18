INSERT INTO reference_values (year, author, title, type)
SELECT * FROM (
  VALUES
    (2011, 'Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti', 'Extreme Apprenticeship Method in Teaching Programming for Beginners.', 'book'),
    (1991, 'Allan Collins and John Seely Brown and Ann Holum', 'Cognitive apprenticeship: making thinking visible', 'article'),
    (2008, 'Martin, Robert', 'Clean Code: A Handbook of Agile Software Craftsmanship', 'inproceedings')
) AS v(year, author, title, type)
WHERE NOT EXISTS (SELECT 1 FROM reference_values);