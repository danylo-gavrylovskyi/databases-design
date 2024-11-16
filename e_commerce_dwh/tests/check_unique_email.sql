SELECT email
FROM {{ ref('stage_normalized_customers') }}
GROUP BY email
HAVING COUNT(*) > 1
