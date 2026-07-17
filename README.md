# oks-connector

Independent **Level-1** multimodal extractor for
[Open Knowledge Studio](https://github.com/itxaiohanglover/open-knowledge-studio).
It converts video / audio / image / Office / PDF sources into an OKS **Raw
Bundle** (`content.md` + `evidence.jsonl` provenance sidecar).

This package is deliberately **separate from the OKS core** (`oks` / `cli/`):

- Per CONSTITUTION **P4/P5**, the OKS core stays API-free and never wraps tools
  at runtime. Extractors are L1 capabilities the Agent spawns via Bash, guided
  by the routing table in `settings/handlers.json`.
- Per the reframed **A1**, this is **not** a repo maintenance script (those stay
  in `scripts/` inside the knowledge repo). It is an independently versioned,
  independently installed L1 tool — which is why it lives in its own package.

It **never summarizes, corrects, grades, or promotes** source content. Its only
contract is faithful extraction plus provenance (P3: `raw/` is mechanical).

## Install

The core CLI is stdlib-only. Heavy extractors are opt-in extras, each best
installed in its **own isolated Python 3.12 interpreter** (they pin conflicting
heavyweight deps such as MinerU / PaddleOCR / faster-whisper):

```bash
# one interpreter per modality
pip install "oks-connector[document]"   # docx / pptx via markitdown
pip install "oks-connector[pdf]"        # PDF via MinerU
pip install "oks-connector[watch]"      # video / audio via faster-whisper + rapidocr
pip install "oks-connector[formula]"    # formula OCR via paddleocr
```

## Use

```bash
oks-raw-bundle --version
oks-raw-bundle route  <source>                       # print the extraction plan
oks-raw-bundle image  <img>  --output <bundle_dir>   # OCR + bbox evidence
oks-raw-bundle markitdown <docx> --output <bundle_dir>
oks-raw-bundle mineru <mineru_result> --source <pdf> --output <bundle_dir>
oks-raw-bundle watch  <video> --output <bundle_dir>  # transcript + frames + OCR
oks-raw-bundle validate <bundle_dir>                 # check a bundle against v0.1
```

Output contract: `raw-multimodal/v0.1` — see `docs/raw-multimodal-standard.md`
in the OKS repo.

## Wiring into the knowledge repo

Point `settings/handlers.json` `command_argv` at the installed entry point
instead of the in-repo script path. For example:

```json
"command_argv": ["{watch_python}", "-m", "raw_bundle_adapter", "watch", "{input}", "--output", "{output}"]
```

or, if the modality's interpreter is on PATH:

```json
"command_argv": ["oks-raw-bundle", "watch", "{input}", "--output", "{output}"]
```

`{watch_python}` / `{mineru_python}` / `{document_python}` are resolved from
`settings/raw-tools.json` so each modality can use its isolated environment.

## Develop / test

```bash
python -m pytest scripts/tests -q
```
