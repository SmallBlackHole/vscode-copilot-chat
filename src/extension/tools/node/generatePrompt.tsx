/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { GeneratePromptTool } from "ai-mlstudio/lmt/generatePromptTool";
import { ToolRegistry } from '../common/toolsRegistry';

ToolRegistry.registerTool(GeneratePromptTool);
