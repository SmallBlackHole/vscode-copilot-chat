/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { GetTracingCodeGenBestPracticesTool, ITracingCodeGenBestPracticesParameters } from "ai-mlstudio/lmt/getTracingCodeGenBestPracticesTool";
import { inspect } from 'util';
import type * as vscode from 'vscode';
import { LanguageModelTextPart, LanguageModelToolResult } from '../../../vscodeTypes';
import { ToolName } from '../common/toolNames';
import { ICopilotTool, ToolRegistry } from '../common/toolsRegistry';

export class TracingCodeBestPracticesTool implements ICopilotTool<void> {
	public static toolName = ToolName.GetTracingCodeGenBestPractices;
	public static getTracingCodeGenBestPractices = new GetTracingCodeGenBestPracticesTool();
	constructor() {
		console.log('TracingCodeBestPracticesTool initialized');
	}

	async invoke(options: vscode.LanguageModelToolInvocationOptions<void>, token: vscode.CancellationToken) {
		console.log('TracingCodeBestPracticesTool invoked');
		console.log('Tool invocation options:', inspect(options, { depth: null, colors: true }));
		const invokeOptions: vscode.LanguageModelToolInvocationOptions<ITracingCodeGenBestPracticesParameters> = {
			toolInvocationToken: options.toolInvocationToken,
			input: {
				language: (options.input as any).language,
				sdk: (options.input as any).sdk,
			} as ITracingCodeGenBestPracticesParameters
		};
		console.log('Real invoke options:', inspect(invokeOptions, { depth: null, colors: true }));
		const toolResult = await TracingCodeBestPracticesTool.getTracingCodeGenBestPractices.invoke(invokeOptions, token);
		console.log('TracingCodeBestPracticesTool invoke completed', JSON.stringify(toolResult, null, 2));
		return new LanguageModelToolResult([
			new LanguageModelTextPart(
				(toolResult.content[0] as any).value
			)
		]);
	}
}

ToolRegistry.registerTool(TracingCodeBestPracticesTool);
