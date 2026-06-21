# hotel-kpi-dashboard
Power BI dashboard analyzing 99K+ hotel bookings; channel profitability, cancellation risk, and guest reliability, built on a Python → SQL → Power BI pipeline.

Data source
Hotel Booking Demand dataset
— booking-level records from a City Hotel and a Resort Hotel, originally published by
Antonio, Almeida and Nunes (2019). Raw source file not committed here (18MB); 
see link to download - https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand

The summary below highlights the core findings at a glance. The full operational report including detailed analysis, supporting statistics, and complete recommendations is available in operational_summary.docx. The underlying SQL queries are in queries.sql, and the Python cleaning script is in clean_data.py.

Key Business Questions:
Which booking channels generate the highest net revenue?
How much revenue is lost to OTA commissions?
What factors drive cancellation behavior?
How do repeat guests differ from first-time guests?
Is current pricing aligned with seasonal demand?
Are room type mismatches operational issues or revenue-management decisions?

Key Findings
1. OTA Dependence Creates Revenue Leakage
2. Online Travel Agencies generated the highest booking volume.
3. OTA bookings showed significantly higher cancellation rates than Direct bookings.
4. Estimated commission expense exceeded $6.7M.
-Potential Opportunity:
-- Redirecting 10% of OTA volume to Direct channels could significantly reduce commission costs while improving booking reliability.
   
5. Cancellation Risk Increases With Lead Time
6. Cancellation rates increased from 8.5% (0-7 days) to 36.7% (90+ days).
7. Long-lead refundable bookings represent the highest revenue risk.
- Recommendation:
-- Restrict refundable inventory during high-demand periods.

8. Repeat Guests Are More Reliable
9. Repeat guests showed less than half the cancellation rate of first-time guests.
10. Despite lower ADR, repeat guests generated more predictable revenue.
- Recommendation:
-- Increase loyalty and direct-booking initiatives.

11. Pricing Appears Reactive
12. ADR peaks followed demand peaks rather than anticipating them.
- Recommendation:
-- Introduce forward-looking revenue management pricing strategies.
