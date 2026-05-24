# PROTECTION.md – Branch Protection Rules

## ClinicEase Online Doctor Appointment Booking System

---

## What is Branch Protection?

Branch protection rules in GitHub prevent direct pushes to critical branches and enforce quality gates before any code can be merged. For ClinicEase, the `main` branch is protected to ensure that only tested, reviewed code ever reaches the production-ready state.

---

## Branch Protection Rules Applied to `main`

### How to Set It Up on GitHub

1. Go to your repository on GitHub
2. Click **Settings** → **Branches**
3. Click **Add branch protection rule**
4. In "Branch name pattern" type: `main`
5. Enable the following options:

| Rule | Setting | Why |
|---|---|---|
| **Require a pull request before merging** | ✅ Enabled | No direct pushes to main — all changes go through a PR |
| **Require approvals** | 1 approval minimum | At least one reviewer must approve before merge |
| **Require status checks to pass** | ✅ Enabled | CI pipeline must pass before merge is allowed |
| **Require branches to be up to date** | ✅ Enabled | Branch must be current with main before merge |
| **Do not allow bypassing the above settings** | ✅ Enabled | Even administrators cannot bypass the rules |
| **Restrict who can push to matching branches** | ✅ Enabled | Only authorised collaborators can push |

### Status Checks to Require
After your first CI run, add these as required checks:
- `🧪 Run All Tests`
- `🔍 Code Quality Check`

---

## Why These Rules Matter

### 1. Protecting Code Quality
Without branch protection, any developer (or even a mistake) could push broken code directly to `main`. For ClinicEase, this means a patient could try to book an appointment on a broken system. The CI pipeline runs all 188 tests automatically — if even one fails, the merge is blocked.

### 2. Enforcing Code Review
The pull request review requirement ensures that at least one other person reads and approves every change before it reaches `main`. This catches logic errors, missing business rules, and security issues that automated tests might miss — for example, a reviewer might notice that a new endpoint is missing authentication.

### 3. Preventing Accidental Direct Pushes
Disabling direct pushes means that even if a developer runs `git push origin main` by accident, GitHub will reject it. All changes must go through a PR, which creates an audit trail of who changed what and why.

### 4. Ensuring the CI Pipeline Always Runs
By requiring status checks to pass, we guarantee that no merge can happen unless GitHub Actions has run the full test suite. This means:
- 69 creational pattern tests must pass
- 47 repository layer tests must pass
- 40 service layer tests must pass
- 32 REST API integration tests must pass
- All 188 tests green before any merge

### 5. Release Artifacts Are Trustworthy
Because the CD pipeline (artifact build) only runs after a merge to `main`, and merges to `main` require all tests to pass, every release artifact is guaranteed to come from tested, reviewed code. The wheel file attached to each GitHub Release can be trusted.

### 6. Industry Standard Practice
Branch protection with CI/CD is used by virtually every professional software team. It implements the Agile principle of continuous integration — integrating and testing code frequently to catch bugs early. For a healthcare system like ClinicEase, where incorrect appointment bookings or medication reminders could have real consequences, this level of quality control is not optional — it is essential.

---

## What Happens When a PR is Created

```
Developer creates PR → GitHub Actions triggers → All 188 tests run
         ↓                                              ↓
   Tests FAIL                                    Tests PASS
         ↓                                              ↓
  ❌ Merge blocked                         Reviewer notified for approval
  Error shown on PR                                    ↓
                                           Reviewer approves
                                                        ↓
                                           ✅ PR can be merged to main
                                                        ↓
                                           CD pipeline builds wheel artifact
                                                        ↓
                                           GitHub Release created automatically
```

---

## Screenshot Instructions

After setting up the rules, take a screenshot of:
1. **Settings → Branches** showing the protection rule on `main`
2. **A PR page** showing the required status checks (green ticks or red crosses)
3. **GitHub Actions tab** showing the CI pipeline runs

Save screenshots in the `screenshort/` folder of your repository.

---

*Document prepared by: Sithembiso Lungisani Mthembu | [222618698] | CPUT | May 2026*