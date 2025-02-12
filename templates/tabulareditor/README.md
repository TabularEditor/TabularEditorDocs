# Build Your Docs with Docfx and Tabular Editor Styling

This template is based on the modern template in the [docfx](https://github.com/dotnet/docfx) repository. It includes an additional template, `tabulareditor`, which incorporates extra SCSS and TypeScript files inspired by the HubSpot Tabular Editor theme.

Some HubSpot "hubl CSS" files have been rewritten to Sass, and parts of JavaScript have been rewritten to TypeScript. Additionally, a small JavaScript tool converts HubSpot developer info exported JSON to Sass variables used in the template build.

## Getting Started

> Prerequisites
> - Familiarity with the command line
> - Install [.NET SDK](https://dotnet.microsoft.com/en-us/download) 8.0 or higher
> - Install [Node.js](https://nodejs.org/) v20 or higher (Optional: It's required when using [Create PDF Files](https://filzrev.github.io/docfx/docs/pdf.html))

Make sure you have [.NET SDK](https://dotnet.microsoft.com/en-us/download) installed, then open a terminal and enter the following command to install the latest docfx as a global tool:

```bash
dotnet tool install -g docfx
```

Install the latest docfx:

```bash
dotnet tool update -g docfx
```

Navigate to the templates directory:

```bash
cd templates
```

Install Node.js dependencies:

```bash
npm install
```

Ensure the sample data uses the correct template:

Edit the `samples/seed/docfx.json` file to include `tabulareditor` in the "template" section.

To build the template and start a local website:

```bash
npm run start
```

This will build the templates and start a local website with Browsersync, opening the page in your default browser. Any changes made to Sass and TypeScript files will automatically trigger a reload of the page in the browser.


## Tools

You can update theme variables in this template using HubSpot developer information. Follow these steps to extract and process the information:

1. **Open the TabularEditor HubSpot site while logged in to HubSpot backend.**

2. **Click the "HubSpot tools" icon and select "Developer info".**

3. **Copy the JSON code and paste it into `tabulareditor/tools/hs-developer-info.json`.**

4. **Run the script to process the JSON data:**

  ```bash
  node tabulareditor/tools/extract-theme-settings.js
  ```

5. **Check the generated `theme_variables.scss` file:**

  The script will create `tabulareditor/src/hubspot/theme_variables.scss` containing the theme variables and their values.

## Copy template to TabularEditorDocs

Assuming we have this directory structure, both `TabularEditorDocs` and `tabular-editor-docfx-template` within same parent directory,
we could exec followng command when standing in the root directory of `tabular-editor-docfx-template`.

### Parts of directory structure
```bash
├── tabular-editor-docfx-template
│   └── templates
│      ├── common
│      ├── ...
│      └── tabulareditor
│          ├── layout
│          ├── partials
│          ├── public
│          ├── src
│          └── tools
└── TabularEditorDocs
    ├── api
    ├── assets
    ├── bin
    ├── common
    ├── images
    ├── onboarding
    ├── te2
    ├── te3
    ├── templates
    │   ├── api
    │   ├── bootstrap-modal
    │   └── tabulareditor
    └── whats-new
```

### Sync command

```bash
rsync -av --exclude='src' --exclude='tools' ./templates/tabulareditor ../TabularEditorDocs/templates/
```

And temporary for the forked repository.

```bash
rsync -av --exclude='src' --exclude='tools' ./templates/tabulareditor ../TabularEditorDocsFork/templates/
```

## Additional Files

- **`tabulareditor/src/hubspot`**: Contains rewritten Sass and TypeScript files based on the HubSpot theme.
- **`tabulareditor/conceptual.html.primary.js`**: Contains variables used in the new header and footer.
- **`tabulareditor/ManagedReference.extension.js`**: Contains variables used in the new header and footer in the "API" section.

### Variables

- **model.__header**: Contains the main menu and buttons for the header section.
  - **mainMenu**: An array of menu items, each with `text` and `url` properties. The "Support" menu item includes a `subMenu` with additional items.
  - **button1**: Represents the first button in the header with `text` and `url` properties.
  - **button2**: Represents the second button in the header with `text` and `url` properties.

- **model.__footer**: Contains the buttons and links for the footer section.
  - **buttons**: An array of button objects, each with `text` and `url` properties.
  - **leftLinks**: An array of link objects for the left side of the footer, each with `text`, `url`, and optionally `rel` and `target` properties.
  - **rightLinks**: An array of link objects for the right side of the footer, each with `text` and `url` properties.
  - **bottomLinks**: An array of link objects for the bottom of the footer, each with `text` and `url` properties.

## Changes in Original Files

- **`tabulareditor/layout/_master.tmpl`**: Master template, added new header, restructured content, original menu moved, changed footer etc.
- **`tabulareditor/partials/class.tmpl.partial`**: Changes in template to match previous version.
- **`tabulareditor/partials/class.header.tmpl.partial`**: Changes in template to match previous version.
- **`tabulareditor/src/docfx.scss`**: Includes theme variables and additional Sass files. Adds more variables for use with Bootstrap and additional Sass files.
- **`tabulareditor/src/docfx.ts`**: Includes and initializes headerSearch, adds additional Sass files.
- **`tabulareditor/src/layout.scss`**: Changes header and footer height variables. Comments out header and footer layout.
- **`tabulareditor/src/local.scss`**: Adds additional footer HubSpot inline style, adds and overrides additional styles.
- **`tabulareditor/src/nav.scss`**: Small adjustments to `#navbar` style.
- **`tabulareditor/src/nav.ts`**: Changes to render the original navbar as buttons and exclude any submenu.
- **`tabulareditor/src/toc.ts`**: Small addition to exclude TOC on first page.