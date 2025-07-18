# HomelabWiki User Guide

A comprehensive guide for using HomelabWiki - your self-hosted knowledge base for homelab documentation.

## 🚀 Getting Started

### Accessing HomelabWiki

1. **Open your web browser** and navigate to your HomelabWiki instance:
   ```
   http://your-homelab-wiki-server:3000
   ```

2. **Login with your domain credentials**:
   - Username: Your Active Directory username (e.g., `aegis` or `wyk\aegis`)
   - Password: Your domain password

3. **First-time setup**:
   - Your first login will create your user profile
   - Your permissions are determined by your Active Directory group membership

### User Roles and Permissions

HomelabWiki uses your Active Directory groups to determine your access level:

- **WikiAdmins**: Full administrative access
  - Create, edit, and delete all pages
  - Upload and manage all files
  - Access administrative functions
  - Manage users and system settings

- **WikiUsers**: Standard user access
  - Create, edit, and delete your own pages
  - Upload and manage your own files
  - View all published pages
  - Comment on pages

- **WikiReadOnly**: Read-only access
  - View published pages
  - Search content
  - Download files
  - Cannot create or modify content

## 📝 Creating and Managing Pages

### Creating a New Page

1. **Click the "New Page" button** in the navigation bar
2. **Enter page details**:
   - **Title**: Descriptive page title
   - **Content**: Write your content in Markdown format
   - **Summary**: Brief description of the page (optional)
   - **Tags**: Add relevant tags for organization
3. **Preview your page** using the preview tab
4. **Save as draft** or **publish immediately**

### Markdown Basics

HomelabWiki supports full Markdown syntax. Here are the essentials:

#### Headers
```markdown
# Header 1
## Header 2
### Header 3
```

#### Text Formatting
```markdown
**Bold text**
*Italic text*
~~Strikethrough~~
`Inline code`
```

#### Lists
```markdown
- Unordered list item
- Another item
  - Sub-item

1. Ordered list item
2. Another item
   1. Sub-item
```

#### Links and Images
```markdown
[Link text](https://example.com)
![Image alt text](image-url.jpg)
```

#### Code Blocks
```markdown
```python
def hello_world():
    print("Hello, World!")
```
```

#### Tables
```markdown
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
```

### Editing Pages

1. **Navigate to the page** you want to edit
2. **Click the "Edit" button** (only visible for pages you can modify)
3. **Make your changes** in the editor
4. **Use the preview** to check your formatting
5. **Save your changes** or **save as draft**

### Page Organization

#### Using Tags
- **Add relevant tags** to your pages for better organization
- **Use consistent naming** (e.g., "homelab", "networking", "docker")
- **Tags are searchable** and help others find related content

#### Page Hierarchy
- **Use descriptive titles** that indicate the page's purpose
- **Create index pages** for major topics
- **Link related pages** together using markdown links

### Publishing and Drafts

- **Draft pages** are only visible to you and administrators
- **Published pages** are visible to all users with appropriate permissions
- **Archive pages** that are outdated but worth keeping

## 📁 File Management

### Uploading Files

1. **Navigate to the Files section** or use the file upload in the page editor
2. **Click "Upload File"** or drag and drop files
3. **Add file details**:
   - **Description**: Brief description of the file
   - **Associate with page**: Link to a specific page (optional)
4. **Upload the file**

### Supported File Types

HomelabWiki supports various file types:

- **Images**: PNG, JPG, JPEG, GIF
- **Documents**: PDF, DOC, DOCX, XLS, XLSX, TXT, MD
- **Archives**: ZIP, TAR, GZ
- **Maximum size**: 16MB per file (configurable)

### Using Files in Pages

#### Embedding Images
```markdown
![Description](http://your-wiki/api/files/1/download)
```

#### Linking to Files
```markdown
[Download Manual](http://your-wiki/api/files/2/download)
```

### File Organization

- **Use descriptive filenames** that indicate the file's purpose
- **Add detailed descriptions** to help others understand the file
- **Associate files with pages** when relevant
- **Keep files organized** by removing outdated uploads

## 🔍 Searching Content

### Basic Search

1. **Use the search bar** at the top of any page
2. **Enter your search terms** (e.g., "docker networking")
3. **Review the results** across pages, files, and tags
4. **Click on results** to navigate to relevant content

### Search Tips

- **Use specific terms** for better results
- **Search by tags** to find related content
- **Use quotes** for exact phrases: `"exact phrase"`
- **Combine terms** with space for AND search
- **Search in specific content types** using filters

### Advanced Search

- **Filter by content type**: Pages, files, or tags only
- **Filter by author**: Find content by specific users
- **Filter by date**: Find recently updated content
- **Filter by tags**: Search within specific categories

## 📊 Exporting Content

### Export Individual Pages

1. **Navigate to the page** you want to export
2. **Click the "Export" button** in the page toolbar
3. **Choose export format**:
   - **PDF**: Formatted document with styling
   - **Markdown**: Raw markdown file
4. **Download** the exported file

### Export Multiple Pages

1. **Go to the Pages section**
2. **Select multiple pages** using checkboxes
3. **Click "Export Selected"**
4. **Choose export format** and options
5. **Download** the ZIP archive containing all exported pages

### Export Options

- **Include images**: Embed images in PDF exports
- **Include metadata**: Add author, date, and tags
- **Custom styling**: Apply custom CSS to PDF exports
- **Batch export**: Export entire tag categories

## 🔧 User Settings

### Profile Management

1. **Click your username** in the top-right corner
2. **Select "Profile"** from the dropdown menu
3. **Update your information**:
   - Profile picture (if enabled)
   - Display name preferences
   - Email notifications (if configured)
   - Theme preferences

