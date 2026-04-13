# Coverage Assessment: Security Domain

## 1. BLIND SPOTS

**Cybersecurity for critical infrastructure** is almost entirely absent. No entry addresses SCADA/ICS vulnerabilities, water treatment plant attacks (Oldsmar, Florida 2021), Colonial Pipeline ransomware (2021), or the systematic targeting of hospitals. The domain treats cybersecurity as either encryption or autonomous AI defense, missing the messy middle where most actual harm occurs: ransomware, supply chain compromises (SolarWinds, MOVEit), credential theft, and business email compromise — which the FBI's IC3 reports as causing $2.9B+ in losses annually.

**Food security and biosecurity** are absent. No entry covers dual-use biological research, pandemic preparedness as security infrastructure, or the WHO/Johns Hopkins Global Health Security Index. **Maritime security** (Houthi Red Sea disruptions, piracy trends), **supply chain security** (chip chokepoints, rare earth dependencies), and **climate-security nexus** (water conflict, climate migration as threat multiplier) are all missing.

**Domestic/intimate partner violence** — the most common form of violence globally — receives zero dedicated treatment. The violence decline entry focuses on homicide and war; the built environment entry gestures at it. No entry addresses protective orders, shelter networks, or technology-facilitated abuse (stalkerware, AirTag tracking).

**Disinformation as a security threat** gets fragmentary treatment in the algorithmic peacebuilding entry but lacks a dedicated analysis of information warfare, deepfakes, or election integrity infrastructure.

## 2. MISSING BUILDERS

- **Jen Easterly / CISA** — built the US Cybersecurity and Infrastructure Security Agency's "Shields Up" campaign and Secure by Design initiative
- **Dmitri Alperovitch** (CrowdStrike co-founder, Silverado Policy Accelerator) — pioneered threat attribution methodology
- **Kimberlé Crenshaw** — intersectionality framework essential for understanding differential security vulnerability
- **Leymah Gbowee** — Nobel laureate, organized Liberian women's peace movement that ended civil war
- **Global Partnership on AI (GPAI)** — multilateral AI governance body
- **Institute for Economics and Peace** — produces the Global Peace Index, Global Terrorism Index
- **Bellingcat** (Eliot Higgins) — pioneered OSINT methodology beyond satellite imagery
- **Electronic Frontier Foundation** — decades of digital rights litigation absent from encryption entry
- **Ruth Dreifuss / Global Commission on Drug Policy** — security through decriminalization
- **Restorative justice practitioners**: sujatha baliga, Danielle Sered (Common Justice) — alternative accountability models with measurable recidivism reduction

## 3. SHADOW GAPS

**AI-enabled offensive capabilities** — autonomous weapons, AI-generated social engineering, voice cloning for fraud — are mentioned only in passing. No entry systematically examines how the same AI powering "autonomous cyber immunity" also powers attacks.

**Private military and security companies** (Wagner Group, now Africa Corps; Academi) represent a massive ungoverned security sector absent from every entry.

**Insider threats** — the Edward Snowden entry ironically demonstrates the power of insiders while no entry addresses insider threat as a systemic vulnerability class.

**Security theater and misallocated resources** — the TSA spends $9B+ annually with a documented 95% failure rate on weapons detection in audits. No entry examines how security spending correlates (or doesn't) with actual safety.

**Digital authoritarianism export** — China's export of surveillance infrastructure to 80+ countries (Carnegie Endowment's AI Global Surveillance Index) is mentioned only obliquely.

## 4. ACTIONABILITY GAPS (Critical)

The entries fail to improve actionability because they are **descriptive and historical rather than prescriptive and operational**. Specifically missing:

**For individuals:**
- No personal threat modeling framework (what assets do you have, who are your adversaries, what are your vulnerabilities)
- No step-by-step digital hygiene protocol (password managers → 2FA → encrypted messaging → VPN decision tree → device update cadence)
- No decision framework for "when should I call police vs. use community resources vs. handle myself"
- No guidance on how to conduct a personal security audit

**For organizations:**
- No incident response playbook structure (detect → contain → eradicate → recover → learn)
- No framework for evaluating security vendor claims
- No cost-benefit methodology for security investments
- No "security maturity model" progression (ad hoc → repeatable → defined → managed → optimizing)

