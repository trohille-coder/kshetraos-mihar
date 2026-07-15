# KshetraOS — Mihar Follow-Up Desk

> Automated farmer loan follow-up CRM powered by n8n, Google Sheets, and WhatsApp

## What Is This?

**KshetraOS** is a rural fintech operating system built for India's agrarian economy.
**Mihar Follow-Up Desk** is its first module — an n8n automation workflow that replaces manual loan follow-up calls with intelligent, WhatsApp-first outreach.

## Problem

- Rural loan officers make 50–100 manual follow-up calls per day
- 60–70% of calls go unanswered
- No structured tracking = loans fall through the cracks
- Farmers miss repayment windows due to lack of timely reminders

## Solution

- n8n workflow auto-triggers follow-up messages based on loan due dates
- WhatsApp-first communication (farmers already use it)
- Google Sheets as CRM backend (no new software for field officers)
- Escalation logic: reminder → follow-up → officer alert

## Repository Structure

```text
kshetraos-mihar/
├── workflows/
│   └── mihar-followup-desk.json     ← n8n workflow export
├── sheets/
│   └── schema.md                    ← 16-column Google Sheets CRM schema
├── docs/
│   └── hub71-pitch.md               ← Hub71 pitch deck content
└── README.md
```

## Tech Stack

| Layer | Tool |
|---|---|
| Automation Engine | n8n (self-hosted) |
| CRM Backend | Google Sheets |
| Communication | WhatsApp (via Twilio/WATI) |
| Version Control | GitHub |
| AI Logic Layer | Perplexity AI |

## Status

🚧 Active build — Hub71 application in progress

## Builder

**R T** — KshetraOS, India