### Preferences

- **Theme**: Choose between light and dark modes
- **Editor preferences**: Font size, line numbers, etc.
- **Notification settings**: Email alerts for page updates
- **Default page settings**: Default tags, privacy settings

## 🎯 Best Practices

### Content Creation

1. **Write clear, descriptive titles** that explain the page's purpose
2. **Start with a summary** of what the page covers
3. **Use headers** to organize content into logical sections
4. **Add relevant tags** for better discoverability
5. **Include screenshots** and diagrams when helpful
6. **Link to related pages** to create a knowledge network

### Documentation Structure

#### For Technical Guides
```markdown
# Guide Title

## Overview
Brief description of what this guide covers

## Prerequisites
What you need before starting

## Step-by-Step Instructions
1. First step
2. Second step
3. Third step

## Troubleshooting
Common issues and solutions

## Additional Resources
Links to related documentation
```

#### For Reference Material
```markdown
# Reference Title

## Quick Reference
Key information at a glance

## Detailed Information
Comprehensive details

## Examples
Practical examples and use cases

## See Also
Related reference materials
```

### Collaboration

1. **Use descriptive edit summaries** when updating pages
2. **Communicate changes** in shared spaces
3. **Respect others' work** - don't delete without discussion
4. **Use comments** to provide feedback on pages
5. **Create index pages** for collaborative projects

### Organization

1. **Use consistent naming conventions** for pages and tags
2. **Create category pages** for major topics
3. **Maintain a site map** or index of important pages
4. **Regular cleanup** of outdated content
5. **Use tags strategically** - not too many, not too few

## 🚨 Troubleshooting

### Common Issues

#### Cannot Login
- **Check your credentials** - use your domain username/password
- **Verify domain format** - try both `username` and `domain\username`
- **Contact your administrator** if account is locked

#### Page Not Saving
- **Check your internet connection**
- **Verify you have edit permissions** for the page
- **Try refreshing the page** and attempting again
- **Check for conflicting edits** from other users

#### File Upload Failing
- **Check file size** - maximum 16MB by default
- **Verify file type** is supported
- **Check available disk space** on the server
- **Try a different browser** if issues persist

#### Search Not Working
- **Try different search terms**
- **Check spelling** of search terms
- **Use broader terms** if specific search returns no results
- **Clear browser cache** and try again

### Getting Help

1. **Check this user guide** for answers to common questions
2. **Search existing pages** - someone might have documented the solution
3. **Contact administrators** using the contact information provided
4. **Create a support ticket** if your organization has a ticketing system

## 📱 Mobile Usage

### Mobile Interface

HomelabWiki is designed to work on mobile devices:

- **Responsive design** adapts to screen size
- **Touch-friendly** navigation and controls
- **Optimized performance** for mobile connections
- **Offline reading** capabilities (limited)

### Mobile Best Practices

- **Use the mobile menu** for easier navigation
- **Zoom in** when editing on small screens
- **Use voice-to-text** for faster content entry
- **Save drafts frequently** to prevent data loss

## 🔒 Security and Privacy

### Data Security

- **Your data is encrypted** in transit and at rest
- **Access is controlled** by Active Directory groups
- **Regular backups** protect against data loss
- **Audit logs** track all changes for security

### Privacy Considerations

- **Published pages** are visible to all users with access
- **Draft pages** are only visible to you and administrators
- **File uploads** follow the same visibility rules as pages
- **Search logs** may be kept for system optimization

### Best Practices

1. **Don't share sensitive information** in public pages
2. **Use appropriate tags** to indicate content sensitivity
3. **Mark pages as drafts** until ready for publication
4. **Regularly review** your published content
5. **Report security concerns** to administrators immediately

## 📚 Additional Resources

### Learning Resources

- **Markdown Tutorial**: Learn more about Markdown syntax
- **Documentation Best Practices**: Industry standards for technical writing
- **Knowledge Management**: Strategies for organizing information

### Community

- **Internal Forums**: Connect with other users in your organization
- **Feature Requests**: Suggest improvements to the system
- **User Groups**: Join topic-specific discussion groups

### Support

- **Administrator Contact**: [Contact your system administrator]
- **Technical Support**: [IT support contact information]
- **Training Sessions**: [Available training opportunities]

---

## 📋 Quick Reference

### Keyboard Shortcuts

- **Ctrl+S** (Cmd+S): Save page
- **Ctrl+P** (Cmd+P): Preview page
- **Ctrl+F** (Cmd+F): Search current page
- **Ctrl+K** (Cmd+K): Global search
- **Ctrl+N** (Cmd+N): New page
- **Ctrl+E** (Cmd+E): Edit current page

### Common Markdown

| Element | Syntax |
|---------|--------|
| Header | `# H1` `## H2` `### H3` |
| Bold | `**bold text**` |
| Italic | `*italic text*` |
| Code | `` `code` `` |
| Link | `[title](url)` |
| Image | `![alt](url)` |
| List | `- item` or `1. item` |
| Quote | `> quote` |
| Table | `| col1 | col2 |` |

### File Size Limits

- **Maximum file size**: 16MB
- **Supported formats**: Images, documents, archives
- **Bulk upload**: Up to 10 files at once
- **Storage quota**: Varies by user role

### Contact Information

- **System Administrator**: [Admin contact]
- **Technical Support**: [Support contact]
- **Training**: [Training contact]
- **Emergency**: [Emergency contact]

---

**Welcome to HomelabWiki!** This user guide covers the essential features and best practices for using your knowledge base effectively. For additional help or feature requests, please contact your system administrator.