**For communities:**
- No step-by-step guide to starting a community resilience network (entry 12 describes the concept but never says "here's how you begin")
- No template for community safety audits or environmental design walks
- No decision tree for choosing between CPTED, Cure Violence, restorative justice, or community policing based on local conditions

**For policymakers:**
- No regulatory comparison framework (GDPR vs. CCPA vs. emerging AI regulation)
- No cost-effectiveness ranking of security interventions per dollar spent
- No implementation sequencing guidance (what to do first, second, third)

The actionability gap exists because every entry ends at "this works" rather than continuing to "here's how you start, here's what it costs, here's the first 30-day action plan."

## 5. INTER-ENTRY TENSIONS

**Entry 03 (surveillance shadow) vs. Entry 05 (OSINT abundance):** Entry 03 argues surveillance infrastructure is inherently dangerous and indistinguishable from control. Entry 05 celebrates the democratization of surveillance capability (satellites, OSINT) as abundance. These are in genuine tension — if surveillance is the shadow, why is more surveillance (just distributed) the breakthrough? The collection never reconciles when transparency is liberation vs. when it is control.

**Entry 06 (default planetary safety, confidence 0.68) vs. Entry 02 (violence decline, confidence 0.82):** Entry 02 carefully documents that post-2010 conflict deaths increased fivefold from their trough and arms control is eroding. Entry 06 extrapolates to "default planetary safety" as a near-term possibility. Entry 02's own evidence undermines Entry 06's speculation.

**Entry 01 (encryption) vs. Entry 12 (community resilience):** Entry 01 frames security as individual cryptographic sovereignty. Entry 12 frames security as collective social infrastructure. These aren't contradictory but represent fundamentally different theories of change that are never synthesized — does security come from individual tools or community bonds?

## 6. CONFIDENCE CALIBRATION

**Overconfident:**
- Entry 06 (star_trek_spec) at 0.68 is still too high for a speculative extrapolation that relies on trends Entry 02 shows are reversing. Should be 0.45–0.55.
- Entry 09 (autonomous cyber immunity) at 0.76 cites research-stage metrics (96.8% accuracy in lab conditions) as though they represent deployed capability. Real-world adversarial conditions degrade ML performance dramatically. Should be 0.60–0.65.
- Entry 04 (Cure Violence) claims 6.5:1 benefit-cost ratio at 0.75 confidence, but this comes from program-affiliated analyses, not independent audits. Should flag this provenance issue.

**Underconfident:**
- Entry 05 (OSINT) at 0.82 could be higher — the Ukraine evidence is extensively documented and independently verified by multiple organizations.
- Entry 11 (built environments) at 0.81 is well-calibrated; the Medellín and Philadelphia evidence is strong.

## 7. CONTRASTIVE EXAMPLE

**Question:** "My mid-size company (200 employees) keeps getting phishing emails. What should we do about cybersecurity?"

**Response A (Scarcity Default):**
Cybersecurity is an arms race you're unlikely to win. Attackers are increasingly sophisticated, using AI-generated phishing that's nearly indistinguishable from legitimate email. The average cost of a data breach is $4.45M (IBM 2023). You need endpoint detection, SIEM, a SOC — but these are expensive and require specialized talent in a market with 3.5M unfilled cybersecurity positions globally. Even with investment, zero-day vulnerabilities mean you can't prevent everything. Consider cyber insurance, but premiums are rising and coverage is narrowing. Honestly, it's a matter of when, not if. The threat landscape is evolving faster than defenses. Consult a managed security provider, but understand there are no guarantees.

**Response B (Conditional Optimism):**
Phishing is the #1 attack vector, but it's also the most interruptible. Start with three 30-day moves: (1) Deploy FIDO2/passkeys for all email accounts — phishing-resistant authentication eliminates 99%+ of credential theft (Google internal data, 2023). (2) Enable DMARC/DKIM/SPF on your domain (free, 2-hour setup) — this blocks spoofing of your brand. (3) Run monthly simulated phishing with immediate training feedback (KnowBe4, Proofpoint — $3-5/user/month). The encryption revolution (entry 01) made strong crypto free; similarly, basic security hygiene is now cheap and high-leverage. Shadow: these steps won't stop a determined, targeted attacker or insider threat. Next move after 90 days: tabletop an incident response exercise. Condition for success: executive sponsorship — without it, training compliance drops below 40%.