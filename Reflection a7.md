# reflection.md – Lessons Learned in Template Selection and Kanban Customisation

## ClinicEase Online Doctor Appointment Booking System — Assignment 7

---

## Introduction

Setting up the GitHub Project board for ClinicEase taught me more about project management than I expected. What seemed like a straightforward task — pick a template and add some columns — turned into a process that required genuine decisions about workflow design, tool limitations, and the gap between theory and practice in Agile methodology.

---

## Challenge 1: Choosing the Right Template Without Prior Experience

The first challenge was evaluating GitHub's project templates without having used most of them in a real project before. The template names — Basic Kanban, Automated Kanban, Bug Triage, Team Planning — sound self-explanatory, but the actual differences only become clear when you look inside them and ask: *"Would this support the way ClinicEase actually needs to work?"*

My initial instinct was to choose Automated Kanban because the word "automated" sounded the most advanced and therefore the best. But when I mapped it against the ClinicEase sprint plan from Assignment 6, I realised it only has three columns and no sprint/iteration support. It would have required me to rebuild it almost entirely from scratch. This taught me that the most feature-rich template is not always the right one — the right template is the one that requires the least customisation to fit your actual workflow.

Team Planning required adding only two columns (Testing and Blocked) and configuring the sprint iteration field. Everything else was already aligned with how ClinicEase is structured. Choosing the right starting point saved significant setup time.

---

## Challenge 2: Designing Meaningful WIP Limits as a Solo Developer

WIP limits are a core concept in Kanban, but applying them as a solo developer felt strange at first. WIP limits exist to prevent team members from pulling too much work simultaneously and creating bottlenecks. But if there is only one developer, does limiting In Progress to 3 cards actually help?

After thinking about it carefully, I concluded that WIP limits are even more important for solo developers. Without a team to review work or flag when something has been In Progress too long, there is no external accountability. A WIP limit of 3 on the In Progress column acts as a self-imposed rule: if I already have 3 tasks in progress and want to start a fourth, the board forces me to stop and ask why those 3 are not finished yet. This is a form of self-discipline that the board enforces visually.

Setting the limits was still difficult because there is no formula for the right number. I settled on 3 for active columns based on research suggesting that context-switching between more than 3 tasks significantly reduces productivity. This felt right for a solo project but would need to be re-evaluated if the team grew.

---

## Challenge 3: Comparing GitHub Projects to Other Tools

Part of this assignment required thinking about how GitHub Projects compares to other tools like Trello and Jira. This comparison revealed both the strengths and limitations of GitHub's approach.

**GitHub Projects vs Trello:**
Trello is simpler and more visually polished than GitHub Projects. Its drag-and-drop interface is more intuitive for non-developers, and it is easier to attach images, files, and external links to cards. However, Trello has no native integration with code repositories, pull requests, or commits. For a software project like ClinicEase, this means Trello cards and GitHub commits exist in two separate places with no automatic connection. GitHub Projects wins on traceability — a card can be directly linked to a commit, a PR, and a closed issue, creating an unbroken chain from requirement to deployed code.

**GitHub Projects vs Jira:**
Jira is significantly more powerful than GitHub Projects for enterprise-level Agile management. It supports velocity charts, burndown charts, epic tracking, release planning, and detailed reporting out of the box. GitHub Projects has none of these natively. For ClinicEase as a student project, GitHub Projects is sufficient and keeps everything in one place. But for a real clinic deploying this system at scale, Jira would provide far better sprint analytics and stakeholder reporting. The trade-off is complexity — Jira has a steep learning curve and requires paid plans for full features.

**Conclusion on tooling:** GitHub Projects is the right choice for ClinicEase because it integrates directly with the repository where the code lives. Every issue, commit, and PR is in the same place. For a solo developer working on a portfolio project, this cohesion outweighs the missing analytics features of Jira.

---

## Key Lesson Learned

The most important lesson from this assignment is that **a project board is only useful if it is kept up to date**. A beautifully designed Kanban board that is not updated as work progresses becomes misleading — it shows a false picture of the project's status. The discipline of moving cards, updating statuses, and respecting WIP limits must be maintained throughout the project, not just set up once at the start.

For ClinicEase, I plan to update the board at the beginning and end of every coding session. This keeps the board honest and makes it a genuine reflection of progress rather than a decorative artifact.

---

*Word count: approximately 720 words*

*Document prepared by: [sithembiso Lungisani Mthembu] | [222618698] | CPUT | March 2026*