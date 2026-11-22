// news-image-20261121 entry (Node 22, standard library only).
//
// The entry image is the entry.png sitting next to this file. Running
// this program copies it into the make.fun output directory so the
// judge sees exactly those bytes.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output.

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const sourcePath = join(here, "entry.png");

  const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(outputDir, { recursive: true });

  const destPath = join(outputDir, "entry.png");
  copyFileSync(sourcePath, destPath);

  const sourceSize = statSync(sourcePath).size;
  const destSize = statSync(destPath).size;
  if (sourceSize !== destSize) {
    throw new Error(
      `entry.png copy mismatch: source ${sourceSize} bytes, ` +
        `destination ${destSize} bytes`,
    );
  }
  console.log(`copied entry.png (${sourceSize} bytes) to ${destPath}`);
}

main();
