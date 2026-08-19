# Managed Graph Database Benchmark

This repository benchmarks CognoDB Cloud and comparable managed graph databases using the same public graph, client machine, query shapes, and measurement code. It intentionally keeps credentials out of Git.

## What the assignment means

You must compare at least five platforms: CognoDB plus four others. For each platform you need the same dataset, a documented free or entry tier, the same region where possible, and the same client machine. The required evidence is load time and ingest rates; p50/p95 latency for 1-hop, 2-hop, 3-hop, point lookup, indexed/filtered lookup, and an aggregation; concurrent mixed read/write throughput; and observable resource footprint. Missing observability is reported as `not observable`, not guessed.

## Fast setup

1. Install Node.js 22 LTS from https://nodejs.org/ and restart VS Code.
2. Create a CognoDB account at https://console.cognodb.com/signup.
3. Create one free `c0` instance. Record its region, advertised CPU, RAM, disk, URI, and password. The password is shown once.
4. Create free or equivalent small instances for Neo4j AuraDB, Memgraph Cloud, and FalkorDB Cloud. A fifth platform is recommended for the assignment; add it only after its protocol and tier are documented. Do not compare a free CognoDB instance against a paid large instance.
5. In this folder run:

```powershell
npm install
Copy-Item .env.example .env
notepad .env
npm run download
```

6. Edit `.env` with one platform at a time. Never commit `.env`.
7. For each platform, run:

```powershell
$env:BENCHMARK_DB="cognodb"
npm run load
npm run benchmark
```

Repeat with `neo4j`, `memgraph`, and `falkordb`, then add the fifth adapter/account. Results are written to `results/<platform>.json`.

## Dataset and model

The runner downloads SNAP `soc-Slashdot0811`: https://snap.stanford.edu/data/soc-Slashdot0811.html. It parses the directed edge list into `Person` nodes with integer `id` and `FOLLOWS` relationships. The downloaded file contains **77,360 nodes** and **905,468 relationships**. This exceeds the required 100,000 relationships; verify actual footprint on every service before claiming it fits the selected tiers.

## Reproducibility settings

`ITERATIONS=100`, `CONCURRENCY=10`, and `BATCH_SIZE=1000` are defaults. Change them in `.env`, record the values, and use the same values for every platform. The runner performs five warm-up queries, then measures 100 queries per read workload and reports p50/p95. The mixed workload uses 10 concurrent clients and an 80% read / 20% write mix.

## Required final report

### CognoDB measured result

This is the first completed platform run. Values are from the client machine in the `us-east4` CognoDB region on 2026-08-19. The instance was the free `c0` tier: burst to 0.5 vCPU, 512 MB memory, 1 GiB storage, and up to 200 connections.

| Category | Workload | Iterations | p50 (ms) | p95 (ms) |
|---|---|---:|---:|---:|
| Traversal | 1-hop | 100 | 250.96 | 284.23 |
| Traversal | 2-hop | 100 | 251.04 | 272.97 |
| Traversal | 3-hop | 100 | 264.61 | 412.08 |
| Lookup | Point lookup | 100 | 251.83 | 286.89 |
| Lookup | Filtered lookup | 100 | 249.91 | 273.69 |
| Aggregation | Count persons | 100 | 250.08 | 284.07 |

| Load metric | Result |
|---|---:|
| Nodes loaded | 77,360 |
| Relationships loaded | 905,468 |
| Total load time | 370.94 s |
| Node ingest rate | 208.55 nodes/s |
| Relationship ingest rate | 2,440.98 relationships/s |
| Mixed workload | 34.04 queries/s |
| Mixed workload concurrency | 10 clients |
| Mixed workload mix | 80% reads / 20% writes |

The run used Node.js 22, the official `neo4j-driver` package, batch size 1,000, five warm-up requests, and 100 measured iterations per read workload. The benchmark output is saved in the ignored local file `results/cognodb.json`; regenerate it with `npm run benchmark` rather than committing credentials or unverifiable output.

### Interpretation and caveats

The connection and complete load succeeded. Read latency clustered around 250 ms, while the 3-hop p95 was higher at 412.08 ms, indicating more tail variance for deeper traversal. The mixed workload sustained 34.04 queries/s at 10 clients, but this is a single run and should not be treated as a platform ranking.

To keep the 512 MB free tier alive, 2-hop and 3-hop traversals use a documented fanout cap of 50 neighbors per hop (`TRAVERSAL_FANOUT=50`). These are bounded neighborhood traversals, not unrestricted path enumeration. Start nodes are randomly sampled. Repeat the run for every comparison platform with the same cap and settings. Resource usage after loading was not collected by the harness; use the provider console or report it as `not observable`.

Create the final comparison table below after running the other platforms. Do not fill missing cells with estimates.

| Platform | Load time | Nodes/s | Relationships/s | 1-hop p50/p95 | 2-hop p50/p95 | 3-hop p50/p95 | Point p50/p95 | Filtered p50/p95 | Aggregation p50/p95 | Mixed q/s |
|---|---:|---:|---:|---|---|---|---|---|---|---:|
| CognoDB | 370.94 s | 208.55 | 2,440.98 | 250.96 / 284.23 | 251.04 / 272.97 | 264.61 / 412.08 | 251.83 / 286.89 | 249.91 / 273.69 | 250.08 / 284.07 | 34.04 |
| Neo4j | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending |
| Memgraph | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending |
| FalkorDB | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending |
| Fifth platform | pending | pending | pending | pending | pending | pending | pending | pending | pending | pending |

Include date, client region, platform region, tier specs, driver version, Node version, dataset counts, batch size, iteration count, concurrency, and any query translation for every platform. Explain network variance, throttling, cold starts, timeouts, failed runs, and unobservable resources. Do not delete failed results; document them.

The current runner targets Bolt/Cypher-compatible services. If a selected fifth database does not expose Bolt, add a small adapter with the same method names and keep its query translation visible in the report. Do not claim a result was measured until the corresponding JSON file exists.

## Submission checklist

- [ ] Five platforms provisioned on comparable tiers and documented.
- [ ] Same dataset loaded into every platform.
- [ ] All required metrics measured, with p50 and p95 for latency metrics.
- [ ] `results/` files reviewed and copied into README tables.
- [ ] No passwords, URIs, or `.env` committed.
- [ ] README includes methodology, analysis, caveats, and reproduction commands.
- [ ] Repository pushed publicly, then email its URL to `hr@wexa.ai` with subject `CognoDB Assignment 1 - Your Name`.

The scaffold is an honest starting point, not a fabricated submission: you must provision the services, run it, inspect the output, and write the measured results and analysis.