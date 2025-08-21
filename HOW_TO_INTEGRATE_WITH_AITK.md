# AI Toolkit (AITK) Integration Guide

This document outlines how to integrate and test the VS Code Copilot Chat extension with the AI Toolkit.

## Prerequisites

- Node.js and npm installed
- Git access to both repositories
- GitHub OAuth token for authentication

## Setup Instructions

1. **Repository Setup**
   ```bash
   # Clone both repositories to the same parent directory
   git clone <copilot-chat-repo-url>
   git clone <skylight-repo-url>
   ```

2. **Install Dependencies**
   ```bash
   cd my-vscode-copilot-chat
   npm install
   ```

3. **Authentication Setup**
   Choose one of the following options:
   - Run `npm run get_token` to obtain a GitHub OAuth token interactively
   - Or set the `GITHUB_OAUTH_TOKEN` environment variable with your token

4. **Skylight code update**
   - Skip send Telemetry in tool implementation
   - Skip `fetchNewestTemplateZip` in templateUtils.ts
   - Better follow this branch change to fix compile error 'https://github.com/microsoft/Skylight/tree/refactor/run-in-simulate'

5. **Build the Project**
   ```bash
   npm run build
   ```

## Testing

### Unit Tests
Run the basic unit test suite:
```bash
npm run simulate
```

### End-to-End Tests
Run comprehensive e2e tests with model suggestions:
```bash
node dist/simulationMain.js --external-scenarios <your-repo-path>/test/scenarios/test-model-suggestion  --parallelism 1 --sidebar -n 1 --disable-tools=get_errors --in-extension-host --scenario-workspace-folder --verbose --output c:/temp/out --skip-cache --model claude-sonnet-4
```