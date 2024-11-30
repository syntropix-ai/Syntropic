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

from pathlib import Path
from typing import Any, Dict, List, Optional, Self, Type, Union

import yaml

from synthora.configs.base import BaseConfig
from synthora.configs.model_config import ModelConfig
from synthora.configs.tool_config import ToolConfig
from synthora.prompts.base import BasePrompt
from synthora.types.enums import AgentType
from synthora.utils import YAMLLoader


class AgentConfig(BaseConfig):
    """Configuration class for Agents

    Attributes:
        name (str): Name identifier for the agent
        type (AgentType): Type of the agent from AgentType enum
        description (Optional[str]): Optional description of the agent's purpose
        model (Union[List[ModelConfig], ModelConfig]): Single model or list of models config
        prompt (Union[BasePrompt, Dict[str, BasePrompt]]): Prompt template(s) for the agent
        tools (Optional[List[ToolConfig]]): Optional list of tool configurations
    """

    name: str
    type: AgentType
    description: Optional[str] = None
    model: Union[List[ModelConfig], ModelConfig]
    prompt: Union[BasePrompt, Dict[str, BasePrompt]]
    tools: Optional[List[ToolConfig]] = None

    @classmethod
    def from_file(cls: Type[Self], path: Union[str, Path]) -> Self:
        """Load agent configuration from a YAML file

        Args:
            path (Union[str, Path]): Path to the YAML configuration file

        Returns:
            Self: Instance of AgentConfig

        Raises:
            ValueError: If YAML file cannot be loaded
        """
        try:
            with open(path, "r") as file:
                data = yaml.load(file, YAMLLoader)
        except yaml.YAMLError as e:
            raise ValueError(f"Error loading yaml file {path}: {e}")
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls: Type[Self], data: Dict[str, Any]) -> Self:
        """Create agent configuration from a dictionary

        Args:
            data (Dict[str, Any]): Dictionary containing agent configuration

        Returns:
            Self: Instance of AgentConfig
        """
        if tools := data.get("tools", None):
            data["tools"] = ToolConfig.parse_tools(tools)
        prompt = data.get("prompt")
        if isinstance(prompt, dict):
            for key, value in prompt.items():
                prompt[key] = BasePrompt(value)
        else:
            prompt = BasePrompt(prompt)
        data["prompt"] = prompt
        return cls(**data)
