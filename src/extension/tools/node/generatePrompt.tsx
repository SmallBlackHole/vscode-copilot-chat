/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { GeneratePromptTool, IGeneratePromptParameters } from "ai-mlstudio/lmt/generatePromptTool";
import { inspect } from 'util';
import type * as vscode from 'vscode';
import { LanguageModelTextPart, LanguageModelToolResult } from '../../../vscodeTypes';
import { ToolName } from '../common/toolNames';
import { ICopilotTool, ToolRegistry } from '../common/toolsRegistry';

export class CopilotGeneratePromptTool implements ICopilotTool<void> {
	public static toolName = ToolName.GeneratePrompt;
	public static generatePromptTool = new GeneratePromptTool();
	constructor() {
		console.log('GeneratePromptTool initialized');
	}

	async invoke(options: vscode.LanguageModelToolInvocationOptions<void>, token: vscode.CancellationToken) {
		console.log('GeneratePromptTool invoked');
		console.log('Tool invocation options:', inspect(options, { depth: null, colors: true }));
		const invokeOptions: vscode.LanguageModelToolInvocationOptions<IGeneratePromptParameters> = {
			toolInvocationToken: options.toolInvocationToken,
			input: {
				scenario: (options.input as any).scenario ?? undefined,
			} as IGeneratePromptParameters
		};
		console.log('Real invoke options:', inspect(invokeOptions, { depth: null, colors: true }));
		const toolResult = await CopilotGeneratePromptTool.generatePromptTool.invoke(invokeOptions, token);
		console.log('GeneratePromptTool invoke completed', JSON.stringify(toolResult, null, 2));
		return new LanguageModelToolResult([
			new LanguageModelTextPart(
				(toolResult.content[0] as any).value
			)
		]);
	}
}

ToolRegistry.registerTool(CopilotGeneratePromptTool);
