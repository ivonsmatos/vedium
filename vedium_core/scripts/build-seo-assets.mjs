import { readFile, writeFile } from "node:fs/promises";
import { extname, join } from "node:path";
import CleanCSS from "clean-css";
import { minify } from "terser";

const publicRoot = join("vedium_core", "public");
const assets = [
  "css/luxo_theme.css",
  "css/public-foundations.css",
  "js/pwa-register.js",
  "js/cookie-consent.js",
  "js/meta-pixel.js",
  "js/push-notifications.js",
  "js/vedium-language.js",
  "vedium_assets/css/vedium.css",
  "vedium_assets/css/vedium-responsive.css",
  "vedium_assets/js/vedium.js",
  "vedium_assets/vendors/animate/custom-animate.css",
  "vedium_assets/vendors/icomoon-icons/style.css",
  "vedium_assets/vendors/jquery-magnific-popup/jquery.magnific-popup.css",
  "vedium_assets/vendors/nouislider/nouislider.pips.css",
  "vedium_assets/vendors/twentytwenty/jquery.event.move.js",
  "vedium_assets/vendors/twentytwenty/twentytwenty.css",
  "vedium_assets/vendors/twentytwenty/twentytwenty.js",
];

function minifiedPath(sourcePath) {
  const extension = extname(sourcePath);
  return `${sourcePath.slice(0, -extension.length)}.min${extension}`;
}

for (const relativePath of assets) {
  const sourcePath = join(publicRoot, relativePath);
  const outputPath = minifiedPath(sourcePath);
  const source = await readFile(sourcePath, "utf8");
  let output;

  if (extname(sourcePath) === ".css") {
    const result = new CleanCSS({ level: 1, rebase: false }).minify(source);
    if (result.errors.length) {
      throw new Error(`${relativePath}: ${result.errors.join("; ")}`);
    }
    output = result.styles;
  } else {
    const result = await minify(source, {
      compress: true,
      mangle: true,
      format: { comments: false },
    });
    if (!result.code) {
      throw new Error(`${relativePath}: terser did not produce output`);
    }
    output = result.code;
  }

  await writeFile(outputPath, `${output}\n`, "utf8");
  console.log(`${relativePath} -> ${minifiedPath(relativePath)}`);
}
