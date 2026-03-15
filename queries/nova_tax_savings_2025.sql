WITH property_tax_year_cte AS (
    SELECT
        p.id,
        p.state_code,
        p.state_id,
        p.county_id,
        p.client_id,
        u.email AS consultant,
        pv.interest_type AS property_type,
        COALESCE(mc.name, c.name) AS masterclientname,
        c1.name AS cdp_client,
        c.name AS legal_entity,
        c.id AS tax_year_client_id,
        cp.tax_year,
        ct.name AS county,
        pv.initial_market_value AS ProposedValue,
        pv.revised_market_value AS RevisedValue,
        pv.initial_taxable_value AS InitialTaxableValue,
        pv.revised_taxable_value AS RevisedTaxableValue
    FROM main.public.nova_property p
    LEFT JOIN main.public.nova_client_property cp ON p.id = cp.property_id
    LEFT JOIN main.public.nova_client c ON cp.client_id = c.id
    LEFT JOIN main.public.nova_client mc ON mc.id = c.master_client_id
    LEFT JOIN nova_users u ON mc.assigned_user_id = u.id
    LEFT JOIN main.public.nova_property_value pv ON p.id = pv.property_id AND cp.tax_year = pv.tax_year_short
    LEFT JOIN main.public.nova_county ct ON ct.id = p.county_id
    LEFT JOIN cdp.cdp.client_channel_associations AS cca1 ON cca1.channel_entry_id = mc.id AND cca1.channel_identifier = 'nova'
    LEFT JOIN cdp.cdp.clients AS c1 ON c1.id = cca1.client_id
    WHERE
        p.deleted_at IS NULL
        AND (cp.tax_year = 2025 OR cp.tax_year IS NULL)
        AND c.deleted_at IS NULL
        AND (mc.deleted_at IS NULL OR c.master_client_id IS NULL)
),

tax_calculation AS (
    SELECT
        p.tax_year,
        p.id AS property_id,
        p.state_code AS state,
        p.county,
        p.masterclientname,
        p.cdp_client,
        p.legal_entity,
        p.consultant,
        p.property_type,
        p.ProposedValue,
        p.RevisedValue,
        p.InitialTaxableValue,
        p.RevisedTaxableValue,
        SUM(ter.rate) AS total_rate,
        ROUND((
            COALESCE(p.RevisedTaxableValue, p.InitialTaxableValue)
            * COALESCE(pj.split_rate_override, can.split_rate) / 100
            * (ter.rate / 100)
        )::NUMERIC, 2) AS taxdue,
        ROUND((
            CASE
                WHEN p.RevisedTaxableValue IS NULL THEN 0
                ELSE (
                    p.InitialTaxableValue * (ter.rate / 100)
                    - p.RevisedTaxableValue * (ter.rate / 100)
                )
            END
        )::NUMERIC, 2) AS TaxSavings,
        ROUND(p.InitialTaxableValue * (ter.rate / 100), 2) AS initialTax,
        ROUND(p.RevisedTaxableValue * (ter.rate / 100), 2) AS revisedTax
    FROM property_tax_year_cte p
    JOIN main.public.nova_collector_account_number can ON can.property_id = p.id AND can.tax_year = p.tax_year
    JOIN main.public.nova_property_jurisdiction pj ON pj.collector_account_number_id = can.id
    JOIN main.public.nova_tax_entity_rate ter ON ter.tax_entity_id = pj.tax_entity_id
        AND ter.tax_year_short = p.tax_year
    WHERE
        can.account_number IS NOT NULL
    GROUP BY
        p.tax_year,
        p.id,
        p.state_code,
        p.county,
        p.masterclientname,
        p.cdp_client,
        p.property_type,
        p.legal_entity,
        p.consultant,
        p.ProposedValue,
        p.RevisedValue,
        p.InitialTaxableValue,
        p.RevisedTaxableValue,
        pj.split_rate_override,
        can.split_rate,
        ter.rate
)

SELECT
    property_id,
    tax_year,
    state,
    county,
    masterclientname,
    COALESCE(cdp_client, masterclientname) as cdp_client,
    consultant,
    property_type,
    ProposedValue AS init_mkt,
    COALESCE(RevisedValue, ProposedValue) AS rev_mkt,
    InitialTaxableValue AS init_tax,
    COALESCE(RevisedTaxableValue, InitialTaxableValue) AS rev_tax,
    SUM(taxdue) AS taxdue,
    SUM(TaxSavings) AS TaxSavings,
    SUM(initialTax) AS initialTax,
    SUM(revisedTax) AS revisedTax,
    'nova' as system_type
FROM tax_calculation
GROUP BY
    property_id,
    tax_year,
    state,
    county,
    masterclientname,
    cdp_client,
    consultant,
    ProposedValue,
    RevisedValue,
    property_type,
    InitialTaxableValue,
    RevisedTaxableValue,
    system_type