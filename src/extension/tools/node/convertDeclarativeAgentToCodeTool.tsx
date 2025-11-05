/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { ConvertDeclarativeAgentToCodeTool } from "ai-mlstudio/lmt/convertDeclarativeAgentToCodeTool";
import { ToolRegistry } from '../common/toolsRegistry';

ToolRegistry.registerTool(ConvertDeclarativeAgentToCodeTool);
