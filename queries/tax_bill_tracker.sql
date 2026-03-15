WITH all_combinations_nova AS (
    SELECT
        COALESCE(cdpmc.name, mc.name, c.name, '') AS client,
        COALESCE(cdpcl.name, c.name) AS legal_entity,
        COALESCE(cdpcol.name, col.contact) AS collector,
        p.state_code
    FROM
        main.public.nova_collector_account_number can
    LEFT JOIN main.public.nova_collector col ON col.id = can.collector_id
    LEFT JOIN main.public.nova_property p ON can.property_id = p.id
    LEFT JOIN main.public.nova_client_property cp ON p.id = cp.property_id AND cp.tax_year = 2025
    LEFT JOIN main.public.nova_client c ON cp.client_id = c.id
    LEFT JOIN main.public.nova_client mc ON mc.id = c.master_client_id
    LEFT JOIN cdp.cdp.client_channel_associations cdpch1 ON cdpch1.channel_entry_id = c.id and cdpch1.channel_identifier = 'nova'
    LEFT JOIN cdp.cdp.client_channel_associations cdpch2 ON cdpch2.channel_entry_id = mc.id and cdpch2.channel_identifier = 'nova'
    LEFT JOIN cdp.cdp.clients cdpcl ON cdpcl.id = cdpch1.client_id and cdpcl.parent_id is not null
    LEFT JOIN cdp.cdp.clients cdpmc ON cdpmc.id = cdpch2.client_id
    LEFT JOIN cdp.cdp.collector_channel_associations colch ON col.id = colch.chanel_entry_id and colch.channel_identifier = 'nova'
    LEFT JOIN cdp.cdp.collectors cdpcol on colch.collector_id = cdpcol.id
    WHERE p.deleted_at IS NULL
    AND can.tax_year = 2025
    GROUP BY
        mc.name,
        c.name,
        cdpcl.name,
        cdpmc.name,
        COALESCE(cdpcol.name, col.contact),
        p.state_code
),
current_data_nova AS (
    SELECT
        COALESCE(cdpmc.name, mc.name, c.name, '') AS client,
        COALESCE(cdpcl.name, c.name) AS legal_entity,
        COALESCE(cdpcol.name, col.contact) AS collector,
        p.state_code,
        COUNT(can.id) AS current_open_bills
    FROM
        main.public.nova_collector_account_number can
    LEFT JOIN main.public.nova_collector col ON col.id = can.collector_id
    LEFT JOIN main.public.nova_property p ON can.property_id = p.id
    LEFT JOIN main.public.nova_client_property cp ON p.id = cp.property_id AND cp.tax_year = 2025
    LEFT JOIN main.public.nova_client c ON cp.client_id = c.id
    LEFT JOIN main.public.nova_client mc ON mc.id = c.master_client_id
    LEFT JOIN cdp.cdp.client_channel_associations cdpch1 ON cdpch1.channel_entry_id = c.id and cdpch1.channel_identifier = 'nova'
    LEFT JOIN cdp.cdp.client_channel_associations cdpch2 ON cdpch2.channel_entry_id = mc.id and cdpch2.channel_identifier = 'nova'
    LEFT JOIN cdp.cdp.clients cdpcl ON cdpcl.id = cdpch1.client_id and cdpcl.parent_id is not null
    LEFT JOIN cdp.cdp.clients cdpmc ON cdpmc.id = cdpch2.client_id
    LEFT JOIN cdp.cdp.collector_channel_associations colch ON col.id = colch.chanel_entry_id and colch.channel_identifier = 'nova'
    LEFT JOIN cdp.cdp.collectors cdpcol on colch.collector_id = cdpcol.id
    WHERE p.deleted_at IS NULL
      AND can.received_at IS NULL
      AND can.processed_at IS NULL
      AND c.name IS NOT NULL
      AND can.tax_year = 2025
    GROUP BY
        mc.name,
        c.name,
        cdpcl.name,
        cdpmc.name,
        COALESCE(cdpcol.name, col.contact),
        p.state_code
)
SELECT
    COALESCE(a.client, '') || '-' || COALESCE(a.legal_entity, '') || '-' || COALESCE(a.state_code, '') || '-' || COALESCE(a.collector, '') || '-Nova-Minerals' AS account,
    a.client,
    a.legal_entity,
    a.collector,
    a.state_code,
    COALESCE(current_data_nova.current_open_bills, 0) AS current_open_bills,
    'nova' AS system_type,
    'Minerals' AS account_type
FROM
    all_combinations_nova AS a
LEFT JOIN current_data_nova
ON a.client = current_data_nova.client
   AND a.legal_entity = current_data_nova.legal_entity
   AND a.collector = current_data_nova.collector
   AND a.state_code = current_data_nova.state_code;