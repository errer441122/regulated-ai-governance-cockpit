(function () {
  "use strict";

  const data = window.cockpitData;

  const state = {
    chartInstances: []
  };

  const stageOrder = data ? data.pipelineStages.map(stage => stage.name) : [];
  const stageProbabilityMap = data ? Object.fromEntries(data.pipelineStages.map(stage => [stage.name, stage.probability])) : {};

  function byId(id) {
    return document.getElementById(id);
  }

  function formatCurrency(value, precision = 1) {
    if (value >= 1000000) return `€${(value / 1000000).toFixed(precision)}M`;
    return `€${Math.round(value / 1000)}k`;
  }

  function formatProbability(value) {
    return `${Math.round(value * 100)}%`;
  }

  function accountById(id) {
    return data.accounts.find(account => account.id === id);
  }

  function weightedFitScore(account) {
    const dimensions = data.scoringMethodology.dimensions;
    const totalWeight = dimensions.reduce((sum, dimension) => sum + dimension.weight, 0);
    const weightedTotal = dimensions.reduce((sum, dimension) => {
      return sum + (account.scoreComponents[dimension.key] || 0) * dimension.weight;
    }, 0);
    return weightedTotal / totalWeight;
  }

  function dealProbability(deal) {
    return stageProbabilityMap[deal.stage] || 0;
  }

  function weightedDealValue(deal) {
    return deal.value * dealProbability(deal);
  }

  function allPipelineValue() {
    return data.pipelineDeals.reduce((sum, deal) => sum + deal.value, 0);
  }

  function allWeightedPipelineValue() {
    return data.pipelineDeals.reduce((sum, deal) => sum + weightedDealValue(deal), 0);
  }

  function openDeals() {
    return data.pipelineDeals.filter(deal => !["Closed Won", "CS Handoff"].includes(deal.stage));
  }

  function average(values) {
    if (!values.length) return 0;
    return values.reduce((sum, value) => sum + value, 0) / values.length;
  }

  function stageAggregates() {
    return stageOrder.map(stage => {
      const deals = data.pipelineDeals.filter(deal => deal.stage === stage);
      const total = deals.reduce((sum, deal) => sum + deal.value, 0);
      const weighted = deals.reduce((sum, deal) => sum + weightedDealValue(deal), 0);
      const avgDays = deals.length ? average(deals.map(deal => deal.daysInStage)) : 0;
      return { stage, deals, total, weighted, avgDays, probability: stageProbabilityMap[stage] || 0 };
    });
  }

  function setText(id, value) {
    const element = byId(id);
    if (element) element.textContent = value;
  }

  function setFallbackMetrics() {
    document.querySelectorAll(".kpi-value, .metric-value").forEach(element => {
      if (element.textContent.trim() === "Loading...") {
        element.textContent = "Unavailable";
      }
    });
  }

  function renderKpis() {
    const total = allPipelineValue();
    const weighted = allWeightedPipelineValue();
    const avgStageAge = average(data.pipelineDeals.map(deal => deal.daysInStage));
    const avgPocReadiness = average(data.pipelineDeals.map(deal => deal.pocReadiness));
    const avgFit = average(data.accounts.map(account => weightedFitScore(account)));

    setText("kpi-total-pipeline", formatCurrency(total));
    setText("kpi-weighted-pipeline", formatCurrency(weighted));
    setText("kpi-accounts", String(data.accounts.length));
    setText("kpi-stage-age", `${avgStageAge.toFixed(1)} days`);
    setText("kpi-poc", `${Math.round(avgPocReadiness)}%`);

    setText("dashboard-total-pipeline", formatCurrency(total));
    setText("dashboard-weighted-pipeline", formatCurrency(weighted));
    setText("dashboard-open-opps", String(openDeals().length));
    setText("dashboard-fit-score", avgFit.toFixed(2));
  }

  function renderInsights() {
    const grid = byId("insights-grid");
    if (!grid) return;

    grid.innerHTML = data.executiveInsights.map((insight, index) => `
      <article class="glass-panel insight-card">
        <div class="eyebrow">Insight ${index + 1}</div>
        <h3>${insight.title}</h3>
        <p><strong>Observed signal:</strong> ${insight.signal}</p>
        <p><strong>Operational risk:</strong> ${insight.risk}</p>
        <p><strong>Recommended action:</strong> ${insight.action}</p>
        <p><strong>Expected impact:</strong> ${insight.impact.replace("Expected impact: ", "")}</p>
      </article>
    `).join("");
  }

  function renderReviewPaths() {
    const grid = byId("review-paths-grid");
    if (!grid || !Array.isArray(data.reviewPaths)) return;

    grid.innerHTML = data.reviewPaths.map(path => `
      <article class="glass-panel review-path-card">
        <div class="eyebrow">Review path</div>
        <h3>${path.title}</h3>
        <div class="review-path-meta">
          <span class="review-path-label">Best for</span>
          <p>${path.bestFor}</p>
        </div>
        <div class="review-path-meta">
          <span class="review-path-label">What to inspect</span>
          <p>${path.whatToInspect}</p>
        </div>
        <button class="jump-button review-path-button" type="button" data-nav-target="${path.target}">${path.cta}</button>
      </article>
    `).join("");
  }

  function renderReviewerGuide() {
    const container = byId("reviewer-guide-list");
    if (!container || !Array.isArray(data.reviewerGuide)) return;

    container.innerHTML = data.reviewerGuide.map((item, index) => `
      <article class="checklist-item checked reviewer-guide-item">
        <span class="check-indicator" aria-hidden="true"></span>
        <div class="reviewer-guide-copy">
          <strong>${index + 1}. ${item.title}</strong>
          <p>${item.note}</p>
          <button class="jump-button review-guide-button" type="button" data-nav-target="${item.target}">Open ${item.title}</button>
        </div>
      </article>
    `).join("");
  }

  function renderDecisionDemo() {
    const scenarios = data.demoScenarios || [];
    const accountList = byId("decision-demo-accounts");
    const gateRail = byId("decision-demo-gates");
    const prevButton = byId("decision-demo-prev");
    const nextButton = byId("decision-demo-next");

    if (!accountList || !gateRail || !scenarios.length) return;

    let scenarioIndex = 0;
    let gateIndex = 0;

    function activeScenario() {
      return scenarios[scenarioIndex];
    }

    function activeGate() {
      const scenario = activeScenario();
      return scenario.gates[gateIndex] || scenario.gates[0];
    }

    function accountForScenario(scenario) {
      return data.accounts.find(account => account.id === scenario.accountId);
    }

    function renderAccountButtons() {
      accountList.innerHTML = scenarios.map((scenario, index) => {
        const account = accountForScenario(scenario);
        return `
          <button class="decision-demo-account${index === scenarioIndex ? " active" : ""}" type="button" data-demo-index="${index}">
            <span>${scenario.label}</span>
            <strong>${account ? account.company : "Simulated account"}</strong>
          </button>
        `;
      }).join("");
    }

    function renderGateRail() {
      const scenario = activeScenario();
      gateRail.innerHTML = scenario.gates.map((gate, index) => `
        <button class="decision-gate${index === gateIndex ? " active" : ""}" type="button" data-gate-index="${index}">
          <span>${String(index + 1).padStart(2, "0")}</span>
          ${gate.name}
        </button>
      `).join("");
    }

    function updateDemo() {
      const scenario = activeScenario();
      const gate = activeGate();
      const account = accountForScenario(scenario);

      setText("decision-demo-sector", account ? account.sector : "Governance workflow");
      setText("decision-demo-gate-count", `Gate ${gateIndex + 1} of ${scenario.gates.length}`);
      setText("decision-demo-title", scenario.label);
      setText("decision-demo-context", scenario.context);
      setText("decision-demo-check", gate.check);
      setText("decision-demo-evidence", gate.evidence);
      setText("decision-demo-blocker", gate.blocker);
      setText("decision-demo-decision", gate.decision);
      setText("decision-demo-artifact", gate.artifact);

      renderAccountButtons();
      renderGateRail();

      if (prevButton) prevButton.disabled = gateIndex === 0;
      if (nextButton) nextButton.disabled = gateIndex === scenario.gates.length - 1;
    }

    accountList.addEventListener("click", event => {
      const button = event.target.closest("[data-demo-index]");
      if (!button) return;
      scenarioIndex = Number(button.getAttribute("data-demo-index"));
      gateIndex = 0;
      updateDemo();
    });

    gateRail.addEventListener("click", event => {
      const button = event.target.closest("[data-gate-index]");
      if (!button) return;
      gateIndex = Number(button.getAttribute("data-gate-index"));
      updateDemo();
    });

    if (prevButton) {
      prevButton.addEventListener("click", () => {
        gateIndex = Math.max(0, gateIndex - 1);
        updateDemo();
      });
    }

    if (nextButton) {
      nextButton.addEventListener("click", () => {
        gateIndex = Math.min(activeScenario().gates.length - 1, gateIndex + 1);
        updateDemo();
      });
    }

    updateDemo();
  }

  function renderStageProbabilities() {
    const container = byId("stage-probability-row");
    if (!container) return;

    container.innerHTML = data.pipelineStages.map(stage => `
      <div class="probability-pill">
        <span>${stage.name}</span>
        <strong>${formatProbability(stage.probability)}</strong>
      </div>
    `).join("");
  }

  function renderKanban() {
    const board = byId("kanban-board");
    if (!board) return;

    board.innerHTML = stageAggregates().map(group => `
      <section class="kanban-column">
        <div class="kanban-header">
          <span>${group.stage}</span>
          <small>${formatProbability(group.probability)} · ${formatCurrency(group.weighted, 2)} weighted</small>
        </div>
        <div class="kanban-cards">
          ${group.deals.length ? group.deals.map(deal => {
            const account = accountById(deal.accountId);
            return `
              <article class="kanban-card">
                <div class="card-title">${account ? account.company : "Unknown account"}</div>
                <div class="card-value">${formatCurrency(deal.value, 2)} <span>${formatCurrency(weightedDealValue(deal), 2)} weighted</span></div>
                <div class="card-meta">
                  <span><i class="fa-regular fa-clock"></i>${deal.daysInStage} days</span>
                  <span><i class="fa-solid fa-triangle-exclamation"></i>${deal.risk}</span>
                </div>
                <div class="card-next"><strong>Next:</strong> ${deal.nextStep}</div>
              </article>
            `;
          }).join("") : `<div class="empty-column">No simulated deals</div>`}
        </div>
      </section>
    `).join("");
  }

  function renderExitCriteria() {
    const container = byId("exit-criteria-grid");
    if (!container) return;

    container.innerHTML = data.stageExitCriteria.map(item => `
      <article class="glass-panel criteria-card">
        <h3>${item.transition}</h3>
        <ul>
          ${item.criteria.map(criterion => `<li>${criterion}</li>`).join("")}
        </ul>
      </article>
    `).join("");
  }

  function renderScoring() {
    const formula = byId("scoring-formula");
    const weights = byId("scoring-weights");
    const body = document.querySelector("#scoring-table tbody");
    if (!formula || !weights || !body) return;

    formula.textContent = data.scoringMethodology.formula;

    weights.innerHTML = data.scoringMethodology.dimensions.map(dimension => `
      <article class="weight-card">
        <div class="weight-value">${dimension.weight}%</div>
        <h4>${dimension.label}</h4>
        <p>${dimension.definition}</p>
      </article>
    `).join("");

    const sortedAccounts = [...data.accounts].sort((a, b) => weightedFitScore(b) - weightedFitScore(a));
    body.innerHTML = sortedAccounts.map(account => {
      const score = weightedFitScore(account);
      const components = data.scoringMethodology.dimensions.map(d => account.scoreComponents[d.key]).join(" / ");
      const badgeClass = account.regulatorySensitivity === "High" ? "badge-high" : account.regulatorySensitivity === "Medium" ? "badge-medium" : "badge-low";

      return `
        <tr>
          <td><strong>${account.company}</strong><br><small>${account.type}</small></td>
          <td>${account.sector}</td>
          <td><span class="badge ${badgeClass}">${account.regulatorySensitivity}</span></td>
          <td>${account.dataComplexityLabel}</td>
          <td><strong>${score.toFixed(2)}</strong></td>
          <td><span class="mono">${components}</span></td>
          <td>${account.useCasePotential}</td>
        </tr>
      `;
    }).join("");
  }

  function renderBriefSimulator() {
    const select = byId("account-select");
    const generateBtn = byId("generate-brief");
    const output = byId("brief-output");
    const promptList = byId("brief-prompt-structure");
    if (!select || !generateBtn || !output || !promptList) return;

    select.innerHTML = `<option value="">Select target account</option>` + data.accounts
      .map(account => `<option value="${account.id}">${account.company} · ${account.sector}</option>`)
      .join("");

    promptList.innerHTML = data.briefPromptStructure.map(item => `<li>${item}</li>`).join("");

    generateBtn.addEventListener("click", () => {
      const selectedId = Number(select.value);
      const account = accountById(selectedId);
      if (!account) {
        output.innerHTML = `<div class="empty-state">Select an account to generate the structured simulator output.</div>`;
        return;
      }

      const score = weightedFitScore(account);
      const sectorDriver = data.sectorBuyingDrivers[account.sector] || "regulated enterprise governance and measurable workflow improvement";
      const topRisks = [];
      if (account.scoreComponents.procurementFeasibility <= 2) topRisks.push("procurement complexity");
      if (account.scoreComponents.stakeholderClarity <= 3) topRisks.push("incomplete stakeholder coverage");
      if (account.scoreComponents.deploymentFit >= 4) topRisks.push("deployment and security review");
      if (!topRisks.length) topRisks.push("scope clarity before PoC");

      output.innerHTML = `
        <article class="brief-card">
          <div class="brief-header">
            <div>
              <div class="eyebrow">LLM-assisted simulator output</div>
              <h3>${account.company}</h3>
            </div>
            <div class="brief-score">Fit ${score.toFixed(2)}</div>
          </div>

          <section>
            <h4>Account context</h4>
            <p>${account.reason}</p>
          </section>

          <section>
            <h4>Likely buying drivers</h4>
            <p>For ${account.sector}, likely buying drivers include ${sectorDriver}. The commercial conversation should connect the AI use case to measurable workflow improvement and governance readiness.</p>
          </section>

          <section>
            <h4>Potential AI use case</h4>
            <p>${account.useCasePotential}. The goal should be scoped as an assisted workflow with clear human oversight and a measurable PoC acceptance criterion.</p>
          </section>

          <section>
            <h4>Stakeholders to involve</h4>
            <p>${account.decisionMakers}. Add IT/Security, Compliance or Privacy, Procurement, and a business sponsor before moving past Discovery.</p>
          </section>

          <section>
            <h4>Discovery questions</h4>
            <ul>
              <li>Which workflow would create the clearest measurable business value within a 6–10 week pilot?</li>
              <li>Which data sources would be required, and who owns access approval?</li>
              <li>What auditability, logging, human oversight, or deployment constraints must be satisfied?</li>
              <li>Which stakeholder has budget ownership and which team controls vendor risk review?</li>
            </ul>
          </section>

          <section>
            <h4>Commercial risks</h4>
            <p>${topRisks.join(", ")}. These should be captured as CRM risks before PoC resources are committed.</p>
          </section>

          <section>
            <h4>Recommended CRM next step</h4>
            <p>Move only when the next stage exit criteria are satisfied: business pain, owner, data path, compliance sensitivity, and success metric must be explicit.</p>
          </section>

          <section>
            <h4>Sales-to-CS handoff notes</h4>
            <p>Document the target workflow, data owner, technical owner, success metric, governance constraints, and first milestone before handoff.</p>
          </section>
        </article>
      `;
    });
  }

  function renderPlaybook() {
    const handoff = byId("handoff-checklist");
    const compliance = byId("compliance-checklist");
    if (!handoff || !compliance) return;

    handoff.innerHTML = data.handoffChecklist.map((item, index) => `
      <li class="checklist-item ${index < 3 ? "checked" : ""}">
        <span class="check-indicator"></span>
        <div>
          <strong>${item.title}</strong>
          <p>${item.desc}</p>
        </div>
      </li>
    `).join("");

    compliance.innerHTML = data.complianceChecklist.map(item => `
      <li class="checklist-item">
        <span class="check-indicator muted"></span>
        <div><p>${item}</p></div>
      </li>
    `).join("");
  }

  function renderBottlenecks() {
    const body = document.querySelector("#bottlenecks-table tbody");
    if (!body) return;

    body.innerHTML = data.bottlenecks.map(item => `
      <tr>
        <td><strong>${item.stage}</strong></td>
        <td>${item.signal}</td>
        <td>${item.cause}</td>
        <td>${item.action}</td>
        <td>${item.impact}</td>
      </tr>
    `).join("");
  }

  function renderCaseStudy() {
    const caseStudy = data.caseStudy;
    if (!caseStudy) return;

    setText("case-study-summary", data.project.oneLineSummary);
    setText("case-study-context", caseStudy.context);
    setText("case-study-problem", caseStudy.problem);
    setText("case-study-solution", caseStudy.solution);
    setText("case-study-role", caseStudy.role);
    setText("case-study-value", caseStudy.businessValue);
    setText("case-study-limitations", caseStudy.limitations);
    setText("case-study-next-iteration", caseStudy.nextIteration);

    const outputs = byId("case-study-outputs");
    if (outputs) {
      outputs.innerHTML = caseStudy.outputs.map(item => `
        <article class="glass-panel output-card">
          <p>${item}</p>
        </article>
      `).join("");
    }
  }

  function renderAdoption() {
    const adoption = data.adoptionGovernance;
    if (!adoption) return;

    const stakeholderBody = document.querySelector("#stakeholder-table tbody");
    const rolloutBody = document.querySelector("#rollout-table tbody");
    const deliverablesBody = document.querySelector("#deliverables-table tbody");
    const guardrails = byId("guardrails-list");
    const training = byId("training-list");
    const metrics = byId("adoption-metrics");

    if (stakeholderBody) {
      stakeholderBody.innerHTML = adoption.stakeholderMap.map(item => `
        <tr>
          <td><strong>${item.stakeholder}</strong></td>
          <td>${item.need}</td>
          <td>${item.role}</td>
        </tr>
      `).join("");
    }

    if (rolloutBody) {
      rolloutBody.innerHTML = adoption.rolloutPlan.map(item => `
        <tr>
          <td><strong>${item.phase}</strong></td>
          <td>${item.goal}</td>
          <td>${item.output}</td>
        </tr>
      `).join("");
    }

    if (deliverablesBody) {
      deliverablesBody.innerHTML = adoption.consultingDeliverables.map(item => `
        <tr>
          <td><strong>${item.deliverable}</strong></td>
          <td>${item.purpose}</td>
        </tr>
      `).join("");
    }

    if (guardrails) {
      guardrails.innerHTML = adoption.guardrails.map(item => `
        <li class="checklist-item">
          <span class="reference-kicker">Guardrail</span>
          <p>${item}</p>
        </li>
      `).join("");
    }

    if (training) {
      training.innerHTML = adoption.trainingPlan.map(item => `
        <li class="checklist-item">
          <span class="reference-kicker">Timing: ${item.timing}</span>
          <div>
            <strong>${item.audience}</strong>
            <p>${item.focus}</p>
          </div>
        </li>
      `).join("");
    }

    if (metrics) {
      metrics.innerHTML = adoption.successMetrics.map(item => `
        <article class="glass-panel output-card">
          <p>${item}</p>
        </article>
      `).join("");
    }
  }

  function renderTrainingMaterial() {
    const trainingMaterial = data.trainingMaterial;
    if (!trainingMaterial) return;

    setText("training-material-intro", trainingMaterial.intro);

    const agendaBody = document.querySelector("#training-agenda-table tbody");
    const objectives = byId("learning-objectives-list");
    const slides = byId("slide-outline-grid");

    if (agendaBody) {
      agendaBody.innerHTML = trainingMaterial.workshopAgenda.map(item => `
        <tr>
          <td><strong>${item.slot}</strong></td>
          <td>${item.topic}</td>
          <td>${item.purpose}</td>
        </tr>
      `).join("");
    }

    if (objectives) {
      objectives.innerHTML = trainingMaterial.learningObjectives.map(item => `
        <li class="checklist-item checked">
          <span class="check-indicator"></span>
          <div><p>${item}</p></div>
        </li>
      `).join("");
    }

    if (slides) {
      slides.innerHTML = trainingMaterial.slideOutline.map(item => `
        <article class="glass-panel output-card">
          <h3>${item.title}</h3>
          <ul class="training-slide-points">
            ${item.points.map(point => `<li>${point}</li>`).join("")}
          </ul>
        </article>
      `).join("");
    }
  }

  function renderProductBrief() {
    const product = data.productBrief;
    if (!product) return;

    setText("product-problem", product.problemStatement);

    const userBody = document.querySelector("#users-table tbody");
    const stories = byId("user-stories");
    const scopeIn = byId("scope-in");
    const scopeOut = byId("scope-out");
    const metrics = byId("product-metrics");
    const backlog = document.querySelector("#backlog-table tbody");
    const decisionLog = document.querySelector("#decision-log-table tbody");

    if (userBody) {
      userBody.innerHTML = product.targetUsers.map(item => `
        <tr>
          <td><strong>${item.user}</strong></td>
          <td>${item.need}</td>
        </tr>
      `).join("");
    }

    if (stories) {
      stories.innerHTML = product.userStories.map(item => `
        <article class="glass-panel story-card">
          <p>${item}</p>
        </article>
      `).join("");
    }

    if (scopeIn) {
      scopeIn.innerHTML = product.mvpScope.inScope.map(item => `
        <li class="checklist-item checked">
          <span class="check-indicator"></span>
          <div><p>${item}</p></div>
        </li>
      `).join("");
    }

    if (scopeOut) {
      scopeOut.innerHTML = product.mvpScope.outOfScope.map(item => `
        <li class="checklist-item">
          <span class="check-indicator muted"></span>
          <div><p>${item}</p></div>
        </li>
      `).join("");
    }

    if (metrics) {
      metrics.innerHTML = product.productMetrics.map(item => `
        <li class="checklist-item">
          <span class="check-indicator"></span>
          <div><p>${item}</p></div>
        </li>
      `).join("");
    }

    if (backlog) {
      backlog.innerHTML = product.backlog.map(item => `
        <tr>
          <td><span class="priority-pill priority-${item.priority.toLowerCase()}">${item.priority}</span></td>
          <td><strong>${item.feature}</strong></td>
          <td>${item.reason}</td>
        </tr>
      `).join("");
    }

    if (decisionLog) {
      decisionLog.innerHTML = product.decisionLog.map(item => `
        <tr>
          <td><strong>${item.decision}</strong></td>
          <td>${item.reason}</td>
        </tr>
      `).join("");
    }
  }

  function renderAutomations() {
    const grid = byId("workflow-grid");
    const toolNote = byId("automation-tool-note");
    const automation = data.automationLayer;
    if (!automation || !grid) return;

    grid.innerHTML = automation.workflows.map(flow => `
      <article class="workflow-card">
        <div class="workflow-header">
          <div>
            <h3>${flow.name}</h3>
            ${flow.platform ? `<div class="workflow-platform">${flow.platform}</div>` : ""}
          </div>
          <span class="workflow-trigger">${flow.trigger}</span>
        </div>
        <div class="workflow-section-title">Conditions</div>
        <ul class="workflow-conditions">
          ${flow.conditions.map(c => `<li>${c}</li>`).join("")}
        </ul>
        <div class="workflow-action">
          <strong>Action:</strong> ${flow.action} <span style="color:var(--muted)">· ${flow.delay}</span>
        </div>
        <div class="workflow-value"><strong>Value:</strong> ${flow.value}</div>
      </article>
    `).join("");

    if (toolNote) toolNote.textContent = automation.toolNote;
  }

  function renderResearchNotes() {
    const grid = byId("research-grid");
    const product = data.productBrief;
    if (!grid || !product || !product.researchNotes) return;

    grid.innerHTML = product.researchNotes.map(note => `
      <article class="research-card">
        <div class="research-method">${note.method}</div>
        <h3>Key Finding</h3>
        <p>${note.finding}</p>
        <div class="research-impact"><strong>Impact on product:</strong> ${note.impact}</div>
      </article>
    `).join("");
  }

  function renderBusinessMetrics() {
    const body = document.querySelector("#business-metrics-table tbody");
    const product = data.productBrief;
    if (!body || !product || !product.businessMetrics) return;

    body.innerHTML = product.businessMetrics.map(item => `
      <tr>
        <td><strong>${item.productMetric}</strong></td>
        <td>${item.businessImpact}</td>
      </tr>
    `).join("");
  }

  function initPdfExport() {
    const btn = byId("export-governance-pdf");
    if (!btn) return;

    btn.addEventListener("click", () => {
      const { jsPDF } = window.jspdf;
      if (!jsPDF) {
        alert("PDF library not loaded. Please try again later.");
        return;
      }

      const doc = new jsPDF({ unit: "pt", format: "a4" });
      const pageWidth = doc.internal.pageSize.getWidth();
      const margin = 40;
      const maxContentY = 720;
      let y = 50;
      const ensurePageSpace = (neededHeight = 0) => {
        if (y + neededHeight > maxContentY) {
          doc.addPage();
          y = 50;
        }
      };

      // Header
      doc.setFillColor(7, 9, 20);
      doc.rect(0, 0, pageWidth, 80, "F");
      doc.setTextColor(42, 211, 167);
      doc.setFontSize(10);
      doc.text("AI & DATA GOVERNANCE", margin, 32);
      doc.setTextColor(255, 255, 255);
      doc.setFontSize(20);
      doc.text("Governance Checklist", margin, 58);

      y = 100;
      doc.setTextColor(100, 100, 100);
      doc.setFontSize(9);
      doc.text("Regulated AI & Data Governance Cockpit | Portfolio Case Study", margin, y);

      y += 22;
      doc.setTextColor(60, 60, 60);
      doc.text("Document", margin, y);
      doc.setTextColor(30, 30, 30);
      doc.text("Governance Checklist - AI Commercial Ops", margin + 62, y);
      doc.setTextColor(60, 60, 60);
      doc.text("Version", pageWidth - 185, y);
      doc.setTextColor(30, 30, 30);
      doc.text("v1.0", pageWidth - 135, y);

      y += 16;
      doc.setTextColor(60, 60, 60);
      doc.text("Date", margin, y);
      doc.setTextColor(30, 30, 30);
      doc.text("April 2026", margin + 62, y);
      doc.setTextColor(60, 60, 60);
      doc.text("Owner", pageWidth - 185, y);
      doc.setTextColor(30, 30, 30);
      doc.text("Riccardo Capanna", pageWidth - 135, y);

      y += 16;
      doc.setTextColor(60, 60, 60);
      doc.text("Status", margin, y);
      doc.setTextColor(30, 30, 30);
      doc.text("Draft / For Review", margin + 62, y);

      y += 26;
      doc.setTextColor(30, 30, 30);
      doc.setFontSize(10);
      doc.text("This document summarizes the governance guardrails, human oversight requirements, and operational risk boundaries designed for AI-enabled workflows in regulated organizations.", margin, y, { maxWidth: pageWidth - margin * 2 });

      y += 55;
      doc.setFontSize(13);
      doc.setTextColor(7, 9, 20);
      doc.text("Guardrails", margin, y);
      y += 18;

      const guardrails = data.adoptionGovernance.guardrails;
      doc.setFontSize(10);
      guardrails.forEach((g, i) => {
        doc.setTextColor(42, 211, 167);
        doc.text(`${i + 1}.`, margin, y);
        doc.setTextColor(50, 50, 50);
        doc.text(g, margin + 18, y, { maxWidth: pageWidth - margin * 2 - 18 });
        const lines = doc.splitTextToSize(g, pageWidth - margin * 2 - 18).length;
        y += lines * 14 + 10;
        if (y > maxContentY) {
          doc.addPage();
          y = 50;
        }
      });

      y += 20;
      doc.setFontSize(13);
      doc.setTextColor(7, 9, 20);
      doc.text("Compliance Qualification Checklist", margin, y);
      y += 18;

      const checklist = data.complianceChecklist;
      const checklistIndexWidth = doc.getTextWidth(`${checklist.length}.`);
      const checklistTextX = margin + checklistIndexWidth + 12;
      const checklistTextWidth = pageWidth - margin - checklistTextX;
      doc.setFontSize(10);
      checklist.forEach((item, i) => {
        doc.setTextColor(81, 122, 255);
        doc.text(`${i + 1}.`, margin, y);
        doc.setTextColor(50, 50, 50);
        doc.text(item, checklistTextX, y, { maxWidth: checklistTextWidth });
        const checklistLines = doc.splitTextToSize(item, checklistTextWidth).length;
        y += checklistLines * 14 + 10;
        if (y > maxContentY) {
          doc.addPage();
          y = 50;
        }
      });

      const escalationRule = data.complianceEscalationRule;
      const escalationLines = doc.splitTextToSize(escalationRule, pageWidth - margin * 2 - 20);
      ensurePageSpace(escalationLines.length * 12 + 34);
      doc.setFillColor(248, 243, 231);
      doc.roundedRect(margin, y, pageWidth - margin * 2, escalationLines.length * 12 + 22, 8, 8, "F");
      doc.setTextColor(120, 88, 32);
      doc.setFontSize(9);
      doc.text(escalationLines, margin + 10, y + 15);
      y += escalationLines.length * 12 + 34;

      y += 25;
      ensurePageSpace(110);
      doc.setFontSize(13);
      doc.setTextColor(7, 9, 20);
      doc.text("Training Plan Summary", margin, y);
      y += 18;

      const training = data.adoptionGovernance.trainingPlan;
      const trainingLabelWidth = 170;
      const trainingGutter = 24;
      const trainingLabelRightX = margin + trainingLabelWidth;
      const trainingFocusX = trainingLabelRightX + trainingGutter;
      const trainingFocusWidth = pageWidth - margin - trainingFocusX;
      doc.setFontSize(10);
      training.forEach(t => {
        ensurePageSpace(48);
        doc.setTextColor(7, 9, 20);
        doc.setFont(undefined, "bold");
        doc.text(t.audience, trainingLabelRightX, y, { align: "right" });
        doc.setFontSize(8);
        doc.setFont(undefined, "normal");
        doc.setTextColor(120, 120, 120);
        doc.text(t.timing, trainingLabelRightX, y + 11, { align: "right" });
        doc.setFontSize(10);
        doc.setFont(undefined, "normal");
        doc.setTextColor(80, 80, 80);
        doc.text(t.focus, trainingFocusX, y, { maxWidth: trainingFocusWidth });
        const lines = doc.splitTextToSize(t.focus, trainingFocusWidth).length;
        y += Math.max(lines * 14, 24) + 10;
        if (y > maxContentY) {
          doc.addPage();
          y = 50;
        }
      });

      // Footer
      const totalPages = doc.internal.getNumberOfPages();
      for (let i = 1; i <= totalPages; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(150, 150, 150);
        doc.text(`Page ${i} of ${totalPages} | Regulated AI & Data Governance Cockpit | Case Study`, margin, 810);
        doc.text("Simulated data | Not a legal compliance tool", pageWidth - margin, 810, { align: "right" });
      }

      doc.save("Governance_Checklist_AI_Data_Governance_Cockpit.pdf");
    });
  }

  function renderMethodology() {
    const container = byId("methodology-grid");
    if (!container) return;

    container.innerHTML = data.methodologySections.map(section => `
      <article class="glass-panel methodology-card">
        <h3>${section.title}</h3>
        <ul>
          ${section.items.map(item => `<li>${item}</li>`).join("")}
        </ul>
      </article>
    `).join("");
  }

  function chartFallback() {
    document.querySelectorAll(".chart-container").forEach(container => {
      container.innerHTML = `<div class="chart-fallback">Charts require Chart.js. The underlying values are still rendered in the KPI cards and tables.</div>`;
    });
  }

  function resetCharts() {
    state.chartInstances.forEach(chart => chart.destroy());
    state.chartInstances = [];
  }

  function renderCharts() {
    if (typeof Chart === "undefined") {
      chartFallback();
      return;
    }

    resetCharts();
    Chart.defaults.color = "rgba(180, 189, 208, 0.72)";
    Chart.defaults.font.family = "Inter, Arial, sans-serif";

    const aggregates = stageAggregates();

    state.chartInstances.push(new Chart(byId("pipelineChart"), {
      type: "bar",
      data: {
        labels: aggregates.map(item => item.stage),
        datasets: [
          {
            label: "Total pipeline (€M)",
            data: aggregates.map(item => Number((item.total / 1000000).toFixed(2))),
            backgroundColor: "rgba(212, 168, 83, 0.55)",
            borderColor: "rgba(212, 168, 83, 1)",
            borderWidth: 1,
            borderRadius: 6
          },
          {
            label: "Weighted pipeline (€M)",
            data: aggregates.map(item => Number((item.weighted / 1000000).toFixed(2))),
            backgroundColor: "rgba(199, 91, 58, 0.45)",
            borderColor: "rgba(199, 91, 58, 1)",
            borderWidth: 1,
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true, ticks: { callback: value => `€${value}M` } },
          x: { ticks: { maxRotation: 45, minRotation: 0 } }
        },
        plugins: { legend: { labels: { boxWidth: 12 } } }
      }
    }));

    const sectors = data.accounts.reduce((acc, account) => {
      acc[account.sector] = (acc[account.sector] || 0) + 1;
      return acc;
    }, {});

    state.chartInstances.push(new Chart(byId("sectorChart"), {
      type: "doughnut",
      data: {
        labels: Object.keys(sectors),
        datasets: [{
          data: Object.values(sectors),
          backgroundColor: [
            "rgba(212, 168, 83, 0.85)",
            "rgba(199, 91, 58, 0.75)",
            "rgba(180, 140, 80, 0.7)",
            "rgba(160, 100, 60, 0.7)",
            "rgba(120, 80, 50, 0.7)",
            "rgba(100, 120, 160, 0.6)",
            "rgba(180, 189, 208, 0.5)"
          ],
          borderWidth: 0
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, cutout: "68%" }
    }));

    state.chartInstances.push(new Chart(byId("daysChart"), {
      type: "line",
      data: {
        labels: aggregates.map(item => item.stage),
        datasets: [{
          label: "Average days in current stage",
          data: aggregates.map(item => Number(item.avgDays.toFixed(1))),
          borderColor: "rgba(212, 168, 83, 1)",
          backgroundColor: "rgba(212, 168, 83, 0.12)",
          fill: true,
          tension: 0.35,
          pointRadius: 4
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
    }));

    const topAccounts = [...data.accounts]
      .map(account => ({ ...account, score: weightedFitScore(account) }))
      .sort((a, b) => b.score - a.score)
      .slice(0, 8);

    state.chartInstances.push(new Chart(byId("fitChart"), {
      type: "bar",
      data: {
        labels: topAccounts.map(account => account.company),
        datasets: [{
          label: "Weighted fit score",
          data: topAccounts.map(account => Number(account.score.toFixed(2))),
          backgroundColor: "rgba(212, 168, 83, 0.5)",
          borderColor: "rgba(212, 168, 83, 1)",
          borderWidth: 1,
          borderRadius: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: "y",
        scales: { x: { beginAtZero: true, max: 5 } }
      }
    }));
  }

  function initNavigation() {
    const navItems = document.querySelectorAll(".nav-item");
    const jumpButtons = document.querySelectorAll("[data-nav-target]");
    const sections = document.querySelectorAll(".view-section");
    const headerTitle = byId("current-view-title");

    function activateSection(targetId) {
      const targetNav = [...navItems].find(item => item.getAttribute("data-target") === targetId);
      navItems.forEach(nav => nav.classList.toggle("active", nav === targetNav));
      sections.forEach(section => section.classList.toggle("active", section.id === targetId));
      if (headerTitle && targetNav) headerTitle.textContent = targetNav.textContent.trim();
      if (targetId === "commercial-ops") window.requestAnimationFrame(renderCharts);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    navItems.forEach(item => {
      item.addEventListener("click", () => activateSection(item.getAttribute("data-target")));
    });

    jumpButtons.forEach(button => {
      button.addEventListener("click", () => activateSection(button.getAttribute("data-nav-target")));
    });
  }

  function init() {
    if (!data) {
      console.error("cockpitData was not loaded. Check data.js for syntax or loading errors.");
      setFallbackMetrics();
      return;
    }

    setText("project-title", data.project.title);
    setText("project-subtitle", data.project.subtitle);
    setText("project-positioning", data.project.positioning);
    setText("hero-review-line", data.project.heroReviewLine);
    setText("project-disclaimer", data.project.disclaimer);
    setText("header-subtitle", data.project.headerSubtitle);
    setText("profile-label", data.project.profileLabel);
    setText("cta-demo", data.project.demoCta);
    setText("cta-cockpit", data.project.cockpitCta);
    setText("cta-adoption", data.project.adoptionCta);
    setText("cta-product", data.project.productCta);
    setText("scoring-disclaimer", data.project.scoringDisclaimer);
    setText("scoring-scale", data.scoringMethodology.scale);

    renderReviewPaths();
    renderReviewerGuide();
    renderDecisionDemo();
    initNavigation();
    renderKpis();
    renderInsights();
    renderStageProbabilities();
    renderKanban();
    renderExitCriteria();
    renderScoring();
    renderBriefSimulator();
    renderPlaybook();
    renderBottlenecks();
    renderCaseStudy();
    renderAutomations();
    renderAdoption();
    renderTrainingMaterial();
    renderProductBrief();
    renderResearchNotes();
    renderBusinessMetrics();
    initPdfExport();
    renderMethodology();
  }

  document.addEventListener("DOMContentLoaded", () => {
    try {
      init();
    } catch (error) {
      console.error("Cockpit initialization failed.", error);
      setFallbackMetrics();
      chartFallback();
    }
  });
})();
