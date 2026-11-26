// Entry point for the make.fun harness.
//
// The front page itself is produced by generate_image.py and committed as
// entry.png. This program does nothing creative: it copies that committed
// image into the directory the harness collects from, so the submitted
// artefact is exactly the image in the repository.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

if (!existsSync(source)) {
  console.error(`entry.png is missing next to main.ts (${source})`);
  process.exit(1);
}

mkdirSync(targetDir, { recursive: true });
const target = join(targetDir, "entry.png");
copyFileSync(source, target);
console.log(`entry.png -> ${target}`);
