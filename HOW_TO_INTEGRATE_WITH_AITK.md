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

## AI Toolkit Tool Integration

The repository includes an automated script for generating VS Code Copilot Chat tool wrappers for AI Toolkit (AITK) tools.

### Tool Generator Script (`generateAitkTool`)

The `generateAitkTool.ts` script automatically creates tool wrapper files that integrate AI Toolkit tools with VS Code Copilot Chat, including automatic extraction of real displayName and modelDescription values from the Skylight package files.

#### Usage

```bash
npm run generate-aitk-tool <referenceToolName> <importToolName> [generatedClassName]
```

#### Parameters

- **referenceToolName**: The reference tool name from Skylight package.json (e.g., "aitk-get_ai_model_guidance")
- **importToolName**: The exact name of the tool class to import from `ai-mlstudio/lmt`
- **generatedClassName**: Optional. The name for the generated wrapper class. If not provided, defaults to ImportToolName + "Wrapper"

#### Examples

```bash
# Generate tracing best practices tool with custom class name
npm run generate-aitk-tool aitk-get_tracing_code_gen_best_practices GetTracingCodeGenBestPracticesTool TracingCodeBestPracticesTool

# Generate model guidance tool with default class name (GetAiModelGuidanceToolWrapper)
npm run generate-aitk-tool aitk-get_ai_model_guidance GetAiModelGuidanceTool

# Generate prompt tool with custom class name
npm run generate-aitk-tool aitk-generate_prompt GeneratePromptTool PromptGeneratorTool

# Generate tracing page opener tool
npm run generate-aitk-tool aitk-open_tracing_page OpenTracingPageTool TracingPageTool
```

#### What the Script Does Automatically

1. **✅ Creates the tool wrapper file** in `/src/extension/tools/node/` with proper imports and structure
2. **✅ Updates allTools.ts** with the new import statement
3. **✅ Updates toolNames.ts** with both ToolName and ContributedToolName enum entries
4. **✅ Updates package.json** directly with the complete tool configuration
5. **✅ Extracts real values** from Skylight's package.json and package.nls.json:
   - Real displayName (e.g., "Get AI Model Guidance")
   - Real modelDescription with complete descriptions
   - Complete inputSchema with proper enum values and required fields

#### Manual Steps After Generation

The generator handles most integration steps automatically, but a few manual steps may remain:

1. **Review the generated configuration**: Check the package.json entry and adjust if needed
2. **Add localization entries**: If using localization, add display name entries to package.nls.json
3. **Test the integration**: Verify the tool works correctly in VS Code Copilot Chat
4. **Customize if needed**: Update the tool description and input schema to match specific requirements

#### Generated File Structure

The script creates tool files with this structure:

```typescript
export class GeneratedClassName implements ICopilotTool<void> {
	public static toolName = ToolName.GeneratedName;
	public static importToolName = new ImportToolName();

	async invoke(options: vscode.LanguageModelToolInvocationOptions<void>, token: vscode.CancellationToken) {
		const toolResult = await GeneratedClassName.importToolName.invoke(options as any, token);
		return new LanguageModelToolResult([
			new LanguageModelTextPart((toolResult.content[0] as any).value)
		]);
	}
}
```

#### Available AITK Tools

Common AI Toolkit tools that can be integrated:

| Reference Tool Name | Import Tool Name | Purpose |
|-------------------|------------------|---------|
| `aitk-get_ai_model_guidance` | `GetAiModelGuidanceTool` | AI model selection and guidance |
| `aitk-get_tracing_code_gen_best_practices` | `GetTracingCodeGenBestPracticesTool` | Tracing implementation best practices |
| `aitk-open_tracing_page` | `OpenTracingPageTool` | Open AI Toolkit tracing page |

#### Prerequisites for Tool Generation

Before using the generator script, ensure:

1. **Skylight repository** is cloned to `C:\code\Skylight\vscode\ai-mlstudio` (or update the path in the script)
2. **AI Toolkit dependencies** are properly installed in your project
3. **Reference tool exists** in Skylight's package.json under `contributes.languageModelTools`

For more details, see `/src/util/aitk/README.md`.

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