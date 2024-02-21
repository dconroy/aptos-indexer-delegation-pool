SELECT COUNT(*)
FROM (
    SELECT 
        pool_address, 
        delegator_address
    FROM 
        delegation_pool.delegation_pool_events
    WHERE 
        event_type = 'AddStakeEvent'
    GROUP BY 
        pool_address, 
        delegator_address
) AS unique_combinations;
