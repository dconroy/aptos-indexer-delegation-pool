SELECT 
    transaction_timestamp,    COUNT(*)
FROM 
    delegation_pool.delegation_pool_events
GROUP BY 
    transaction_timestamp
HAVING 
    COUNT(*) > 1;
