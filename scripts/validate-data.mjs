import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");
const dataPath = path.join(rootDir, "data.js");

const source = fs.readFileSync(dataPath, "utf8");
const html = fs.readFileSync(path.join(rootDir, "index.html"), "utf8");
const appSource = fs.readFileSync(path.join(rootDir, "app.js"), "utf8");
const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(source, sandbox, { filename: "data.js" });

const data = sandbox.window.cockpitData;
const errors = [];

function assert(condition, message) {
  if (!condition) errors.push(message);
}

function assertNonEmptyString(value, message) {
  assert(typeof value === "string" && value.trim().length > 0, message);
}

function assertNonEmptyArray(value, message) {
  assert(Array.isArray(value) && value.length > 0, message);
}

function collectAttributeValues(sourceText, attribute) {
  return [...sourceText.matchAll(new RegExp(`${attribute}="([^"]+)"`, "g"))].map(match => match[1]);
}

assert(data && typeof data === "object", "cockpitData was not loaded from data.js");

if (data) {
  const dimensions = data.scoringMethodology?.dimensions ?? [];
  const accounts = data.accounts ?? [];
  const deals = data.pipelineDeals ?? [];
  const stages = data.pipelineStages ?? [];
  const stageExitCriteria = data.stageExitCriteria ?? [];
  const trainingMaterial = data.trainingMaterial ?? {};
  const demoScenarios = data.demoScenarios ?? [];
  const sectionIds = new Set(collectAttributeValues(html, "id"));
  const navTargets = new Set([
    ...collectAttributeValues(html, "data-target"),
    ...collectAttributeValues(html, "data-nav-target")
  ]);

  const dimensionKeys = new Set(dimensions.map(dimension => dimension.key));
  const accountIds = new Set(accounts.map(account => account.id));
  const stageNames = new Set(stages.map(stage => stage.name));
  const stageProbability = new Map(stages.map(stage => [stage.name, stage.probability]));

  assertNonEmptyArray(data.reviewPaths, "reviewPaths must not be empty");
  assertNonEmptyArray(data.reviewerGuide, "reviewerGuide must not be empty");
  assertNonEmptyArray(data.adoptionGovernance?.guardrails, "adoption guardrails must not be empty");
  assertNonEmptyArray(data.methodologySections, "methodologySections must not be empty");
  assertNonEmptyArray(data.complianceChecklist, "complianceChecklist must not be empty");
  assertNonEmptyArray(demoScenarios, "demoScenarios must not be empty");
  assertNonEmptyArray(trainingMaterial.workshopAgenda, "trainingMaterial.workshopAgenda must not be empty");
  assertNonEmptyArray(trainingMaterial.learningObjectives, "trainingMaterial.learningObjectives must not be empty");
  assertNonEmptyArray(trainingMaterial.slideOutline, "trainingMaterial.slideOutline must not be empty");

  assert(
    dimensions.reduce((sum, dimension) => sum + (dimension.weight || 0), 0) === 100,
    "scoring weights must sum to 100%"
  );

  assert(new Set(accounts.map(account => account.id)).size === accounts.length, "account IDs must be unique");
  assert(new Set(deals.map(deal => deal.id)).size === deals.length, "deal IDs must be unique");
  assert(new Set(stages.map(stage => stage.name)).size === stages.length, "pipeline stage names must be unique");

  navTargets.forEach(target => {
    assert(sectionIds.has(target), `navigation target "${target}" does not match any section id`);
  });

  ["decision-demo", "decision-demo-accounts", "decision-demo-gates", "decision-demo-prev", "decision-demo-next"].forEach(id => {
    assert(sectionIds.has(id), `required decision demo element id "${id}" is missing from index.html`);
  });

  assert(appSource.includes("function renderDecisionDemo"), "app.js must define renderDecisionDemo");
  assert(appSource.includes("renderDecisionDemo();"), "app.js must call renderDecisionDemo during init");

  stages.forEach(stage => {
    assertNonEmptyString(stage.name, "each pipeline stage must have a name");
    assert(typeof stage.probability === "number" && stage.probability >= 0 && stage.probability <= 1, `stage "${stage.name}" must have a probability between 0 and 1`);
  });

  accounts.forEach(account => {
    assertNonEmptyString(account.company, `account ${account.id} must have a company`);
    assert(account.scoreComponents && typeof account.scoreComponents === "object", `account ${account.id} must have scoreComponents`);
    for (const key of dimensionKeys) {
      const value = account.scoreComponents?.[key];
      assert(typeof value === "number" && value >= 1 && value <= 5, `account ${account.id} is missing a valid score for "${key}"`);
    }
  });

  deals.forEach(deal => {
    assert(accountIds.has(deal.accountId), `deal ${deal.id} references missing account ${deal.accountId}`);
    assert(stageNames.has(deal.stage), `deal ${deal.id} uses unknown stage "${deal.stage}"`);
    assert(typeof deal.value === "number" && deal.value > 0, `deal ${deal.id} must have a positive value`);
    assert(typeof deal.pocReadiness === "number" && deal.pocReadiness >= 0 && deal.pocReadiness <= 100, `deal ${deal.id} must have pocReadiness between 0 and 100`);
    assertNonEmptyString(deal.risk, `deal ${deal.id} must have a risk label`);
    assertNonEmptyString(deal.nextStep, `deal ${deal.id} must have a nextStep`);
  });

  stageExitCriteria.forEach(item => {
    assertNonEmptyString(item.transition, "each stage exit criterion must declare a transition");
    assertNonEmptyArray(item.criteria, `transition "${item.transition}" must include criteria`);

    const normalized = item.transition
      .replace(/â†’/g, "->")
      .replace(/→/g, "->");
    const [fromStage, toStage] = normalized.split("->").map(part => part?.trim());

    assert(stageNames.has(fromStage), `transition "${item.transition}" references unknown start stage "${fromStage}"`);
    assert(stageNames.has(toStage), `transition "${item.transition}" references unknown end stage "${toStage}"`);
  });

  data.reviewPaths.forEach(pathItem => {
    assertNonEmptyString(pathItem.title, "each review path must have a title");
    assertNonEmptyString(pathItem.target, `review path "${pathItem.title}" must have a target`);
  });

  data.reviewerGuide.forEach(item => {
    assertNonEmptyString(item.title, "each reviewer guide item must have a title");
    assertNonEmptyString(item.note, `reviewer guide "${item.title}" must have a note`);
    assertNonEmptyString(item.target, `reviewer guide "${item.title}" must have a target`);
    assert(sectionIds.has(item.target), `reviewer guide "${item.title}" targets missing section "${item.target}"`);
  });

  data.reviewPaths.forEach(pathItem => {
    assert(sectionIds.has(pathItem.target), `review path "${pathItem.title}" targets missing section "${pathItem.target}"`);
  });

  demoScenarios.forEach(scenario => {
    assert(accountIds.has(scenario.accountId), `demo scenario "${scenario.label}" references missing account ${scenario.accountId}`);
    assertNonEmptyString(scenario.label, "each demo scenario must have a label");
    assertNonEmptyString(scenario.context, `demo scenario "${scenario.label}" must have context`);
    assert(Array.isArray(scenario.gates) && scenario.gates.length >= 3, `demo scenario "${scenario.label}" must have at least 3 gates`);
    scenario.gates.forEach(gate => {
      ["name", "check", "evidence", "blocker", "decision", "artifact"].forEach(key => {
        assertNonEmptyString(gate[key], `demo scenario "${scenario.label}" has a gate missing "${key}"`);
      });
    });
  });

  trainingMaterial.workshopAgenda?.forEach(item => {
    assertNonEmptyString(item.slot, "each training agenda item must have a slot");
    assertNonEmptyString(item.topic, `training agenda "${item.slot}" must have a topic`);
    assertNonEmptyString(item.purpose, `training agenda "${item.slot}" must have a purpose`);
  });

  trainingMaterial.slideOutline?.forEach(item => {
    assertNonEmptyString(item.title, "each training slide must have a title");
    assertNonEmptyArray(item.points, `training slide "${item.title}" must include points`);
  });

  const totalPipeline = deals.reduce((sum, deal) => sum + deal.value, 0);
  const weightedPipeline = deals.reduce((sum, deal) => sum + deal.value * (stageProbability.get(deal.stage) || 0), 0);

  assert(totalPipeline > 0, "total pipeline must be positive");
  assert(weightedPipeline > 0, "weighted pipeline must be positive");
  assert(weightedPipeline <= totalPipeline, "weighted pipeline cannot exceed total pipeline");

  if (!errors.length) {
    console.log(`Dataset validation passed: ${accounts.length} accounts, ${deals.length} deals, ${demoScenarios.length} decision demos.`);
    console.log(`Computed pipeline: total=${Math.round(totalPipeline)} weighted=${Math.round(weightedPipeline)}.`);
  }
}

if (errors.length) {
  console.error("Dataset validation failed:");
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  process.exit(1);
}
