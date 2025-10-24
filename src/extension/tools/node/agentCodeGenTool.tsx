/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { GetAgentCodeGenTool } from "ai-mlstudio/lmt/getAgentCodeGenTool";
import { ToolRegistry } from '../common/toolsRegistry';

// export class AgentCodeGenTool implements ICopilotTool<void> {
// 	public static toolName = ToolName.GetAgentCodeGenBestPractices;
// 	public static getAgentCodeGenTool = new GetAgentCodeGenTool();
// 	constructor() {
// 	}

// 	async invoke(options: vscode.LanguageModelToolInvocationOptions<void>, token: vscode.CancellationToken) {
// 		const toolResult = await AgentCodeGenTool.getAgentCodeGenTool.invoke(options as any, token);
// 		return new LanguageModelToolResult([
// 			new LanguageModelTextPart(
// 				(toolResult.content[0] as any).value
// 			)
// 		]);
// 	}
// }

ToolRegistry.registerTool(GetAgentCodeGenTool);
