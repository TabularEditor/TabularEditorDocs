const fs = require("fs");
const path = require("path");

/**
 * Adds theme settings to the specified path within the theme_settings object.
 *
 * @param {Object} theme_settings - The object to which the theme settings will be added.
 * @param {Array<string>} path - An array representing the path where the theme setting should be added.
 * @param {*} element - The theme setting value to be added at the specified path.
 */
const addThemeSettings = (
  theme_settings,
  path,
  element
) => {
  // if (element) {
    if (path.length > 0) {
      let current = theme_settings;
      for (let i = 0; i < path.length - 1; i++) {
        if (!current[path[i]]) {
          current[path[i]] = {};
        }
        current = current[path[i]];
      }
      current[path[path.length - 1]] = element;
      console.info(`Include variable "${path.join('.')}" (${element})`);
    }
  // } else {
  //   console.warn(`Exclude empty variable "${path.join('.')}" (${element})`);
  // }
};

/**
 * Recursively parses the children of a given element and updates the theme settings.
 *
 * @param {Object} theme_settings - The object to store the parsed theme settings.
 * @param {Array} path - The current path of element names being traversed.
 * @param {Object} element - The current element being parsed.
 * @param {string} [element.name] - The name of the current element.
 * @param {Array} [element.children] - The children of the current element.
 * @param {*} [element.default] - The default value of the current element.
 */
const parseChildrenRecursive = (theme_settings, path, element) => {
  const name = element.name ?? "";
  const children = element.children ?? [];
  path.push(name);
  if (children.length) {
    for (const child of children) {
      parseChildrenRecursive(theme_settings, path, child);
    }
  } else {
    parseElementValueRecursive(theme_settings, path, element.default);
  }
  path.pop();
  return;
};


/**
 * Recursively parses the value of an element and adds it to the theme settings.
 *
 * @param {Object} theme_settings - The object to store the parsed theme settings.
 * @param {Array} path - The current path of properties being traversed.
 * @param {Object|any} element - The current element being parsed. If it's an object, the function will recurse into its properties.
 */
const parseElementValueRecursive = (theme_settings, path, element) => {
  if (element && typeof element === "object") {
    for (const propertyName in element) {
      if (element.hasOwnProperty(propertyName)) {
        const subElement = element[propertyName];
        path.push(propertyName);
        parseElementValueRecursive(theme_settings, path, subElement);
        path.pop();
      } else {
        console.error(`Unknown propertyName "${propertyName}"`);
      }
    }
  } else {
    addThemeSettings(theme_settings, path, element);
  }
};


// Define the path to the JSON file
const filePath = path.join(__dirname, "hs-developer-info.json");

// Read the file
fs.readFile(filePath, "utf8", (err, data) => {
  if (err) {
    console.error("Error reading file:", err);
    return;
  }
  // Extract information from the JSON data
  let theme_settings = {};
  try {
    // Parse the JSON data
    const jsonData = JSON.parse(data);
    const theme_meta = jsonData.theme_meta.fields;
    if (!theme_meta) {
      console.error("No theme_meta found in JSON data");
      return;
    }
    for (const key in theme_meta) {
      if (theme_meta.hasOwnProperty(key)) {
        const section = theme_meta[key];
        const sectionName = section.name;
        parseChildrenRecursive(theme_settings, [], section);
      }
    }

    // console.log('Extracted theme_settings:', JSON.stringify(theme_settings));
    const outputFilePath = path.join(__dirname, "../src/hubspot/theme_variables.scss");
    const outputStream = fs.createWriteStream(outputFilePath);

    const outputThemeSettings = (obj, prefix = "") => {
      for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
          const value = obj[key];
          const newPrefix = prefix ? `${prefix}-${key}` : key;
          if (typeof value === "object" && value !== null) {
            outputThemeSettings(value, newPrefix);
          } else {
            if (typeof value === "string" && value.includes(" ")) {
              outputStream.write(`$theme-${newPrefix}: '${value}';\n`);
            } else {
              outputStream.write(`$theme-${newPrefix}: ${value};\n`);
            }
          }
        }
      }
    };
    outputThemeSettings(theme_settings);
    outputStream.end(() => {
      console.log(`\nTheme settings have been written to file "${outputFilePath}"`);
    });
  } catch (parseErr) {
    console.error("Error parsing JSON:", parseErr);
  }
});
