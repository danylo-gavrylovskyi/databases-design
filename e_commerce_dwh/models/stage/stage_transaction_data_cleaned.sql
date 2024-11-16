SELECT DISTINCT
    transaction_id,
    order_id,
    transaction_amount,
    transaction_date
FROM {{ ref('raw_transaction_data') }}
WHERE transaction_amount > 0
