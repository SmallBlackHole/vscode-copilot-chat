/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { EvaluationPlannerTool } from "ai-mlstudio/lmt/evaluationPlannerTool";
import { ToolRegistry } from '../common/toolsRegistry';

ToolRegistry.registerTool(EvaluationPlannerTool);
