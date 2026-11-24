// world-news-20261124 entry (Node 22, standard library only).
//
// The entry image is the committed entry.png beside this file; this program
// copies it, byte for byte, to the output directory. The asset is located
// from this file's own path — never from the process working directory — so
// the program works no matter which directory the grader invokes it from.
// The program needs no network and produces identical bytes on every run.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, 'entry.png'), join(outDir, 'entry.png'));
