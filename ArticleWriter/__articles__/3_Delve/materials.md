# Delve Compliance Scandal — Research Materials

Compiled: 2026-03-20

---

## 1. Timeline of Events

| Date | Event |
|---|---|
| 2023 | Delve founded by Karun Kaushik and Selin Kocalar (MIT dropouts, Forbes 30 Under 30) |
| 2024 | Delve goes through Y Combinator (W24 batch) |
| Jul 2025 | Delve raises $32M Series A led by Insight Partners at $300M valuation |
| Nov 2025 | GRC Uncensored podcast flags Delve's practices alongside CompAI concerns |
| Dec 2025 (late) | Anonymous email sent to hundreds of Delve clients revealing a publicly accessible Google Spreadsheet linking to ~575 confidential audit reports |
| Dec 2025 (days later) | CEO Karun Kaushik sends email to clients calling allegations "falsified claims" from an "AI-generated email" |
| Jan 9, 2026 | Delve publishes blog post "Inside Delve's Trusted Compliance Process" claiming reports are "triple verified" and "no two audit reports are the same" |
| Jan 16, 2026 | Daily Compliance newsletter reports on compliance platforms selling pre-filled audit reports (name withheld pending investigation) |
| Mar 13, 2026 | ComplyJet publishes "Delve SOC 2 Customer Experience in 2026: Good, Bad, & Reality Check" |
| Mar 19, 2026 | DeepDelver publishes full investigation "Delve – Fake Compliance as a Service – Part I" on Substack |
| Mar 20, 2026 | Tweet by @ohryansbelt summarizing the investigation goes viral |

---

## 2. Core Allegations (from DeepDelver investigation)

### 2.1 Audit Integrity & Independence Violations

- Delve allegedly generates auditor conclusions, test procedures, and final reports before any auditor reviews evidence
- 493 out of 494 leaked SOC 2 reports contain identical boilerplate text (99.8%), including same grammatical errors and nonsensical sentences — only company name, logo, org chart, and signature differ
- Draft reports already contain pre-written auditor verdicts before customers provide their company description, which would violate AICPA independence rules (AT-C Section 205, AT-C Section 315)
- All 259 Type II reports claim zero security incidents, zero personnel changes, zero customer terminations, and zero cyber incidents, with identical "unable to test" conclusions across every client

### 2.2 Auditor Concerns

- Delve markets "US-based CPA firms" but the investigation claims 99%+ of clients in the preceding 6 months went through either Accorp or Gradient Certification
- These firms are described as Indian certification mills operating through US shell entities and mailbox agents
- High-profile clients are reportedly paired with legitimate US-based firms (Prescient, Aprio) but do compliance mostly off-platform with a vCISO
- Post-leak, Delve reportedly switched to Glocert as primary ISO 27001 auditing firm

### 2.3 Product & Process Claims

- Trust pages are fully populated with security claims (vulnerability scanning, pentesting, data recovery simulations) before any compliance work is performed
- Platform pre-fabricates board meeting minutes, risk assessments, security incident simulations, and employee evidence
- Most "integrations" are containers for manual screenshots with no actual API connections
- When clients threaten to leave, Delve reportedly pairs them with an external vCISO for manual off-platform work

### 2.4 Regulatory Risk for Affected Companies

- Companies relying on these reports could face criminal liability under HIPAA (willful neglect)
- GDPR fines up to 4% of global annual revenue or €20M
- SOC 2 reports used as proof of compliance in enterprise sales may be invalid

### 2.5 Named Affected Companies

Lovable, Bland, Cluely, BrowserUse, Greptile, Knowtex, HockeyStack, Slash, Sully, Incorta, WisprFlow, Duos Edge AI (NASDAQ-traded)

---

## 3. Delve's Official Response

### 3.1 CEO Email to Clients (Dec 2025)

Key claims from Karun Kaushik's email:

> "Yesterday, an AI-generated email was sent to Delve customers with falsified claims and an alert about a publicly accessible internal audit automation document. While this email is not from a credible source, in the spirit of transparency, we want to proactively address this situation."

> "First and foremost, I personally assure you that you are in compliance and there is no impact to the validity of your audit report."

> "We determined that human error resulted in a document being made publicly available. [...] No external party gained access to the Delve platform, integrations, or any databases where sensitive data resides. The scope of this situation is limited to the aforementioned document."

### 3.2 Blog Post: "Inside Delve's Trusted Compliance Process" (Jan 9, 2026)

Published by Charles Nwatu (Head of Security and Compliance) and Karun Kaushik. Claims:
- AI evidence validation combined with dedicated human review
- Vetted audit firms deliver reports
- "No two audit reports are the same"
- Reports are "triple verified"

URL: https://delve.co/blog/inside-delve-trusted-audit-process

### 3.3 Series A Announcement (Jul 2025)

- $32M Series A at $300M valuation
- Led by Insight Partners
- Prior: $3.3M seed round
- Claims "AI agents for compliance"

