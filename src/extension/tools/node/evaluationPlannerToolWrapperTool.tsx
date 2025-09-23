/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { EvaluationPlannerTool } from "ai-mlstudio/lmt/evaluationPlannerTool";
import type * as vscode from 'vscode';
import { LanguageModelTextPart, LanguageModelToolResult } from '../../../vscodeTypes';
import { ToolName } from '../common/toolNames';
import { ICopilotTool, ToolRegistry } from '../common/toolsRegistry';

export class EvaluationPlannerToolWrapper implements ICopilotTool<void> {
	public static toolName = ToolName.EvaluationPlannerToolWrapper;
	public static evaluationPlannerTool = new EvaluationPlannerTool();
	constructor() {
	}

	async invoke(options: vscode.LanguageModelToolInvocationOptions<void>, token: vscode.CancellationToken) {
		const toolResult = await EvaluationPlannerToolWrapper.evaluationPlannerTool.invoke(options as any, token);
		return new LanguageModelToolResult([
			new LanguageModelTextPart(
				(toolResult.content[0] as any).value
			)
		]);
	}
}

ToolRegistry.registerTool(EvaluationPlannerToolWrapper);
