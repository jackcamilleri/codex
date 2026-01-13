# PTO & Travel Tracker Workbook

`PTO_Travel_Tracker.xlsx` contains two worksheets:

- **Inputs**: Team members log PTO or travel items with dates, times, and notes.
- **Calendar**: A month view that reads the Inputs sheet, filters rows for each date, sorts by start time, and lists events in order for each day cell.

## How to use

1. Create the workbook from the base64 file:

   ```bash
   base64 -d PTO_Travel_Tracker.xlsx.base64 > PTO_Travel_Tracker.xlsx
   ```

2. Open `PTO_Travel_Tracker.xlsx`.
3. In **Calendar!B1**, enter the first day of the month you want to view (e.g., `2024-05-01`).
4. In **Inputs**, add rows with:
   - Team Member
   - Event Type (e.g., Flight Arrival, PTO)
   - Start Date
   - Start Time
   - End Date / End Time (optional)
   - Location / Notes

The calendar cells will automatically populate with matching entries for each date and list them in time order.
