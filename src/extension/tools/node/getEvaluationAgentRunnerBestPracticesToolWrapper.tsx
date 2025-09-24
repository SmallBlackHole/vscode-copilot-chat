/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { GetEvaluationAgentRunnerBestPracticesTool } from "ai-mlstudio/lmt/getEvaluationAgentRunnerBestPracticesTool";
import type * as vscode from 'vscode';
import { LanguageModelTextPart, LanguageModelToolResult } from '../../../vscodeTypes';
import { ToolName } from '../common/toolNames';
import { ICopilotTool, ToolRegistry } from '../common/toolsRegistry';

export class GetEvaluationAgentRunnerBestPracticesToolWrapper implements ICopilotTool<void> {
	public static toolName = ToolName.EvaluationAgentRunnerBestPracticesToolWrapper;
	public static getBulkResultCollectionBestPracticesTool = new GetEvaluationAgentRunnerBestPracticesTool();
	constructor() {
	}

	async invoke(options: vscode.LanguageModelToolInvocationOptions<void>, token: vscode.CancellationToken) {
		const toolResult = await GetEvaluationAgentRunnerBestPracticesToolWrapper.getBulkResultCollectionBestPracticesTool.invoke(options as any, token);
		return new LanguageModelToolResult([
			new LanguageModelTextPart(
				(toolResult.content[0] as any).value
			)
		]);
	}
}

ToolRegistry.registerTool(GetEvaluationAgentRunnerBestPracticesToolWrapper);
