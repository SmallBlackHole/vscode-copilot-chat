/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { GetEvaluationCodeGenBestPracticesTool } from "ai-mlstudio/lmt/getEvaluationCodeGenBestPracticesTool";
import type * as vscode from 'vscode';
import { LanguageModelTextPart, LanguageModelToolResult } from '../../../vscodeTypes';
import { ToolName } from '../common/toolNames';
import { ICopilotTool, ToolRegistry } from '../common/toolsRegistry';

export class GetEvaluationCodeGenBestPracticesToolWrapper implements ICopilotTool<void> {
	public static toolName = ToolName.GetEvaluationCodeGenBestPracticesToolWrapper;
	public static getEvaluationCodeGenBestPracticesTool = new GetEvaluationCodeGenBestPracticesTool();
	constructor() {
	}

	async invoke(options: vscode.LanguageModelToolInvocationOptions<void>, token: vscode.CancellationToken) {
		const toolResult = await GetEvaluationCodeGenBestPracticesToolWrapper.getEvaluationCodeGenBestPracticesTool.invoke(options as any, token);
		return new LanguageModelToolResult([
			new LanguageModelTextPart(
				(toolResult.content[0] as any).value
			)
		]);
	}
}

ToolRegistry.registerTool(GetEvaluationCodeGenBestPracticesToolWrapper);
