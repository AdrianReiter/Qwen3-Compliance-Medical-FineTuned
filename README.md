# Compliance Agent

## Overview
The **Compliance Agent** is a specialized AI tool designed to assist medical device software engineers and quality assurance professionals in navigating complex regulatory frameworks. Built upon a fine-tuned Qwen architecture, this agent provides instant, context-aware guidance on standards such as **ISO 13485**, **IEC 62304**, **ISO 14971**, and **FDA 21 CFR**.

By leveraging domain-specific training data, the Compliance Agent helps bridge the gap between technical engineering tasks and regulatory requirements, ensuring that compliance is integrated into the development lifecycle rather than treated as an afterthought.

## Use Cases

### 1. Regulatory Interpretation & Guidance
**Scenario:** A developer is unsure how a specific software change affects the device's safety classification.
**Benefit:** The agent interprets clauses from IEC 62304 or ISO 14971, explaining the regulatory impact of technical decisions in plain English.

### 2. Risk Management Support
**Scenario:** A team is brainstorming hazards for a new feature but struggles to formalize them.
**Benefit:** The agent assists in identifying potential hazards, suggesting mitigation strategies (Design vs. Labeling), and structuring the audit trail for the Risk Management File.

### 3. Audit Preparation & Gap Analysis
**Scenario:** A startup is preparing for their first ISO 13485 audit and wants to verify their "SOUP" (Software of Unknown Provenance) documentation strategy.
**Benefit:** The agent simulates auditor inquiries, pointing out gaps in documentation logic (e.g., missing risk assessments for 3rd party libraries) and recommending corrective actions.

### 4. Quality System Training
**Scenario:** Onboarding new engineers who are unfamiliar with medical device regulations.
**Benefit:** Serves as an interactive knowledge base, allowing new hires to ask specific "what if" questions and receive grounded, citation-backed answers.

## Training & Usage

To get started with the Compliance Agent, you can use the provided automation script. This script handles the entire lifecycle from model acquisition to interactive testing.

### Automated Setup
Run the following command in your terminal:

```bash
./train_and_fuse.sh
```

**Alternative Installation:**
If you prefer not to use `uv`, you can install the dependencies manually using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

**What this script does:**
1.  **Model Download:** Automatically checks for the base model `Qwen/Qwen3-0.6B`. If not found locally, it downloads it using the Hugging Face CLI.
2.  **Fine-Tuning:** Trains the model using LoRA (Low-Rank Adaptation) on the dataset located in `./data`.
3.  **Model Fusing:** Merges the trained adapters with the base model to create a standalone `Qwen3-compliance_agent_medical-v1` model.
4.  **Interactive CLI:** Automatically launches `compliance_cli.py` upon completion, allowing you to interact with your newly trained regulatory assistant immediately.

---

## Model Test Log
**Model:** Qwen 0.6B (Fine-Tuned)
**Date:** 2025-01-03
**Status:** Prototype v1

---

### 1. Open Source Library (SOUP)
**User:** "We want to use an open-source Python library for data visualization in our diagnostic app. We didn't write the code ourselves. What are the requirements for using this?"

**⚙️ Audit Trail:**
1. **Identify Item:** Open-source Python library for visualization.
2. **Clause Analysis:** Analyze requirements for SOUP (Software of Unknown Provenance).
3. **Risk Analysis:** Can open-source visualization cause a hazardous situation (e.g., misinterpretation of data)?
4. **Conclusion:** Document findings in Risk Management File.

**📋 Regulatory Guidance:**
You must have a documented risk-based approach. **ISO 13485 Clause 7.3.9** requires that software systems be designed and developed using principles that control **Software of Unknown Provenance (SOUP)**. You cannot simply copy and paste a library without assessment. You must develop a plan to assess the impact of the software's use on safety and existing functionality. Document how the plan is executed and what risks are associated with its use. If the library contains unknown risks (e.g., poor documentation or lack of verification), the risk may be unacceptable.

---

### 2. Software Safety Classification
**User:** "Our software monitors patient temperature. If the software crashes, the nurse will simply notice the blank screen and check the patient manually with a thermometer. No injury can result. What software safety class is this?"

**⚙️ Audit Trail:**
1. **Event:** Potential software failure.
2. **Clause Analysis:** IEC 62304 Clause 4.3 (Software Safety Classification).
3. **Risk Analysis:** Does the failure result in injury? (No, widely accepted manual fallback exists).
4. **Conclusion:** Class A (No injury or damage to health).

**📋 Regulatory Guidance:**
This appears to be **Class A**. According to **IEC 62304 Clause 4.3**, software is classified as Class A if no hazardous situation or injury can occur from its failure. Since a "blank screen" is easily detectable and a standard of care (manual thermometer) exists to mitigate the harm entirely, the risk of injury is negligible. However, you must document this justification in your Risk Management File to prove that the hazard is effectively controlled by the user's awareness.

---

### 3. Labeling vs. Design Control
**User:** "To prevent a pinch-point hazard where a user could lose a finger, we added a bright red 'WARNING: PINCH POINT' label next to the moving part. Is this sufficient risk control?"

**⚙️ Audit Trail:**
1. **Hazard:** Pinch point (High Severity: Loss of finger).
2. **Current Control:** Labeling (Information for Safety).
3. **Priority Check:** Design > Protection > Information.

**📋 Regulatory Guidance:**
Likely not. Under **ISO 14971 Clause 7.1**, risk control options are prioritized: (1) Inherent safety by design, (2) Protective measures, (3) Information for safety. Labeling is the lowest tier of control. For a high-severity injury like losing a finger, relying solely on a warning label is generally considered insufficient if a physical guard or sensor (Protective Measure) is feasible. You must demonstrate why a design solution was not reasonably practicable.

---

