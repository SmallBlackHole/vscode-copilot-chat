/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { execSync } from 'child_process';
import { inspect } from 'util';
import type * as vscode from 'vscode';
import { ToolName } from '../common/toolNames';
import { ICopilotTool, ToolRegistry } from '../common/toolsRegistry';
import { LanguageModelTextPart, LanguageModelToolResult } from '../../../vscodeTypes';

export class BasicRunInTerminal implements ICopilotTool<void> {
	public static toolName = ToolName.BasicRunInTerminal;
	constructor() {
	}

	async invoke(options: vscode.LanguageModelToolInvocationOptions<void>, token: vscode.CancellationToken) {
		console.log('BasicRunInTerminal invoked with options:', inspect(options, { depth: null }));
		const { command } = (options as any).input;
		console.log('Executing command:', command);
		try {
			const output = execSync(command, { encoding: 'utf-8' });
			console.log('Command output:', output);
			return new LanguageModelToolResult([
				new LanguageModelTextPart(
					`Command executed successfully: ${command}\n${output}`
				)
			]);
		} catch (error: any) {
			const stderr = error.stderr ? error.stderr.toString() : '';
			const stdout = error.stdout ? error.stdout.toString() : '';

			console.error('Command failed:', command, error, stderr, stdout);
			return new LanguageModelToolResult([
				new LanguageModelTextPart(
					`Command failed: ${command}\n${stderr || stdout || error.message}`
				)
			]);
		}
	}
}

ToolRegistry.registerTool(BasicRunInTerminal);