URL: https://www.prnewswire.com/news-releases/delve-raises-32m-series-a-to-build-ai-agents-for-compliance-302510121.html
Blog: https://delve.co/blog/series-a

---

## 4. Independent Corroboration & Industry Context

### 4.1 GRC Uncensored Podcast (Nov 2025)

Episode "Do Ethical GRC auditors really exist?" explicitly flagged Delve:
- Hosts (Troy Fine — active auditor, Kendra Cooley, Elliot Volkman) discussed Delve alongside CompAI for problematic positioning
- Troy Fine had been posting about Delve's rubber-stamp practices on LinkedIn
- Key findings: "Automation platforms are accelerating GRC's decline: Surface-level checks produce green checkmarks that don't reflect real controls, and some auditors sign off without verification"
- "The market rewards speed, not rigor"

URL: https://grcpod.substack.com/p/do-ethical-grc-auditors-really-exist

### 4.2 Daily Compliance Newsletter (Jan 16, 2026)

Reported (without naming Delve directly):
- "At least one major compliance management platform has been selling pre-filled, 'AI-generated' audit reports without conducting actual assessments"
- "Customers paid $15K-$30K for SOC 2 and ISO 27001 reports that were essentially templates with their company name inserted"
- "The platform marketed itself as '10x faster than traditional audits' and had raised $50M in VC funding"

URL: https://dailycompliance.substack.com/p/compliance-platform-scandal-tiktok

### 4.3 Gartner Research (cited in Daily Compliance, Jan 2026)

- 80% of AI audits are "fundamentally flawed"
- Auditors lack technical expertise, use inadequate methodologies, or rely on vendor self-attestation without verification

### 4.4 ComplyJet Customer Experience Review (Mar 13, 2026)

Independent review documenting:
- Limited integration library forcing manual evidence collection
- Customer experience concerns

URL: https://www.complyjet.com/blog/delve-soc-2-customer-experience

---

## 5. Source Links

### Primary Sources

| Source | URL |
|---|---|
| DeepDelver investigation (Mar 19, 2026) | https://deepdelver.substack.com/p/delve-fake-compliance-as-a-service |
| Archive backup 1 | https://archive.is/HokPb |
| Archive backup 2 | https://archive.ph/YTsgc |
| Web Archive backup | https://web.archive.org/web/20260319020740/https://deepdelver.substack.com/p/delve-fake-compliance-as-a-service |
| Archived leaked spreadsheet | https://archive.ph/6ZSzX |
| Leaked reports backup | https://mega.nz/folder/3ZNi3DqZ#ZH-M2Au1zErISCPD5Hgegg |
| Tweet by @ohryansbelt | https://x.com/ohryansbelt/status/2034752685631574022 |

### Delve Official Sources

| Source | URL |
|---|---|
| Delve blog — Trusted Compliance Process | https://delve.co/blog/inside-delve-trusted-audit-process |
| Delve blog — Series A announcement | https://delve.co/blog/series-a |
| Series A press release (PRNewswire) | https://www.prnewswire.com/news-releases/delve-raises-32m-series-a-to-build-ai-agents-for-compliance-302510121.html |

### Independent Coverage

| Source | URL |
|---|---|
| GRC Uncensored podcast (Nov 2025) | https://grcpod.substack.com/p/do-ethical-grc-auditors-really-exist |
| Daily Compliance newsletter (Jan 2026) | https://dailycompliance.substack.com/p/compliance-platform-scandal-tiktok |
| ComplyJet review (Mar 2026) | https://www.complyjet.com/blog/delve-soc-2-customer-experience |

### Regulatory References (cited in investigation)

| Reference | URL |
|---|---|
| AICPA Code of Professional Conduct | https://pub.aicpa.org/codeofconduct/ethicsresources/et-cod.pdf |
| AT-C Section 205 & 315 | https://assets.ctfassets.net/rb9cdnjh59cm/49M1391nsNvsSx6gou3EKW/d0e0475caf4596239d342b35acfabe4d/at-c-sections-100-300.pdf |
| AICPA SOC 2 Reporting Guide | https://assets.ctfassets.net/rb9cdnjh59cm/2paxzm46AxmwDDSZGkdtFS/c01813c67d26de154898653c121a92ea/AAGSOP22E.pdf |

---

## 6. Key Numerical Claims from the Investigation

- **575** total files in the leak (494 SOC 2 + 81 ISO 27001)
- **494** SOC 2 reports in the leaked spreadsheet
- **493/494** (99.8%) contain identical boilerplate text
- **259** SOC 2 Type II reports — all claim zero incidents across all categories
- **99%+** of clients reportedly went through Accorp or Gradient in the preceding 6 months
- **$32M** Series A raised (Jul 2025)
- **$300M** valuation at Series A
- **$15,000** → **$6,000** price drop when client mentioned a competitor (per investigation)

---

## 7. Contact for Original Investigator

DeepDelver reporter contact: aicpnay@proton.me
Hashtag for contact: #AICPNAY
