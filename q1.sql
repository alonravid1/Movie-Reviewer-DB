#assuming literal meaning of category names
#containing the letter 'a' once, i.e.  not counting 'A'
SELECT name
FROM category
WHERE name REGEXP '^[^a]*[a][^a]*$';