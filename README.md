# Hugo Static Blog

A minimalist static blog built with [Hugo](https://gohugo.io/) using the [Bear Blog theme](https://github.com/janraasch/hugo-bearblog).

## Setup

### Initial Setup

Fetch blog theme files (required before running the site):
```sh
git submodule update --init --recursive
```

### Local Development

Start the Hugo development server:
```sh
hugo server
```

The site will be available at `http://localhost:1313/`

To include draft posts in the preview:
```sh
hugo server -D
```

## Content Management

### Creating a New Blog Post

Create a new blog post using Hugo's built-in command:
```sh
hugo new blog/my-post-title.md
```

This creates a file at `content/blog/my-post-title.md` with the default frontmatter:
```yaml
---
title: "My Post Title"
date: 2025-01-15T10:00:00-00:00
draft: true
---
```

You can add additional frontmatter fields:
```yaml
---
title: "My Post Title"
date: 2025-01-15T10:00:00-00:00
tags: ["hugo", "blogging"]
tldr: "Brief summary of the post"
draft: false
---
```

### Creating a New Page

Create a standalone page (like About, Contact, etc.):
```sh
hugo new pages/my-page.md
```

For pages that should appear in the main menu, add these frontmatter fields:
```yaml
---
title: "About me"
date: 2025-01-15
tags: ["about"]
draft: false
type: page
menu: main
---
```

### Content Structure

```
content/
├── _index.md          # Homepage content
├── blog/              # Blog posts
│   ├── _index.md      # Blog section page
│   └── post-name.md   # Individual posts
├── pages/             # Standalone pages
│   └── about.md       # Example: About page
└── eli5/              # Custom section (ELI5 posts)
    └── eli5-1.md
```

### Publishing Posts

1. Edit the post content in `content/blog/your-post.md`
2. Change `draft: true` to `draft: false` in the frontmatter
3. Commit and push to your repository

### Building for Production

Generate the static site:
```sh
hugo
```

This creates the site in the `public/` directory.

## Configuration

Site configuration is in `config.toml`:
- Base URL
- Site title and author
- Theme settings
- Permalink structure

## Deployment

This site appears to use GitHub Pages for deployment. The static files are generated in the `public/` directory and served directly.
