/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { GetAiModelGuidanceTool, IAiModelGuidanceParameters } from "ai-mlstudio/lmt/getAiModelGuidanceTool";
import { inspect } from 'util';
import type * as vscode from 'vscode';
import { LanguageModelTextPart, LanguageModelToolResult } from '../../../vscodeTypes';
import { ToolName } from '../common/toolNames';
import { ICopilotTool, ToolRegistry } from '../common/toolsRegistry';

export class ModelSuggestionTool implements ICopilotTool<void> {
	public static toolName = ToolName.ModelSuggestion;
	public static getAiModelGuidanceTool = new GetAiModelGuidanceTool();
	constructor() {
		console.log('ModelSuggestionTool initialized');
	}

	async invoke(options: vscode.LanguageModelToolInvocationOptions<void>, token: vscode.CancellationToken) {
		console.log('ModelSuggestionTool invoked');
		console.log('Tool invocation options:', inspect(options, { depth: null, colors: true }));
		const invokeOptions: vscode.LanguageModelToolInvocationOptions<IAiModelGuidanceParameters> = {
			toolInvocationToken: options.toolInvocationToken,
			input: {
				preferredHost: (options.input as any).preferredHost ?? [],
				preferredLanguage: (options.input as any).preferredLanguage ?? [],
				preferredSDK: (options.input as any).preferredSDK ?? [],
				moreIntent: (options.input as any).moreIntent ?? ""
			} as IAiModelGuidanceParameters
		};
		console.log('Real invoke options:', inspect(invokeOptions, { depth: null, colors: true }));
		const toolResult = await ModelSuggestionTool.getAiModelGuidanceTool.invoke(invokeOptions, token);
		console.log('ModelSuggestionTool invoke completed', JSON.stringify(toolResult, null, 2));
		return new LanguageModelToolResult([
			new LanguageModelTextPart(
				(toolResult.content[0] as any).value
			)
		]);
	}
}

ToolRegistry.registerTool(ModelSuggestionTool);