### 4. Benefit-Risk Analysis
**User:** "Our new laser device causes minor skin redness in 10% of patients, which is considered a 'harm'. However, it is the only device that cures a specific life-threatening condition. Can we accept this risk?"

**⚙️ Audit Trail:**
1. **Event:** Minor harm (skin redness) vs. Major Benefit (cure life-threatening condition).
2. **Requirement:** ISO 14971 Clause 7.4 (Benefit-Risk Analysis).
3. **Conclusion:** Benefits likely outweigh risks.

**📋 Regulatory Guidance:**
Yes, this risk is likely acceptable, but it requires documentation. According to **ISO 14971 Clause 7.4**, if a residual risk is not judged acceptable by standard criteria, you may accept it if the **medical benefits** of the intended use outweigh the residual risk. In this case, curing a life-threatening condition outweighs the minor harm of skin redness. You must document this Benefit-Risk Analysis, citing clinical data or literature to support the claim.

---

### 5. CAPA vs. Correction
**User:** "We found that 5% of our devices failed final testing last month due to a loose screw. We tightened the screws and shipped them. Do we need to open a CAPA?"

**⚙️ Audit Trail:**
1. **Issue:** Trend of failures (5% is significant).
2. **Action Taken:** Correction (tightening).
3. **Clause Analysis:** ISO 13485 Clause 8.5.2 (Corrective Action).
4. **Decision:** Need to investigate the process, not just fix units.

**📋 Regulatory Guidance:**
Yes. **ISO 13485 Clause 8.5.2** requires **Corrective Action** to eliminate the cause of non-conformities in order to prevent recurrence. Simply tightening the screws is a "Correction" (fixing the specific unit). You must open a CAPA to investigate **why** the screws were loose (e.g., torque tool calibration, operator training, or vibration in assembly) and implement a systemic fix to prevent the 5% failure rate from continuing.

---

### 6. Supplier Change
**User:** "We are changing our PCB manufacturer to a new vendor in Vietnam who is cheaper. They sent us a sample that looks good. Can we start ordering immediately?"

**⚙️ Audit Trail:**
1. **Change Type:** Supplier change (Purchasing).
2. **Clause Analysis:** ISO 13485 Clause 7.4 (Purchasing).
3. **Risk:** Quality variance, material changes.
4. **Decision:** Must qualify supplier first.

**📋 Regulatory Guidance:**
No. According to **ISO 13485 Clause 7.4.1**, you must establish criteria for the evaluation and selection of suppliers. A "good sample" is not enough. You must perform **Supplier Qualification**, which may include auditing the vendor, verifying their Quality System, and validating the component's performance in your device (First Article Inspection). You must also establish a Quality Agreement before volume purchasing.

---

### 7. MDR Reporting (Post-Market)
**User:** "A doctor reported that our surgical drill overheated and caused a delay in surgery, but the patient was not injured. This has happened twice now. Do we need to report this to the FDA?"

**⚙️ Audit Trail:**
1. **Event:** Malfunction (Overheating) + Surgery Delay.
2. **Regulation:** 21 CFR 803 (MDR).
3. **Key Question:** Would recurrence likely cause serious injury?

**📋 Regulatory Guidance:**
Potentially yes. Under **21 CFR 803.50**, you must submit a Medical Device Report (MDR) if a device malfunction would be likely to cause or contribute to a **serious injury** if it were to recur. A delay in surgery caused by equipment failure can be considered a serious injury if it complicates the procedure or compromises the patient. Since this has happened twice (a trend), you must evaluate it for reportability within **30 days**.

---

### 8. Software Change Control (Hotfix)
**User:** "A developer found a typo in a user message on the Class B device screen. He wants to fix it and recompile the build immediately for release tomorrow. Is this allowed?"

**⚙️ Audit Trail:**
1. **Event:** Uncontrolled code change.
2. **Clause Analysis:** IEC 62304 Clause 8 (Configuration Management).
3. **Risk:** Lack of verification, version control issues.

**📋 Regulatory Guidance:**
No. **IEC 62304 Clause 8** requires that all changes to configuration items (code) be identified, controlled, and documented. Even for a typo, you must raise a Change Request, perform a simplified impact analysis (to ensure the recompile didn't break anything else), and verify the fix. "Hot-fixing" directly to release without these steps is a non-conformity.

---

### 9. Startup "Spirit of the Standard"
**User:** "We are a small startup and ISO 13485 seems too expensive. Can we just follow the 'spirit' of the standard without all the documentation?"

**⚙️ Audit Trail:**
1. **Identify Item:** Compliance strategy.
2. **Regulation:** ISO 13485 / FDA 21 CFR 820.
3. **Reality:** Documentation *is* the proof of compliance.

**📋 Regulatory Guidance:**
No. In the medical device industry, "if it isn't documented, it didn't happen." **ISO 13485 Clause 4.1** and **21 CFR 820** explicitly require a **documented** Quality Management System. You cannot prove you followed the "spirit" of safety testing or risk management without the records to back it up. Auditors and regulators assess the physical evidence (documents and records), not the intent.

---

### 10. Tool Validation
**User:** "We made a small update to our automated testing tool. It's just an internal tool, so we don't need to re-validate it, right?"

**⚙️ Audit Trail:**
1. **Change:** Update to QMS software (Test Tool).
2. **Clause:** ISO 13485 Clause 4.1.6 / IEC 62304.
3. **Risk:** Invalid test results leading to release of bad product.

**📋 Regulatory Guidance:**
Verification is mandatory. **ISO 13485 Clause 4.1.6** requires that software used in the Quality Management System (including automated test tools) be validated prior to use. If you update the tool, you must re-validate it to ensure the update didn't break its ability to detect bugs. If your test tool is broken, your "passed" tests are meaningless.