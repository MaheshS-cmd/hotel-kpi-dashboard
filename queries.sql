
-- QUERY 1: Monthly Revenue & ADR Trend by Hotel

SELECT
    hotel,
    strftime('%Y-%m', arrival_date) AS year_month,
    SUM(net_revenue)                AS total_net_revenue,
    ROUND(AVG(adr), 2)              AS avg_adr,
    SUM(total_nights)               AS room_nights_sold,
    COUNT(*)                        AS completed_stays
FROM bookings
WHERE is_checked_out = 1
GROUP BY hotel, year_month
ORDER BY year_month, hotel;


-- QUERY 2: Channel Profitability — Gross vs Net Revenue Leakage

SELECT
    market_segment,
    COUNT(*)                                       AS bookings,
    ROUND(AVG(channel_discount) * 100, 1)          AS avg_commission_pct,
    ROUND(SUM(room_revenue), 0)                    AS gross_revenue,
    ROUND(SUM(net_revenue), 0)                     AS net_revenue,
    ROUND(SUM(room_revenue) - SUM(net_revenue), 0) AS commission_cost
FROM bookings
WHERE is_checked_out = 1
GROUP BY market_segment
ORDER BY net_revenue DESC;


-- QUERY 3: Cancellation Risk by Lead Time Bucket

SELECT
    CASE
        WHEN lead_time <= 7   THEN '0-7 days'
        WHEN lead_time <= 30  THEN '8-30 days'
        WHEN lead_time <= 90  THEN '31-90 days'
        ELSE '90+ days'
    END AS lead_time_bucket,
    COUNT(*)                                          AS total_bookings,
    SUM(is_canceled)                                  AS canceled_count,
    ROUND(100.0 * SUM(is_canceled) / COUNT(*), 1)     AS cancellation_rate_pct,
    SUM(is_no_show)                                   AS no_show_count,
    ROUND(100.0 * SUM(is_no_show) / COUNT(*), 1)      AS no_show_rate_pct
FROM bookings
GROUP BY lead_time_bucket
ORDER BY MIN(lead_time);


-- QUERY 4: Room Type Mismatch Rate by Hotel

SELECT
    hotel,
    reserved_room_type,
    COUNT(*)                                              AS total_bookings,
    SUM(room_type_mismatch)                               AS mismatched_count,
    ROUND(100.0 * SUM(room_type_mismatch) / COUNT(*), 1)  AS mismatch_rate_pct
FROM bookings
WHERE is_checked_out = 1
GROUP BY hotel, reserved_room_type
ORDER BY hotel, mismatch_rate_pct DESC;


-- QUERY 5: Repeat Guest Value vs First-Time Guest

SELECT
    CASE WHEN is_repeated_guest = 1 THEN 'Repeat Guest' ELSE 'First-Time Guest' END AS guest_type,
    COUNT(*)                        AS bookings,
    ROUND(AVG(adr), 2)              AS avg_adr,
    ROUND(AVG(total_of_special_requests), 2) AS avg_special_requests,
    ROUND(100.0 * SUM(is_canceled) / COUNT(*), 1) AS cancellation_rate_pct
FROM bookings
GROUP BY guest_type;


-- QUERY 6: Seasonality Bookings & ADR by Month (both hotels combined)

SELECT
    strftime('%m', arrival_date) AS month_num,
    strftime('%Y', arrival_date) AS year,
    COUNT(*)                      AS total_bookings,
    ROUND(AVG(adr), 2)             AS avg_adr,
    SUM(total_nights)             AS room_nights_sold
FROM bookings
WHERE is_checked_out = 1
GROUP BY year, month_num
ORDER BY year, month_num;
