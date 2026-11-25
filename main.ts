import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Resolve every path from this file's own location, never from the
// process working directory: the grader runs `node /bot/main.ts` from
// a working directory of its own choosing.
const root = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
const src = join(root, "entry.png");
const dst = join(outDir, "entry.png");
copyFileSync(src, dst);
if (statSync(src).size !== statSync(dst).size) {
  throw new Error("entry.png copy size mismatch");
}
console.log(`wrote ${dst} (${statSync(dst).size} bytes)`);
