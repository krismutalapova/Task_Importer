# Template Files Guide

This directory contains template files that you can use as a starting point for your own projects.

## 📁 Available Templates

### 1. **Customizable Templates** (Copy and edit)
- `project-template.md` - Markdown template with `{{PLACEHOLDER}}` variables
- `config-template.json` - Configuration template with variables

### 2. **Ready-to-Use Examples** (in `../examples/`)
- `generic-project.md` - Generic software project template  
- `generic-config.json` - Common configuration for most projects

## 🚀 Quick Start Guide

### Option 1: Use Ready Examples (Recommended)
```bash
# 1. Copy the example files
cp examples/generic-project.md my-project.md
cp examples/generic-config.json my-config.json

# 2. Edit your files with your project details
# 3. Test with dry-run
python import_trello.py -f my-project.md -c my-config.json --dry-run

# 4. Create the board
python import_trello.py -f my-project.md -c my-config.json
```

### Option 2: Start from Template
```bash
# 1. Copy the template files
cp templates/project-template.md my-project.md
cp templates/config-template.json my-config.json

# 2. Replace all {{VARIABLES}} with your actual values
# 3. Test and create as above
```

## 📝 Customization Guide

### Markdown File Customization
Replace these placeholders in `project-template.md`:

| Placeholder | Example | Description |
|-------------|---------|-------------|
| `{{PROJECT_NAME}}` | "E-commerce Platform" | Main project title |
| `{{PHASE_1_NAME}}` | "Foundation" | Phase/sprint name |
| `{{SECTION_1_NAME}}` | "Project Setup" | Section name |
| `{{COMPLETED_TASK_EXAMPLE_1}}` | "Initialize Git repository" | Completed task |
| `{{INCOMPLETE_TASK_EXAMPLE_1}}` | "Set up CI/CD pipeline" | To-do task |

### Configuration File Customization
Replace these variables in `config-template.json`:

| Variable | Example | Options |
|----------|---------|---------|
| `{{YOUR_PROJECT_NAME}}` | "My Web App" | Any string |
| `{{YOUR_MARKDOWN_FILE}}` | "my-plan" | Filename without .md |
| `{{LABEL_1_NAME}}` | "Backend" | Any label name |
| `{{LABEL_1_COLOR}}` | "blue" | red, orange, yellow, green, blue, purple, pink, sky, lime, black |
| `{{LIST_1_NAME}}` | "To Do" | Any list name |
| `{{KEYWORD_1_1}}` | "server" | Words that trigger this label |

## 🎨 Common Label & Color Schemes

### Software Development
```json
{"name": "Backend", "color": "blue"}
{"name": "Frontend", "color": "purple"}
{"name": "Database", "color": "yellow"}
{"name": "Testing", "color": "lime"}
{"name": "DevOps", "color": "black"}
```

### Project Management
```json
{"name": "Planning", "color": "blue"}
{"name": "Development", "color": "green"}
{"name": "Review", "color": "orange"}
{"name": "Bug Fix", "color": "red"}
{"name": "Documentation", "color": "sky"}
```

### Priority-Based
```json
{"name": "Critical", "color": "red"}
{"name": "High", "color": "orange"}
{"name": "Medium", "color": "yellow"}
{"name": "Low", "color": "green"}
{"name": "Nice to Have", "color": "blue"}
```

## 📋 Common List Configurations

### Kanban Style
```json
[
  {"name": "To Do", "pos": "top"},
  {"name": "Doing", "pos": "bottom"},
  {"name": "Done", "pos": "bottom"}
]
```

### Scrum/Agile Style
```json
[
  {"name": "Backlog", "pos": "top"},
  {"name": "Sprint Planning", "pos": "bottom"},
  {"name": "In Progress", "pos": "bottom"},
  {"name": "Review", "pos": "bottom"},
  {"name": "Done", "pos": "bottom"}
]
```

### Development Workflow
```json
[
  {"name": "Ideas", "pos": "top"},
  {"name": "To Do", "pos": "bottom"},
  {"name": "In Development", "pos": "bottom"},
  {"name": "Testing", "pos": "bottom"},
  {"name": "Deployed", "pos": "bottom"}
]
```

## 🔍 Keyword Examples for Categorization

### Technology-Specific Keywords
```json
"Frontend": ["react", "vue", "angular", "ui", "component", "css", "html"],
"Backend": ["api", "server", "node", "python", "java", "database"],
"Mobile": ["ios", "android", "react native", "flutter", "swift"],
"DevOps": ["docker", "kubernetes", "aws", "deploy", "ci/cd"]
```

### Task Type Keywords
```json
"Setup": ["setup", "install", "configure", "initialize"],
"Feature": ["implement", "add", "create", "build", "develop"],
"Bug Fix": ["fix", "bug", "error", "issue", "debug"],
"Testing": ["test", "testing", "unit", "integration", "e2e"]
```

## 💡 Tips for Effective Templates

1. **Start Simple**: Begin with the example templates and modify gradually
2. **Use Consistent Naming**: Keep label and keyword naming consistent across projects
3. **Test First**: Always use `--dry-run` to preview before creating
4. **Version Control**: Keep your template files in version control for reuse
5. **Team Standards**: Create team-specific templates for consistency
6. **Documentation**: Document your categorization rules for team members

## 🎯 Project Type Examples

### Web Application
- Labels: Frontend, Backend, Database, API, Security, Testing
- Keywords: "react", "node", "mongodb", "auth", "jest"

### Mobile App
- Labels: iOS, Android, UI/UX, API, Testing, Store
- Keywords: "swift", "kotlin", "design", "rest", "testflight"

### Data Science
- Labels: Data Collection, Analysis, Modeling, Visualization, Deployment
- Keywords: "pandas", "analysis", "ml", "charts", "production"

### Game Development
- Labels: Gameplay, Graphics, Audio, UI, Testing, Publishing
- Keywords: "mechanics", "sprites", "sound", "menu", "playtesting"
