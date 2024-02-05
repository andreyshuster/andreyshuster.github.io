---
title: "Todo Lists Are Enough"
date: 2024-02-04T20:34:42-06:00
draft: false
---

I always try to organize my workspace using a minimum of tools and simple rules that work for 90% of my tasks. Simple rules are easier to follow, and it doesn't take much time to get used to them.

For example, managing pet projects. I work on them quite irregularly, with breaks of several days or even a couple of weeks. Context is forgotten, and returning to project tasks takes half an hour, even though I only have an hour of free time for the project.

Originally, in my ideal task management tool, I wanted to see familiar JIRA labels: Backlog, In Scope, In Progress, In Review, Done, Cancel, Blocked.

I tried several lightweight JIRA alternatives - Trello, Asana, Basecamp, and some others whose names I forgot. I also periodically tried the org-mode outliner in Emacs, tried the Projects plugin in Obsidian, but I always returned to using simple to-do lists that can be created in any text editor with checkboxes and optionally basic text formatting styles such as strikethrough and highlight. Any Markdown editor will do, but you can also do the same in Apple Notes or even in Word.

## The solution I came to.
In a regular to-do list, all these features are already there:
* Completed/not completed is the main and basic task of a to-do list.
* Subtasks can be highlighted with indentation. It is important to note that subtasks should be described so that they can be closed before the main task.
* Canceled tasks are not deleted but crossed out. This way, you can see the history of events.
* An important task is highlighted in bold or with a marker (highlight) if available.

These simple rules are almost sufficient for everything. Even for work tasks, I
sometimes use lists - I write down thoughts that I don't want to forget, and
then transfer them to JIRA.

### Example task list.
- [ ] Make coffee
  * [x] Wash the coffee machine.
  * [ ] Fill with water
  * [ ] Add 2 spoons of coffee
* [ ] ==Walk the dog==
* [x] Wash up
  with soap.
* [ ] ~~Read the news~~
* [ ] [Link to hobby project](https://github.com/andreyshuster/andreyshuster.github.io)

When my tasks become more complicated, a to-do list may not be enough, but for
now, it's an excellent option. An additional plus is that cognitive load
decreases - there is no need to keep in mind various ways of managing
information and learn new applications.
## In Progress state
Each recorded task should be small and simple enough to be completed in one go.
If a task takes more than half an hour, it is broken down into subtasks.
Therefore - no need to transition task into "In Progress" state. I select a task
and then complete it.
## README.md
Such lists can be kept right in the README.md file in the project repository, and thus, I am not dependent on any platform like GitHub or GitLab. At any time, I can move my projects anywhere, even to personal hosting, and project management will not change, no time will be wasted on task migration. README.md files have many applications. For example, you can describe the structure of entities or list the steps needed to run the project locally.

## Lists drawbacks
Of course, there are drawbacks. This structure is suitable for one, maximum two people. A larger team will probably find it difficult to synchronize work in one list. I've seen it work, but there, one person leads the central task list. When the project is very extensive, with many diverse tasks, managing such a list becomes more difficult - sometimes you even want to isolate a separate branch of tasks so that others don't distract.
