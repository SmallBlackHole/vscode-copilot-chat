/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { GetAiModelGuidanceTool } from "ai-mlstudio/lmt/getAiModelGuidanceTool";
import { ToolRegistry } from '../common/toolsRegistry';

ToolRegistry.registerTool(GetAiModelGuidanceTool);
