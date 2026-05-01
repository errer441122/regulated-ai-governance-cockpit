const candidates = [
  {
    id: "WF-006",
    sector: "Research infrastructure",
    useCase: "AI workload intake triage",
    score: "4.55",
    status: "controlled_pilot_ready"
  },
  {
    id: "WF-003",
    sector: "Financial services",
    useCase: "Regulatory reporting checklist",
    score: "4.20",
    status: "prepare_then_pilot"
  },
  {
    id: "WF-011",
    sector: "Customer analytics",
    useCase: "Feedback insight brief",
    score: "4.15",
    status: "prepare_then_pilot"
  },
  {
    id: "WF-012",
    sector: "Climate",
    useCase: "Forecast dataset metadata assistant",
    score: "4.50",
    status: "controlled_pilot_ready"
  },
  {
    id: "WF-009",
    sector: "Healthcare",
    useCase: "Research cohort documentation assistant",
    score: "4.00",
    status: "prepare_then_pilot"
  }
];

const table = document.querySelector("#candidate-table");

table.innerHTML = candidates.map(candidate => `
  <tr>
    <td>${candidate.id}</td>
    <td>${candidate.sector}</td>
    <td>${candidate.useCase}</td>
    <td>${candidate.score}</td>
    <td><span class="badge ${candidate.status === "controlled_pilot_ready" ? "" : "warn"}">${candidate.status.replaceAll("_", " ")}</span></td>
  </tr>
`).join("");
