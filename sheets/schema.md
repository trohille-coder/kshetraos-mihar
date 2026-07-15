# Google Sheets CRM Schema — Mihar Follow-Up Desk

## Sheet Name: `Mihar_Borrowers`

| # | Column Name | Type | Description |
|---|---|---|---|
| 1 | `borrower_id` | Text | Unique ID per borrower (e.g. MH-001) |
| 2 | `full_name` | Text | Borrower full name |
| 3 | `phone_number` | Text | WhatsApp-enabled mobile number |
| 4 | `village` | Text | Village name |
| 5 | `district` | Text | District name |
| 6 | `loan_amount` | Number | Sanctioned loan amount (INR) |
| 7 | `loan_disbursed_date` | Date | Date loan was disbursed (DD/MM/YYYY) |
| 8 | `due_date` | Date | Repayment due date (DD/MM/YYYY) |
| 9 | `amount_due` | Number | Amount pending repayment (INR) |
| 10 | `last_contact_date` | Date | Last date contact was attempted |
| 11 | `contact_status` | Dropdown | `Not Contacted` / `Reached` / `No Answer` / `Callback Requested` |
| 12 | `follow_up_count` | Number | Number of follow-up attempts made |
| 13 | `whatsapp_sent` | Boolean | TRUE/FALSE — whether WhatsApp message was sent |
| 14 | `repayment_status` | Dropdown | `Pending` / `Partial` / `Paid` / `Overdue` |
| 15 | `officer_assigned` | Text | Field officer name responsible for this borrower |
| 16 | `notes` | Text | Free-text notes from field officer |

## Workflow Trigger Logic

- Rows where `repayment_status` = `Pending` or `Overdue`
- AND `due_date` is within 3 days OR already passed
- AND `whatsapp_sent` = FALSE
→ Trigger WhatsApp message via n8n
