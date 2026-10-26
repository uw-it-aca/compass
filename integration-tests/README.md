# Deployed Integration Tests

Standalone Playwright runner for deployed Compass test, not local builds.
Each app owns its suite. Visits UI tests and its verification workflow belong
to the Compass Visits repository, including any Compass staff interaction needed
to complete that workflow. Other apps are normally treated as data sources.
No browser requests, APIs, databases, or GCS are mocked. The default read-only
smoke test establishes authenticated UI/API access. The opt-in staff visit test
exercises the Compass-to-Visits lifecycle through the Compass UI; neither test
exercises every upstream service, including GCS.

## Setup

Requires Node 20+, a graphical desktop for login, and network access to
`https://test.compass.uw.edu`. From this directory:

```bash
npm install
npx playwright install chromium
npm run check
```

If Playwright reports missing OS libraries, follow its platform prerequisites.
No application containers or local server are needed.

## Sign In And Run

```bash
npm run auth
npm test
```

Complete SAML/MFA yourself in the opened browser, then press Enter in the
terminal once the app loads. No passwords are collected by the runner.
Use an authorized adviser for Compass. Each login uses a fresh browser context.
Cookie presence is only a heuristic; smoke tests verify actual app access.

State is saved separately under ignored `.auth/`, with directory permissions
700 and file permissions 600. It is a credential: never commit, upload, or share
it. Delete `.auth/` to remove local saved credentials; this does not revoke the
server sessions. Repeat login when sessions expire. Missing state files require
login first. Authentication redirects or API authorization failures require
checking login/access before diagnosing an integration regression.

```bash
npm run test:headed
npm test -- --project=compass
npm test -- --list
```

Only the Compass test host is an initial navigation target. Normal SAML
redirects are allowed. Tests run serially without retries.

## Staff Visit Lifecycle

Run the opt-in mutation scenario against deployed Compass test:

```bash
npm run test:visits -- --headed
```

This uses `/ic-dashboard` (the current IC visits UI route) and requires an
authorized manager session with write access, without a read-only user override.
Ordinary `npm test` and `npm run test:headed` still run only the read-only smoke.
Running bare `npx playwright test` runs all projects, including this mutation.

The student is configured in ignored `local-settings.json` beside this guide,
using the key `visitStudentNetid`. The designated synthetic student has already
been configured locally. Do not commit the file or move its value into a test.
On a new machine create this file with your approved synthetic student's NetID.

The test searches through the UI, requires existing IC eligibility and no active
or pending visit, selects a currently offered program/tutoring/course or writing
service, and creates the check-in through the UI. It checks the returned ID in
the live active list and checks the student's row is visible. If the deployed
version requires verification, it clicks Verify on that row first; otherwise it
proceeds directly to Check Out. It asserts the exact visit leaves the active
list and has a checkout timestamp. History is retained, not deleted.

If the test fails after creation, it attempts authenticated API verification
(if needed) and checkout of only the visit it created. Cleanup failure requires
manual review before retrying. The original workflow error remains the failure.
A crash or a lost create response may prevent cleanup; never blindly rerun or
clear another session's active visit. Do not run this workflow concurrently from
multiple machines for the same student. Prerequisite failures are failures, not
silent skips. Missing options or eligibility must be resolved outside the test;
the test never clicks Approve or changes eligibility.

## Live Data Strategy

- Never hardcode NetIDs, names, student numbers, or record IDs in scenarios.
- Smoke tests use the logged-in user's normal UI requests and assert response
  structure and stable UI labels, not identities, counts, eligibility, hours,
  or history. An empty caseload is valid.
- Later tests can use existing service API clients to discover authorized
  candidates by capability, and obtain expected values at runtime. Keep
  identifiers in memory and limit discovery to the authorized test scope.
- Prefer an independent source of truth: comparing UI to its own backing API
  verifies rendering but cannot detect a shared backend defect. A cross-app
  check should compare the source visit with its synchronized representation.
- Data can change between reads. Recheck prerequisites, compare stable fields
  where possible, and use bounded polling for documented eventual consistency.
  Missing suitable data is a distinct prerequisite outcome, never a silent pass.
- Python service clients would need a separate, authorized helper/environment;
  browser SAML sessions do not supply service credentials. Do not export large
  datasets to fixtures, copy production secrets locally, or print helper output.
- Do not randomly select real students or mutate discovered records. Mutation
  tests need an approved identity/data lifecycle and explicit opt-in.
- Screenshots, video, and traces are disabled. Do not log bodies or identifiers.
  Errors can still include sensitive URLs/page text; treat terminal output and
  ignored `test-results/` as sensitive. Do not upload raw artifacts to CI without
  a reviewed redaction/access policy.

## Future Pipeline

The same scenarios can run headlessly in GitHub Actions or another runner.
First establish approved authentication, data prerequisites, network access,
artifact handling, and readiness/version checks for both deployed apps.
There is deliberately no automated login bypass or workflow in this starter.
