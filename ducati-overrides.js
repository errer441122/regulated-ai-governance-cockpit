(function () {
  "use strict";

  const d = window.cockpitData;
  if (!d) return;

  d.project = {
    title: "Customer Experience Data Analytics Cockpit",
    subtitle: "A static interactive case study showing how a Customer Experience team could organize satisfaction reporting, customer segmentation, journey diagnostics, and cross-functional improvement actions.",
    disclaimer: `This is an independent portfolio case study using simulated customer-experience data.
It is not connected to Ducati systems, does not use confidential customer data, and is designed only to demonstrate analytical reasoning, dashboard logic, and responsible data handling.`,
    positioning: `I adapted the original cockpit into a Customer Experience analytics version aligned with a Data Analyst internship.
The focus is on collecting and organizing data, building reporting views, segmenting customers, identifying trends, and translating insights into clear improvement actions for business teams.`,
    oneLineSummary: "An interactive case study showing how a Customer Experience team could turn customer behavior, satisfaction signals, and journey feedback into dashboards, segments, trends, and action-ready recommendations.",
    headerSubtitle: "Customer Experience Analytics · Segmentation · Reporting",
    profileLabel: "Data Analyst Customer Experience Case Study",
    heroReviewLine: "Designed to be reviewed from four angles: customer satisfaction reporting, segmentation, journey diagnostics, and cross-functional improvement actions.",
    cockpitCta: "Review CX Analytics Layer",
    adoptionCta: "Review Insight-to-Action Layer",
    productCta: "Review Dashboard MVP Brief",
    caseStudyCta: "Read Case Study Brief",
    scoringDisclaimer: `Scores and segment examples are illustrative.
They use simulated customer-experience assumptions and do not represent Ducati data, real customer evaluations, or confidential company information.`
  };

  d.caseStudy = {
    context: "A premium automotive or motorcycle brand needs structured ways to understand customer satisfaction, service experience, digital behavior, dealer follow-up, and owner journey signals across multiple touchpoints.",
    problem: "Customer data can be fragmented across surveys, CRM notes, dealer interactions, digital forms, service records, and campaign feedback. Without a repeatable reporting workflow, teams may miss recurring pain points or struggle to communicate findings clearly.",
    solution: "I designed a simulated Customer Experience analytics cockpit that combines data intake, segment scoring, journey-stage tracking, trend diagnosis, dashboard reporting, privacy-aware guardrails, and action handoff logic.",
    role: `I designed the analytical framing, scoring dimensions, workflow structure, dashboard narrative, and reviewer-facing documentation.
AI-assisted development was used to accelerate coding and iteration, while the data logic, CX framing, project structure, and use-case adaptation were defined independently.`,
    businessValue: "The case study shows how a CX team could standardize customer satisfaction review, prioritize high-impact segments, detect journey friction, communicate insights clearly, and coordinate improvement actions with CRM, dealer network, service, marketing, and product stakeholders.",
    limitations: "The project uses simulated data, has no live CRM integration, and is intended as a portfolio prototype rather than a production analytics system.",
    nextIteration: "With a real operating environment, the next iteration would add CRM or survey integration, Power BI-style reporting, role-based views, automated refreshes, data-quality checks, customer privacy controls, and feedback-loop measurement after actions are taken.",
    outputs: [
      "Customer segment scoring and data-driven prioritization.",
      "Journey-stage analysis with total versus weighted insight volume.",
      "Trend and bottleneck diagnosis tied to concrete Customer Experience actions.",
      "CX-to-business handoff workflow for service, dealer, CRM, and product teams.",
      "Insight-to-action tracker with privacy guardrails, reporting guide notes, and follow-up KPIs.",
      "Dashboard MVP brief with users, MVP scope, metrics, backlog, and validation notes.",
      "Transparent methodology separating simulated customer data from portfolio assumptions."
    ]
  };

  d.reviewPaths = [
    {
      title: "Customer Satisfaction Analytics",
      bestFor: "Customer Experience, CRM, and Data Analyst reviewers looking for reporting, dashboard, and insight communication evidence.",
      whatToInspect: "Segment scoring, weighted insight volume, satisfaction drivers, trend signals, and methodology boundaries.",
      target: "commercial-ops",
      cta: "Review CX Analytics Layer"
    },
    {
      title: "Segmentation and Profiling",
      bestFor: "Teams assessing whether customer groups can be organized into meaningful action priorities.",
      whatToInspect: "Customer segments, score components, journey categories, feedback volume, and next-action logic.",
      target: "commercial-ops",
      cta: "Review Segment Scoring"
    },
    {
      title: "Journey Improvement Workflow",
      bestFor: "Business, service, dealer-network, and product teams evaluating process improvement reasoning.",
      whatToInspect: "Journey stages, bottlenecks, action pilots, handoff checklist, automations, and operating documentation.",
      target: "commercial-ops",
      cta: "Review Workflow Layer"
    },
    {
      title: "Dashboard MVP View",
      bestFor: "Teams evaluating dashboard design, MVP scope, user needs, and measurable reporting adoption.",
      whatToInspect: "Problem framing, users, MVP scope, dashboard metrics, backlog, and validation notes.",
      target: "product",
      cta: "Review Dashboard MVP Brief"
    }
  ];

  d.reviewerGuide = [
    {
      title: "Case Study Brief",
      note: "Start here for the two-minute summary of context, problem, solution, outputs, and limits for a CX analytics role.",
      target: "case-study"
    },
    {
      title: "Customer Segment Scoring",
      note: "Review the weighted scoring model, segment priorities, data-quality assumptions, and actionability logic.",
      target: "commercial-ops"
    },
    {
      title: "Journey Diagnostics",
      note: "Inspect workflow stages, bottleneck signals, service/dealer handoff needs, and recommended actions.",
      target: "commercial-ops"
    },
    {
      title: "Insight-to-Action Tracker",
      note: "Review stakeholder mapping, privacy guardrails, rollout phases, reporting focus, and follow-up KPIs.",
      target: "adoption"
    },
    {
      title: "Insight Brief Simulator",
      note: "See how a structured brief can turn approved data inputs into a human-reviewed customer insight summary.",
      target: "commercial-ops"
    },
    {
      title: "Reporting Guide",
      note: "Open the sample agenda, learning objectives, and slide outline for a CX analytics enablement session.",
      target: "training-material"
    },
    {
      title: "Methodology",
      note: "Check the simulated-data boundaries and non-production claims before reviewing the dashboard as evidence.",
      target: "methodology"
    }
  ];

  d.adoptionGovernance = {
    stakeholderMap: [
      {
        stakeholder: "Customer Experience team",
        need: "Reliable satisfaction views, clear segment priorities, and recurring trend visibility.",
        role: "Insight owner"
      },
      {
        stakeholder: "CRM / Marketing",
        need: "Segmented customer profiles, campaign feedback, and follow-up logic.",
        role: "Activation partner"
      },
      {
        stakeholder: "Dealer network / Retail operations",
        need: "Actionable feedback on follow-up, delivery, test ride, and service experience.",
        role: "Frontline process owner"
      },
      {
        stakeholder: "Service / After-sales",
        need: "Signals on appointment friction, warranty issues, and post-service satisfaction.",
        role: "Improvement owner"
      },
      {
        stakeholder: "Product / Digital teams",
        need: "Recurring customer pain points tied to app, configurator, connected services, or product feedback.",
        role: "Experience improvement partner"
      },
      {
        stakeholder: "Data / IT / Privacy",
        need: "Data quality, source clarity, access controls, and responsible handling of customer information.",
        role: "Data-quality and privacy enabler"
      }
    ],
    rolloutPlan: [
      {
        phase: "Discovery",
        goal: "Understand available survey, CRM, service, dealer, and digital touchpoint data.",
        output: "Data-source map, stakeholder notes, priority use cases, and customer journey stages."
      },
      {
        phase: "Prototype",
        goal: "Test a simulated reporting view with a small CX, CRM, and service stakeholder group.",
        output: "Feedback, missing metrics, data-quality notes, and refinement backlog."
      },
      {
        phase: "Reporting Routine",
        goal: "Define a repeatable cadence for dashboard review, insight notes, and action tracking.",
        output: "Weekly or monthly review template and owner list."
      },
      {
        phase: "Privacy Review",
        goal: "Validate customer-data boundaries, aggregation rules, and access responsibilities.",
        output: "Data-use checklist and escalation logic."
      },
      {
        phase: "Action Loop",
        goal: "Translate insights into improvement pilots and measure whether the customer signal changes.",
        output: "Action tracker, post-action KPI view, and lessons learned."
      }
    ],
    guardrails: [
      "Segment scoring should support prioritization, not replace human judgment about customers or dealers.",
      "Personal customer data should be minimized, aggregated where possible, and handled only through approved systems.",
      "Dashboard results should be checked for sample size, missing values, and survey bias before being shared as findings.",
      "Draft customer insight summaries should be clearly labeled as support material and reviewed by a human owner.",
      "Customer feedback should be used to improve processes, not to make unsupported individual-level assumptions.",
      "CRM, survey, and dealer data quality should be checked before comparing segments or journey stages.",
      "Unclear use of personal data should be escalated to Privacy, Legal, or Data/IT before any pilot."
    ],
    trainingPlan: [
      {
        audience: "Customer Experience team",
        timing: "Prototype onboarding + monthly refresh",
        focus: "How to interpret segment scores, trend signals, confidence limits, and recommended actions."
      },
      {
        audience: "CRM / Marketing",
        timing: "Before campaign or follow-up planning",
        focus: "How segments and satisfaction drivers can inform messaging, timing, and follow-up logic."
      },
      {
        audience: "Service / Dealer stakeholders",
        timing: "Pre-action workshop",
        focus: "How to read journey bottlenecks and translate them into practical process changes."
      },
      {
        audience: "Data / IT / Privacy",
        timing: "Before moving from prototype to real data",
        focus: "How source systems, access controls, aggregation, and responsible data-use checks are applied."
      }
    ],
    successMetrics: [
      "Weekly or monthly active users reviewing the CX cockpit.",
      "Percentage of segments reviewed with explicit data-source and sample-size notes.",
      "Reduction in unresolved recurring pain points across priority journey stages.",
      "Dashboard preparation time for CX reporting.",
      "Insight-to-action handoff completion rate.",
      "Number of improvement actions with a named owner and follow-up metric.",
      "Stakeholder satisfaction with reporting clarity.",
      "Percentage of draft insight summaries reviewed by a human before use."
    ],
    consultingDeliverables: [
      {
        deliverable: "Customer journey data map",
        purpose: "Understand where survey, CRM, dealer, service, and digital signals enter the workflow."
      },
      {
        deliverable: "Segment prioritization model",
        purpose: "Rank customer groups by satisfaction impact, data confidence, and actionability."
      },
      {
        deliverable: "Customer Data Quality & Privacy Checklist",
        purpose: "Define aggregation, privacy, human review, and escalation guardrails."
      },
      {
        deliverable: "Reporting guide",
        purpose: "Support consistent dashboard review by CX, CRM, service, and dealer stakeholders."
      },
      {
        deliverable: "Reporting guide",
        purpose: "Show how a workshop agenda and slide storyline would support consistent use of the reporting workflow."
      },
      {
        deliverable: "Action KPI tracker",
        purpose: "Measure whether insights turn into process changes and whether customer signals improve."
      }
    ]
  };

  d.trainingMaterial = {
    intro: "This reporting guide shows the kind of analyst-facing artifact I would prepare before a CX analytics reporting pilot: agenda, learning objectives, and a simple slide storyline focused on customer data, interpretation, and action follow-up.",
    workshopAgenda: [
      {
        slot: "0-10 min",
        topic: "Why this reporting workflow matters",
        purpose: "Align on customer satisfaction, journey friction, and what the team wants to improve."
      },
      {
        slot: "10-20 min",
        topic: "Data-source walkthrough",
        purpose: "Review survey, CRM, service, dealer, and digital signals plus known data-quality limits."
      },
      {
        slot: "20-35 min",
        topic: "Segment and trend interpretation",
        purpose: "Explain the scoring dimensions, trend flags, confidence limits, and how to avoid over-reading the data."
      },
      {
        slot: "35-50 min",
        topic: "Insight-to-action review",
        purpose: "Walk through one simulated segment brief and decide which team should own the next action."
      },
      {
        slot: "50-60 min",
        topic: "Cadence and follow-up",
        purpose: "Confirm reporting owners, action tracker fields, review cadence, and next data-quality checks."
      }
    ],
    learningObjectives: [
      "Explain the target customer journey workflow and where analytics supports decision-making.",
      "Recognize data-quality limits such as sample size, missing values, bias, and fragmented sources.",
      "Use the insight brief simulator as structured support material rather than as an automatic conclusion.",
      "Identify the minimum data, owner, and success-metric conditions required before an improvement pilot proceeds.",
      "Leave the session with clear follow-up actions, owners, and adoption metrics."
    ],
    slideOutline: [
      {
        title: "Slide 1 - Customer journey context",
        points: [
          "Which customer moments are being monitored",
          "Where friction appears today",
          "What success looks like in customer and operational terms"
        ]
      },
      {
        title: "Slide 2 - Data sources and quality limits",
        points: [
          "Which inputs are approved",
          "What data is missing or inconsistent",
          "How sample size and bias are documented"
        ]
      },
      {
        title: "Slide 3 - Segment scoring and trend logic",
        points: [
          "Which dimensions drive prioritization",
          "How scores are interpreted",
          "Which signals require human validation"
        ]
      },
      {
        title: "Slide 4 - From insight to action",
        points: [
          "How to write an action-ready finding",
          "Who owns follow-up",
          "Which metric should change after the action"
        ]
      },
      {
        title: "Slide 5 - Reporting cadence and next steps",
        points: [
          "Immediate actions after the workshop",
          "Who owns dashboard refresh and notes",
          "Which adoption KPIs will be monitored first"
        ]
      }
    ]
  };

  d.automationLayer = {
    title: "Customer Experience Follow-up Workflows",
    subtitle: "How customer signals could trigger follow-up, owner assignment, and reporting routines.",
    description: "This section demonstrates how operational signals from the cockpit could be connected to no-code or low-code tools to reduce manual follow-up and make insight-to-action tracking more consistent.",
    workflows: [
      {
        platform: "Power Automate / Zapier",
        name: "Low-Satisfaction Segment Alert",
        trigger: "A priority segment drops below the satisfaction threshold",
        conditions: ["Weighted score >= 4.0", "Satisfaction trend negative", "Sample size above minimum threshold"],
        action: "Notify CX owner and create an action-tracker item with segment, driver, and target follow-up date",
        delay: "Same day",
        value: "Turns recurring customer pain points into assigned review actions instead of passive dashboard observations."
      },
      {
        platform: "n8n / Make",
        name: "Dealer Follow-Up Digest",
        trigger: "Weekly review cycle",
        conditions: ["Dealer-related feedback exists", "Open action items > 0", "Owner assigned"],
        action: "Send a digest to dealer operations with top signals, affected journey stages, and unresolved actions",
        delay: "Weekly",
        value: "Improves visibility across central CX and frontline retail teams."
      },
      {
        platform: "Power Automate",
        name: "Privacy Review Check",
        trigger: "A new customer data source is proposed",
        conditions: ["Personal data involved", "Aggregation method unclear", "Access owner not named"],
        action: "Route a checklist to Data/IT/Privacy before the source is used in reporting",
        delay: "Before pilot use",
        value: "Keeps customer-data handling explicit before the workflow moves beyond a prototype."
      },
      {
        platform: "n8n / Zapier",
        name: "Action Pilot Reminder",
        trigger: "An improvement action is created",
        conditions: ["Due date approaching", "Follow-up metric missing or stale"],
        action: "Remind the action owner to update status, metric, and evidence notes",
        delay: "48h before due date",
        value: "Closes the loop between insight generation and measurable process improvement."
      },
      {
        platform: "Copilot Studio",
        name: "Post-Workshop FAQ Assistant",
        trigger: "Stakeholder asks how to read a dashboard signal",
        conditions: ["Approved reporting guidance available", "Escalation route to CX owner defined"],
        action: "Answer routine interpretation questions and escalate ambiguous data or privacy questions to a human owner",
        delay: "On demand",
        value: "Supports adoption while keeping interpretation and data-use decisions human-reviewed."
      }
    ],
    toolNote: "These workflows are designed for no-code or low-code tooling such as Power Automate, n8n, Make, Zapier, and Copilot Studio. They require approved data sources, clear owners, and privacy checks before real customer data is used."
  };

  d.productBrief = {
    problemStatement: "Customer Experience teams need a structured way to combine survey, CRM, dealer, service, and digital signals into clear dashboards, customer segments, trend explanations, and action tracking.",
    targetUsers: [
      {
        user: "Customer Experience analyst",
        need: "Organize fragmented customer signals into recurring reports and action-ready findings."
      },
      {
        user: "CX manager",
        need: "Identify high-priority customer segments, recurring pain points, and owners for improvement actions."
      },
      {
        user: "CRM / Marketing stakeholder",
        need: "Understand which customer profiles or journey moments should influence follow-up strategy."
      },
      {
        user: "Service / Dealer operations",
        need: "Receive clear, specific feedback signals that can be translated into process changes."
      },
      {
        user: "Data / Privacy reviewer",
        need: "See source assumptions, aggregation logic, and responsible data-use boundaries."
      }
    ],
    userStories: [
      "As a CX analyst, I want to identify recurring satisfaction drivers by segment so that I can prepare clearer reporting notes.",
      "As a CX manager, I want to see which customer groups need attention so that I can prioritize improvement actions.",
      "As a CRM stakeholder, I want segment-level insight so that follow-up campaigns are better matched to customer context.",
      "As a service or dealer stakeholder, I want specific journey signals so that operational teams can act on the right friction points.",
      "As a data or privacy reviewer, I want clear guardrails so that customer information is handled responsibly."
    ],
    mvpScope: {
      inScope: [
        "Simulated customer segment data and scoring model.",
        "Journey-stage overview and weighted insight volume.",
        "Trend diagnosis and action handoff checklist.",
        "Customer insight brief simulator.",
        "Privacy-aware data-use checklist.",
        "Static frontend prototype for portfolio review."
      ],
      outOfScope: [
        "Live Ducati, CRM, dealer, or survey-system integration.",
        "Individual customer profiling or automated customer decisions.",
        "Production authentication, access controls, or data pipelines.",
        "Real Power BI deployment.",
        "Legal privacy assessment."
      ]
    },
    productMetrics: [
      "Dashboard review cadence completion.",
      "Weekly usage by role.",
      "Percentage of segments with data-source and sample-size notes.",
      "Insight-to-action handoff completion rate.",
      "Time from trend detection to owner assignment.",
      "Number of actions with post-action measurement.",
      "Stakeholder satisfaction with report clarity."
    ],
    backlog: [
      {
        priority: "High",
        feature: "Power BI-style report export",
        reason: "Aligns the prototype with common reporting workflows for Data Analyst roles."
      },
      {
        priority: "High",
        feature: "Data-quality panel",
        reason: "Shows missing values, sample size, source freshness, and confidence notes before conclusions are drawn."
      },
      {
        priority: "Medium",
        feature: "Segment drill-down",
        reason: "Allows reviewers to inspect how satisfaction, behavior, and journey stage differ across customer groups."
      },
      {
        priority: "Medium",
        feature: "Action tracker history",
        reason: "Connects insight generation to process improvement and follow-up measurement."
      },
      {
        priority: "Low",
        feature: "CRM or survey mock integration",
        reason: "Would make the data flow more realistic without requiring confidential data."
      }
    ],
    researchNotes: [
      {
        method: "Job Requirement Mapping",
        finding: "The target internship asks for data collection, organization, analysis, reporting, customer segmentation, and clear communication.",
        impact: "Led to a CX analytics version focused on dashboarding, segment prioritization, trend diagnosis, and action handoff."
      },
      {
        method: "Customer Journey Framing",
        finding: "A premium brand experience depends on multiple touchpoints: discovery, purchase, delivery, service, digital support, and loyalty.",
        impact: "Led to journey-stage logic and customer segment categories instead of a sales-only pipeline."
      },
      {
        method: "Responsible Data-Use Review",
        finding: "Customer analytics must handle privacy, aggregation, sample size, and interpretation limits carefully.",
        impact: "Led to explicit guardrails, data-use checks, and simulated-data methodology notes."
      }
    ],
    businessMetrics: [
      { productMetric: "Dashboard preparation time", businessImpact: "Faster recurring CX reporting" },
      { productMetric: "Insight-to-action handoff completion", businessImpact: "More consistent ownership of improvement actions" },
      { productMetric: "Segment trend detection", businessImpact: "Earlier identification of recurring journey friction" },
      { productMetric: "Post-action measurement", businessImpact: "Clearer link between analytics and customer experience improvement" }
    ],
    decisionLog: [
      {
        decision: "Keep data simulated",
        reason: "The project must demonstrate analysis and communication without using confidential customer information."
      },
      {
        decision: "Use customer segments instead of individual customers",
        reason: "Segment-level analysis is more appropriate for portfolio work and supports privacy-aware framing."
      },
      {
        decision: "Keep the original static architecture",
        reason: "The goal is to demonstrate analytical reasoning and dashboard structure, not to overbuild a backend."
      },
      {
        decision: "Prioritize Power BI and data-quality improvements in the backlog",
        reason: "Those additions would make the prototype even closer to a Data Analyst Customer Experience internship."
      }
    ]
  };

  d.scoringMethodology = {
    formula: "CX Fit Score = Satisfaction Impact x 30% + Customer Priority x 20% + Data Complexity x 15% + Owner Clarity x 15% + Reporting Fit x 10% + Actionability x 10%",
    scale: `Each variable is scored from 1 to 5.
The final score is a weighted average on the same 1-5 scale.`,
    dimensions: [
      {
        key: "useCaseValue",
        label: "Satisfaction Impact",
        weight: 30,
        definition: "1 = weak or unclear CX signal. 5 = clear high-impact segment or journey issue with measurable customer value."
      },
      {
        key: "regulatoryUrgency",
        label: "Customer Priority",
        weight: 20,
        definition: "1 = low urgency or small segment. 5 = high-value segment, visible journey moment, or recurring dissatisfaction risk."
      },
      {
        key: "dataComplexity",
        label: "Data Complexity",
        weight: 15,
        definition: "1 = simple source and clean fields. 5 = multi-source feedback, CRM, service, dealer, and digital context."
      },
      {
        key: "stakeholderClarity",
        label: "Owner Clarity",
        weight: 15,
        definition: "1 = no clear business owner. 5 = CX, CRM, service, dealer, or product owner is clear."
      },
      {
        key: "deploymentFit",
        label: "Reporting Fit",
        weight: 10,
        definition: "1 = low reporting value. 5 = strong fit for dashboards, segmentation, and recurring trend review."
      },
      {
        key: "procurementFeasibility",
        label: "Actionability",
        weight: 10,
        definition: "1 = unclear next action. 5 = realistic improvement owner, action path, and follow-up metric."
      }
    ]
  };

  d.pipelineStages = [
    { name: "Data Source Identified", probability: 0.10 },
    { name: "Data Cleaned", probability: 0.20 },
    { name: "Segment Analysis", probability: 0.35 },
    { name: "Satisfaction Reporting", probability: 0.50 },
    { name: "Journey Diagnosis", probability: 0.65 },
    { name: "Improvement Backlog", probability: 0.75 },
    { name: "Action Pilot", probability: 0.85 },
    { name: "Action Completed", probability: 1.00 },
    { name: "CX Handoff", probability: 1.00 }
  ];

  d.accounts = [
    {
      id: 1,
      company: "New Ducati Owner Onboarding",
      type: "Simulated customer segment",
      sector: "Owner Onboarding",
      useCasePotential: "First 30-day satisfaction analysis, delivery feedback, and onboarding friction detection",
      regulatorySensitivity: "Medium",
      dataComplexityLabel: "High",
      decisionMakers: "Customer Experience, CRM, dealer operations",
      reason: "The first ownership period shapes long-term loyalty and gives a clear window for satisfaction measurement and proactive follow-up.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 4, stakeholderClarity: 5, deploymentFit: 5, procurementFeasibility: 4 }
    },
    {
      id: 2,
      company: "Multistrada Touring Customers",
      type: "Simulated customer segment",
      sector: "Loyalty",
      useCasePotential: "Segment long-distance owner feedback by service needs, accessories, community, and post-trip support",
      regulatorySensitivity: "Low",
      dataComplexityLabel: "Medium",
      decisionMakers: "CX, product marketing, after-sales",
      reason: "Touring customers generate rich feedback across usage, service, accessories, and brand community touchpoints.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 4, dataComplexity: 4, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 4 }
    },
    {
      id: 3,
      company: "Panigale Performance Owners",
      type: "Simulated customer segment",
      sector: "Premium Owners",
      useCasePotential: "Analyze premium-owner satisfaction, expectations, technical support needs, and post-delivery experience",
      regulatorySensitivity: "Low",
      dataComplexityLabel: "Medium",
      decisionMakers: "CX, product, dealer network",
      reason: "Premium customers are highly valuable and expect precise, responsive, technically credible support.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 3, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 3 }
    },
    {
      id: 4,
      company: "Scrambler First-Time Riders",
      type: "Simulated customer segment",
      sector: "Owner Onboarding",
      useCasePotential: "Profile new rider needs, confidence-building content, dealer education, and early ownership questions",
      regulatorySensitivity: "Low",
      dataComplexityLabel: "Medium",
      decisionMakers: "CRM, CX, training, dealer operations",
      reason: "Newer riders may need clearer onboarding, support content, and tailored communication after purchase.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 4, dataComplexity: 3, stakeholderClarity: 4, deploymentFit: 4, procurementFeasibility: 5 }
    },
    {
      id: 5,
      company: "Service Appointment Journey",
      type: "Simulated customer journey",
      sector: "Service",
      useCasePotential: "Identify friction in booking, reminders, wait time, service explanation, and post-service satisfaction",
      regulatorySensitivity: "Medium",
      dataComplexityLabel: "High",
      decisionMakers: "After-sales, dealer operations, CX",
      reason: "Service interactions are frequent, measurable, and strongly linked to repeat loyalty and dealer perception.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 5, stakeholderClarity: 5, deploymentFit: 5, procurementFeasibility: 4 }
    },
    {
      id: 6,
      company: "Warranty Claim Journey",
      type: "Simulated customer journey",
      sector: "Service",
      useCasePotential: "Analyze complaint themes, resolution time, communication clarity, and customer sentiment after claims",
      regulatorySensitivity: "Medium",
      dataComplexityLabel: "High",
      decisionMakers: "After-sales, legal/privacy, dealer operations",
      reason: "Warranty experiences can create dissatisfaction if communication, timing, or ownership is unclear.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 3 }
    },
    {
      id: 7,
      company: "Digital Configurator Leads",
      type: "Simulated customer segment",
      sector: "Digital",
      useCasePotential: "Connect configurator behavior to test ride requests, lead quality, drop-off, and follow-up timing",
      regulatorySensitivity: "Medium",
      dataComplexityLabel: "High",
      decisionMakers: "Digital, CRM, sales operations",
      reason: "Digital behavior can indicate intent, but needs careful organization before it becomes useful for CX and CRM teams.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 4, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 4 }
    },
    {
      id: 8,
      company: "Test Ride Participants",
      type: "Simulated customer segment",
      sector: "Events",
      useCasePotential: "Measure post-event satisfaction, follow-up quality, conversion blockers, and brand perception",
      regulatorySensitivity: "Low",
      dataComplexityLabel: "Medium",
      decisionMakers: "Events, CRM, dealer network",
      reason: "Test rides are a clear moment to capture customer expectations, objections, and follow-up quality.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 4, dataComplexity: 3, stakeholderClarity: 4, deploymentFit: 4, procurementFeasibility: 5 }
    },
    {
      id: 9,
      company: "App and Connected Services Users",
      type: "Simulated customer segment",
      sector: "Digital",
      useCasePotential: "Analyze app feedback, feature usage, support requests, and digital satisfaction trends",
      regulatorySensitivity: "Medium",
      dataComplexityLabel: "High",
      decisionMakers: "Digital product, CX, data/IT",
      reason: "Digital services generate recurring signals that can be translated into product and support improvements.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 4, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 4 }
    },
    {
      id: 10,
      company: "Dealer Follow-Up Experience",
      type: "Simulated customer journey",
      sector: "Dealer Network",
      useCasePotential: "Compare follow-up timing, response quality, and customer satisfaction after inquiry or delivery",
      regulatorySensitivity: "Low",
      dataComplexityLabel: "Medium",
      decisionMakers: "Dealer operations, CRM, CX",
      reason: "Follow-up quality is highly actionable and can be reviewed without needing a complex technical system.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 5, dataComplexity: 3, stakeholderClarity: 5, deploymentFit: 4, procurementFeasibility: 5 }
    },
    {
      id: 11,
      company: "Accessories and Apparel Customers",
      type: "Simulated customer segment",
      sector: "Retail",
      useCasePotential: "Analyze accessory purchase patterns, satisfaction with availability, and post-purchase support",
      regulatorySensitivity: "Low",
      dataComplexityLabel: "Medium",
      decisionMakers: "Retail, e-commerce, CRM",
      reason: "Retail touchpoints create useful signals for loyalty, personalization, and service expectations.",
      scoreComponents: { useCaseValue: 3, regulatoryUrgency: 3, dataComplexity: 3, stakeholderClarity: 4, deploymentFit: 3, procurementFeasibility: 5 }
    },
    {
      id: 12,
      company: "Lapsed Service Customers",
      type: "Simulated customer segment",
      sector: "Retention",
      useCasePotential: "Profile customers who stop using official service channels and identify retention opportunities",
      regulatorySensitivity: "Medium",
      dataComplexityLabel: "High",
      decisionMakers: "After-sales, CRM, dealer network",
      reason: "Lapsed service behavior can signal satisfaction gaps, price concerns, convenience issues, or weak follow-up.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 4, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 3 }
    },
    {
      id: 13,
      company: "Pre-Owned and Trade-In Prospects",
      type: "Simulated customer segment",
      sector: "Retail",
      useCasePotential: "Analyze decision drivers, financing questions, dealer response time, and satisfaction by prospect type",
      regulatorySensitivity: "Medium",
      dataComplexityLabel: "Medium",
      decisionMakers: "Retail, CRM, dealer network",
      reason: "Trade-in and pre-owned paths involve multiple decision points and can benefit from clearer profiling.",
      scoreComponents: { useCaseValue: 4, regulatoryUrgency: 3, dataComplexity: 4, stakeholderClarity: 3, deploymentFit: 4, procurementFeasibility: 4 }
    },
    {
      id: 14,
      company: "VIP and Repeat Owners",
      type: "Simulated customer segment",
      sector: "Premium Owners",
      useCasePotential: "Monitor loyalty drivers, event satisfaction, exclusive services, and high-value owner expectations",
      regulatorySensitivity: "Low",
      dataComplexityLabel: "Medium",
      decisionMakers: "CX, brand, CRM, events",
      reason: "Repeat and premium owners are valuable for loyalty, advocacy, and brand perception.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 4, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 4 }
    },
    {
      id: 15,
      company: "International Visitors and Tourists",
      type: "Simulated customer segment",
      sector: "Events",
      useCasePotential: "Profile museum, factory, or event visitor satisfaction and language/support needs",
      regulatorySensitivity: "Low",
      dataComplexityLabel: "Medium",
      decisionMakers: "Events, customer care, brand experience",
      reason: "International visitors can reveal service, language, and brand-experience improvement opportunities.",
      scoreComponents: { useCaseValue: 3, regulatoryUrgency: 3, dataComplexity: 3, stakeholderClarity: 4, deploymentFit: 3, procurementFeasibility: 4 }
    },
    {
      id: 16,
      company: "Post-Delivery Detractors",
      type: "Simulated customer segment",
      sector: "Owner Onboarding",
      useCasePotential: "Detect recurring low-NPS themes after delivery and assign recovery actions",
      regulatorySensitivity: "Medium",
      dataComplexityLabel: "High",
      decisionMakers: "CX, dealer operations, CRM, privacy",
      reason: "Early detractor signals are high priority because they affect satisfaction, loyalty, referrals, and brand trust.",
      scoreComponents: { useCaseValue: 5, regulatoryUrgency: 5, dataComplexity: 5, stakeholderClarity: 4, deploymentFit: 5, procurementFeasibility: 4 }
    }
  ];

  d.pipelineDeals = [
    { id: "CX1", accountId: 1, stage: "Satisfaction Reporting", value: 42000, daysInStage: 8, pocReadiness: 74, risk: "Sample size", nextStep: "Validate first 30-day survey coverage and add dealer delivery notes." },
    { id: "CX2", accountId: 2, stage: "Journey Diagnosis", value: 36000, daysInStage: 12, pocReadiness: 68, risk: "Data linkage", nextStep: "Connect service feedback with touring-use segment notes." },
    { id: "CX3", accountId: 3, stage: "Segment Analysis", value: 18000, daysInStage: 6, pocReadiness: 54, risk: "Expectation gap", nextStep: "Separate delivery feedback from product-support requests." },
    { id: "CX4", accountId: 4, stage: "Improvement Backlog", value: 28000, daysInStage: 5, pocReadiness: 71, risk: "Content ownership", nextStep: "Assign onboarding content owner and define follow-up metric." },
    { id: "CX5", accountId: 5, stage: "Action Pilot", value: 61000, daysInStage: 16, pocReadiness: 82, risk: "Dealer process", nextStep: "Test appointment reminder and post-service explanation template." },
    { id: "CX6", accountId: 6, stage: "Journey Diagnosis", value: 24000, daysInStage: 18, pocReadiness: 63, risk: "Resolution timing", nextStep: "Map claim status fields and recurring communication gaps." },
    { id: "CX7", accountId: 7, stage: "Data Cleaned", value: 52000, daysInStage: 9, pocReadiness: 46, risk: "Attribution", nextStep: "Define the event path from configurator to lead follow-up." },
    { id: "CX8", accountId: 8, stage: "Action Completed", value: 17000, daysInStage: 2, pocReadiness: 91, risk: "None", nextStep: "Compare post-event follow-up satisfaction after the pilot." },
    { id: "CX9", accountId: 9, stage: "Satisfaction Reporting", value: 31000, daysInStage: 10, pocReadiness: 69, risk: "Digital source quality", nextStep: "Separate support tickets from feature feedback." },
    { id: "CX10", accountId: 10, stage: "Improvement Backlog", value: 47000, daysInStage: 7, pocReadiness: 77, risk: "Owner alignment", nextStep: "Assign dealer follow-up owner and target response-time metric." },
    { id: "CX11", accountId: 11, stage: "Data Source Identified", value: 14000, daysInStage: 4, pocReadiness: 31, risk: "Low priority", nextStep: "Confirm which retail touchpoint has enough sample size." },
    { id: "CX12", accountId: 12, stage: "Journey Diagnosis", value: 33000, daysInStage: 14, pocReadiness: 61, risk: "Retention logic", nextStep: "Check service-history completeness before segment conclusions." },
    { id: "CX13", accountId: 13, stage: "Segment Analysis", value: 21000, daysInStage: 11, pocReadiness: 57, risk: "Follow-up clarity", nextStep: "Map financing and trade-in questions by dealer response time." },
    { id: "CX14", accountId: 14, stage: "Satisfaction Reporting", value: 19000, daysInStage: 6, pocReadiness: 73, risk: "Small sample", nextStep: "Use qualitative notes alongside quantitative trend signals." },
    { id: "CX15", accountId: 15, stage: "Data Cleaned", value: 12000, daysInStage: 5, pocReadiness: 42, risk: "Language fields", nextStep: "Tag language and visit-type fields before analysis." },
    { id: "CX16", accountId: 16, stage: "Action Pilot", value: 26000, daysInStage: 13, pocReadiness: 84, risk: "Recovery ownership", nextStep: "Create recovery contact rule and post-action satisfaction check." }
  ];

  d.executiveInsights = [
    {
      title: "Service journey feedback has the clearest action path",
      signal: "Service appointment and warranty segments combine high satisfaction impact, high data complexity, and named after-sales owners.",
      risk: "If service feedback remains fragmented, recurring issues may be visible in comments but not converted into improvement actions.",
      action: "Create a service journey view with booking, reminder, wait-time, explanation, and post-service satisfaction fields.",
      impact: "Expected impact: clearer prioritization of after-sales improvements and faster owner assignment."
    },
    {
      title: "Digital behavior needs stronger source mapping",
      signal: "Configurator, app, and connected-services segments have high reporting value but depend on data linkage and source clarity.",
      risk: "Teams may confuse interest signals, support needs, and satisfaction feedback if the source taxonomy is weak.",
      action: "Separate lead behavior, support tickets, feature feedback, and satisfaction survey fields before trend reporting.",
      impact: "Expected impact: more reliable segmentation and clearer CRM follow-up logic."
    },
    {
      title: "Early ownership is a high-priority feedback window",
      signal: "New owner onboarding and post-delivery detractor segments show high satisfaction impact and strong actionability.",
      risk: "If early dissatisfaction is detected late, recovery actions may miss the moment when customer perception is still forming.",
      action: "Add a first 30-day owner view with delivery feedback, onboarding questions, dealer follow-up, and recovery status.",
      impact: "Expected impact: stronger retention signals and more timely customer recovery actions."
    }
  ];

  d.bottlenecks = [
    {
      stage: "Data Source Mapping",
      signal: "Feedback exists across surveys, CRM, service notes, dealer follow-up, and digital touchpoints.",
      cause: "Customer signals are collected in different systems and may use inconsistent labels or timing.",
      action: "Create a source map with owner, refresh cadence, field quality, and customer journey stage.",
      impact: "Improve reporting reliability before drawing segment conclusions."
    },
    {
      stage: "Journey Diagnosis",
      signal: "High-priority segments often need both quantitative survey signals and qualitative comment themes.",
      cause: "Scores alone do not explain whether the issue is timing, communication, product support, or dealer process.",
      action: "Pair dashboard metrics with structured insight notes and a human-reviewed theme summary.",
      impact: "Make findings easier to communicate and turn into actions."
    },
    {
      stage: "Action Follow-Up",
      signal: "Insight quality matters only if ownership and post-action measurement are clear.",
      cause: "Reports can be reviewed without a named action owner or target metric.",
      action: "Use an action handoff checklist with owner, due date, expected metric change, and next review date.",
      impact: "Close the loop between analytics and customer experience improvement."
    }
  ];

  d.stageExitCriteria = [
    {
      transition: "Data Source Identified -> Data Cleaned",
      criteria: [
        "Source owner is identified.",
        "Refresh cadence is known.",
        "Relevant customer journey stage is mapped.",
        "Personal-data boundaries are understood.",
        "Missing or inconsistent fields are logged."
      ]
    },
    {
      transition: "Data Cleaned -> Segment Analysis",
      criteria: [
        "Minimum sample size is checked.",
        "Segment definition is documented.",
        "Missing values and duplicates are handled.",
        "Survey or feedback bias is noted.",
        "First analysis question is explicit."
      ]
    },
    {
      transition: "Segment Analysis -> Satisfaction Reporting",
      criteria: [
        "Satisfaction trend is calculated.",
        "Primary driver hypothesis is documented.",
        "Comparison segment or baseline is available.",
        "Limitations are written in plain language.",
        "Reporting owner is assigned."
      ]
    },
    {
      transition: "Journey Diagnosis -> Improvement Backlog",
      criteria: [
        "Root-cause hypothesis is reviewed by a human owner.",
        "Affected touchpoint is clear.",
        "Business owner is named.",
        "Expected customer or operational metric is selected.",
        "Privacy or data-use questions are resolved."
      ]
    },
    {
      transition: "Action Pilot -> CX Handoff",
      criteria: [
        "Action owner and timeline are confirmed.",
        "Target metric and baseline are recorded.",
        "Follow-up reporting date is scheduled.",
        "Stakeholders know what evidence will be reviewed.",
        "Lessons learned will be added to the backlog."
      ]
    }
  ];

  d.handoffChecklist = [
    { title: "Customer segment clearly defined", desc: "The segment, journey stage, and source data are documented." },
    { title: "Satisfaction signal validated", desc: "Sample size, missing data, and trend direction are checked before conclusions are shared." },
    { title: "Primary driver hypothesis written", desc: "The likely cause is stated clearly and separated from confirmed facts." },
    { title: "Business owner named", desc: "A CX, CRM, service, dealer, product, or digital owner is assigned." },
    { title: "Action metric selected", desc: "The improvement has a measurable follow-up metric, not only a qualitative goal." },
    { title: "Data-use boundary checked", desc: "Personal data, aggregation, and access responsibilities are clear." },
    { title: "Follow-up cadence scheduled", desc: "The next review date and evidence source are documented." },
    { title: "Learning captured", desc: "Results are fed back into the segment model or reporting backlog." }
  ];

  d.complianceChecklist = [
    "Does the analysis involve personal customer data or identifiable dealer/customer notes?",
    "Can the finding be reported at aggregate or segment level instead of individual level?",
    "Is sample size large enough to support a dashboard conclusion?",
    "Are survey bias, missing values, duplicates, or stale fields documented?",
    "Is a human owner reviewing any draft customer insight summary before use?",
    "Who owns approval across CX, CRM, Data/IT, Privacy, and the business stakeholder?"
  ];
  d.complianceEscalationRule = "Escalation rule: If personal data use, unclear aggregation, or unknown source ownership appears, flag for Data/IT or Privacy review before using the source in reporting.";

  d.sectorBuyingDrivers = {
    "Owner Onboarding": "first 30-day satisfaction, delivery clarity, dealer follow-up, onboarding content, and early recovery actions",
    "Loyalty": "repeat ownership, service experience, community engagement, accessories, and long-term satisfaction",
    "Premium Owners": "high expectations, technical credibility, responsiveness, exclusive experience, and brand trust",
    "Service": "booking ease, communication clarity, wait time, repair explanation, and post-service satisfaction",
    "Digital": "app usability, configurator behavior, digital support, lead quality, and feature feedback",
    "Events": "test ride satisfaction, visitor experience, follow-up quality, language support, and brand perception",
    "Dealer Network": "response time, follow-up consistency, delivery quality, and frontline process improvement",
    "Retail": "availability, post-purchase support, cross-sell signals, and satisfaction by purchase type",
    "Retention": "service lapse reasons, convenience, pricing perception, relationship quality, and reactivation opportunities"
  };

  d.briefPromptStructure = [
    "Customer segment context",
    "Relevant journey touchpoints",
    "Primary satisfaction or behavior signal",
    "Likely data sources",
    "Data-quality and privacy questions",
    "Trend or friction hypothesis",
    "Recommended CX next action",
    "Action handoff notes"
  ];

  d.methodologySections = [
    {
      title: "What is simulated",
      items: [
        "Customer segments, feedback volumes, journey stages, trend signals, action readiness, and score components.",
        "Scores are illustrative and designed to show prioritization logic, not factual judgments about Ducati customers, dealers, or products.",
        "Insight briefs are generated from predefined structured data and simulated customer-experience assumptions."
      ]
    },
    {
      title: "What is based on job-relevant assumptions",
      items: [
        "The internship requires data collection, organization, analysis, reporting, segmentation, and clear communication.",
        "Customer Experience teams commonly work with surveys, CRM, service, dealer, digital, and campaign feedback.",
        "Responsible customer analytics requires privacy awareness, aggregation, source quality, and careful interpretation."
      ]
    },
    {
      title: "What the project demonstrates",
      items: [
        "Customer data workflow thinking and explicit stage criteria.",
        "Segment prioritization through a weighted scoring framework.",
        "Dashboard logic using total and weighted insight volume.",
        "Trend diagnostics: signals, likely causes, actions, and expected impact.",
        "CX-to-business handoff design and privacy-aware data qualification."
      ]
    },
    {
      title: "What the project is not",
      items: [
        "A production CX analytics system, a CRM integration, or a Power BI deployment.",
        "A representation of confidential Ducati customer data, internal surveys, or dealer information.",
        "A claim that Ducati uses or evaluates this specific solution."
      ]
    }
  ];
})();
