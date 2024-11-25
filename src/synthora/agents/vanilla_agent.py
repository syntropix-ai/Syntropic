# LICENSE HEADER MANAGED BY add-license-header
#
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
#

import json
from typing import Any, Dict, List, Union, cast

from synthora.agents import BaseAgent
from synthora.configs.agent_config import AgentConfig
from synthora.messages.base import BaseMessage
from synthora.models.base import BaseModelBackend
from synthora.prompts.base import BasePrompt
from synthora.toolkits.base import BaseFunction
from synthora.types.enums import CallBackEvent, Err, MessageRole, NodeType, Ok, Result
from synthora.types.node import Node
from synthora.utils.macros import FORMAT_PROMPT, GET_FINAL_MESSAGE, STR_TO_USERMESSAGE, UPDATE_SYSTEM


class VanillaAgent(BaseAgent):
    def __init__(
        self,
        config: AgentConfig,
        source: Node,
        model: BaseModelBackend,
        prompt: BasePrompt,
        tools: List[Union["BaseAgent", BaseFunction]] = [],
    ) -> None:
        super().__init__(config, source, model, prompt, tools)
        self.model: BaseModelBackend = (
            self.model[0] if isinstance(self.model, list) else self.model
        )
        self.model.config["tools"] = [tool.schema for tool in tools]
        self.prompt = (
            list(self.prompt.values())[0]
            if isinstance(self.prompt, dict)
            else self.prompt
        )
        self.prompt: BasePrompt = cast(BasePrompt, self.prompt)

    def step(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:

        UPDATE_SYSTEM(prompt=FORMAT_PROMPT())
        message = STR_TO_USERMESSAGE()
        if message.content:
            self.history.append(message)

        response = self.model.run(self.history, *args, **kwargs)
        response = GET_FINAL_MESSAGE()

        self.history.append(response)
        return Ok(response)

    def run(
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:
        if isinstance(message, str):
            message = BaseMessage.create_message(
                role=MessageRole.USER,
                content=message,
                source=Node(name="user", type=NodeType.USER),
            )
        if self.source.ancestor:
            self.callback_manager.call(CallBackEvent.TOOL_START, self.source, message, *args, **kwargs)
        self.callback_manager.call(
            CallBackEvent.AGENT_START, self.source, message, *args, **kwargs
        )
        while True:
            response = self.step(message, *args, **kwargs)
            message = ""
            if response.is_ok:
                data = response.value
                if data.tool_calls:
                    for tool_call in data.tool_calls:
                        func = tool_call.function
                        try:
                            tool = self.get_tool(func.name)
                            tool_args = json.loads(func.arguments)
                            resp = tool.run(**tool_args)
                            self.history.append(
                                BaseMessage.create_message(
                                    id=tool_call.id,
                                    role=MessageRole.TOOL_RESPONSE,
                                    content=resp.value,
                                    source=Node(name=tool.name, type=NodeType.TOOL),
                                )
                            )
                        except Exception as e:
                            self.history.append(
                                BaseMessage.create_message(
                                    id=tool_call.id,
                                    role=MessageRole.TOOL_RESPONSE,
                                    content=f"Error: {str(e)}",
                                    source=Node(name=tool.name, type=NodeType.TOOL),
                                )
                            )

                else:
                    if self.source.ancestor:
                        self.callback_manager.call(CallBackEvent.TOOL_END, self.source, Ok(data.content))
                    self.callback_manager.call(
                        CallBackEvent.AGENT_END, self.source, data, *args, **kwargs
                    )
                    return Ok(data.content)

            else:
                if self.source.ancestor:
                    self.callback_manager.call(CallBackEvent.TOOL_ERROR, self.source, response, *args, **kwargs)

                self.callback_manager.call(
                    CallBackEvent.AGENT_ERROR,
                    self.source,
                    response.error,
                    *args,
                    **kwargs,
                )
                return response

    async def async_run(  # type: ignore[empty-body]
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:
        pass

    async def async_step(  # type: ignore[empty-body]
        self, message: Union[str, BaseMessage], *args: Any, **kwargs: Dict[str, Any]
    ) -> Result[Any, Exception]:
        pass
