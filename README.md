# Trello Import Tool - Usage Guide

Convert markdown checklists into organized Trello boards automatically, with templates and configurations for easy customization.

## 🚀 Quick Start

### Option 1: Use Ready-Made Examples
```bash
# 1. Copy example files
cp examples/generic-project.md my-project.md
cp examples/generic-config.json my-config.json

# 2. Edit the files with your project details
# 3. Set your Trello credentials
export TRELLO_KEY="your_api_key_here"
export TRELLO_TOKEN="your_token_here"
```
> <sub>**Note:** Set your Trello credentials as described in the [troubleshooting instructions](#please-set-trello_key-and-trello_token-environment-variables).</sub>

```bash
# 4. Test first (safe preview)
python import_trello.py -f my-project.md -c my-config.json --dry-run

# 5. Create the actual board
python import_trello.py -f my-project.md -c my-config.json
```

### Option 2: Customize Templates
```bash
# 1. Copy template files
cp templates/project-template.md my-project.md
cp templates/config-template.json my-config.json

# 2. Replace all {{VARIABLES}} with your values
# 3. Test and create as above
```
## 📁 Available Files

### Template Files (in `templates/`)
- **`project-template.md`** - Markdown template with `{{PLACEHOLDER}}` variables
- **`config-template.json`** - Configuration template to customize
- **`README.md`** - Complete template customization guide

### Example Files (in `examples/`)
- **`generic-project.md`** - Ready-to-use generic project example
- **`generic-config.json`** - Common configuration for most projects

### Core Files
- **`import_trello.py`** - Universal Trello import script with template support
- **`requirements.txt`** - Python dependencies (install with `pip install -r requirements.txt`)

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Trello API credentials:**
   - Go to https://trello.com/app-key
   - Copy your API Key
   - Generate a Token

3. **Set environment variables:**
   ```bash
   export TRELLO_KEY="your_api_key_here"
   export TRELLO_TOKEN="your_token_here"
   ```
   > <sub>**Note:** If you run into problem try [troubleshooting instructions](#please-set-trello_key-and-trello_token-environment-variables).</sub>

4. **Choose your starting point:**
   - **New to this?** → Use `examples/generic-project.md` and `examples/generic-config.json`
   - **Want full control?** → Use `templates/project-template.md` and `templates/config-template.json`
   - **Have existing project_plan.md?** → Adjust the config.json and run the script directly on your file

## The Import Script

### `import_trello.py` - Universal Trello Import Tool
The universal script for importing markdown checklists into Trello boards with full template support.

**Usage (Examples):**
```bash
# Basic usage (uses project_plan.md if it exists)
python import_trello.py

# Custom markdown file
python import_trello.py -f my_project_plan.md

# Custom board name
python import_trello.py -b "My Project Board"

# Dry run (PREVIEW ONLY - see what would be created without creating)
python import_trello.py --dry-run

# Use custom configuration
python import_trello.py -c example-config.json

# Combine options
python import_trello.py -f my_project_plan.md -c my-config.json --dry-run
```

### 🔍 **Dry Run vs Actual Creation**

**Dry Run Mode** (`--dry-run`) aka **SAFE PREVIEW**:
- ✅ Parses your markdown file and shows found tasks
- ✅ Shows how tasks would be categorized (labels)
- ✅ Displays which Trello list each task would go to
- ✅ Provides summary statistics
- ❌ **Does NOT** create any actual Trello boards, lists, or cards
- ❌ **Does NOT** use your Trello API credentials
- ❗️**TIP: Use this first** to test your configuration!

**Actual Creation** - **CREATES REAL BOARD**:
- ✅ Creates a real Trello board in your account
- ✅ Creates all labels, lists, and cards
- ✅ Uses your TRELLO_KEY and TRELLO_TOKEN
- ❗️❗️ **Will modify your Trello account**
- ❗️**TIP: Use this when you're ready** for the real board

**Example workflow:**
```bash
# Step 1: Preview what will be created (safe)
python import_trello.py -f examples/generic-project.md --dry-run

# Step 2: If happy with preview, create the actual board
python import_trello.py -f examples/generic-project.md -b "My Real Project Board"
```

**Features:**
- Command-line interface with options
- Template and configuration file support
- Dry-run mode to preview changes
- Duplicate detection
- Section and subsection tracking
- Detailed progress reporting
- Task categorization based on keywords
- Maps completed tasks to "Done" list, incomplete to "To Do" (based on checkmarks)
- Board naming from project title or config
- **Automatic removal of Trello's default lists** to prevent duplicates

## Configuration

You can customize the behavior using configuration files:

### **Using Existing Configurations:**
- **`examples/generic-config.json`** - General software development with common labels and workflows

### **Creating Custom Configurations:**
- **labels**: Define board labels and colors (red, orange, yellow, green, blue, purple, pink, sky, lime, black)
- **lists**: Define board lists and their positions
- **categorization_rules**: Keyword-based automatic categorization
- **list_mapping**: How completion status maps to lists

### **Example Custom Config:**
```json
{
    "board_name": "My Project",
    "labels": [
        {"name": "Backend", "color": "blue"},
        {"name": "Frontend", "color": "purple"}
    ],
    "categorization_rules": {
        "Backend": ["api", "server", "database"],
        "Frontend": ["ui", "component", "design"]
    }
}
```

## How It Works

1. **Parsing**: The script reads your markdown file and extracts:
   - Task names from checklist items `- [x]` or `- [ ]`
   - Completion status (checked = completed)
   - Section headers for context

2. **Categorization**: Tasks are automatically labeled based on keywords:
   - "setup", "configure" → Setup label
   - "model", "database" → Model label
   - "template", "ui", "design" → Template/Frontend label
   - And many more...

3. **List Assignment**: 
   - Completed tasks (`[x]`) → "Done" list
   - Incomplete tasks (`[ ]`) → "To Do" list

4. **Board Creation**: Creates a complete Trello board with:
   - Proper lists (Backlog, To Do, In Progress, Review, Done)
   - Color-coded labels
   - Categorized and organized cards

## Customizing for Your Workflow

### Different List Names
If you use "Doing" instead of "In Progress", update the `lists` section in your config file:

```json
{
  "lists": [
    {"name": "Backlog", "pos": "top"},
    {"name": "To Do", "pos": "bottom"},
    {"name": "Doing", "pos": "bottom"},
    {"name": "Review", "pos": "bottom"},
    {"name": "Done", "pos": "bottom"}
  ]
}
```

### Different Categories
Add your own categorization rules:

```json
{
  "categorization_rules": {
    "Backend": ["django", "python", "database"],
    "Frontend": ["html", "css", "javascript"],
    "DevOps": ["deploy", "docker", "ci/cd"]
  }
}
```

## Troubleshooting

### "Please set TRELLO_KEY and TRELLO_TOKEN environment variables"
This is the most common error. Here's how to fix it:

**Step 1: Get your credentials**
1. Go to https://trello.com/app-key
2. Copy your **API Key**
3. Click "Generate a Token" and copy your **Token**

**Step 2: Set environment variables**
```bash
# Replace with your actual credentials
export TRELLO_KEY=your_actual_api_key_here
export TRELLO_TOKEN=your_actual_token_here
```

**Step 3: Verify they're set**
```bash
echo "Key: $TRELLO_KEY"
echo "Token: $TRELLO_TOKEN"
# Both should show your credentials, not empty lines
```

**Step 4: Run in the same terminal**
Make sure to run the script in the same terminal where you set the variables:
```bash
# Test with dry-run first (doesn't need credentials)
python import_trello.py --dry-run

# Then create actual board (needs credentials)
python import_trello.py -f my-project.md -c my-config.json
```

**Common issues:**
- **Forgot to export**: Use `export` before the variable assignment
- **Used quotes**: Don't put quotes around the actual values
- **Different terminal**: Environment variables only exist in the current terminal session
- **Spaces**: Make sure there are no spaces around the `=` sign

### "No tasks found"
- Check that your markdown file has the correct format: `- [x]` or `- [ ]`
- Ensure the file exists and is readable
- **If your list is in a different format**, see the [Supported File Formats](#supported-file-formats) section below for conversion options

### "List not found"
- Make sure your list names in the config match exactly
- Check for extra spaces or different cases

### "Unknown labels"
- Add missing labels to your configuration
- Or update categorization rules to use existing labels

### Duplicate Lists in Trello
**Problem**: You see duplicate columns like two "To Do" lists or two "Done" lists.

**Cause**: Trello automatically creates default lists when a new board is created.

**Solution**: The script now automatically removes these default lists before creating your configured ones. If you still see duplicates:
1. **For new boards**: This should no longer happen with the updated script
2. **For existing boards**: You'll need to manually archive the unwanted lists in Trello
3. **To verify**: Use `--dry-run` to see which lists would be created

**Default lists that are automatically removed**: "To Do", "Doing", "Done"

### API Errors
- **"Please set TRELLO_KEY and TRELLO_TOKEN"**: See the detailed solution above
- **"Invalid key/token"**: Double-check your credentials at https://trello.com/app-key
- **"Network error"**: Check your internet connection
- **"Permission denied"**: Ensure you have permission to create boards in your Trello account
- **"Rate limited"**: Wait a few minutes if you've made many API calls

## 📋 Template System

This project includes a comprehensive template system to help you get started quickly:

### **For detailed guidance:** See [`templates/README.md`](templates/README.md) in this repo for examples, color schemes, and best practices.

## 📄 Supported File Formats

### **Currently Supported:**
- **Markdown (.md)** with checklist format:
  ```markdown
  # Project Name
  ## Section
  - [x] Completed task
  - [ ] Incomplete task
  ```

### **Other Formats? Here are your options:**

#### **Option 1: Convert to Markdown** (Recommended)
Most formats can be easily converted to markdown:

**From Plain Text Lists:**
```
// Original
✓ Setup project
✓ Create database
○ Build UI
○ Add tests

// Convert to Markdown
- [x] Setup project  
- [x] Create database
- [ ] Build UI
- [ ] Add tests
```

**From CSV/Excel:**
1. Export as CSV
2. Use a simple script to convert to markdown format
3. Or manually convert: `Task Name, Status` → `- [x] Task Name`

**From Other Todo Apps:**
- **Todoist**: Export as template, convert to markdown
- **Notion**: Copy checklist blocks, format as markdown
- **Trello**: Export existing board, extract card names
- **Asana**: Export as CSV, convert to markdown

#### **Option 2: Create a Custom Parser**
If you frequently use a specific format, you can modify the scripts:

1. **Copy `import_trello.py`**
2. **Modify the `MarkdownParser` class** to handle your format
3. **Example formats you could add:**
   - Plain text with bullet points
   - JSON task lists
   - CSV files
   - YAML task definitions

#### **Option 3: Use Templates as Starting Point**
Instead of converting existing lists:
1. Use `templates/project-template.md` or `examples/generic-project.md`
2. Copy your tasks into the markdown format
3. This often works faster than conversion for smaller lists

### **Quick Conversion Tips:**

**Text Replacement (using VS Code, etc.):**
- Find: `✓ (.+)` → Replace: `- [x] $1`
- Find: `○ (.+)` → Replace: `- [ ] $1`
- Find: `☐ (.+)` → Replace: `- [ ] $1`
- Find: `☑ (.+)` → Replace: `- [x] $1`

**Command Line (macOS/Linux):**
```bash
# Convert checkmarks to markdown format
sed 's/^✓ /- [x] /' your-list.txt > converted-plan.md
sed 's/^○ /- [ ] /' your-list.txt >> converted-plan.md
```

## Final Tips

1. **Always start with dry-run**: Use `--dry-run` to preview what would be created before making any actual changes to your Trello account

2. **Test your configuration**: Dry-run mode is perfect for testing different categorization rules and seeing how tasks get labeled

3. **Backup important boards**: The scripts create new boards, but always be careful with API operations

4. **Customize gradually**: Start with the default configuration and adjust as needed

5. **Regular updates**: Re-run the script periodically to sync your markdown progress with Trello

6. **Multiple projects**: Use different configuration files for different projects

7. **Safe experimentation**: Since dry-run doesn't modify anything, you can experiment freely with different settings

8. **Use templates**: Start with `examples/*` files or customize `templates/*` files for your needs

9. **Version control**: The included `.gitignore` file prevents accidentally committing sensitive data like API keys or personal project files

10. **Read the guide**: Check `templates/README.md` for comprehensive examples and best practices

11. **Non-markdown lists**: If your tasks are in a different format, see the [Supported File Formats](#supported-file-formats) section for conversion tips