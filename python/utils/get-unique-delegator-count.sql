SELECT 
    pool_address, 
    delegator_address, 
    SUM(amount_added) as total_amount_added
FROM 
    delegation_pool.delegation_pool_events
WHERE 
    event_type = 'AddStakeEvent'
GROUP BY 
    pool_address, 
    delegator_address;
