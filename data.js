window.cockpitData = {
  project: {
    title: "Regulated AI & Data Governance Cockpit",
    subtitle: "A static interactive case study showing how a regulated organization could structure data-driven AI adoption, governance, workflow analytics, and human-reviewed decision support before production rollout.",
    disclaimer: `This is an independent portfolio case study using simulated commercial data and public-company assumptions.
It is not connected to a real CRM, does not process confidential data, and is not intended as a legal compliance tool.`,
    positioning: `I designed the business logic, scoring framework, workflow structure, governance assumptions, and reviewer-facing documentation behind this cockpit.
AI-assisted development was used to accelerate coding and iteration, while the data logic, product structure, adoption framing, and use case design were defined independently.`,
    oneLineSummary: "An interactive case study showing how a regulated organization could structure GenAI adoption, data governance, workflow analytics, and human-reviewed decision support before production rollout.",
    headerSubtitle: "Data Analytics · AI Governance · Workflow Automation · Product Thinking",
    profileLabel: "Applied AI, Data Governance & Innovation Case Study",
    heroReviewLine: "Designed to be reviewed from four angles: Data / Analytics / Risk, Digital AI Governance, Workflow Operations, and AI Product Thinking.",
    demoCta: "Open Decision Demo",
    cockpitCta: "Review Data Workflow Layer",
    adoptionCta: "Review Adoption/Governance Layer",
    productCta: "Review Product Layer",
    caseStudyCta: "Read Case Study Brief",
    scoringDisclaimer: `Scores and account examples are illustrative.
Real company names are used only as public-company assumptions and do not represent confidential information, real pipeline data, or factual evaluations of those organizations.`
  },

  caseStudy: {
    context: "Regulated organizations adopting GenAI need structured ways to identify use cases, assess data and workflow readiness, align stakeholders, govern risk, and operationalize AI support without overclaiming automation.",
    problem: "Teams often work with fragmented CRM or workflow data, inconsistent qualification logic, unclear stage progression, weak data-quality checks, and incomplete training or governance around AI-assisted processes.",
    solution: "I designed an interactive case study that combines use-case prioritization, weighted workflow logic, adoption guardrails, training by audience, PoC readiness checks, data-quality thinking, and structured handoff logic.",
    role: `I designed the business logic, scoring framework, workflow structure, governance assumptions, and interactive prototype.
AI-assisted development was used to accelerate coding and iteration, while the data logic, product structure, adoption framing, and use case design were defined independently.`,
    businessValue: "The case study shows how a regulated team could standardize prioritization, improve data-driven review discipline, reduce ambiguity in handoff, and introduce AI-supported workflows with explicit governance and human oversight.",
    limitations: "The project uses simulated data, has no live CRM integration, and is intended as a portfolio prototype rather than a production system.",
    nextIteration: "With a real operating environment, the next iteration would add CRM integration, role-based views, adoption analytics, explainability for scoring, user testing feedback, and automated handoff notes.",
    outputs: [
      "Weighted account scoring and data-driven prioritization.",
      "Workflow stage analysis with total versus weighted forecast logic.",
      "Bottleneck diagnosis tied to concrete Commercial Ops actions.",
      "Sales-to-Customer Success handoff workflow and qualification logic.",
      "AI adoption and governance layer with rollout, training, guardrails, and capacity-building material.",
      "Mini product brief with users, MVP scope, metrics, backlog, and validation notes.",
      "Responsible AI documentation suitable for data/risk, innovation, programme-support, and governance reviewers."
    ]
  },

  reviewPaths: [
    {
      title: "Data / Analytics / Risk View",
      bestFor: "Financial services, business information, advanced analytics, data enhancement, risk, and ML-adjacent internship reviewers.",
      whatToInspect: "Scoring methodology, weighted forecast logic, risk labels, data-quality assumptions, account brief workflow, and methodology boundaries.",
      target: "commercial-ops",
      cta: "Review Data Workflow Layer"
    },
    {
      title: "Digital AI Governance View",
      bestFor: "Digital transformation, responsible AI, public innovation, programme support, and capacity-building reviewers.",
      whatToInspect: "Case Study Brief, stakeholder map, rollout plan, guardrails, training material, governance checklist, adoption KPIs, and methodology.",
      target: "adoption",
      cta: "Review Adoption/Governance Layer"
    },
    {
      title: "Workflow Operations View",
      bestFor: "Business analyst, operations, product operations, and consulting reviewers assessing process discipline and workflow clarity.",
      whatToInspect: "Pipeline/workflow stages, scoring, handoff, bottlenecks, automations, and operational documentation.",
      target: "commercial-ops",
      cta: "Review Workflow Layer"
    },
    {
      title: "AI Product View",
      bestFor: "AI Product, Product Ops, and product-minded commercial teams evaluating workflow design quality.",
      whatToInspect: "Problem framing, users, MVP scope, backlog, metrics, and product decision log.",
      target: "product",
      cta: "Review Product Layer"
    }
  ],

  reviewerGuide: [
    {
      title: "Case Study Brief",
      note: "Start here for the two-minute summary of context, problem, solution, outputs, and limits across data, governance, and workflow operations.",
      target: "case-study"
    },
    {
      title: "Regulated Account Scoring",
      note: "Review the weighted scoring model, risk labels, PoC readiness, stage criteria, and transparent simulated-data assumptions.",
      target: "commercial-ops"
    },
    {
      title: "Adoption & Governance",
      note: "Review stakeholder mapping, rollout phases, guardrails, training by audience, and adoption KPIs.",
      target: "adoption"
    },
    {
      title: "Training Material Example",
      note: "Open the sample workshop agenda, learning objectives, and slide outline to see a consulting-style enablement deliverable.",
      target: "training-material"
    },
    {
      title: "LLM-Assisted Brief Simulator",
      note: "See how structured prompt logic, approved-data framing, output validation, and human review are positioned in the workflow.",
      target: "commercial-ops"
    },
    {
      title: "Governance Checklist",
      note: "Inspect the compliance questions and escalation logic used before a pilot or PoC begins.",
      target: "adoption"
    },
    {
      title: "Methodology",
      note: "Check the simulated-data boundaries, limitations, and non-production claims to avoid overstatement.",
      target: "methodology"
    }
  ],

  demoScenarios: [
    {
      accountId: 11,
      label: "Healthcare anonymization pilot",
      context: "A sensitive healthcare workflow needs a controlled path from use-case idea to human-reviewed pilot.",
      gates: [
        {
          name: "Intake",
          check: "Is the workflow narrow enough to evaluate without touching production records?",
          evidence: "Use-case hypothesis, target document class, operational owner, and expected value metric.",
          blocker: "Data owner is named, but the initial dataset still mixes patient and research context.",
          decision: "Keep the pilot in discovery until the data boundary is rewritten.",
          artifact: "Use-case intake note with excluded data categories."
        },
        {
          name: "Data boundary",
          check: "Can the pilot run on approved, minimized, or anonymized sample data?",
          evidence: "Data-source inventory, anonymization rule, sample-size note, and privacy review trigger.",
          blocker: "Anonymization workflow is plausible but needs a reviewer sign-off before PoC.",
          decision: "Advance only after privacy owner confirms the sample policy.",
          artifact: "Data boundary checklist and privacy escalation note."
        },
        {
          name: "Pilot gate",
          check: "Does the PoC have measurable success criteria and human oversight?",
          evidence: "Success metric, business owner, technical owner, logging requirement, and review workflow.",
          blocker: "Success metric exists, but escalation conditions are not yet explicit.",
          decision: "Create a human-review gate before outputs can be operationally used.",
          artifact: "Pilot scorecard with acceptance criteria."
        }
      ]
    },
    {
      accountId: 2,
      label: "Insurance claims assistant",
      context: "A document-heavy insurance use case needs governance proof before it can become a credible AI support workflow.",
      gates: [
        {
          name: "Triage",
          check: "Does the use case solve a repeated operational pain rather than a generic AI ambition?",
          evidence: "Claims volume hypothesis, repeated document types, current handoff issue, and owner.",
          blocker: "The claims pain is clear, but the business value is not yet quantified.",
          decision: "Move to value sizing before any technical demo is requested.",
          artifact: "Claims workflow triage note."
        },
        {
          name: "Risk review",
          check: "Which outputs need human review, logging, and auditability?",
          evidence: "Output categories, sensitive data flag, legal/compliance stakeholder, and logging need.",
          blocker: "Compliance reviewer is identified, but audit log fields are incomplete.",
          decision: "Add auditability requirements before Security Review.",
          artifact: "Governance questions mapped to workflow outputs."
        },
        {
          name: "Handoff",
          check: "Can Sales, Security, and Customer Success read the same next-step record?",
          evidence: "Named owner, first milestone, success metric, known risks, and implementation notes.",
          blocker: "First milestone is present, but Customer Success has no adoption metric yet.",
          decision: "Add adoption KPI before handoff is considered complete.",
          artifact: "Sales-to-CS handoff card."
        }
      ]
    },
    {
      accountId: 17,
      label: "Infrastructure knowledge search",
      context: "A safety-sensitive operations workflow needs a stronger evidence path than a normal productivity demo.",
      gates: [
        {
          name: "Workflow fit",
          check: "Is the assistant limited to retrieval and support rather than automated operational decisions?",
          evidence: "Workflow map, excluded decision types, user role, and target document repository.",
          blocker: "Retrieval scope is clear, but excluded decision types need sharper wording.",
          decision: "Document non-automation boundaries before demo.",
          artifact: "Workflow scope card."
        },
        {
          name: "Security model",
          check: "Are access controls and data residency assumptions explicit enough for review?",
          evidence: "User groups, source systems, deployment preference, logging needs, and access model.",
          blocker: "Access groups are known, but deployment constraints are still high level.",
          decision: "Route to Security Review with a standard data-flow summary.",
          artifact: "Security review pack outline."
        },
        {
          name: "Adoption gate",
          check: "Who owns training, misuse prevention, and post-pilot measurement?",
          evidence: "Training audience, guardrails, adoption owner, and usage metric.",
          blocker: "Training audience exists, but misuse examples are missing.",
          decision: "Add guardrail examples before the pilot readout.",
          artifact: "Adoption readiness checklist."
        }
      ]
    }
  ],

  adoptionGovernance: {
    stakeholderMap: [
      {
        stakeholder: "CRO / Revenue Lead",
        need: "Reliable forecast, clearer pipeline risk, and consistent executive visibility.",
        role: "Executive sponsor"
      },
      {
        stakeholder: "Sales Ops / RevOps",
        need: "Standardized CRM workflow, scoring logic, and forecast discipline.",
        role: "Process owner"
      },
      {
        stakeholder: "Account Executives",
        need: "Clear qualification criteria, next-step logic, and account prioritization.",
        role: "Daily user"
      },
      {
        stakeholder: "Customer Success",
        need: "Structured handoff context, risk visibility, and success criteria.",
        role: "Post-sale owner"
      },
      {
        stakeholder: "Legal / Compliance",
        need: "Evidence that governance, oversight, and data boundaries are respected.",
        role: "Governance reviewer"
      },
      {
        stakeholder: "Data / IT / Security",
        need: "Data quality, integration clarity, access controls, and deployment feasibility.",
        role: "Technical enabler"
      }
    ],
    rolloutPlan: [
      {
        phase: "Discovery",
        goal: "Understand CRM pain points, reporting friction, and workflow gaps.",
        output: "Process map, stakeholder notes, prioritized use-case list, and change impact alignment using stakeholder readiness mapping (ADKAR-style: Awareness, Desire, Knowledge, Ability, Reinforcement)."
      },
      {
        phase: "Pilot",
        goal: "Test the cockpit with a small Sales / CS / RevOps group.",
        output: "Pilot feedback, usage data, and refinement backlog"
      },
      {
        phase: "Training",
        goal: "Teach teams how to read scores, forecast, bottlenecks, and handoff logic.",
        output: "User guide, onboarding walkthrough, and example use cases"
      },
      {
        phase: "Governance Review",
        goal: "Validate data assumptions, human oversight, and AI usage boundaries.",
        output: "Guardrail checklist and operating policy"
      },
      {
        phase: "Rollout",
        goal: "Expand usage to the wider commercial organization.",
        output: "Standard operating workflow and adoption KPI tracking"
      }
    ],
    guardrails: [
      "Scoring should support prioritization, not replace human judgment or deal ownership.",
      "No sensitive customer data should be entered into external LLM tools without explicit approval.",
      "Forecast outputs should be reviewed by Sales or RevOps before executive use.",
      "AI-assisted summaries should be clearly labeled and treated as draft support material.",
      "Account prioritization logic should be reviewed periodically for bias, stale assumptions, and overweighted factors.",
      "CRM data quality should be checked before using scores or metrics in planning decisions.",
      "Use an EU AI Act risk-triage lens for sensitive or potentially high-risk use cases, and escalate unclear cases to Legal/Compliance before pilot approval."
    ],
    trainingPlan: [
      {
        audience: "Sales team",
        timing: "Onboarding + quarterly refresh",
        focus: "How to interpret scores, bottlenecks, next-step logic, and exit criteria."
      },
      {
        audience: "Customer Success",
        timing: "Pre-handoff workshop",
        focus: "How to use handoff notes, risks, and success criteria during onboarding."
      },
      {
        audience: "Managers",
        timing: "Monthly business review prep",
        focus: "How to read forecast signals, pipeline health, and adoption KPIs."
      },
      {
        audience: "Legal / Compliance / Security",
        timing: "Pilot gate review",
        focus: "How human oversight, governance notes, and usage guardrails are applied."
      }
    ],
    successMetrics: [
      "Weekly active users reviewing pipeline through the cockpit.",
      "Percentage of opportunities reviewed with explicit stage exit criteria.",
      "Reduction in unclear or premature stage transitions.",
      "Forecast review time for managers and RevOps.",
      "Sales-to-CS handoff completion rate.",
      "Number of recurring misalignment cases between Sales and Customer Success.",
      "Pilot user satisfaction and qualitative adoption feedback.",
      "Percentage of AI-assisted outputs reviewed by a human before use."
    ],
    consultingDeliverables: [
      {
        deliverable: "Process map",
        purpose: "Understand the current Sales-to-CS workflow and where coordination breaks down."
      },
      {
        deliverable: "Use case backlog",
        purpose: "Prioritize AI-enabled workflow improvements by impact and feasibility."
      },
      {
        deliverable: "Governance checklist",
        purpose: "Define human review, data boundaries, and operational risk guardrails."
      },
      {
        deliverable: "Training guide",
        purpose: "Support adoption by Sales, Customer Success, managers, and governance stakeholders."
      },
      {
        deliverable: "Training material example",
        purpose: "Show how a workshop agenda, learning objectives, and slide storyline would support enablement before rollout."
      },
      {
        deliverable: "Adoption KPI tracker",
        purpose: "Measure whether the workflow is actually used and where adoption stalls."
      }
    ]
  },

  trainingMaterial: {
    intro: "This mini deliverable shows the kind of enablement artifact I would prepare before a pilot or early rollout: a workshop agenda, explicit learning objectives, and a simple slide storyline aligned with AI adoption work.",
    workshopAgenda: [
      {
        slot: "0-10 min",
        topic: "Why this workflow matters",
        purpose: "Align on the business problem, target process, and expected value before discussing tooling."
      },
      {
        slot: "10-20 min",
        topic: "Workflow walkthrough",
        purpose: "Review the current process, pain points, stage exits, and where AI-assisted support is introduced."
      },
      {
        slot: "20-35 min",
        topic: "Governance and risk boundaries",
        purpose: "Clarify approved data sources, human review expectations, escalation triggers, and environment constraints."
      },
      {
        slot: "35-50 min",
        topic: "Hands-on use-case review",
        purpose: "Walk through one simulated account brief and discuss what good prompt/output review looks like."
      },
      {
        slot: "50-60 min",
        topic: "Adoption commitments and next steps",
        purpose: "Confirm owners, training follow-up, success metrics, and the first post-workshop actions."
      }
    ],
    learningObjectives: [
      "Explain the target workflow and where AI-assisted support fits within it.",
      "Recognize which decisions remain human-owned and when Legal, Compliance, or Security escalation is required.",
      "Use the account brief simulator as a structured support tool rather than as an autonomous decision-maker.",
      "Identify the minimum data, stakeholder, and success-metric conditions required before a PoC or pilot proceeds.",
      "Leave the session with clear follow-up actions, owners, and adoption metrics."
    ],
    slideOutline: [
      {
        title: "Slide 1 - Business context and target workflow",
        points: [
          "What problem the workflow is solving",
          "Who uses it and where friction appears today",
          "What success looks like in operational terms"
        ]
      },
      {
        title: "Slide 2 - Where GenAI fits in the process",
        points: [
          "Which tasks are assisted by GenAI",
          "What input data is allowed",
          "What outputs are draft support material only"
        ]
      },
      {
        title: "Slide 3 - Governance and human oversight",
        points: [
          "Who reviews outputs before use",
          "When to escalate to Legal, Compliance, or Security",
          "How auditability and approvals are documented"
        ]
      },
      {
        title: "Slide 4 - Prompt and output quality checklist",
        points: [
          "Prompt structure and context fields",
          "Validation checks for hallucination or missing context",
          "What a good reviewer comment looks like"
        ]
      },
      {
        title: "Slide 5 - Rollout next steps and adoption metrics",
        points: [
          "Immediate actions after the workshop",
          "Who owns training reinforcement",
          "Which adoption KPIs will be monitored first"
        ]
      }
    ]
  },

  automationLayer: {
    title: "Automation Layer",
    subtitle: "How the cockpit could trigger real-world actions through no-code/low-code workflows.",
    description: "This section demonstrates how the operational signals from the cockpit could be connected to automation tools such as n8n, Make, Zapier, Power Automate, or Copilot Studio to reduce manual follow-up and improve response time.",
    workflows: [
      {
        platform: "n8n / Zapier",
        name: "Security Review Alert",
        trigger: "Deal reaches 'Security Review' stage",
        conditions: ["Stage = Security Review", "Days in stage > 14", "Risk label contains 'Compliance' or 'Security'"],
        action: "Send Slack/Teams alert to Legal + Security team",
        delay: "Immediate",
        value: "Prevents deals from stalling in security review due to lack of visibility."
      },
      {
        platform: "n8n / Zapier",
        name: "High-Fit Account Notification",
        trigger: "Account fit score exceeds 4.2",
        conditions: ["Weighted fit score ≥ 4.2", "Account not already in active deal"],
        action: "Create task in CRM for AE + send email to CRO",
        delay: "Immediate",
        value: "Ensures top-priority accounts receive proactive outreach."
      },
      {
        platform: "Power Automate",
        name: "Sensitive Use Case Approval Flow",
        trigger: "Use case is flagged for Legal/Compliance review",
        conditions: ["Sensitive or unclear AI use case", "Business owner identified", "Pilot request submitted"],
        action: "Route an approval package through Teams/Outlook with required approvers, tracked comments, and escalation reminders",
        delay: "Same business day",
        value: "Turns governance review into a traceable approval workflow instead of ad hoc email coordination."
      },
      {
        platform: "Power Automate",
        name: "PoC Readiness Gate",
        trigger: "Deal moves to 'PoC' stage",
        conditions: ["PoC readiness < 60%", "Missing success metric or data owner"],
        action: "Block stage transition + notify Sales Ops with checklist",
        delay: "On stage change attempt",
        value: "Reduces weak PoCs and improves handoff quality."
      },
      {
        platform: "n8n / Make",
        name: "Handoff Completion Reminder",
        trigger: "Deal reaches 'Closed Won'",
        conditions: ["Handoff checklist incomplete", "CS kickoff not scheduled"],
        action: "Escalate to Sales Manager + CS Lead",
        delay: "24h after closing",
        value: "Ensures clean Sales-to-CS transition before resources are committed."
      },
      {
        platform: "Copilot Studio",
        name: "Post-Workshop FAQ Copilot",
        trigger: "User asks for support after enablement training",
        conditions: ["Approved FAQ and workflow guidance available", "Escalation route to a human owner defined"],
        action: "Answer routine questions, surface approved prompts/checklists, and escalate unresolved issues to the enablement lead",
        delay: "On demand",
        value: "Reinforces adoption after training while keeping human escalation available for edge cases."
      },
      {
        platform: "n8n / Power Automate",
        name: "Weekly Pipeline Digest",
        trigger: "Every Monday at 9:00 AM",
        conditions: ["Open deals > 0"],
        action: "Generate summary with top 3 bottlenecks + weighted forecast delta",
        delay: "Weekly",
        value: "Creates consistent forecast discipline without manual report building."
      }
    ],
    toolNote: "These workflows are designed for no-code or low-code tooling such as n8n, Make, Zapier, Power Automate, and Copilot Studio. They require CRM events or scheduled polling plus clear ownership, approvals, and escalation rules, but they do not require a custom backend to demonstrate workflow logic."
  },

  productBrief: {
    problemStatement: "Revenue teams in enterprise AI companies need a structured way to prioritize accounts, monitor pipeline health, and coordinate handoff between Sales and Customer Success when selling complex solutions into regulated industries.",
    targetUsers: [
      {
        user: "RevOps Manager",
        need: "Understand pipeline health, bottlenecks, and forecast consistency."
      },
      {
        user: "Account Executive",
        need: "Prioritize accounts and understand the next best commercial action."
      },
      {
        user: "CRO",
        need: "Review weighted forecast, commercial risk, and operational signals."
      },
      {
        user: "Customer Success Manager",
        need: "Receive better handoff context before onboarding or pilot delivery."
      },
      {
        user: "Compliance reviewer",
        need: "See governance assumptions, risk boundaries, and oversight logic."
      }
    ],
    userStories: [
      "As a RevOps Manager, I want to identify bottlenecks by pipeline stage so that I can improve conversion and stage progression.",
      "As an Account Executive, I want to understand why an account receives a high or low score so that I can prioritize outreach more consistently.",
      "As a Customer Success Manager, I want structured handoff information so that I can prepare onboarding with better context.",
      "As a CRO, I want a weighted forecast view so that I can assess commercial risk and expected revenue more consistently.",
      "As a Compliance reviewer, I want clear guardrails so that AI-assisted workflows remain transparent and human-reviewed."
    ],
    mvpScope: {
      inScope: [
        "Simulated account data and scoring model.",
        "Pipeline stage overview and weighted forecast.",
        "Bottleneck analysis and stage exit criteria.",
        "Sales-to-CS handoff checklist and governance notes.",
        "Adoption guidance and product metrics."
      ],
      outOfScope: [
        "Live CRM integration and real customer data.",
        "Automated decision-making without human review.",
        "Production security architecture or user authentication.",
        "Model training or custom ML development."
      ]
    },
    productMetrics: [
      "Activation rate after first cockpit review session.",
      "Weekly usage by role.",
      "Number of accounts reviewed and reprioritized.",
      "Forecast review completion rate.",
      "Handoff completion rate before onboarding.",
      "Time saved during pipeline review.",
      "Pilot user feedback score.",
      "Percentage of opportunities with complete exit criteria."
    ],
    backlog: [
      {
        priority: "High",
        feature: "CRM integration",
        reason: "Connect the cockpit to real pipeline and stage data."
      },
      {
        priority: "High",
        feature: "Explainability layer",
        reason: "Show why an account receives a score and which factors drive it."
      },
      {
        priority: "High",
        feature: "Role-based views",
        reason: "Tailor what Sales, CS, and leadership teams see."
      },
      {
        priority: "Medium",
        feature: "Human-reviewed account brief draft",
        reason: "Summarize approved structured context before reviews or discovery calls."
      },
      {
        priority: "Medium",
        feature: "Handoff note generator",
        reason: "Support cleaner transition from Sales to Customer Success."
      },
      {
        priority: "Medium",
        feature: "Risk flag alerts",
        reason: "Highlight stalled or governance-heavy opportunities earlier."
      },
      {
        priority: "Low",
        feature: "Executive PDF export",
        reason: "Support leadership reporting and offline review."
      }
    ],
    researchNotes: [
      {
        method: "Desk Research + Industry Pattern Analysis",
        finding: "Public GTM playbooks and SaaS benchmarking often describe unclear success metrics and missing stakeholder alignment as recurring drivers of PoC failure in enterprise AI sales.",
        impact: "Justified the inclusion of explicit PoC readiness gating and stakeholder coverage scoring."
      },
      {
        method: "Hypothetical Stakeholder Interviews (simulated)",
        finding: "RevOps managers consistently prioritize 'forecast confidence' over 'data volume'. Sales leaders need explainability, not just scores.",
        impact: "Led to the weighted scoring model with visible components and the explainability layer in the backlog."
      },
      {
        method: "Competitive Landscape Review",
        finding: "Standard CRM dashboards (Salesforce, HubSpot) provide pipeline visibility but lack integrated governance guardrails and handoff logic for AI-specific sales motions.",
        impact: "Validated the need for a dedicated 'Regulated AI' layer with compliance-aware qualification and AI adoption governance."
      }
    ],
    businessMetrics: [
      { productMetric: "Forecast review time", businessImpact: "Shorter sales cycle, faster resource allocation" },
      { productMetric: "Handoff completion rate", businessImpact: "Reduced onboarding friction, lower early churn" },
      { productMetric: "PoC success rate", businessImpact: "Higher conversion to paid contracts" },
      { productMetric: "Security Review throughput", businessImpact: "Fewer late-stage deal losses to compliance" }
    ],
    decisionLog: [
      {
        decision: "Keep data simulated",
        reason: "Avoid implying access to real CRM or confidential customer intelligence."
      },
      {
        decision: "Use rule-based scoring",
        reason: "Make prioritization logic explainable, inspectable, and easy to discuss in interviews."
      },
      {
        decision: "Add human-review guardrails",
        reason: "Prevent AI-assisted outputs from being interpreted as automated decisions."
      },
      {
        decision: "Prioritize CRM integration in the backlog",
        reason: "Keep the prototype realistic without pretending it is already operational."
      },
      {
        decision: "Separate Commercial Ops, Adoption, and Product views",
        reason: "Make the same workflow readable by recruiters and stakeholders with different goals."
      },
      {
        decision: "Choose static frontend over full-stack",
        reason: "The goal is to validate workflow logic and stakeholder alignment before committing engineering resources. A no-code/low-code prototype allows 10x faster iteration with RevOps stakeholders."
      }
    ]
  },

  scoringMethodology: {
    formula: "Fit Score = Use Case Value × 30% + Regulatory Urgency × 20% + Workflow/Data Complexity × 15% + Stakeholder Clarity × 15% + Deployment Fit × 10% + Procurement Feasibility × 10%",
    scale: `Each variable is scored from 1 to 5.
The final score is a weighted average on the same 1-5 scale.`,
    dimensions: [
      {
        key: "useCaseValue",
        label: "Use Case Value",
        weight: 30,
        definition: "1 = weak or unclear business case. 5 = clear high-impact use case with measurable operational value."
      },
      {
        key: "regulatoryUrgency",
        label: "Regulatory Urgency",
        weight: 20,
        definition: "1 = low compliance pressure. 5 = highly regulated environment requiring strong controls."
      },
      {
        key: "dataComplexity",
        label: "Workflow/Data Complexity",
        weight: 15,
        definition: "1 = simple workflow and limited data context. 5 = multi-source, knowledge-heavy, high-sensitivity workflow requiring tighter orchestration."
      },
      {
        key: "stakeholderClarity",
        label: "Stakeholder Clarity",
        weight: 15,
        definition: "1 = no clear buyer or owner. 5 = business, IT, and compliance stakeholders identifiable."
      },
      {
        key: "deploymentFit",
        label: "Deployment Fit",
        weight: 10,
        definition: "1 = standard SaaS likely sufficient. 5 = strong need for governed, private, or sovereign deployment."
      },
      {
        key: "procurementFeasibility",
        label: "Procurement Feasibility",
        weight: 10,
        definition: "1 = unclear or very slow buying path. 5 = realistic route to pilot, innovation budget, or procurement sponsor."
      }
    ]
  },

  pipelineStages: [
    { name: "Target Identified", probability: 0.05 },
    { name: "Qualified", probability: 0.10 },
    { name: "Discovery", probability: 0.20 },
    { name: "Use Case Mapping", probability: 0.35 },
    { name: "Security Review", probability: 0.50 },
    { name: "PoC", probability: 0.65 },
    { name: "Procurement", probability: 0.80 },
    { name: "Closed Won", probability: 1.00 },
    { name: "CS Handoff", probability: 1.00 }
  ],

  accounts: [
    {
      id: 1,
      company: "Intesa Sanpaolo",
      type: "Public-company assumption",
      sector: "Banking",
      useCasePotential: "Advisor knowledge assistant and compliance document analysis",
      regulatorySensitivity: "High",
      dataComplexityLabel: "High",
      decisionMakers: "Chief Data Officer, Head of AI, compliance sponsor",
      reason: "Large regulated organization with significant internal knowledge volume and strong governance requirements.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 3 }
    },
    {
      id: 2,
      company: "Generali",
      type: "Public-company assumption",
      sector: "Insurance",
      useCasePotential: "Claims triage support and agent knowledge retrieval",
      regulatorySensitivity: "High",
      dataComplexityLabel: "High",
      decisionMakers: "CIO, Head of Claims, innovation sponsor",
      reason: "Document-heavy insurance workflows create a strong case for governed AI assistance.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 4, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 3 }
    },
    {
      id: 3,
      company: "Poste Italiane",
      type: "Public-company assumption",
      sector: "Public Administration",
      useCasePotential: "Customer request routing and internal operations knowledge base",
      regulatorySensitivity: "High",
      dataComplexityLabel: "Medium",
      decisionMakers: "CDO, Operations Director, IT sponsor",
      reason: "Combination of public services, financial services, and operations implies complex stakeholder alignment.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 5, dataComplexity: 3, stakeholderClarity: 4, deploymentFit: 4, procurementFeasibility: 3 }
    },
    {
      id: 4,
      company: "A2A",
      type: "Public-company assumption",
      sector: "Energy & Utilities",
      useCasePotential: "Maintenance knowledge search and regulatory reporting support",
      regulatorySensitivity: "Medium",
      dataComplexityLabel: "Medium",
      decisionMakers: "Head of Digital, CTO, operations sponsor",
      reason: "Utility operations create strong workflow use cases, but regulatory urgency is lower than core banking or insurance.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 3, dataComplexity: 3, stakeholderClarity: 4, deploymentFit: 3, procurementFeasibility: 4 }
    },
    {
      id: 5,
      company: "Enel",
      type: "Public-company assumption",
      sector: "Energy & Utilities",
      useCasePotential: "Operational intelligence for distributed energy assets",
      regulatorySensitivity: "High",
      dataComplexityLabel: "High",
      decisionMakers: "Digital transformation lead, security, operations sponsor",
      reason: "Scale, critical infrastructure context, and distributed knowledge workflows make governance and deployment fit relevant.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 4, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 3 }
    },
    {
      id: 6,
      company: "UniCredit",
      type: "Public-company assumption",
      sector: "Banking",
      useCasePotential: "Risk policy assistant and branch advisor support",
      regulatorySensitivity: "High",
      dataComplexityLabel: "High",
      decisionMakers: "Head of Digital Strategy, Risk, Compliance",
      reason: "A pan-European banking context makes governance, multilingual workflows, and stakeholder coverage commercially important.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 3 }
    },
    {
      id: 7,
      company: "UnipolSai",
      type: "Public-company assumption",
      sector: "Insurance",
      useCasePotential: "Policy comparison and claims documentation assistant",
      regulatorySensitivity: "High",
      dataComplexityLabel: "Medium",
      decisionMakers: "CIO, Head of Claims, Legal",
      reason: "Insurance document workflows offer clear efficiency potential if governance and auditability are addressed early.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 5, dataComplexity: 4, stakeholderClarity: 4, deploymentFit: 4, procurementFeasibility: 3 }
    },
    {
      id: 8,
      company: "Cassa Depositi e Prestiti",
      type: "Public-company assumption",
      sector: "Public Administration",
      useCasePotential: "Tender analysis and research assistant for strategic documents",
      regulatorySensitivity: "High",
      dataComplexityLabel: "High",
      decisionMakers: "IT, compliance, public-sector sponsor",
      reason: "State-linked workflows and sensitive research contexts make controlled deployment and stakeholder mapping important.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 2 }
    },
    {
      id: 9,
      company: "Northstar Insurance Group",
      type: "Fictitious account",
      sector: "Insurance",
      useCasePotential: "Underwriting support and broker knowledge assistant",
      regulatorySensitivity: "High",
      dataComplexityLabel: "High",
      decisionMakers: "VP Underwriting, CDO, compliance lead",
      reason: "High-volume underwriting documentation creates a measurable operational case with clear governance concerns.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 4, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 4, procurementFeasibility: 4 }
    },
    {
      id: 10,
      company: "Alpina Utilities",
      type: "Fictitious account",
      sector: "Energy & Utilities",
      useCasePotential: "Predictive maintenance log analysis",
      regulatorySensitivity: "Medium",
      dataComplexityLabel: "Low",
      decisionMakers: "VP Operations, maintenance lead",
      reason: "Good operational use case, but lower regulatory pressure may reduce the need for a premium governed AI platform.",
      scoreComponents: { useCaseValue: 3, regulatoryUrgency: 2, dataComplexity: 2, stakeholderClarity: 4, deploymentFit: 2, procurementFeasibility: 4 }
    },
    {
      id: 11,
      company: "MedGov Services",
      type: "Fictitious account",
      sector: "Healthcare",
      useCasePotential: "Patient record anonymization and clinical trial document matching",
      regulatorySensitivity: "High",
      dataComplexityLabel: "High",
      decisionMakers: "CMIO, privacy officer, research operations",
      reason: "Sensitive health-related workflows require privacy, auditability, and careful human oversight before a pilot.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 3 }
    },
    {
      id: 12,
      company: "EuroBanca Corp",
      type: "Fictitious account",
      sector: "Banking",
      useCasePotential: "KYC and AML document parsing support",
      regulatorySensitivity: "High",
      dataComplexityLabel: "Medium",
      decisionMakers: "Head of Compliance, Operations, IT security",
      reason: "Compliance-driven document workflows align well with an enterprise AI qualification motion.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 5, dataComplexity: 4, stakeholderClarity: 5, deploymentFit: 4, procurementFeasibility: 4 }
    },
    {
      id: 13,
      company: "Vanguard Regional Admin",
      type: "Fictitious account",
      sector: "Public Administration",
      useCasePotential: "Citizen request classification and routing",
      regulatorySensitivity: "High",
      dataComplexityLabel: "Medium",
      decisionMakers: "IT Director, service operations, procurement",
      reason: "Clear service workflow, but procurement path and stakeholder ownership may slow conversion.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 4, dataComplexity: 3, stakeholderClarity: 3, deploymentFit: 3, procurementFeasibility: 2 }
    },
    {
      id: 14,
      company: "Aegis Wealth",
      type: "Fictitious account",
      sector: "Banking",
      useCasePotential: "Portfolio insight generation for relationship managers",
      regulatorySensitivity: "High",
      dataComplexityLabel: "High",
      decisionMakers: "Head of Wealth Tech, Risk, business sponsor",
      reason: "High-value advisor productivity use case with strict governance requirements and plausible business sponsorship.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 4 }
    },
    {
      id: 15,
      company: "Optima Energy",
      type: "Fictitious account",
      sector: "Energy & Utilities",
      useCasePotential: "Smart meter data Q&A and operations reporting",
      regulatorySensitivity: "Medium",
      dataComplexityLabel: "High",
      decisionMakers: "CDO, analytics lead",
      reason: "Large data volume is attractive, but commercial urgency depends on a clearly scoped workflow and value case.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 3, dataComplexity: 5, stakeholderClarity: 3, deploymentFit: 3, procurementFeasibility: 3 }
    },
    {
      id: 16,
      company: "Meridian Health",
      type: "Fictitious account",
      sector: "Healthcare",
      useCasePotential: "Medical literature synthesis for internal research teams",
      regulatorySensitivity: "High",
      dataComplexityLabel: "High",
      decisionMakers: "Director of Research, privacy, medical operations",
      reason: "Research workflows have clear productivity potential but require explicit limitations, validation, and human oversight.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 5, dataComplexity: 4, stakeholderClarity: 3, deploymentFit: 4, procurementFeasibility: 3 }
    },
    {
      id: 17,
      company: "Ferrovie dello Stato Italiane",
      type: "Public-company assumption",
      sector: "Transport & Infrastructure",
      useCasePotential: "Operational knowledge search and maintenance documentation assistant",
      regulatorySensitivity: "High",
      dataComplexityLabel: "High",
      decisionMakers: "Operations, IT, safety and procurement stakeholders",
      reason: "Critical infrastructure context implies complex workflows, safety sensitivity, and cross-functional procurement.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 4, dataComplexity: 4, stakeholderClarity: 3, deploymentFit: 4, procurementFeasibility: 3 }
    },
    {
      id: 18,
      company: "Leonardo",
      type: "Public-company assumption",
      sector: "Aerospace & Defense",
      useCasePotential: "Engineering knowledge retrieval and controlled document intelligence",
      regulatorySensitivity: "High",
      dataComplexityLabel: "High",
      decisionMakers: "Engineering operations, security, innovation sponsor",
      reason: "Controlled information environments make security, access management, and deployment fit commercially central.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 5, stakeholderClarity: 3, deploymentFit: 5, procurementFeasibility: 2 }
    },
    {
      id: 19,
      company: "Hera Group",
      type: "Public-company assumption",
      sector: "Energy & Utilities",
      useCasePotential: "Operations knowledge base and regulatory documentation support",
      regulatorySensitivity: "Medium",
      dataComplexityLabel: "Medium",
      decisionMakers: "Digital operations, compliance, business unit sponsor",
      reason: "Strong operations use case with moderate regulatory pressure and a plausible internal productivity angle.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 3, dataComplexity: 3, stakeholderClarity: 4, deploymentFit: 3, procurementFeasibility: 4 }
    },
    {
      id: 20,
      company: "Lombardy Digital Services",
      type: "Fictitious account",
      sector: "Public Administration",
      useCasePotential: "Administrative knowledge assistant for internal service teams",
      regulatorySensitivity: "High",
      dataComplexityLabel: "Medium",
      decisionMakers: "Service director, IT, procurement, privacy office",
      reason: "Public-sector workflow modernization has strong fit, but procurement and governance requirements must be qualified early.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 5, dataComplexity: 3, stakeholderClarity: 4, deploymentFit: 4, procurementFeasibility: 2 }
    }
  ],

  pipelineDeals: [
    { id: "D1", accountId: 1, stage: "PoC", value: 600000, daysInStage: 14, pocReadiness: 76, risk: "Technical validation", nextStep: "Confirm success metric and schedule security architecture review." },
    { id: "D2", accountId: 2, stage: "Security Review", value: 520000, daysInStage: 25, pocReadiness: 54, risk: "Compliance", nextStep: "Send standard infosec pack and map deployment constraints." },
    { id: "D3", accountId: 3, stage: "Discovery", value: 320000, daysInStage: 6, pocReadiness: 38, risk: "Budget", nextStep: "Quantify request-routing value case and identify sponsor." },
    { id: "D4", accountId: 4, stage: "Qualified", value: 200000, daysInStage: 3, pocReadiness: 31, risk: "Stakeholder alignment", nextStep: "Book discovery with operations and IT owner." },
    { id: "D5", accountId: 5, stage: "Procurement", value: 780000, daysInStage: 18, pocReadiness: 82, risk: "Legal", nextStep: "Resolve pilot scope and final security wording with Legal." },
    { id: "D6", accountId: 6, stage: "Use Case Mapping", value: 650000, daysInStage: 9, pocReadiness: 59, risk: "Technical validation", nextStep: "Run workflow mapping with branch advisor team." },
    { id: "D7", accountId: 8, stage: "Target Identified", value: 900000, daysInStage: 4, pocReadiness: 22, risk: "Procurement", nextStep: "Identify innovation or public procurement entry path." },
    { id: "D8", accountId: 9, stage: "Closed Won", value: 480000, daysInStage: 2, pocReadiness: 91, risk: "None", nextStep: "Prepare Customer Success kickoff and adoption scorecard." },
    { id: "D9", accountId: 11, stage: "PoC", value: 460000, daysInStage: 21, pocReadiness: 69, risk: "Privacy", nextStep: "Validate anonymization workflow and human review gates." },
    { id: "D10", accountId: 12, stage: "Discovery", value: 350000, daysInStage: 12, pocReadiness: 44, risk: "Stakeholder alignment", nextStep: "Bring compliance owner into discovery before use-case mapping." },
    { id: "D11", accountId: 14, stage: "Security Review", value: 610000, daysInStage: 19, pocReadiness: 66, risk: "Compliance", nextStep: "Complete vendor risk questionnaire and data-flow summary." },
    { id: "D12", accountId: 16, stage: "CS Handoff", value: 420000, daysInStage: 3, pocReadiness: 88, risk: "Adoption", nextStep: "Finalize first milestone with CS manager and research sponsor." },
    { id: "D13", accountId: 17, stage: "Procurement", value: 570000, daysInStage: 23, pocReadiness: 73, risk: "Procurement", nextStep: "Run procurement readiness checkpoint with sponsor and Legal." },
    { id: "D14", accountId: 18, stage: "Use Case Mapping", value: 410000, daysInStage: 11, pocReadiness: 57, risk: "Security", nextStep: "Confirm access-control assumptions before technical review." },
    { id: "D15", accountId: 19, stage: "Qualified", value: 250000, daysInStage: 5, pocReadiness: 35, risk: "Business case", nextStep: "Document operational value hypothesis and initial KPI." },
    { id: "D16", accountId: 20, stage: "Security Review", value: 880000, daysInStage: 17, pocReadiness: 62, risk: "Governance", nextStep: "Clarify data residency and approval chain with privacy office." }
  ],

  executiveInsights: [
    {
      title: "Security Review is the main bottleneck",
      signal: "Security Review contains three open opportunities and the highest average current stage age among materially qualified stages.",
      risk: "Qualified opportunities may stall because infosec, deployment, and data-flow concerns are addressed too late in the sales motion.",
      action: "Move security qualification earlier: pre-discovery checklist, standard infosec one-pager, deployment FAQ, and mandatory data-flow capture before PoC.",
      impact: "Expected impact: fewer reactive infosec loops and higher confidence when Sales requests technical resources."
    },
    {
      title: "PoC readiness needs stricter gating",
      signal: "Several opportunities have strong fit but only mid-range PoC readiness because success metrics, data owners, or deployment assumptions are not fully captured.",
      risk: "Sales may request technical or Customer Success resources before the pilot has a measurable acceptance criterion and named owners.",
      action: "Require success metric, data source owner, technical owner, and first workflow milestone before a deal can move beyond Use Case Mapping.",
      impact: "Expected impact: cleaner PoCs, better Sales-to-CS handoff, and more reliable weighted forecast."
    },
    {
      title: "High-fit regulated accounts need earlier multi-threading",
      signal: "Top-scoring accounts usually require business, IT, security, compliance, and procurement alignment; engaging these stakeholders late can slow conversion.",
      risk: "A deal can appear commercially strong while still lacking the stakeholder coverage needed to survive procurement and governance review.",
      action: "Add stakeholder coverage score to the CRM and make it part of Discovery exit criteria.",
      impact: "Expected impact: fewer late-stage surprises and a more credible enterprise buying motion."
    }
  ],

  bottlenecks: [
    {
      stage: "Security Review",
      signal: "Highest concentration of delayed qualified pipeline and recurring governance/security risks.",
      cause: "Security, deployment, and data-flow questions are often handled after use-case enthusiasm rather than during early qualification.",
      action: "Create a reusable security pack, pre-discovery security checklist, and required CRM fields for deployment model and data sensitivity.",
      impact: "Reduce time-to-PoC and improve forecast confidence."
    },
    {
      stage: "PoC Readiness",
      signal: "Some high-fit deals still lack a precise success metric or named data source owner.",
      cause: "Use-case workshops can define ambition without translating it into measurable acceptance criteria.",
      action: "Introduce a PoC scorecard covering success metric, business owner, technical owner, data owner, and first milestone.",
      impact: "Increase PoC quality and reduce weak handoffs to Customer Success."
    },
    {
      stage: "Procurement Alignment",
      signal: "Late-stage opportunities depend on Legal, Security, Finance, and sponsor alignment before paper process starts.",
      cause: "Commercial readiness may be stronger than stakeholder readiness or budget-path clarity.",
      action: "Run a procurement readiness checkpoint before moving from Security Review to PoC or Procurement.",
      impact: "Shorten contracting cycles and reduce preventable last-mile delay."
    }
  ],

  stageExitCriteria: [
    {
      transition: "Target Identified → Qualified",
      criteria: [
        "Sector and company match the target ICP.",
        "Initial use-case hypothesis is documented.",
        "Likely business owner is identifiable.",
        "Public information suggests a realistic operational need.",
        "Next outbound or intro action is assigned."
      ]
    },
    {
      transition: "Discovery → Use Case Mapping",
      criteria: [
        "Business pain is documented in CRM.",
        "Economic buyer or business sponsor is identified.",
        "Primary use case is selected.",
        "Initial compliance sensitivity is assessed.",
        "Next workshop is scheduled."
      ]
    },
    {
      transition: "Use Case Mapping → Security Review",
      criteria: [
        "Target workflow is mapped.",
        "Data sources are identified.",
        "Technical owner is identified.",
        "Deployment preference is captured at high level.",
        "PoC success metric is proposed."
      ]
    },
    {
      transition: "Security Review → PoC",
      criteria: [
        "Infosec stakeholder is involved.",
        "Data-processing constraints are documented.",
        "Auditability and logging requirements are captured.",
        "Deployment model is aligned at high level.",
        "Known legal or procurement blockers are logged."
      ]
    },
    {
      transition: "Closed Won → CS Handoff",
      criteria: [
        "Success metric is confirmed in writing.",
        "Business owner and technical owner are named.",
        "Implementation scope and first milestone are clear.",
        "Data access path and governance constraints are recorded.",
        "Customer Success kickoff date is scheduled."
      ]
    }
  ],

  handoffChecklist: [
    { title: "Business use case clearly defined", desc: "The problem, target workflow, and expected value are documented." },
    { title: "Success metric agreed", desc: "The PoC has a measurable acceptance criterion, not only a qualitative goal." },
    { title: "Business owner named", desc: "The operational owner who will judge value is identified." },
    { title: "Technical owner named", desc: "The counterpart for data access, deployment, and environment constraints is identified." },
    { title: "Data sources mapped", desc: "Relevant sources, sensitivity, and access path are recorded." },
    { title: "Governance constraints captured", desc: "Security, compliance, auditability, and human oversight requirements are known." },
    { title: "Procurement path understood", desc: "Budget owner, Legal/Security review, and expected approval path are logged." },
    { title: "First milestone scheduled", desc: "Customer Success kickoff and first delivery checkpoint are on the calendar." }
  ],

  complianceChecklist: [
    "Does the use case involve personal, financial, health-related, or otherwise sensitive data?",
    "Is the system used for recommendation, decision support, automation, or knowledge retrieval?",
    "Is human oversight required before outputs can be operationally used?",
    "Are logs, versioning, access controls, or audit trails required?",
    "Is private deployment, sovereign cloud, or on-premise deployment required?",
    "Who owns approval across IT, Security, Legal, Compliance, Procurement, and the business sponsor?"
  ],
  complianceEscalationRule: "Escalation rule: If any answer is 'Yes' or 'Unknown', flag for Legal/Compliance review before PoC kickoff. Any 'Yes' to items 1-4 triggers mandatory Privacy/Legal review. Any 'Yes' to item 6 requires documented stakeholder sign-off.",

  sectorBuyingDrivers: {
    "Banking": "risk control, advisor productivity, compliance traceability, and explainable workflows",
    "Insurance": "claims efficiency, underwriting support, document-heavy workflows, and auditability",
    "Public Administration": "service modernization, procurement transparency, privacy, and governance discipline",
    "Energy & Utilities": "operational reliability, critical infrastructure workflows, and controlled knowledge access",
    "Healthcare": "sensitive-data handling, human oversight, traceability, and measurable operational improvement",
    "Transport & Infrastructure": "safety-sensitive operations, maintenance documentation, and stakeholder-heavy procurement",
    "Aerospace & Defense": "controlled access, document intelligence, security assurance, and constrained deployment models"
  },

  briefPromptStructure: [
    "Account context",
    "Sector-specific buying drivers",
    "Likely AI use cases",
    "Stakeholder map",
    "Compliance and governance questions",
    "Commercial risks",
    "Recommended CRM next step",
    "Sales-to-CS handoff notes"
  ],

  methodologySections: [
    {
      title: "What is simulated",
      items: [
        "Pipeline values, deal stages, stage probability, weighted pipeline, stage duration, risk labels, and PoC readiness.",
        "Fit scores and score components are illustrative and designed to show prioritization logic, not factual judgments about the named organizations.",
        "LLM-assisted account briefs are generated from predefined structured data and public-company assumptions."
      ]
    },
    {
      title: "What is based on public-company assumptions",
      items: [
        "Company names and broad sector classification where real organizations are referenced.",
        "Typical buying dynamics in regulated enterprise environments: security review, procurement complexity, governance, and stakeholder alignment.",
        "Generic enterprise AI use-case patterns such as document intelligence, advisor support, knowledge retrieval, and operational workflow assistance."
      ]
    },
    {
      title: "What the project demonstrates",
      items: [
        "CRM workflow thinking and explicit stage governance.",
        "Account prioritization through a weighted scoring framework.",
        "Forecast discipline using total and weighted pipeline.",
        "Commercial diagnostics: bottleneck signals, causes, actions, and expected impact.",
        "Sales-to-Customer Success handoff design and compliance-aware qualification."
      ]
    },
    {
      title: "What the project is not",
      items: [
        "A production CRM, a legal compliance assessment tool, or a real AI product.",
        "A representation of confidential customer data, internal pipeline, or proprietary company information.",
        "A claim that any named organization is currently evaluating or using this specific solution."
      ]
    }
  ]
};
