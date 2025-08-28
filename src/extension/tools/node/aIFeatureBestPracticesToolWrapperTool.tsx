/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { AIFeatureBestPracticesTool } from "ai-mlstudio/lmt/aIFeatureBestPracticesTool";
import type * as vscode from 'vscode';
import { LanguageModelTextPart, LanguageModelToolResult } from '../../../vscodeTypes';
import { ToolName } from '../common/toolNames';
import { ICopilotTool, ToolRegistry } from '../common/toolsRegistry';

export class AIFeatureBestPracticesToolWrapper implements ICopilotTool<void> {
	public static toolName = ToolName.AIFeatureBestPracticesToolWrapper;
	public static aIFeatureBestPracticesTool = new AIFeatureBestPracticesTool();
	constructor() {
	}

	async invoke(options: vscode.LanguageModelToolInvocationOptions<void>, token: vscode.CancellationToken) {
		const toolResult = await AIFeatureBestPracticesToolWrapper.aIFeatureBestPracticesTool.invoke(options as any, token);
		return new LanguageModelToolResult([
			new LanguageModelTextPart(
				(toolResult.content[0] as any).value
			)
		]);
	}
}

ToolRegistry.registerTool(AIFeatureBestPracticesToolWrapper);
