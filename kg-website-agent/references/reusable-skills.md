# Reference: Daily operations and reusable skills

## The everyday loop

There is no dashboard. The whole operation is: open Claude Code Desktop, choose
the project folder, describe the change, preview, push.

```
open folder -> describe the change -> npm run dev (preview) -> commit + push -> Cloudflare auto-publishes (~2 min)
```

Real instructions a non-technical staff member gives the agent:

> "Write a new blog post titled 'Five tips for choosing roofing materials'. Here
> are my notes: [paste]. Make it an MDX file in the blog folder, today's date,
> tag 'guides'. Show me a preview."

> "Change the home page headline to 'Malaysia's Trusted Building Materials Directory'."

> "Update the phone number in the footer and the contact page to 03-1234 5678."

> "Fix the typo on the About page: 'experiance' should be 'experience'."

## Saving and undoing

```bash
git add .                    # .env is excluded by .gitignore
git commit -m "what changed"
git push                     # Cloudflare rebuilds within ~2 min
```

Undo is safe because every change is in GitHub history:

```bash
git revert HEAD && git push  # or click Rollback in the Cloudflare dashboard
```

## Turn repeated work into skills

Any task done more than twice should become a saved skill, so it runs the same
way for any team member. Inside Claude Code, type `/skill-creator` and describe
the operation:

> "Create a skill called publish-post. Given a draft, it checks the post has a
> title, description, date and tags, generates a cover image in our brand style,
> builds the site, and if the build passes, commits with a clear message. Never
> push without asking me first."

The skill saves to `.claude/skills/publish-post/SKILL.md` (this project) or
`~/.claude/skills/publish-post/SKILL.md` (every site). A starter set:

| Skill | What it does |
|-------|--------------|
| `publish-post` | Validate a draft, make its cover, build, commit |
| `site-maintenance` | Find broken links and images, confirm a clean build |
| `add-page` | Add a service/product/listing page from the standard template |
| `seo-check` | Verify title, description, headings, alt text, sitemap inclusion |
| `image-set` | Cover + inline + OG image for a post, in the brand style |

Build each the first time you hit the task by hand. Skills remove the reliance on
any one person remembering the steps — the site gets more reliable the longer you
run it, because every repeated task is captured instead of re-improvised.
